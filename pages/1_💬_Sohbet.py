import streamlit as st
from dotenv import load_dotenv

from rag_pipeline import answer_question
from theme import BOT_AVATAR, ICONS, THEME_CSS, USER_AVATAR, render_topnav
from youtube_search import search_videos

load_dotenv()

st.set_page_config(page_title="StudyLens · Sohbet", page_icon="💬", layout="wide")
st.markdown(THEME_CSS, unsafe_allow_html=True)
st.markdown(render_topnav("chat"), unsafe_allow_html=True)

st.markdown(
    '<div class="sl-hero" style="padding:2.1rem 2.4rem;"><div class="sl-hero-inner">'
    f'<span class="sl-badge">{ICONS["sparkle"]}RAG Destekli</span>'
    "<h1 style=\"font-size:1.9rem;\">Belgenle Sohbet Et</h1>"
    '<p class="sl-hero-sub" style="margin-bottom:0;">Soldan bir PDF yükle ve içeriğiyle '
    "ilgili doğal dille soru sor.</p></div></div>",
    unsafe_allow_html=True,
)


def render_video_card(video: dict) -> None:
    st.markdown(
        f'<div class="sl-video-card"><img src="{video["thumbnail"]}" />'
        f'<div><p class="sl-video-title">{ICONS["video"]} '
        f'<a href="{video["url"]}" target="_blank">{video["title"]}</a></p>'
        f'<p class="sl-video-channel">{video["channel"]}</p></div></div>',
        unsafe_allow_html=True,
    )


# --- Çoklu sohbet geçmişi durumu ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
    st.session_state.chat_counter = 0
    st.session_state.current_chat_id = None


def new_chat() -> None:
    st.session_state.chat_counter += 1
    chat_id = st.session_state.chat_counter
    st.session_state.chats[chat_id] = {"title": f"Sohbet {chat_id}", "messages": []}
    st.session_state.current_chat_id = chat_id


def start_new_chat_if_needed() -> None:
    """Mevcut sohbet zaten boşsa yeni bir tane daha oluşturmaz — üst üste boş
    kayıt birikmesini engeller."""
    current = st.session_state.chats.get(st.session_state.current_chat_id)
    if current is not None and not current["messages"]:
        return
    new_chat()


if st.session_state.current_chat_id is None:
    new_chat()

current_chat = st.session_state.chats[st.session_state.current_chat_id]

with st.sidebar:
    st.markdown(
        f'<div class="sl-sidebar-title">{ICONS["folder"]}Belge & Ayarlar</div>',
        unsafe_allow_html=True,
    )
    uploaded_pdf = st.file_uploader("PDF yükleyin", type=["pdf"])
    show_videos = st.checkbox("İlgili YouTube videosu da göster")

    st.markdown(
        f'<div class="sl-sidebar-subtitle">{ICONS["history"]}Sohbet Geçmişi</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sl-new-chat-marker"></div>', unsafe_allow_html=True)
    if st.button("+  Yeni Sohbet", type="secondary", use_container_width=True):
        start_new_chat_if_needed()
        st.rerun()

    if not st.session_state.chats:
        st.markdown('<p class="sl-chat-history-empty">Henüz sohbet yok.</p>', unsafe_allow_html=True)
    else:
        for chat_id in sorted(st.session_state.chats.keys(), reverse=True):
            chat = st.session_state.chats[chat_id]
            is_active = chat_id == st.session_state.current_chat_id
            label = ("● " if is_active else "") + chat["title"]
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"chat_{chat_id}", type=btn_type, use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.rerun()

for message in current_chat["messages"]:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        if message.get("videos"):
            for video in message["videos"]:
                render_video_card(video)

question = st.chat_input(
    "Sorunuzu yazın..." if uploaded_pdf else "Önce bir PDF yükleyin"
)

if question:
    if not uploaded_pdf:
        st.warning("Lütfen önce bir PDF yükleyin.")
    else:
        if not current_chat["messages"]:
            # Sohbet geçmişinde kolayca bulunabilmesi için başlığı sorulan
            # ilk soruya göre adlandır.
            clean_q = question.strip().rstrip("?!. ").capitalize()
            current_chat["title"] = clean_q[:38] + ("…" if len(clean_q) > 38 else "")

        current_chat["messages"].append({"role": "user", "content": question})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(question)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            try:
                with st.spinner("Belge inceleniyor..."):
                    result = answer_question(uploaded_pdf, question)
            except (RuntimeError, ValueError) as exc:
                st.error(str(exc))
                current_chat["messages"].append({"role": "assistant", "content": f"⚠️ {exc}"})
                st.stop()

            st.write(result["answer"])
            st.markdown(
                f'<span class="sl-source-tag">{ICONS["pin"]}Kaynak: sayfa {result["source_page"]}</span>',
                unsafe_allow_html=True,
            )

            videos = None
            if show_videos:
                try:
                    with st.spinner("İlgili videolar aranıyor..."):
                        videos = search_videos(question)
                    for video in videos:
                        render_video_card(video)
                except RuntimeError as exc:
                    st.warning(f"İlgili videolar getirilemedi: {exc}")

        current_chat["messages"].append(
            {
                "role": "assistant",
                "content": f"{result['answer']}\n\n*Kaynak: sayfa {result['source_page']}*",
                "videos": videos,
            }
        )
        st.rerun()
