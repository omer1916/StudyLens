"""Backend hazır olana kadar arayüzü test etmek için kullanılan sahte (mock) fonksiyonlar.

Yağmur'un rag_pipeline.py ve youtube_search.py modülleri hazır olduğunda,
pages/1_💬_Sohbet.py içindeki importlar buradan gerçek modüllere yönlendirilecek.
"""

import time


def answer_question(pdf_file, question: str) -> dict:
    time.sleep(1)
    return {
        "answer": f"'{question}' sorusuna örnek cevap: yüklediğiniz belgeye göre bu, "
        "backend bağlandığında gerçek içerikten üretilecek bir yanıttır.",
        "source_page": 3,
    }


def search_videos(query: str) -> list[dict]:
    return [
        {
            "title": f"{query} konusunu anlatan örnek video",
            "channel": "Örnek Kanal",
            "url": "https://www.youtube.com/",
            "thumbnail": "https://placehold.co/320x180/6d28d9/ffffff?text=Video",
        }
    ]
