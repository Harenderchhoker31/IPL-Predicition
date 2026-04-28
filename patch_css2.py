with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find CSS block boundaries
start, end = None, None
for i, line in enumerate(lines):
    if '# ── Custom CSS' in line:
        start = i
    if start and "BG   =" in line and "CARD =" in line:
        end = i
        break

print(f"Replacing lines {start+1} to {end+1}")

new_css = '''# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background: deep navy with subtle mesh ── */
    .stApp {
        background-color: #060b14;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(249,115,22,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(59,130,246,0.08) 0%, transparent 60%),
            radial-gradient(circle at 50% 50%, rgba(255,255,255,0.015) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 28px 28px;
        color: #e2e8f0;
        min-height: 100vh;
    }

    /* ── Main content area ── */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0a0f1e 0%, #0d1424 100%) !important;
        border-right: 1px solid rgba(249,115,22,0.12) !important;
        box-shadow: 2px 0 20px rgba(0,0,0,0.6) !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f97316 !important; }
    [data-testid="stSidebar"] .stRadio > div { gap: 2px; }
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 14px !important;
        border-radius: 10px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #94a3b8 !important;
        transition: all 0.18s ease !important;
        cursor: pointer;
        border: 1px solid transparent !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(249,115,22,0.1) !important;
        color: #f97316 !important;
        border-color: rgba(249,115,22,0.2) !important;
    }
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: rgba(249,115,22,0.15) !important;
        color: #f97316 !important;
        border-color: rgba(249,115,22,0.3) !important;
        font-weight: 600 !important;
    }

    /* ── Hero title ── */
    .hero-title {
        font-size: 3.6rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 35%, #fbbf24 65%, #f97316 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 5s linear infinite;
        line-height: 1.15;
        letter-spacing: -0.04em;
        padding: 8px 0 6px;
        filter: drop-shadow(0 0 30px rgba(249,115,22,0.5));
    }
    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .hero-sub {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 6px 0 28px;
        letter-spacing: 0.02em;
    }

    /* ── Section header ── */
    .section-header {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #f97316, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 24px 0 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(249,115,22,0.15);
    }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(17,24,39,0.95));
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 24px 18px;
        text-align: center;
        margin: 5px 0;
        position: relative;
        overflow: hidden;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        backdrop-filter: blur(10px);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(249,115,22,0.04), transparent 60%);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(249,115,22,0.35);
        box-shadow: 0 12px 40px rgba(249,115,22,0.12), 0 4px 12px rgba(0,0,0,0.4);
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #64748b;
        margin-top: 7px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* ── Insight boxes ── */
    .insight-box {
        background: linear-gradient(135deg, rgba(15,23,42,0.8), rgba(17,24,39,0.9));
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 3px solid #f97316;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #cbd5e1;
        transition: border-left-color 0.2s, transform 0.2s;
    }
    .insight-box:hover {
        border-left-color: #fbbf24;
        transform: translateX(3px);
    }
    .insight-box b { color: #f97316; font-weight: 700; }

    /* ── Tags ── */
    .tag {
        display: inline-block;
        background: rgba(249,115,22,0.07);
        border: 1px solid rgba(249,115,22,0.2);
        border-radius: 999px;
        padding: 4px 14px;
        margin: 3px;
        font-size: 0.75rem;
        color: #fb923c;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: background 0.15s;
    }
    .tag:hover { background: rgba(249,115,22,0.15); }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10,15,30,0.7);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 5px;
        gap: 3px;
        backdrop-filter: blur(8px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #64748b !important;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 9px 20px;
        transition: all 0.18s ease;
        border: 1px solid transparent;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #94a3b8 !important;
        background: rgba(255,255,255,0.04);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ea6c0a, #f97316) !important;
        color: #fff !important;
        box-shadow: 0 4px 16px rgba(249,115,22,0.3);
        border-color: rgba(249,115,22,0.4) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #ea6c0a 0%, #f97316 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 11px 28px !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(249,115,22,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(249,115,22,0.4) !important;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Form inputs ── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(10,15,30,0.8) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        transition: border-color 0.18s !important;
    }
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {
        border-color: rgba(249,115,22,0.5) !important;
        box-shadow: 0 0 0 3px rgba(249,115,22,0.1) !important;
    }
    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stTextArea label,
    .stRadio label {
        color: #64748b !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
    }

    /* ── Slider ── */
    .stSlider > div > div > div > div { background: #f97316 !important; }
    .stSlider > div > div > div > div > div { background: #fff !important; border: 2px solid #f97316 !important; }

    /* ── Dataframe ── */
    .stDataFrame {
        border-radius: 14px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }

    /* ── Alerts ── */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        backdrop-filter: blur(8px) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        background: rgba(10,15,30,0.6) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    /* ── Typography ── */
    h1, h2, h3, h4 { color: #f1f5f9 !important; letter-spacing: -0.02em; }
    p, li { color: #cbd5e1; line-height: 1.65; }
    .stMarkdown p { color: #cbd5e1 !important; font-size: 0.95rem; line-height: 1.65; }
    .stCaption, caption { color: #475569 !important; font-size: 0.78rem !important; }
    div[data-testid="stMetricValue"] { color: #f97316 !important; font-weight: 800 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(249,115,22,0.4); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(249,115,22,0.7); }

    /* ── Hide Streamlit chrome ── */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Color Palette ─────────────────────────────────────────────
BG   = '#060b14'; CARD = '#0f1729'
'''

lines[start:end+1] = [new_css]

with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")
