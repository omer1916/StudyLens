"""PDF okuma, parçalama (chunking), embedding, vektör arama ve LLM ile cevap üretme.

Arayüzün (pages/1_💬_Sohbet.py) beklediği tek genel fonksiyon `answer_question`'dır;
geri kalanı ondan bağımsız test edilebilir yardımcı fonksiyonlardır.
"""

from __future__ import annotations

import hashlib
import os

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4

_embedding_model: SentenceTransformer | None = None
# PDF içeriğinin hash'ine göre (index, chunks) önbelleği — aynı belgeye sorulan
# her yeni soru için embedding/indeksleme işlemini tekrarlamamak için.
_index_cache: dict[str, tuple["faiss.Index", list[dict]]] = {}


def _get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def _pdf_bytes(pdf_file) -> bytes:
    if hasattr(pdf_file, "getvalue"):
        return pdf_file.getvalue()
    data = pdf_file.read()
    if hasattr(pdf_file, "seek"):
        pdf_file.seek(0)
    return data


def extract_text_by_page(pdf_file) -> list[tuple[int, str]]:
    """PDF'in her sayfasından metni çıkarır. Sayfa numaraları 1'den başlar;
    metni boş çıkan (örn. taranmış/görüntü tabanlı) sayfalar atlanır."""
    reader = PdfReader(pdf_file)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((i, text))
    return pages


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Metni, aralarında örtüşme (overlap) bırakarak sabit boyutlu parçalara böler."""
    if overlap >= chunk_size:
        raise ValueError("overlap, chunk_size'dan küçük olmalı")

    text = text.strip()
    if not text:
        return []

    chunks = []
    step = chunk_size - overlap
    start = 0
    while start < len(text):
        piece = text[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        start += step
    return chunks


def build_chunks(pdf_file) -> list[dict]:
    """PDF'i sayfa sayfa okuyup parçalara böler; her parça kaynağı olan sayfa
    numarasını da taşır (örn. {"text": ..., "page": 3})."""
    chunks = []
    for page_num, page_text in extract_text_by_page(pdf_file):
        for piece in chunk_text(page_text):
            chunks.append({"text": piece, "page": page_num})
    return chunks


def _build_index(chunks: list[dict]) -> "faiss.Index":
    model = _get_embedding_model()
    embeddings = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
    embeddings = np.asarray(embeddings, dtype="float32")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index


def get_or_build_index(pdf_file) -> tuple["faiss.Index", list[dict]]:
    """Aynı PDF içeriği için embedding/indeksleme işlemini her soruda tekrar
    etmemek üzere sonucu dosya içeriğinin hash'ine göre önbelleğe alır."""
    key = hashlib.sha256(_pdf_bytes(pdf_file)).hexdigest()
    if key not in _index_cache:
        chunks = build_chunks(pdf_file)
        if not chunks:
            raise ValueError("PDF'ten okunabilir metin çıkarılamadı (taranmış/görüntü tabanlı olabilir).")
        index = _build_index(chunks)
        _index_cache[key] = (index, chunks)
    return _index_cache[key]


def retrieve_relevant_chunks(
    question: str, index: "faiss.Index", chunks: list[dict], k: int = TOP_K
) -> list[dict]:
    """Soruya anlam olarak en yakın k parçayı döndürür (en alakalı önce)."""
    model = _get_embedding_model()
    query_vec = model.encode([question], normalize_embeddings=True)
    query_vec = np.asarray(query_vec, dtype="float32")
    k = min(k, len(chunks))
    _, result_indices = index.search(query_vec, k)
    return [chunks[i] for i in result_indices[0] if i != -1]


def _build_llm_client():
    """GEMINI_API_KEY varsa Gemini'yi, yoksa GROQ_API_KEY varsa Groq'u kullanır."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        import google.generativeai as genai

        genai.configure(api_key=gemini_key)
        return "gemini", genai.GenerativeModel("gemini-1.5-flash")

    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        from groq import Groq

        return "groq", Groq(api_key=groq_key)

    raise RuntimeError(
        "GEMINI_API_KEY veya GROQ_API_KEY tanımlı değil. .env dosyanıza en az birini ekleyin "
        "(.env.example'a bakın)."
    )


def _prompt_for(question: str, relevant_chunks: list[dict]) -> str:
    context = "\n\n".join(f"[Sayfa {c['page']}] {c['text']}" for c in relevant_chunks)
    return (
        "Aşağıda bir PDF belgesinden alınmış parçalar var. Yalnızca bu parçalara "
        "dayanarak soruyu cevapla. Cevap bu parçalarda yoksa bunu açıkça belirt; "
        "uydurma bilgi verme.\n\n"
        f"Belge parçaları:\n{context}\n\n"
        f"Soru: {question}\n"
        "Cevap:"
    )


def generate_answer(question: str, relevant_chunks: list[dict]) -> str:
    """Seçilen parçaları ve soruyu dil modeline gönderip cevap metnini döndürür."""
    provider, client = _build_llm_client()
    prompt = _prompt_for(question, relevant_chunks)

    if provider == "gemini":
        response = client.generate_content(prompt)
        return response.text.strip()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def answer_question(pdf_file, question: str) -> dict:
    """Arayüzün beklediği genel fonksiyon: PDF + soru alır, cevap ve kaynak
    sayfa döndürür. Dönüş: {"answer": str, "source_page": int}."""
    index, chunks = get_or_build_index(pdf_file)
    relevant = retrieve_relevant_chunks(question, index, chunks)
    answer = generate_answer(question, relevant)
    source_page = relevant[0]["page"] if relevant else chunks[0]["page"]
    return {"answer": answer, "source_page": source_page}
