# PDF ile Sohbet Uygulaması (StudyLens)

Bir PDF dosyasını yükleyip ona doğal dille soru sorabildiğiniz, cevapların yalnızca o
belgenin içeriğine dayanarak üretildiği bir **RAG (Retrieval-Augmented Generation)**
uygulaması. Yapay zeka, belgeyi baştan sona "okumak" yerine sorunuzla en alakalı
parçaları bulup yalnızca onlara dayanarak cevap üretir — bu da uydurma (halüsinasyon)
riskini azaltır ve belge ne kadar uzun olursa olsun hızlı çalışmasını sağlar.

İsteğe bağlı olarak, aynı soru YouTube'da da aratılıp konuyla ilgili video önerileri
gösterilebilir — özellikle ders çalışırken yazılı cevabın yanında görsel anlatım işe yarar.

## Özellikler

- PDF yükleme ve otomatik parçalama (chunking)
- Parçaların embedding'e çevrilip vektör veritabanında (FAISS / ChromaDB) indekslenmesi
- Soruya anlamca en yakın parçaların bulunup bir dil modeline (Gemini / Groq) gönderilmesi
- Yalnızca belge içeriğine dayalı, kaynağı belirtilen cevaplar
- Opsiyonel: "İlgili YouTube videosu göster" seçeneği ile video önerileri
- Streamlit tabanlı sohbet arayüzü

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

`.env.example` dosyasını `.env` olarak kopyalayıp kendi API key'lerinizi girin
(Gemini/Groq ve YouTube Data API).

## Kullanım

```bash
streamlit run app.py
```

Tarayıcıda açılan arayüzden bir PDF yükleyin, sorunuzu yazın ve isterseniz ilgili
YouTube videolarını görmek için seçeneği işaretleyin.

## Testler

```bash
pytest
```

## Proje Yapısı

```
pdf-chat-app/
├── app.py               # Streamlit arayüzü
├── rag_pipeline.py      # PDF okuma, bölme, embedding, arama fonksiyonları
├── youtube_search.py    # YouTube Data API ile video arama fonksiyonu
├── requirements.txt     # Gerekli kütüphaneler
├── .env.example         # API key için örnek dosya (gerçek key burada olmaz)
├── .gitignore            # .env dosyasını hariç tutar
└── README.md             # Kurulum ve kullanım talimatları
```

## Kullanılan Teknolojiler

| Katman | Araç |
|---|---|
| Arayüz | Streamlit |
| Metin bölme + embedding | LangChain / sentence-transformers |
| Vektör veritabanı | FAISS veya ChromaDB |
| Dil modeli | Google Gemini API veya Groq API |
| Video önerisi | YouTube Data API v3 |
| Yayına alma | Streamlit Community Cloud / Hugging Face Spaces |

## Ekip

- **Ömer** — Arayüz (Streamlit UI, sohbet ekranı, video önerisi arayüzü), backend entegrasyonu, canlı ortama deploy
- **Yağmur** — Veri/Model katmanı (PDF okuma, chunking, embedding, vektör arama), YouTube arama fonksiyonu, dokümantasyon

> **Not:** API key'ler asla kodun içine yazılmaz; `.env` dosyasında tutulur ve `.gitignore`
> ile hariç tutulur. Yayına alırken platformun "secrets" bölümü kullanılır.
