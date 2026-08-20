import base64

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 12% -5%, rgba(139, 92, 246, 0.16) 0%, transparent 40%),
        radial-gradient(circle at 100% 0%, rgba(6, 182, 212, 0.14) 0%, transparent 38%),
        radial-gradient(circle at 50% 100%, rgba(236, 72, 153, 0.08) 0%, transparent 45%),
        #f6f5fb;
    background-attachment: fixed;
}

/* Constrain + center the wide layout like a real landing page */
div[data-testid="stAppViewContainer"] .block-container {
    max-width: 1080px;
    padding-top: 3.4rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit's default multipage nav list + footer chrome */
div[data-testid="stSidebarNav"],
#MainMenu,
footer {
    display: none;
}

/* ---------- Top glass navigation ---------- */
.sl-topnav {
    display: flex;
    gap: .55rem;
    justify-content: flex-end;
    margin: 0 0 1.4rem 0;
}
.sl-glass-btn {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .58rem 1.2rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(14px) saturate(160%);
    -webkit-backdrop-filter: blur(14px) saturate(160%);
    border: 1px solid rgba(124, 58, 237, 0.22);
    box-shadow: 0 4px 18px -8px rgba(99, 102, 241, 0.35);
    color: #312e81 !important;
    font-weight: 600;
    font-size: .87rem;
    text-decoration: none !important;
    transition: transform .25s cubic-bezier(.34,1.56,.64,1), box-shadow .25s ease, background .25s ease, color .25s ease;
}
.sl-glass-btn svg {
    width: 16px;
    height: 16px;
    transition: transform .25s ease;
}
.sl-glass-btn:hover {
    transform: translateY(-3px) scale(1.05);
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white !important;
    box-shadow: 0 10px 26px -6px rgba(124, 58, 237, 0.55);
}
.sl-glass-btn:hover svg { transform: rotate(-8deg) scale(1.12); }
.sl-glass-btn.sl-active {
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white !important;
    box-shadow: 0 8px 22px -6px rgba(124, 58, 237, 0.5);
}

/* ---------- Hero ---------- */
.sl-hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #6d28d9 0%, #4f46e5 48%, #0891b2 100%);
    border-radius: 28px;
    padding: 3.2rem 3rem;
    margin-bottom: 2.2rem;
    box-shadow: 0 24px 55px -22px rgba(76, 29, 149, 0.55);
    color: white;
    background-image:
        radial-gradient(circle, rgba(255,255,255,.14) 1px, transparent 1px),
        linear-gradient(135deg, #6d28d9 0%, #4f46e5 48%, #0891b2 100%);
    background-size: 22px 22px, 100% 100%;
}
.sl-hero::before, .sl-hero::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(50px);
    opacity: .55;
    pointer-events: none;
}
.sl-hero::before { width: 280px; height: 280px; background: #a78bfa; top: -110px; right: -70px; }
.sl-hero::after { width: 240px; height: 240px; background: #22d3ee; bottom: -120px; left: -60px; }
.sl-hero-inner { position: relative; z-index: 1; max-width: 640px; }
.sl-hero h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    line-height: 1.15;
    margin: .8rem 0 .8rem 0;
    color: white;
}
.sl-hero-sub {
    margin: 0 0 1.7rem 0;
    opacity: .93;
    font-size: 1.06rem;
    line-height: 1.55;
    max-width: 540px;
}
.sl-badge {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.4);
    border-radius: 999px;
    padding: .32rem .9rem;
    font-size: .76rem;
    font-weight: 700;
    letter-spacing: .04em;
    text-transform: uppercase;
}
.sl-badge svg { width: 14px; height: 14px; }

.sl-trust-row {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    margin-top: .3rem;
}
.sl-trust-pill {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 999px;
    padding: .3rem .75rem;
    font-size: .78rem;
    font-weight: 600;
}
.sl-trust-pill svg { width: 13px; height: 13px; }

/* ---------- CTA button ---------- */
.sl-cta-btn {
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    gap: .55rem;
    padding: .9rem 1.7rem;
    border-radius: 14px;
    background: white;
    color: #4f46e5 !important;
    font-weight: 700;
    font-size: 1rem;
    text-decoration: none !important;
    box-shadow: 0 16px 34px -12px rgba(15, 10, 40, 0.45);
    transition: transform .25s cubic-bezier(.34,1.56,.64,1), box-shadow .25s ease;
}
.sl-cta-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px -10px rgba(15, 10, 40, 0.5);
}
.sl-cta-btn::after {
    content: "";
    position: absolute;
    top: 0; left: -75%;
    width: 50%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(124,58,237,.25), transparent);
    transform: skewX(-20deg);
    transition: left .65s ease;
}
.sl-cta-btn:hover::after { left: 130%; }
.sl-cta-btn svg { width: 18px; height: 18px; }

