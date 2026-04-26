with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'r') as f:
    content = f.read()

# Fix 1: Hero title — add text-shadow glow so it pops on dark bg, increase size
old_hero = '''    .hero-title {
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
    .hero-sub { text-align: center; color: #6b7280; font-size: 1rem; margin: 8px 0 24px; font-weight: 500; }'''

new_hero = '''    .hero-title {
        font-size: 3.8rem; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #ff8c00 0%, #f97316 30%, #fbbf24 60%, #ff8c00 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        line-height: 1.2; letter-spacing: -0.03em;
        padding: 12px 0 4px 0;
        filter: drop-shadow(0 0 40px rgba(249,115,22,0.6)) drop-shadow(0 0 80px rgba(251,146,60,0.3));
    }
    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .hero-sub {
        text-align: center; color: #c9d1d9;
        font-size: 1.05rem; margin: 10px 0 28px;
        font-weight: 500; letter-spacing: 0.01em;
        text-shadow: 0 1px 8px rgba(0,0,0,0.8);
    }'''

# Fix 2: block-container — more top padding so heading doesn't hug the top
old_block = '    .block-container { padding-top: 2rem !important; }'
new_block = '''    .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }

    /* Override weak Streamlit default text colors */
    p, span, div { color: #e6edf3; }
    .stMarkdown p { color: #e6edf3 !important; font-size: 0.95rem; line-height: 1.6; }
    label { color: #9ca3af !important; }

    /* Make radio buttons in sidebar look better */
    [data-testid="stSidebar"] .stRadio > div { gap: 4px; }
    [data-testid="stSidebar"] .stRadio label {
        padding: 9px 14px !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        transition: background 0.2s, color 0.2s !important;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(249,115,22,0.12) !important; color: #f97316 !important; }

    /* Caption text */
    .stCaption, caption { color: #6b7280 !important; font-size: 0.78rem !important; }

    /* Warning / info / success boxes */
    .stAlert { border-radius: 10px !important; border: 1px solid #1f2937 !important; }

    /* Expander */
    .streamlit-expanderHeader { color: #e6edf3 !important; font-weight: 600 !important; }'''

if old_hero in content and old_block in content:
    content = content.replace(old_hero, new_hero)
    content = content.replace(old_block, new_block)
    with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'w') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("hero found:", old_hero in content)
    print("block found:", old_block in content)
