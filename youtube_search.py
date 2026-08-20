"""YouTube Data API v3 ile, sorulan soruyla ilgili video önerileri arayan fonksiyon."""

from __future__ import annotations

import os

from googleapiclient.discovery import build

MAX_RESULTS = 3

_youtube_client = None


def _get_client():
    global _youtube_client
    if _youtube_client is None:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "YOUTUBE_API_KEY tanımlı değil. .env dosyanıza ekleyin (.env.example'a bakın)."
            )
        _youtube_client = build("youtube", "v3", developerKey=api_key)
    return _youtube_client


def search_videos(query: str, max_results: int = MAX_RESULTS) -> list[dict]:
    """Verilen sorguyla ilgili en alakalı videoları arar.

    Dönüş: [{"title", "channel", "url", "thumbnail"}, ...]
    """
    youtube = _get_client()
    response = (
        youtube.search()
        .list(q=query, part="snippet", type="video", maxResults=max_results)
        .execute()
    )

    videos = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        video_id = item["id"]["videoId"]
        videos.append(
            {
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": snippet["thumbnails"]["medium"]["url"],
            }
        )
    return videos