/* ---------- Section headers ---------- */
.sl-section-head {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin: 0 0 .2rem 0;
}
.sl-section-head .sl-icon-badge { margin: 0; width: 38px; height: 38px; border-radius: 11px; }
.sl-section-head h3 {
    font-family: 'Poppins', sans-serif;
    color: #1e1b4b;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0;
}
.sl-section-sub {
    color: #6b7280;
    font-size: .92rem;
    margin: .35rem 0 1.3rem 50px;
}

/* ---------- Grid ---------- */
.sl-grid {
    display: grid;
    gap: 1.1rem;
    margin-bottom: 1.6rem;
}
.sl-grid-3 { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.sl-grid-4 { grid-template-columns: repeat(auto-fit, minmax(215px, 1fr)); }

/* ---------- Cards ---------- */
.sl-step-card, .sl-feature-card {
    position: relative;
    background: white;
    border-radius: 18px;
    padding: 1.3rem 1.3rem 1.4rem 1.3rem;
    border: 1px solid #ece9fb;
    box-shadow: 0 8px 22px -14px rgba(76, 29, 149, 0.22);
    overflow: hidden;
    transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
.sl-step-card::before, .sl-feature-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #7c3aed, #6366f1, #06b6d4);
    opacity: 0;
    transition: opacity .22s ease;
}
.sl-step-card:hover, .sl-feature-card:hover {
    transform: translateY(-6px);
    border-color: #ddd6fe;
    box-shadow: 0 20px 36px -16px rgba(76, 29, 149, 0.35);
}
.sl-step-card:hover::before, .sl-feature-card:hover::before { opacity: 1; }
.sl-step-card .sl-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 999px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white;
    font-weight: 700;
    font-size: .85rem;
    margin-bottom: .7rem;
    box-shadow: 0 6px 14px -6px rgba(124, 58, 237, 0.5);
}
.sl-step-card h4, .sl-feature-card h4 {
    font-family: 'Poppins', sans-serif;
    margin: 0 0 .35rem 0;
    color: #241f4d;
    font-size: 1.02rem;
    font-weight: 600;
}
.sl-step-card p, .sl-feature-card p {
    margin: 0;
    color: #5c6270;
    font-size: .88rem;
    line-height: 1.5;
}
.sl-icon-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    border-radius: 14px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white;
    margin-bottom: .7rem;
    box-shadow: 0 10px 18px -6px rgba(124, 58, 237, 0.5);
}
.sl-icon-badge svg { width: 22px; height: 22px; }
.sl-icon-badge.c2 { background: linear-gradient(135deg, #db2777, #7c3aed); box-shadow: 0 10px 18px -6px rgba(219, 39, 119, 0.45); }
.sl-icon-badge.c3 { background: linear-gradient(135deg, #0891b2, #0ea5e9); box-shadow: 0 10px 18px -6px rgba(8, 145, 178, 0.45); }
.sl-icon-badge.c4 { background: linear-gradient(135deg, #f59e0b, #ea580c); box-shadow: 0 10px 18px -6px rgba(245, 158, 11, 0.45); }

/* ---------- Callout ---------- */
.sl-callout {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: linear-gradient(135deg, rgba(124,58,237,.07), rgba(6,182,212,.08));
    border: 1px solid #e0d9fb;
    border-radius: 18px;
    padding: 1.1rem 1.4rem;
    color: #312e81;
    font-size: .95rem;
}
.sl-callout .sl-icon-badge { margin: 0; flex-shrink: 0; width: 40px; height: 40px; border-radius: 12px; }
.sl-callout .sl-icon-badge svg { width: 19px; height: 19px; }
.sl-callout b { color: #5b21b6; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
}
section[data-testid="stSidebar"] * { color: #ede9fe !important; }
section[data-testid="stSidebar"] .stFileUploader section {
    background: rgba(255,255,255,.06);
    border: 1.5px dashed rgba(255,255,255,.35);
    border-radius: 14px;
}
/* Primary sidebar action (e.g. "Yeni Sohbet") */
section[data-testid="stSidebar"] button[kind="primary"],
section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600;
}
/* Secondary sidebar buttons (chat history list items) */
section[data-testid="stSidebar"] button[kind="secondary"],
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: rgba(255,255,255,.05) !important;
    color: #ddd6fe !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover,
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    background: rgba(139, 92, 246, .25) !important;
    border-color: rgba(139, 92, 246, .5) !important;
}
/* "+ Yeni Sohbet" gets its own dashed "add" look, distinct from history items */
div.stElementContainer:has(.sl-new-chat-marker) + div.stElementContainer button {
    background: rgba(139, 92, 246, .1) !important;
    border: 1.5px dashed rgba(196, 181, 253, .55) !important;
    color: #ddd6fe !important;
    font-weight: 600 !important;
}
div.stElementContainer:has(.sl-new-chat-marker) + div.stElementContainer button:hover {
    background: rgba(139, 92, 246, .22) !important;
    border-color: #c4b5fd !important;
}
.sl-sidebar-title {
    display: flex;
    align-items: center;
    gap: .5rem;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: #fff !important;
    margin: 0 0 .8rem 0;
}
.sl-sidebar-title svg { width: 18px; height: 18px; }
.sl-sidebar-subtitle {
    display: flex;
    align-items: center;
    gap: .4rem;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .03em;
    text-transform: uppercase;
    color: rgba(237,233,254,.55) !important;
    margin: 1.1rem 0 .5rem 0;
}
.sl-sidebar-subtitle svg { width: 13px; height: 13px; }
.sl-chat-history-empty {
    font-size: .8rem;
    color: rgba(237,233,254,.5) !important;
    padding: .3rem 0;
}

/* ---------- Chat bubbles ---------- */
div[data-testid="stChatMessage"] {
    background: white;
    border-radius: 18px;
    padding: .35rem .6rem;
    margin-bottom: .8rem;
    box-shadow: 0 6px 18px -10px rgba(76, 29, 149, 0.2);
    border: 1px solid #ece9fb;
}
div[data-testid="stChatInput"] textarea { border-radius: 14px !important; }

/* ---------- Video card ---------- */
.sl-video-card {
    display: flex;
    gap: .9rem;
    background: white;
    border-radius: 14px;
    padding: .6rem;
    margin-top: .5rem;
    border: 1px solid #e0e7ff;
    box-shadow: 0 4px 14px -8px rgba(30, 27, 75, 0.25);
    align-items: center;
    transition: transform .15s ease;
}
.sl-video-card:hover { transform: translateY(-2px); }
.sl-video-card img { width: 120px; border-radius: 10px; object-fit: cover; }
.sl-video-title { font-weight: 600; color: #312e81; margin: 0 0 .15rem 0; }
.sl-video-title a { color: #312e81; text-decoration: none; }
.sl-video-channel { font-size: .82rem; color: #7c3aed; }
.sl-source-tag {
    display: inline-flex;
    align-items: center;
    gap: .3rem;
    margin-top: .4rem;
    background: #ecfeff;
    color: #0e7490;
    border: 1px solid #a5f3fc;
    border-radius: 999px;
    padding: .2rem .7rem;
    font-size: .75rem;
    font-weight: 600;
}
.sl-source-tag svg { width: 12px; height: 12px; }
</style>
"""


ICONS = {
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1H9a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1h2.5a1 1 0 0 0 1-1v-9"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 1 1-3.4-6.55L21 4l-1.2 3.9A7.96 7.96 0 0 1 21 12Z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/></svg>',
    "upload": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V4"/><path d="m7 8 5-5 5 5"/><path d="M4.5 15v3.5a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V15"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>',
    "cpu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="m9 11 3 3 9-9"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="5.5" width="14" height="13" rx="2"/><path d="m21.5 8-5 3 5 3z"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z"/></svg>',
    "trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-13"/></svg>',
    "folder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 13.8 8.7 20 10.5l-6.2 1.8L12 19l-1.8-6.7L4 10.5l6.2-1.8L12 2Z"/><path d="M19 15l.8 2.6L22.5 18.4l-2.7.8L19 21.8l-.8-2.6-2.7-.8 2.7-.8L19 15Z"/></svg>',
    "arrow-right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>',
    "point": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4c-4 0-6 2-6 6v3"/><path d="m5 10 3 3 3-3"/><rect x="4" y="15" width="16" height="6" rx="2"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1.04 1.56V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.37a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.56-1.04H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.63 9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1.04-1.56V3a2 2 0 1 1 4 0v.09A1.7 1.7 0 0 0 15 4.63a1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9a1.7 1.7 0 0 0 1.56 1.04H21a2 2 0 1 1 0 4h-.09A1.7 1.7 0 0 0 19.4 15Z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 2.9 6.6 7.1.7-5.4 4.8 1.6 7-6.2-3.7L6 21.1l1.6-7L2.2 9.3l7.1-.7L12 2Z"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
    "history": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 2.6-6.3"/><path d="M3 5v5h5"/><path d="M12 8v4l3 3"/></svg>',
}


def render_topnav(active: str) -> str:
    """active: 'home' or 'chat' — returns HTML for the glass pill navbar."""
    home_cls = "sl-glass-btn sl-active" if active == "home" else "sl-glass-btn"
    chat_cls = "sl-glass-btn sl-active" if active == "chat" else "sl-glass-btn"
    return (
        '<div class="sl-topnav">'
        f'<a class="{home_cls}" href="/" target="_self">{ICONS["home"]}<span>Ana Sayfa</span></a>'
        f'<a class="{chat_cls}" href="/Sohbet" target="_self">{ICONS["chat"]}<span>Sohbet</span></a>'
        "</div>"
    )


def render_section_head(icon_key: str, title: str, subtitle: str = "") -> str:
    sub_html = f'<p class="sl-section-sub">{subtitle}</p>' if subtitle else ""
    return (
        '<div class="sl-section-head">'
        f'<span class="sl-icon-badge">{ICONS[icon_key]}</span>'
        f"<h3>{title}</h3>"
        "</div>" + sub_html
    )


def render_callout(icon_key: str, html: str) -> str:
    return (
        '<div class="sl-callout">'
        f'<span class="sl-icon-badge">{ICONS[icon_key]}</span>'
        f"<div>{html}</div></div>"
    )


def _svg_avatar(bg1: str, bg2: str, inner_svg: str) -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>'
        "</linearGradient></defs>"
        '<circle cx="32" cy="32" r="32" fill="url(#g)"/>'
        f'<g transform="translate(16,16)" stroke="white" stroke-width="2.3" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round">{inner_svg}</g></svg>'
    )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


USER_AVATAR = _svg_avatar(
    "#7c3aed", "#6366f1",
    '<circle cx="16" cy="11" r="6"/><path d="M4 30c0-7 5-12 12-12s12 5 12 12"/>',
)
BOT_AVATAR = _svg_avatar(
    "#0891b2", "#0ea5e9",
    '<rect x="6" y="10" width="20" height="16" rx="4"/><path d="M16 10V4M11 4h10"/>'
    '<circle cx="12.5" cy="18" r="1.6" fill="white" stroke="none"/>'
    '<circle cx="19.5" cy="18" r="1.6" fill="white" stroke="none"/>',
)


HERO_ART_SVG = """
<svg class="sl-hero-art" width="230" height="190" viewBox="0 0 230 190" xmlns="http://www.w3.org/2000/svg" style="position:absolute;right:10px;top:10px;opacity:.85;pointer-events:none;">
  <g opacity="0.95">
    <rect x="100" y="18" width="82" height="108" rx="12" fill="white" fill-opacity="0.14" stroke="white" stroke-opacity="0.5"/>
    <line x1="112" y1="40" x2="168" y2="40" stroke="white" stroke-opacity="0.6" stroke-width="3" stroke-linecap="round"/>
    <line x1="112" y1="55" x2="168" y2="55" stroke="white" stroke-opacity="0.45" stroke-width="3" stroke-linecap="round"/>
    <line x1="112" y1="70" x2="148" y2="70" stroke="white" stroke-opacity="0.45" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="115" r="36" fill="white" fill-opacity="0.16" stroke="white" stroke-opacity="0.5"/>
    <circle cx="50" cy="115" r="12" fill="none" stroke="white" stroke-opacity="0.8" stroke-width="3"/>
    <line x1="59" y1="124" x2="68" y2="133" stroke="white" stroke-opacity="0.8" stroke-width="3" stroke-linecap="round"/>
    <circle cx="158" cy="152" r="4" fill="white"/>
    <circle cx="50" cy="158" r="4" fill="white" fill-opacity="0.7"/>
    <circle cx="195" cy="95" r="3" fill="white" fill-opacity="0.6"/>
    <path d="M85 105 L100 92" stroke="white" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="3 4"/>
  </g>
</svg>
"""
