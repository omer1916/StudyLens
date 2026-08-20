from unittest.mock import MagicMock, patch

import pytest

import youtube_search


def _fake_api_response():
    return {
        "items": [
            {
                "id": {"videoId": "abc123"},
                "snippet": {
                    "title": "vektör veritabanı nedir?",
                    "channelTitle": "Örnek Kanal",
                    "thumbnails": {"medium": {"url": "https://img.example/abc123.jpg"}},
                },
            }
        ]
    }


def test_search_videos_maps_api_response_to_expected_fields(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "test-key")
    youtube_search._youtube_client = None

    mock_client = MagicMock()
    mock_client.search.return_value.list.return_value.execute.return_value = _fake_api_response()

    with patch("youtube_search.build", return_value=mock_client) as mock_build:
        videos = youtube_search.search_videos("vektör veritabanı")

    mock_build.assert_called_once_with("youtube", "v3", developerKey="test-key")
    assert videos == [
        {
            "title": "vektör veritabanı nedir?",
            "channel": "Örnek Kanal",
            "url": "https://www.youtube.com/watch?v=abc123",
            "thumbnail": "https://img.example/abc123.jpg",
        }
    ]


def test_search_videos_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    youtube_search._youtube_client = None

    with pytest.raises(RuntimeError):
        youtube_search.search_videos("herhangi bir konu")
