from mock_backend import answer_question, search_videos


def test_answer_question_includes_the_question_text():
    result = answer_question(pdf_file=None, question="Bu belge ne anlatıyor?")

    assert "Bu belge ne anlatıyor?" in result["answer"]


def test_answer_question_returns_a_source_page():
    result = answer_question(pdf_file=None, question="Herhangi bir soru")

    assert isinstance(result["source_page"], int)
    assert result["source_page"] > 0


def test_search_videos_returns_at_least_one_result():
    videos = search_videos("makine öğrenmesi")

    assert len(videos) >= 1


def test_search_videos_result_has_expected_fields():
    videos = search_videos("örnek konu")

    video = videos[0]
    assert "title" in video
    assert "channel" in video
    assert "url" in video
    assert "thumbnail" in video
    assert video["url"].startswith("http")


def test_search_videos_title_mentions_the_query():
    videos = search_videos("vektör veritabanı")

    assert "vektör veritabanı" in videos[0]["title"]
