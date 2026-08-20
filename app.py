import streamlit as st
from dotenv import load_dotenv

from theme import (
    HERO_ART_SVG,
    ICONS,
    THEME_CSS,
    render_callout,
    render_section_head,
    render_topnav,
)

load_dotenv()

st.set_page_config(
    page_title="StudyLens · PDF ile Sohbet",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)
# Bu sayfada sidebar içeriği yok (sadece Sohbet sayfasında kullanılıyor) — tamamen gizle.
st.markdown(
    '<style>section[data-testid="stSidebar"] {display: none;}</style>',
    unsafe_allow_html=True,
)
st.markdown(render_topnav("home"), unsafe_allow_html=True)

# --- Hero ---
st.markdown(
    f'<div class="sl-hero">{HERO_ART_SVG}<div class="sl-hero-inner">'
    f'<span class="sl-badge">{ICONS["sparkle"]}RAG Destekli</span>'
    "<h1>Belgeni oku, ona soru sor.</h1>"
    '<p class="sl-hero-sub">PDF yükle, içeriğiyle ilgili doğal dille soru sor. '
    "Cevaplar yalnızca yüklediğin belgenin içeriğine dayanır — uydurma bilgi yok, "
    "her cevabın kaynağı belli.</p>"
    f'<a class="sl-cta-btn" href="/Sohbet" target="_self">{ICONS["chat"]}Sohbete Başla{ICONS["arrow-right"]}</a>'
    '<div class="sl-trust-row">'
    f'<span class="sl-trust-pill">{ICONS["check"]}Tamamen ücretsiz</span>'
    f'<span class="sl-trust-pill">{ICONS["check"]}Kaynağı gösterilen cevaplar</span>'
    f'<span class="sl-trust-pill">{ICONS["check"]}Opsiyonel video önerisi</span>'
    "</div></div></div>",
    unsafe_allow_html=True,
)

# --- Nasıl çalışır ---
st.markdown(
    render_section_head("settings", "Nasıl Çalışır?", "Beş basit adımda belgenden cevap alırsın."),
    unsafe_allow_html=True,
)

steps = [
    ("1", "PDF'i Yükle", "Belgeni yükle; sistem içeriği okuyup küçük, yönetilebilir parçalara böler."),
    ("2", "Anlamsal İndeks", "Her parça embedding'e çevrilir ve bir vektör veritabanında (FAISS/Chroma) indekslenir."),
    ("3", "En Alakalı Parçaları Bul", "Soru sorduğunda, anlam olarak en yakın birkaç parça bu indeksten seçilir."),
    ("4", "Dil Modeline Gönder", "Seçilen parçalar, sorunla birlikte bir dil modeline (Gemini/Groq) iletilir."),
    ("5", "Cevabı Al", "Model, yalnızca verilen parçalara dayanarak cevap üretir — kaynağı belli, uydurma yok."),
    ("6", "İstersen Video da Bul", "Aynı soru YouTube'da da aratılıp konuyla ilgili video önerileri getirilir."),
]

step_cards = "".join(
    f'<div class="sl-step-card"><span class="sl-step-num">{num}</span>'
    f"<h4>{title}</h4><p>{desc}</p></div>"
    for num, title, desc in steps
)
st.markdown(f'<div class="sl-grid sl-grid-3">{step_cards}</div>', unsafe_allow_html=True)

# --- Özellikler ---
st.markdown(
    render_section_head("star", "Özellikler", "Bu uygulamayı öne çıkaran temel özellikler."),
    unsafe_allow_html=True,
)

features = [
    ("doc", "", "Belgeye Sadık Cevaplar", "Yanıtlar yalnızca yüklediğin PDF'in içeriğine dayanır."),
    ("pin", "c2", "Kaynak Gösterimi", "Her cevabın hangi sayfadan geldiği ayrıca belirtilir."),
    ("video", "c3", "Video Önerisi", "İstersen aynı soru YouTube'da da aratılır, ilgili videolar önerilir."),
    ("bolt", "c4", "Hızlı ve Ücretsiz", "Tamamen ücretsiz katmanlarla çalışan araçlarla kurulmuştur."),
]

feature_cards = "".join(
    f'<div class="sl-feature-card"><span class="sl-icon-badge {cls}">{ICONS[icon_key]}</span>'
    f"<h4>{title}</h4><p>{desc}</p></div>"
    for icon_key, cls, title, desc in features
)
st.markdown(f'<div class="sl-grid sl-grid-4">{feature_cards}</div>', unsafe_allow_html=True)

st.markdown(
    render_callout(
        "point",
        "Başlamak için <b>Sohbet</b> sayfasını aç — sağ üstteki menüden veya "
        "yukarıdaki butondan ulaşabilirsin.",
    ),
    unsafe_allow_html=True,
)
