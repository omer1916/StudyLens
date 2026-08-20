import re

from theme import (
    BOT_AVATAR,
    ICONS,
    USER_AVATAR,
    render_callout,
    render_section_head,
    render_topnav,
)

EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF]", flags=re.UNICODE
)


def test_no_emoji_in_rendered_topnav():
    html = render_topnav("home")

    assert not EMOJI_PATTERN.search(html)


def test_topnav_marks_the_active_page():
    html = render_topnav("chat")

    assert 'sl-active' in html
    assert html.count("sl-glass-btn") == 2  # iki nav linki


def test_topnav_links_to_both_pages():
    html = render_topnav("home")

    assert 'href="/"' in html
    assert 'href="/Sohbet"' in html


def test_render_section_head_uses_known_icon():
    html = render_section_head("star", "Özellikler", "alt başlık")

    assert ICONS["star"] in html
    assert "Özellikler" in html
    assert "alt başlık" in html


def test_render_callout_wraps_icon_and_text():
    html = render_callout("point", "Merhaba <b>dünya</b>")

    assert ICONS["point"] in html
    assert "Merhaba <b>dünya</b>" in html


def test_avatars_are_valid_svg_data_uris():
    for avatar in (USER_AVATAR, BOT_AVATAR):
        assert avatar.startswith("data:image/svg+xml;base64,")


def test_avatars_are_distinct():
    assert USER_AVATAR != BOT_AVATAR


def test_all_icons_are_non_empty_svg_markup():
    for name, svg in ICONS.items():
        assert svg.strip().startswith("<svg"), f"'{name}' ikonu geçerli bir SVG değil"
