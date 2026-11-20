import streamlit as st

def inject_custom_ui():
    """Injects premium, custom global CSS for the application."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* ── Reset and Fonts ── */
    *, *::before, *::after {
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Streamlit Top Header & Toolbar ── */
    header[data-testid="stHeader"] {
        background: rgba(3, 7, 18, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1) !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }

    .stDeployButton, [data-testid="stToolbar"] {
        color: #94a3b8 !important;
    }

    /* ── Hide Streamlit Auto Sidebar Navigation (Fixes duplicate pages list) ── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavSeparator"],
    nav[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ── App Canvas ── */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 100%) !important;
        background-attachment: fixed !important;
        min-height: 100vh;
        color: #e2e8f0;
    }

    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090d16 0%, #030712 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.14) !important;
        backdrop-filter: blur(24px) !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
    }

    /* ── Main container ── */
    .main .block-container {
        padding: 2rem 3rem 4rem !important;
        max-width: 1350px;
    }

    /* ── Headings ── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em !important;
    }
    
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }

    p:not(.stButton p), li {
        color: #94a3b8 !important;
        line-height: 1.6;
    }

    /* ── Global Button Normalization ── */
    .stButton button {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.01em !important;
        cursor: pointer !important;
    }

    .stButton button,
    .stButton button p,
    .stButton button span,
    .stButton button div {
        text-decoration: none !important;
    }

    /* Primary Buttons (Glowing Gradient CTA) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        padding: 0.65rem 1.8rem !important;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] div,
    .stButton > button[data-testid="baseButton-primary"] p,
    .stButton > button[data-testid="baseButton-primary"] span,
    button[data-testid="baseButton-primary"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: inherit !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 50%, #7e22ce 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Secondary Buttons (Glass Slate) */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-secondary"] {
        background: rgba(30, 41, 59, 0.75) !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
        padding: 0.6rem 1.6rem !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(8px) !important;
    }

    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span,
    .stButton > button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-secondary"] p {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: inherit !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        color: #ffffff !important;
        border-color: #818cf8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
    }

    .stButton > button[kind="secondary"]:hover p,
    .stButton > button[data-testid="baseButton-secondary"]:hover p,
    button[data-testid="baseButton-secondary"]:hover p {
        color: #ffffff !important;
    }

    /* Fallback Default Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 0.65rem 1.8rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.35) !important;
    }

    .stButton > button p,
    .stButton > button span {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Disabled State */
    .stButton > button:disabled,
    .stButton > button[disabled] {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        box-shadow: none !important;
        transform: none !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }

    .stButton > button:disabled p,
    .stButton > button[disabled] p {
        color: #64748b !important;
    }

    /* ── Metrics Cards (Glassmorphism) ── */
    [data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.5rem !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        margin-top: 0.25rem !important;
    }

    /* ── Text and Input Fields ── */
    .stTextInput input,
    .stTextArea textarea {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 0.6rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    /* Selectbox (BaseWeb) */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] > div {
        background: rgba(17, 24, 39, 0.85) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] * {
        color: #f1f5f9 !important;
        fill: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"],
    div[role="listbox"] {
        background: #0b1120 !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6) !important;
    }
    li[role="option"],
    ul[data-baseweb="menu"] li {
        color: #f1f5f9 !important;
        background: transparent !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    ul[data-baseweb="menu"] li:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        color: #ffffff !important;
    }

    /* ── File Uploader ── */
    [data-testid="stFileUploader"] {
        background: rgba(17, 24, 39, 0.4) !important;
        border: 2px dashed rgba(99, 102, 241, 0.25) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        background: rgba(17, 24, 39, 0.6) !important;
        border-color: rgba(99, 102, 241, 0.45) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px dashed rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.45rem 1.2rem !important;
    }
    [data-testid="stFileUploaderDropzone"] button * {
        color: #ffffff !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(17, 24, 39, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background: rgba(17, 24, 39, 0.2) !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        border-top: none !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding: 1.2rem !important;
    }

    /* ── Page Link Pills ── */
    [data-testid="stPageLink"] > a {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s ease !important;
        color: #94a3b8 !important;
        margin-bottom: 0.4rem !important;
    }
    [data-testid="stPageLink"] > a:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.25) !important;
        color: #ffffff !important;
        transform: translateX(2px);
    }
    [data-testid="stPageLink"] > a[data-selected="true"] {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        color: #818cf8 !important;
        font-weight: 600 !important;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin-bottom: 0.75rem !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: rgba(99, 102, 241, 0.08) !important;
        border-color: rgba(99, 102, 241, 0.15) !important;
        margin-left: 2rem !important;
    }

    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: rgba(17, 24, 39, 0.7) !important;
        border-color: rgba(99, 102, 241, 0.1) !important;
        margin-right: 2rem !important;
    }

    /* ── Chat Input ── */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        background: rgba(17, 24, 39, 0.9) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
        backdrop-filter: blur(12px) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3), 0 8px 30px rgba(99, 102, 241, 0.2) !important;
    }

    /* ── Chat Bottom Container (Removes white bar behind chat input) ── */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stChatFloatingInputContainer {
        background: transparent !important;
        background-color: transparent !important;
    }
    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, transparent 0%, rgba(3, 7, 18, 0.95) 40%) !important;
    }

    /* ── Scrollbars ── */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(3, 7, 18, 0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.25);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.45);
    }

    /* ── Alerts Custom Styling ── */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        border-width: 1px !important;
        padding: 0.8rem 1.2rem !important;
    }
    .stSuccess { background: rgba(16, 185, 129, 0.08) !important; border-color: rgba(16, 185, 129, 0.2) !important; color: #34d399 !important; }
    .stError   { background: rgba(244, 63, 94, 0.08) !important; border-color: rgba(244, 63, 94, 0.2) !important; color: #f43f5e !important; }
    .stWarning { background: rgba(245, 158, 11, 0.08) !important; border-color: rgba(245, 158, 11, 0.2) !important; color: #fbbf24 !important; }
    .stInfo    { background: rgba(59, 130, 246, 0.08) !important; border-color: rgba(59, 130, 246, 0.2) !important; color: #60a5fa !important; }

    /* ── Cards Helper ── */
    .glass-card {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1rem !important;
    }

    .hover-lift {
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease !important;
    }
    .hover-lift:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(99, 102, 241, 0.35) !important;
        box-shadow: 0 15px 45px 0 rgba(99, 102, 241, 0.15) !important;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }

    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str, icon: str = "🧠", badge: str = "System Online"):
    """Renders a beautiful visual header card at the top of a page."""
    badge_html = f"""
    <div style="margin-left: auto; display: flex; align-items: center; gap: 8px; padding: 6px 14px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 9999px;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block; box-shadow: 0 0 10px #10b981;"></span>
        <span style="color: #34d399; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">{badge}</span>
    </div>
    """ if badge else ""

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1.2rem; margin-bottom:2rem; padding: 1.4rem 1.8rem; background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 20px; backdrop-filter: blur(16px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);">
        <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius: 16px; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4); flex-shrink: 0;">
            {icon}
        </div>
        <div style="min-width: 0;">
            <h1 style="margin: 0; font-size: 1.9rem; font-weight: 800; background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {title}
            </h1>
            <p style="margin: 0.25rem 0 0; color: #94a3b8 !important; font-size: 0.88rem; font-weight: 500;">
                {subtitle}
            </p>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_branding():
    """Renders the top branding section in the sidebar."""
    st.markdown("""
    <div style="text-align:center; padding: 0.8rem 0 1.2rem;">
        <div style="width: 58px; height: 58px; margin: 0 auto 0.75rem; border-radius: 18px; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);">
            🧠
        </div>
        <h2 style="color:#ffffff !important; font-weight:800; margin:0; font-size:1.35rem; letter-spacing: -0.02em;">
            Knowledge <span style="background: linear-gradient(90deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Copilot</span>
        </h2>
        <p style="color:#64748b !important; font-size:0.75rem; margin:0.25rem 0 0.6rem; font-weight: 500;">RAG-Powered Document Intelligence</p>
        <div style="display:inline-flex; align-items:center; gap:6px; padding:3px 12px; border-radius:9999px; background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.25);">
            <span style="width:6px; height:6px; border-radius:50%; background:#10b981; display:inline-block; box-shadow:0 0 8px #10b981;"></span>
            <span style="color:#34d399 !important; font-size:0.68rem; font-weight:600; letter-spacing:0.04em;">SYSTEM ONLINE</span>
        </div>
    </div>
    <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), transparent); margin: 0.5rem 0 1rem;"></div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the standard sidebar links and logo."""
    with st.sidebar:
        render_sidebar_branding()
        st.page_link("pages/Dashboard.py", label="🏠 Dashboard")
        st.page_link("pages/Chat.py",      label="💬 Chat")
        st.page_link("pages/Upload.py",    label="📤 Upload")
        st.page_link("pages/Knowledge_base.py", label="📚 Knowledge Base")
        st.page_link("pages/Setting.py",   label="⚙️ Settings")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:1rem; background:rgba(17, 24, 39, 0.6); border-radius:14px; border:1px solid rgba(99, 102, 241, 0.15); text-align:center;">
            <div style="display:flex; justify-content:center; align-items:center; gap:6px; margin-bottom:4px;">
                <span style="font-size:0.8rem;">⚡</span>
                <span style="color:#e2e8f0; font-size:0.75rem; font-weight:600;">Gemini 2.5 Flash</span>
            </div>
            <p style="color:#64748b !important; font-size:0.7rem; margin:0; font-weight: 500;">
                BGE-Small · ChromaDB v1.0
            </p>
        </div>
        """, unsafe_allow_html=True)
