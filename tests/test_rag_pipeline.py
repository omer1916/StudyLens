import hashlib
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

import rag_pipeline


def test_chunk_text_splits_long_text_with_overlap():
    text = "a" * 1200

    chunks = rag_pipeline.chunk_text(text, chunk_size=500, overlap=50)

    assert len(chunks) == 3
    assert all(len(c) <= 500 for c in chunks)


def test_chunk_text_empty_string_returns_no_chunks():
    assert rag_pipeline.chunk_text("   ") == []


def test_chunk_text_rejects_overlap_larger_than_chunk_size():
    with pytest.raises(ValueError):
        rag_pipeline.chunk_text("herhangi bir metin", chunk_size=100, overlap=100)


def test_extract_text_by_page_skips_empty_pages():
    page_with_text = MagicMock()
    page_with_text.extract_text.return_value = "Merhaba dünya"
    empty_page = MagicMock()
    empty_page.extract_text.return_value = "   "

    with patch("rag_pipeline.PdfReader") as mock_reader:
        mock_reader.return_value.pages = [page_with_text, empty_page]
        pages = rag_pipeline.extract_text_by_page(pdf_file=object())

    assert pages == [(1, "Merhaba dünya")]


def test_build_chunks_tracks_source_page():
    with patch("rag_pipeline.extract_text_by_page") as mock_extract:
        mock_extract.return_value = [(1, "a" * 10), (2, "b" * 10)]
        chunks = rag_pipeline.build_chunks(pdf_file=object())

    assert [c["page"] for c in chunks] == [1, 2]


def _fake_embed(texts, normalize_embeddings=True):
    # Deterministik, birim uzunlukta sahte "embedding": metnin ilk kelimesini bir
    # açıya eşler. Aynı kelime => aynı vektör => en yüksek iç çarpım (en alakalı
    # eşleşme); gerçek modeli indirmeden arama (retrieval) mantığını test eder.
    vectors = []
    for t in texts:
        word = t.split()[0]
        digest = int(hashlib.sha256(word.encode()).hexdigest(), 16)
        angle = (digest % 3600) / 3600 * 2 * np.pi
        vectors.append([np.cos(angle), np.sin(angle)])
    return np.array(vectors, dtype="float32")


def test_retrieve_relevant_chunks_returns_closest_match():
    chunks = [
        {"text": "elma hakkında bilgi", "page": 1},
        {"text": "zebra hakkında bilgi", "page": 2},
    ]

    with patch.object(rag_pipeline, "_get_embedding_model") as mock_get_model:
        mock_model = MagicMock()
        mock_model.encode.side_effect = _fake_embed
        mock_get_model.return_value = mock_model

        index = rag_pipeline._build_index(chunks)
        result = rag_pipeline.retrieve_relevant_chunks("elma", index, chunks, k=1)

    assert result[0]["page"] == 1


def test_answer_question_uses_top_chunk_as_source_page():
    with patch.object(rag_pipeline, "get_or_build_index") as mock_get_index, patch.object(
        rag_pipeline, "retrieve_relevant_chunks"
    ) as mock_retrieve, patch.object(rag_pipeline, "generate_answer") as mock_generate:
        mock_get_index.return_value = (MagicMock(), [{"text": "x", "page": 5}])
        mock_retrieve.return_value = [{"text": "x", "page": 5}]
        mock_generate.return_value = "cevap metni"

        result = rag_pipeline.answer_question(pdf_file=object(), question="soru?")

    assert result == {"answer": "cevap metni", "source_page": 5}


def test_generate_answer_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        rag_pipeline.generate_answer("soru?", [{"text": "x", "page": 1}])
