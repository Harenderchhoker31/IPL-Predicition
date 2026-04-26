with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'r') as f:
    lines = f.readlines()

# Find start and end line of CSS block
start = None
end = None
for i, line in enumerate(lines):
    if '# ── Custom CSS' in line:
        start = i
    if start and 'BG   =' in line and 'CARD =' in line:
        end = i
        break

print(f"CSS block: lines {start+1} to {end+1}")

new_block = '''# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1117 40%, #0f1923 70%, #0a0e1a 100%);
        background-size: 400% 400%;
        animation: gradientShift 18s ease infinite;
        color: #e6edf3;
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp::before {
        content: '';
        position: fixed; inset: 0;
        background-image: radial-gradient(circle, #ffffff06 1px, transparent 1px);
        background-size: 32px 32px;
        pointer-events: none; z-index: 0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #111827 100%) !important;
        border-right: 1px solid #1f2937;
        box-shadow: 4px 0 24px rgba(0,0,0,0.5);
    }
    [data-testid="stSidebar"] * { color: #e6edf3 !important; }

    .metric-card {
        background: rgba(17,24,39,0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(249,115,22,0.15);
        border-radius: 16px; padding: 22px 16px;
        text-align: center; margin: 6px 0;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        position: relative; overflow: hidden;
    }
    .metric-card::before {
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #f97316, transparent);
        opacity: 0; transition: opacity 0.25s;
    }
    .metric-card:hover { transform: translateY(-5px); border-color: rgba(249,115,22,0.5); box-shadow: 0 8px 32px rgba(249,115,22,0.18); }
    .metric-card:hover::before { opacity: 1; }
    .metric-value { font-size: 2.2rem; font-weight: 900; margin: 0; line-height: 1.1; letter-spacing: -0.02em; }
    .metric-label { font-size: 0.72rem; color: #6b7280; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }

    .section-header {
        background: linear-gradient(90deg, #f97316 0%, #fb923c 50%, #fbbf24 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 1.55rem; font-weight: 900; margin: 20px 0 8px 0;
        letter-spacing: -0.02em;
        filter: drop-shadow(0 0 20px rgba(249,115,22,0.3));
    }
    .insight-box {
        background: rgba(17,24,39,0.8);
        backdrop-filter: blur(8px);
        border-left: 3px solid #f97316;
        border-radius: 0 10px 10px 0;
        padding: 13px 18px; margin: 7px 0; font-size: 0.9rem;
        transition: border-left-width 0.2s;
    }
    .insight-box:hover { border-left-width: 5px; }
    .insight-box b { color: #f97316; }

    .hero-title {
        font-size: 3.4rem; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 40%, #fbbf24 70%, #f97316 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        line-height: 1.15; letter-spacing: -0.03em;
    }
    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .hero-sub { text-align: center; color: #6b7280; font-size: 1rem; margin: 8px 0 24px; font-weight: 500; }

    .tag {
        display: inline-block;
        background: rgba(249,115,22,0.08);
        border: 1px solid rgba(249,115,22,0.25);
        border-radius: 20px; padding: 4px 14px; margin: 3px;
        font-size: 0.75rem; color: #fb923c; font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(17,24,39,0.6);
        border-radius: 12px; padding: 4px; gap: 2px; border: 1px solid #1f2937;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; color: #6b7280 !important;
        font-weight: 600; font-size: 0.85rem; padding: 8px 18px; transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f97316, #fb923c) !important;
        color: #fff !important; box-shadow: 0 4px 12px rgba(249,115,22,0.35);
    }
    .stButton > button {
        background: linear-gradient(135deg, #f97316, #fb923c) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
        font-size: 0.9rem !important; padding: 10px 24px !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 15px rgba(249,115,22,0.3) !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(249,115,22,0.45) !important; }
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background: rgba(17,24,39,0.8) !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important; color: #e6edf3 !important;
    }
    .stSlider > div > div > div > div { background: #f97316 !important; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #f97316; border-radius: 3px; }
    div[data-testid="stMetricValue"] { color: #f97316 !important; }
    h1,h2,h3 { color: #e6edf3 !important; letter-spacing: -0.02em; }
    .stSelectbox label, .stSlider label, .stNumberInput label { color: #6b7280 !important; font-size: 0.8rem !important; font-weight: 600 !important; }
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #1f2937; }
    .block-container { padding-top: 2rem !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Color Palette ─────────────────────────────────────────────
BG   = '#0a0e1a'; CARD = '#111827'
'''

lines[start:end+1] = [new_block]

with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'w') as f:
    f.writelines(lines)

print("Done")
