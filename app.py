import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os
import requests

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', 'ea6106e1d3msh6468af0b37b719bp14ee34jsn6f5cbb9dc289')

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics Dashboard 2008–2025",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
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
ACC1 = '#f97316'; ACC2 = '#3b82f6'; ACC3 = '#22c55e'; ACC4 = '#a855f7'
TEXT = '#e6edf3'; MUTED= '#8b949e'

TEAM_COLORS = {
    'Mumbai Indians':'#004BA0','Chennai Super Kings':'#F4C430',
    'Kolkata Knight Riders':'#3A225D','Royal Challengers Bangalore':'#EC1C24',
    'Royal Challengers Bengaluru':'#EC1C24',
    'Sunrisers Hyderabad':'#FF822A','Punjab Kings':'#AA4545',
    'Kings XI Punjab':'#AA4545','Delhi Capitals':'#0078BC',
    'Delhi Daredevils':'#0078BC','Rajasthan Royals':'#2D68C4',
    'Gujarat Titans':'#1C4B9C','Lucknow Super Giants':'#00A86B',
    'Deccan Chargers':'#FDB913','Rising Pune Supergiant':'#6F1D78',
    'Gujarat Lions':'#E8461A','Kochi Tuskers Kerala':'#F26522',
    'Pune Warriors':'#1C4B9C','Rising Pune Supergiants':'#6F1D78',
}

def style_fig(fig, ax_list=None):
    fig.patch.set_facecolor(BG)
    axes = ax_list if ax_list else [fig.axes[i] for i in range(len(fig.axes))]
    for ax in axes:
        ax.set_facecolor(CARD)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT); ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for sp in ax.spines.values(): sp.set_color('#30363d')
        ax.grid(axis='y', color='#30363d', linewidth=0.5, alpha=0.5)
        ax.set_axisbelow(True)

# ── Data Loading ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    matches  = pd.read_csv(os.path.join(base, 'data', 'all_ipl_matches_data.csv'))
    deliv    = pd.read_csv(os.path.join(base, 'data', 'all_ball_by_ball_data.csv'))
    teams    = pd.read_csv(os.path.join(base, 'data', 'all_teams_data.csv'))
    players  = pd.read_csv(os.path.join(base, 'data', 'all_players-data-updated.csv'))
    finals   = pd.read_csv(os.path.join(base, 'data', 'IPL_finals.csv'))

    t_map = dict(zip(teams['team_id'], teams['team_name']))
    for col in ['team1','team2','toss_winner','match_winner']:
        matches[col] = matches[col].map(t_map)
    for col in ['team_batting','team_bowling']:
        deliv[col] = deliv[col].map(t_map)

    p_map = dict(zip(players['player_id'], players['player_name']))
    matches['pom_name'] = matches['player_of_match'].map(p_map)

    matches['season'] = matches['season'].astype(str).str.replace('/21','').astype(int)
    deliv['season_id'] = deliv['season_id'].astype(str).str.replace('/21','').astype(int)

    def phase(o):
        if o < 6:   return 'Powerplay (1-6)'
        elif o < 15: return 'Middle (7-15)'
        else:        return 'Death (16-20)'
    deliv['phase'] = deliv['over_number'].apply(phase)

    valid = matches[matches['result']=='win'].copy()
    return matches, deliv, teams, players, finals, valid, t_map, p_map

matches, deliv, teams, players, finals, valid, t_map, p_map = load_data()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏏 IPL Analytics")
    st.markdown("---")
    page = st.radio("📌 Navigate", [
        "🏠 Home & Overview",
        "📊 Team Analysis",
        "🏏 Player Analysis",
        "⚡ Match Insights",
        "🔍 Head-to-Head",
        "🔎 Details",
        "🔴 Live Predictor",
    ])
    st.markdown("---")

    # Season filter
    all_seasons = sorted(matches['season'].unique())
    season_range = st.select_slider(
        "📅 Season Range",
        options=all_seasons,
        value=(all_seasons[0], all_seasons[-1])
    )
    filtered = matches[(matches['season']>=season_range[0]) & (matches['season']<=season_range[1])]
    filtered_valid = filtered[filtered['result']=='win']
    filtered_deliv = deliv[(deliv['season_id']>=season_range[0]) & (deliv['season_id']<=season_range[1])]

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.75rem; color:#8b949e; text-align:center;'>
    📁 {len(filtered):,} matches<br>
    🎯 {len(filtered_deliv):,} deliveries<br>
    📅 {season_range[0]} – {season_range[1]}
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════
if page == "🏠 Home & Overview":
    st.markdown('<p class="hero-title">🏏 IPL Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Indian Premier League · 2008–2025 · 18 Seasons · Complete Ball-by-Ball Analysis</p>', unsafe_allow_html=True)

    tags = ['Python','pandas','Matplotlib','Seaborn','Streamlit','EDA']
    st.markdown(' '.join([f'<span class="tag">{t}</span>' for t in tags]), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # KPI Row
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        (c1, "1,169", "Total Matches", "#f97316"),
        (c2, "278K+", "Deliveries", "#3b82f6"),
        (c3, "14", "Teams", "#22c55e"),
        (c4, "18", "Seasons", "#a855f7"),
        (c5, "8,671", "Kohli's Runs", "#f97316"),
    ]
    for col, val, lbl, color in kpis:
        col.markdown(f"""
        <div class="metric-card">
            <p class="metric-value" style="color:{color}">{val}</p>
            <p class="metric-label">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">📌 Key Findings</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    insights_l = [
        ("🏆", "Mumbai Indians", "Most wins — 151 across 18 seasons"),
        ("🏏", "Virat Kohli", "Top run scorer — 8,671 runs"),
        ("🎯", "YS Chahal", "Top wicket taker — 229 wickets"),
    ]
    insights_r = [
        ("⭐", "AB de Villiers", "Most Player of Match — 25 awards"),
        ("🪙", "51.6%", "Toss win → match win rate (near-random!)"),
        ("⚡", "Death Overs", "Highest run rate phase — decides matches"),
    ]
    with col1:
        for emoji, bold, text in insights_l:
            st.markdown(f'<div class="insight-box">{emoji} <b>{bold}</b> — {text}</div>', unsafe_allow_html=True)
    with col2:
        for emoji, bold, text in insights_r:
            st.markdown(f'<div class="insight-box">{emoji} <b>{bold}</b> — {text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">🏆 IPL Champions Timeline</p>', unsafe_allow_html=True)

    finals_ids = finals['id'].tolist()
    champ_df = valid[valid['match_id'].isin(finals_ids)][['season','match_winner']].sort_values('season')
    champ_df.columns = ['Season','Champion']
    champ_df = champ_df.reset_index(drop=True)

    cols = st.columns(6)
    for i, row in champ_df.iterrows():
        col = cols[i % 6]
        color = TEAM_COLORS.get(row['Champion'], ACC1)
        col.markdown(f"""
        <div style="background:{CARD};border:1px solid #30363d;border-top:3px solid {color};
        border-radius:8px;padding:10px;text-align:center;margin:4px 0;">
            <div style="font-size:1.1rem;font-weight:800;color:{color}">{row['Season']}</div>
            <div style="font-size:0.68rem;color:{TEXT};margin-top:2px">{row['Champion'].replace(' ',chr(10))}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: TEAM ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "📊 Team Analysis":
    st.markdown('<p class="section-header">📊 Team Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Win Records", "🔥 Season Heatmap", "📈 Season Trends"])

    with tab1:
        col1, col2 = st.columns([2,1])
        with col1:
            wins = filtered_valid['match_winner'].value_counts().head(12)
            colors = [TEAM_COLORS.get(t, ACC1) for t in wins.index]
            fig, ax = plt.subplots(figsize=(9,6), facecolor=BG)
            bars = ax.barh(wins.index[::-1], wins.values[::-1], color=colors[::-1], height=0.65, edgecolor='none')
            for bar,val in zip(bars, wins.values[::-1]):
                ax.text(val+0.5, bar.get_y()+bar.get_height()/2, str(val), va='center', color=TEXT, fontsize=9, fontweight='bold')
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT)
            ax.set_title('Most Wins by Team', color=TEXT, fontsize=13, fontweight='bold')
            ax.set_xlabel('Total Wins', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.grid(axis='x', color='#30363d', linewidth=0.5, alpha=0.6)
            ax.set_xlim(0, wins.max()*1.15)
            fig.patch.set_facecolor(BG)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("#### 🥇 Win Table")
            win_tbl = filtered_valid['match_winner'].value_counts().reset_index()
            win_tbl.columns = ['Team','Wins']
            win_tbl['Win%'] = (win_tbl['Wins'] / len(filtered) * 100).round(1)
            st.dataframe(win_tbl, use_container_width=True, hide_index=True,
                column_config={"Wins": st.column_config.ProgressColumn("Wins", max_value=int(win_tbl['Wins'].max()), format="%d")})

    with tab2:
        top6 = valid['match_winner'].value_counts().head(6).index.tolist()
        all_t = pd.concat([filtered[['season','team1']].rename(columns={'team1':'team'}),
                           filtered[['season','team2']].rename(columns={'team2':'team'})])
        played = all_t.groupby(['season','team']).size().reset_index(name='played')
        won_df2 = filtered_valid.groupby(['season','match_winner']).size().reset_index(name='won')
        won_df2.columns = ['season','team','won']
        perf = played.merge(won_df2, on=['season','team'], how='left').fillna(0)
        perf['win_pct'] = (perf['won']/perf['played']*100).round(1)
        perf6 = perf[perf['team'].isin(top6)]
        pivot = perf6.pivot(index='team', columns='season', values='win_pct').fillna(0)

        fig, ax = plt.subplots(figsize=(14,5), facecolor=BG)
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax,
            linewidths=0.3, linecolor=BG, cbar_kws={'shrink':0.7}, annot_kws={'size':8,'color':'black'})
        ax.set_facecolor(CARD)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', color=TEXT, size=8)
        plt.setp(ax.get_yticklabels(), rotation=0, color=TEXT, size=9)
        ax.set_title('Win % Heatmap — Top 6 Teams by Season', color=TEXT, fontsize=13, fontweight='bold')
        ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('', color=MUTED)
        fig.patch.set_facecolor(BG)
        plt.tight_layout()
        st.pyplot(fig); plt.close()
        st.caption("💡 Empty cells = team didn't participate that season (bans, new teams)")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            sm = filtered.groupby('season').size()
            fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
            ax.fill_between(sm.index, sm.values, alpha=0.15, color=ACC2)
            ax.plot(sm.index, sm.values, color=ACC2, marker='o', linewidth=2.5, markersize=6)
            for x,y in zip(sm.index, sm.values): ax.text(x, y+0.5, str(y), ha='center', color=TEXT, fontsize=7)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            ax.set_title('Matches Per Season', color=TEXT, fontweight='bold')
            ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Matches', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.set_xticks(sm.index); ax.set_xticklabels(sm.index, rotation=45)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

        with col2:
            sr2 = filtered_deliv.groupby('season_id')['total_runs'].sum()
            fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
            ax.fill_between(sr2.index, sr2.values, alpha=0.15, color=ACC3)
            ax.plot(sr2.index, sr2.values, color=ACC3, marker='s', linewidth=2.5, markersize=6)
            for x,y in zip(sr2.index, sr2.values): ax.text(x, y+300, f'{y//1000}K', ha='center', color=TEXT, fontsize=7)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            ax.set_title('Total Runs Per Season', color=TEXT, fontweight='bold')
            ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Runs', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.set_xticks(sr2.index); ax.set_xticklabels(sr2.index, rotation=45)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════
# PAGE: PLAYER ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "🏏 Player Analysis":
    st.markdown('<p class="section-header">🏏 Player Analysis</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏏 Batsmen", "🎯 Bowlers", "⭐ Player of Match"])

    with tab1:
        n = st.slider("Top N batsmen", 5, 20, 10)
        top_bat = filtered_deliv.groupby('batter')['batter_runs'].sum().sort_values(ascending=False).head(n)
        col1, col2 = st.columns([2,1])
        with col1:
            fig, ax = plt.subplots(figsize=(9,5), facecolor=BG)
            gc = plt.cm.YlOrRd(np.linspace(0.35,0.9,n))
            bars = ax.bar(range(n), top_bat.values, color=gc, edgecolor='none', width=0.7)
            for bar,val in zip(bars, top_bat.values):
                ax.text(bar.get_x()+bar.get_width()/2, val+30, f'{val:,}', ha='center', color=TEXT, fontsize=7.5, fontweight='bold')
            ax.set_xticks(range(n)); ax.set_xticklabels(top_bat.index, rotation=30, ha='right', color=TEXT, fontsize=8.5)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT)
            ax.set_title(f'Top {n} Run Scorers', color=TEXT, fontsize=13, fontweight='bold')
            ax.set_ylabel('Total Runs', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()
        with col2:
            bat_tbl = top_bat.reset_index()
            bat_tbl.columns = ['Batsman','Runs']
            bat_tbl['Avg/Match'] = (bat_tbl['Runs'] / filtered_deliv.groupby('batter').size().reindex(bat_tbl['Batsman']).values).round(1)
            st.dataframe(bat_tbl, use_container_width=True, hide_index=True)

        # Strike rate
        sr_df = filtered_deliv.groupby('batter').agg(runs=('batter_runs','sum'), balls=('batter_runs','count'))
        sr_df = sr_df[sr_df['balls']>=200]
        sr_df['SR'] = (sr_df['runs']/sr_df['balls']*100).round(1)
        top_sr = sr_df.nlargest(10,'SR')
        st.markdown("#### ⚡ Highest Strike Rate (min 200 balls)")
        fig, ax = plt.subplots(figsize=(9,3.5), facecolor=BG)
        colors_sr = plt.cm.plasma(np.linspace(0.3,0.9,10))
        bars = ax.barh(top_sr.index[::-1], top_sr['SR'][::-1], color=colors_sr, edgecolor='none', height=0.6)
        for bar,val in zip(bars, top_sr['SR'][::-1]):
            ax.text(val+0.5, bar.get_y()+bar.get_height()/2, f'{val:.1f}', va='center', color=TEXT, fontsize=8, fontweight='bold')
        ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=9)
        ax.set_title('Top Strike Rates (min 200 balls)', color=TEXT, fontweight='bold')
        ax.set_xlabel('Strike Rate', color=MUTED)
        for sp in ax.spines.values(): sp.set_color('#30363d')
        ax.grid(axis='x', color='#30363d', linewidth=0.5, alpha=0.6)
        fig.patch.set_facecolor(BG); plt.tight_layout()
        st.pyplot(fig); plt.close()

    with tab2:
        n2 = st.slider("Top N bowlers", 5, 20, 10)
        wkts = filtered_deliv[filtered_deliv['is_wicket']==True].groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(n2)
        col1, col2 = st.columns([2,1])
        with col1:
            fig, ax = plt.subplots(figsize=(9,5), facecolor=BG)
            gc2 = plt.cm.PuBu(np.linspace(0.4,0.95,n2))
            bars = ax.bar(range(n2), wkts.values, color=gc2[::-1], edgecolor='none', width=0.7)
            for bar,val in zip(bars, wkts.values):
                ax.text(bar.get_x()+bar.get_width()/2, val+0.5, str(val), ha='center', color=TEXT, fontsize=7.5, fontweight='bold')
            ax.set_xticks(range(n2)); ax.set_xticklabels(wkts.index, rotation=30, ha='right', color=TEXT, fontsize=8.5)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT)
            ax.set_title(f'Top {n2} Wicket Takers', color=TEXT, fontsize=13, fontweight='bold')
            ax.set_ylabel('Wickets', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()
        with col2:
            wkt_tbl = wkts.reset_index(); wkt_tbl.columns = ['Bowler','Wickets']
            st.dataframe(wkt_tbl, use_container_width=True, hide_index=True)

        # Economy rate
        eco = filtered_deliv.groupby('bowler').agg(runs=('total_runs','sum'), balls=('total_runs','count'))
        eco = eco[eco['balls'] >= 120]
        eco['Economy'] = (eco['runs'] / (eco['balls']/6)).round(2)
        best_eco = eco.nsmallest(10,'Economy')
        st.markdown("#### 💰 Best Economy Rate (min 120 balls)")
        fig, ax = plt.subplots(figsize=(9,3.5), facecolor=BG)
        colors_eco = plt.cm.Greens(np.linspace(0.4,0.9,10))
        bars = ax.barh(best_eco.index[::-1], best_eco['Economy'][::-1], color=colors_eco, edgecolor='none', height=0.6)
        for bar,val in zip(bars, best_eco['Economy'][::-1]):
            ax.text(val+0.02, bar.get_y()+bar.get_height()/2, f'{val:.2f}', va='center', color=TEXT, fontsize=8, fontweight='bold')
        ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=9)
        ax.set_title('Best Economy Rates', color=TEXT, fontweight='bold')
        ax.set_xlabel('Economy (runs/over)', color=MUTED)
        for sp in ax.spines.values(): sp.set_color('#30363d')
        ax.grid(axis='x', color='#30363d', linewidth=0.5, alpha=0.6)
        fig.patch.set_facecolor(BG); plt.tight_layout()
        st.pyplot(fig); plt.close()

    with tab3:
        pom = filtered['pom_name'].value_counts().head(15)
        fig, ax = plt.subplots(figsize=(9,5.5), facecolor=BG)
        pc = plt.cm.plasma(np.linspace(0.3,0.9,len(pom)))
        bars = ax.bar(range(len(pom)), pom.values, color=pc, edgecolor='none', width=0.7)
        for bar,val in zip(bars, pom.values):
            ax.text(bar.get_x()+bar.get_width()/2, val+0.1, str(val), ha='center', color=TEXT, fontweight='bold', fontsize=8)
        ax.set_xticks(range(len(pom))); ax.set_xticklabels(pom.index, rotation=30, ha='right', color=TEXT, fontsize=8.5)
        ax.set_facecolor(CARD); ax.tick_params(colors=TEXT)
        ax.set_title('Most Player of the Match Awards', color=TEXT, fontsize=13, fontweight='bold')
        ax.set_ylabel('Awards', color=MUTED)
        for sp in ax.spines.values(): sp.set_color('#30363d')
        fig.patch.set_facecolor(BG); plt.tight_layout()
        st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════
# PAGE: MATCH INSIGHTS
# ═══════════════════════════════════════════════════════════════
elif page == "⚡ Match Insights":
    st.markdown('<p class="section-header">⚡ Match Insights</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🪙 Toss Analysis", "📍 Venues", "🏟️ Phase Analysis"])

    with tab1:
        v2 = filtered_valid.copy()
        v2['toss_match_win'] = v2['toss_winner'] == v2['match_winner']
        pct = v2['toss_match_win'].mean()*100

        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{ACC1}">{pct:.1f}%</p><p class="metric-label">Toss Win → Match Win</p></div>', unsafe_allow_html=True)
        field_pct = (filtered['toss_decision']=='field').mean()*100
        col2.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{ACC2}">{field_pct:.1f}%</p><p class="metric-label">Choose to Field First</p></div>', unsafe_allow_html=True)
        bat_pct = 100 - field_pct
        col3.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{ACC3}">{bat_pct:.1f}%</p><p class="metric-label">Choose to Bat First</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(5,5), facecolor=BG)
            sizes = [pct, 100-pct]
            wedges, texts, at = ax.pie(sizes, labels=['Won Match','Lost Match'], colors=[ACC1,CARD],
                autopct='%1.1f%%', startangle=90, textprops={'color':TEXT},
                wedgeprops={'edgecolor':BG,'linewidth':2})
            for a in at: a.set_color(BG); a.set_fontweight('bold')
            ax.set_facecolor(BG); ax.set_title('Toss Win → Match Win?', color=TEXT, fontsize=12, fontweight='bold')
            fig.patch.set_facecolor(BG); st.pyplot(fig); plt.close()

        with col2:
            toss_team = filtered_valid.groupby('toss_winner').apply(
                lambda x: (x.name==x['match_winner']).mean()*100).sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(6,5), facecolor=BG)
            colors_t = [TEAM_COLORS.get(t, ACC2) for t in toss_team.index]
            bars = ax.barh(toss_team.index[::-1], toss_team.values[::-1], color=colors_t[::-1], height=0.6, edgecolor='none')
            for bar,val in zip(bars, toss_team.values[::-1]):
                ax.text(val+0.5, bar.get_y()+bar.get_height()/2, f'{val:.1f}%', va='center', color=TEXT, fontsize=8)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            ax.set_title('Toss Win Rate by Team', color=TEXT, fontweight='bold')
            ax.set_xlabel('Win Rate %', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.grid(axis='x', color='#30363d', linewidth=0.5, alpha=0.6)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

    with tab2:
        tv = filtered['venue'].value_counts().head(12)
        short = [v[:25] for v in tv.index]
        col1, col2 = st.columns([2,1])
        with col1:
            fig, ax = plt.subplots(figsize=(9,6), facecolor=BG)
            bars = ax.barh(short[::-1], tv.values[::-1], color=ACC4, edgecolor='none', height=0.65)
            for bar,val in zip(bars, tv.values[::-1]):
                ax.text(val+0.3, bar.get_y()+bar.get_height()/2, str(val), va='center', color=TEXT, fontsize=9, fontweight='bold')
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8.5)
            ax.set_title('Top Venues by Matches Hosted', color=TEXT, fontsize=12, fontweight='bold')
            ax.set_xlabel('Matches', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.grid(axis='x', color='#30363d', linewidth=0.5, alpha=0.6)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()
        with col2:
            venue_tbl = tv.reset_index(); venue_tbl.columns = ['Venue','Matches']
            venue_tbl['Venue'] = venue_tbl['Venue'].str[:30]
            st.dataframe(venue_tbl, use_container_width=True, hide_index=True)

    with tab3:
        ph_order = ['Powerplay (1-6)','Middle (7-15)','Death (16-20)']
        ph_runs = filtered_deliv.groupby('phase')['total_runs'].mean().reindex(ph_order)
        ph_wkts = filtered_deliv[filtered_deliv['is_wicket']==True].groupby('phase')['is_wicket'].count().reindex(ph_order)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6,4), facecolor=BG)
            bars = ax.bar(ph_runs.index, ph_runs.values, color=[ACC3,ACC2,ACC1], edgecolor='none', width=0.5)
            for bar,val in zip(bars, ph_runs.values):
                ax.text(bar.get_x()+bar.get_width()/2, val+0.005, f'{val:.3f}', ha='center', color=TEXT, fontweight='bold')
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=9)
            ax.set_title('Avg Runs per Ball by Phase', color=TEXT, fontweight='bold')
            ax.set_ylabel('Avg Runs', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()
        with col2:
            fig, ax = plt.subplots(figsize=(6,4), facecolor=BG)
            bars = ax.bar(ph_wkts.index, ph_wkts.values, color=[ACC3,ACC2,ACC1], edgecolor='none', width=0.5)
            for bar,val in zip(bars, ph_wkts.values):
                ax.text(bar.get_x()+bar.get_width()/2, val+2, f'{int(val):,}', ha='center', color=TEXT, fontweight='bold')
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=9)
            ax.set_title('Total Wickets by Phase', color=TEXT, fontweight='bold')
            ax.set_ylabel('Wickets', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

        st.markdown("#### 🏏 Dismissal Types Distribution")
        dismissals = filtered_deliv[filtered_deliv['is_wicket']==True]['wicket_kind'].value_counts()
        fig, ax = plt.subplots(figsize=(9,4), facecolor=BG)
        gc_d = plt.cm.Set2(np.linspace(0,1,len(dismissals)))
        bars = ax.bar(dismissals.index, dismissals.values, color=gc_d, edgecolor='none', width=0.65)
        for bar,val in zip(bars, dismissals.values):
            ax.text(bar.get_x()+bar.get_width()/2, val+5, str(val), ha='center', color=TEXT, fontsize=8, fontweight='bold')
        ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=9)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_title('Dismissal Types', color=TEXT, fontweight='bold')
        ax.set_ylabel('Count', color=MUTED)
        for sp in ax.spines.values(): sp.set_color('#30363d')
        fig.patch.set_facecolor(BG); plt.tight_layout()
        st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════
# PAGE: HEAD TO HEAD
# ═══════════════════════════════════════════════════════════════
elif page == "🔍 Head-to-Head":
    st.markdown('<p class="section-header">🔍 Head-to-Head Analysis</p>', unsafe_allow_html=True)

    all_team_names = sorted(valid['match_winner'].dropna().unique().tolist())
    col1, col2 = st.columns(2)
    with col1:
        t1 = st.selectbox("Team 1", all_team_names, index=0)
    with col2:
        t2_opts = [t for t in all_team_names if t != t1]
        t2 = st.selectbox("Team 2", t2_opts, index=0)

    h2h = filtered[((filtered['team1']==t1)&(filtered['team2']==t2)) |
                   ((filtered['team1']==t2)&(filtered['team2']==t1))]
    h2h_valid = h2h[h2h['result']=='win']

    if len(h2h) == 0:
        st.warning("No matches found between these teams in the selected season range.")
    else:
        t1_wins = len(h2h_valid[h2h_valid['match_winner']==t1])
        t2_wins = len(h2h_valid[h2h_valid['match_winner']==t2])
        total   = len(h2h)

        c1, c2, c3 = st.columns(3)
        c1_col = TEAM_COLORS.get(t1, ACC2)
        c2_col = TEAM_COLORS.get(t2, ACC1)
        c1.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{c1_col}">{t1_wins}</p><p class="metric-label">{t1[:20]} Wins</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><p class="metric-value" style="color:#8b949e">{total}</p><p class="metric-label">Total Matches</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{c2_col}">{t2_wins}</p><p class="metric-label">{t2[:20]} Wins</p></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(5,5), facecolor=BG)
            if t1_wins + t2_wins > 0:
                sizes = [t1_wins, t2_wins]
                labels = [f'{t1[:15]}\n{t1_wins} wins', f'{t2[:15]}\n{t2_wins} wins']
                wcolors = [TEAM_COLORS.get(t1, ACC2), TEAM_COLORS.get(t2, ACC1)]
                wedges, texts, at = ax.pie(sizes, labels=labels, colors=wcolors,
                    autopct='%1.1f%%', startangle=90, textprops={'color':TEXT, 'fontsize':9},
                    wedgeprops={'edgecolor':BG,'linewidth':2})
                for a in at: a.set_color(BG); a.set_fontweight('bold')
            ax.set_facecolor(BG); ax.set_title('Head-to-Head Win Share', color=TEXT, fontsize=12, fontweight='bold')
            fig.patch.set_facecolor(BG); st.pyplot(fig); plt.close()

        with col2:
            st.markdown("#### 📋 Match History")
            hist = h2h_valid[['season','match_winner','win_by_runs','win_by_wickets']].copy()
            hist.columns = ['Season','Winner','By Runs','By Wickets']
            hist = hist.sort_values('Season', ascending=False)
            st.dataframe(hist, use_container_width=True, hide_index=True)

        # Season-wise wins
        if len(h2h_valid) > 0:
            st.markdown("#### 📅 Season-wise Results")
            sw = h2h_valid.groupby(['season','match_winner']).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(10,3.5), facecolor=BG)
            x = np.arange(len(sw.index))
            w = 0.35
            for i,(team,color) in enumerate([(t1,TEAM_COLORS.get(t1,ACC2)),(t2,TEAM_COLORS.get(t2,ACC1))]):
                if team in sw.columns:
                    ax.bar(x + i*w - w/2, sw[team], width=w, color=color, label=team[:20], edgecolor='none', alpha=0.85)
            ax.set_xticks(x); ax.set_xticklabels(sw.index, rotation=45, color=TEXT, fontsize=8)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT)
            ax.set_title('Wins Per Season', color=TEXT, fontweight='bold')
            ax.set_ylabel('Wins', color=MUTED)
            ax.legend(facecolor=CARD, labelcolor=TEXT, edgecolor='#30363d', fontsize=8)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════
# PAGE: DETAILS  (Player Details + Team Details)
# ═══════════════════════════════════════════════════════════════
elif page == "🔎 Details":
    st.markdown('<p class="section-header">🔎 Details</p>', unsafe_allow_html=True)

    sub = st.tabs(["👤 Player Details", "🏟️ Team Details"])

    # ─────────────────────────────────────────────
    # SUB-TAB 1 : PLAYER DETAILS
    # ─────────────────────────────────────────────
    with sub[0]:
        all_batters  = sorted(deliv['batter'].dropna().unique().tolist())
        sel_player   = st.selectbox("Select Player", all_batters, key='pd_player')

        p_bat  = deliv[deliv['batter']  == sel_player]
        p_bowl = deliv[deliv['bowler']  == sel_player]
        p_field= deliv[(deliv['is_wicket']) & (deliv['fielder'] == sel_player)] if 'fielder' in deliv.columns else pd.DataFrame()

        # ── Batting stats
        total_runs   = int(p_bat['batter_runs'].sum())
        total_balls  = len(p_bat)
        fours        = int((p_bat['batter_runs'] == 4).sum())
        sixes        = int((p_bat['batter_runs'] == 6).sum())
        strike_rate  = round(total_runs / total_balls * 100, 1) if total_balls > 0 else 0
        innings_bat  = p_bat['match_id'].nunique()
        avg_runs     = round(total_runs / innings_bat, 1) if innings_bat > 0 else 0
        highest      = int(p_bat.groupby('match_id')['batter_runs'].sum().max()) if innings_bat > 0 else 0
        fifties      = int((p_bat.groupby('match_id')['batter_runs'].sum() >= 50).sum())
        hundreds     = int((p_bat.groupby('match_id')['batter_runs'].sum() >= 100).sum())

        # ── Bowling stats
        total_wkts   = int(p_bowl['is_wicket'].sum())
        bowl_balls   = len(p_bowl)
        bowl_runs    = int(p_bowl['total_runs'].sum())
        economy      = round(bowl_runs / (bowl_balls / 6), 2) if bowl_balls >= 6 else 0
        bowl_avg     = round(bowl_runs / total_wkts, 1) if total_wkts > 0 else 0

        # ── Teams played for
        teams_for = sorted(p_bat['team_batting'].dropna().unique().tolist())

        # ── POTM
        potm_count = int((matches['pom_name'] == sel_player).sum())

        # ── Seasons played
        seasons_played = sorted(p_bat['season_id'].dropna().unique().tolist())

        st.markdown(f"### 👤 {sel_player}")
        st.markdown(f"<div class='insight-box'>🏏 Teams: <b>{', '.join(teams_for) if teams_for else 'N/A'}</b> &nbsp;|&nbsp; 📅 Seasons: <b>{seasons_played[0] if seasons_played else 'N/A'} – {seasons_played[-1] if seasons_played else 'N/A'}</b> &nbsp;|&nbsp; ⭐ POTM Awards: <b>{potm_count}</b></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # KPI row — batting
        st.markdown("#### 🏏 Batting")
        bc1,bc2,bc3,bc4,bc5,bc6 = st.columns(6)
        for col, val, lbl, color in [
            (bc1, f"{total_runs:,}",  "Total Runs",    ACC1),
            (bc2, f"{innings_bat}",   "Innings",       ACC2),
            (bc3, f"{avg_runs}",      "Batting Avg",   ACC3),
            (bc4, f"{strike_rate}",   "Strike Rate",   ACC4),
            (bc5, f"{fifties}/{hundreds}", "50s/100s", ACC1),
            (bc6, f"{highest}",       "Highest Score", ACC2),
        ]:
            col.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{color}">{val}</p><p class="metric-label">{lbl}</p></div>', unsafe_allow_html=True)

        bc7, bc8 = st.columns(2)
        bc7.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{ACC3}">{fours}</p><p class="metric-label">Fours</p></div>', unsafe_allow_html=True)
        bc8.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{ACC1}">{sixes}</p><p class="metric-label">Sixes</p></div>', unsafe_allow_html=True)

        # KPI row — bowling
        st.markdown("#### 🎯 Bowling")
        wc1,wc2,wc3,wc4 = st.columns(4)
        for col, val, lbl, color in [
            (wc1, f"{total_wkts}",  "Total Wickets", ACC2),
            (wc2, f"{economy}",     "Economy Rate",  ACC3),
            (wc3, f"{bowl_avg}",    "Bowling Avg",   ACC4),
            (wc4, f"{bowl_balls}",  "Balls Bowled",  ACC1),
        ]:
            col.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{color}">{val}</p><p class="metric-label">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Runs per season chart
        col1, col2 = st.columns(2)
        with col1:
            rps = p_bat.groupby('season_id')['batter_runs'].sum().reset_index()
            rps.columns = ['Season','Runs']
            if not rps.empty:
                fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
                ax.fill_between(rps['Season'], rps['Runs'], alpha=0.15, color=ACC1)
                ax.plot(rps['Season'], rps['Runs'], color=ACC1, marker='o', linewidth=2.5, markersize=6)
                for x,y in zip(rps['Season'], rps['Runs']): ax.text(x, y+10, str(y), ha='center', color=TEXT, fontsize=7)
                ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
                ax.set_title(f'{sel_player} — Runs per Season', color=TEXT, fontweight='bold')
                ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Runs', color=MUTED)
                for sp in ax.spines.values(): sp.set_color('#30363d')
                ax.set_xticks(rps['Season']); ax.set_xticklabels(rps['Season'], rotation=45)
                fig.patch.set_facecolor(BG); plt.tight_layout()
                st.pyplot(fig); plt.close()

        with col2:
            wps = p_bowl[p_bowl['is_wicket']].groupby('season_id')['is_wicket'].count().reset_index()
            wps.columns = ['Season','Wickets']
            if not wps.empty:
                fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
                ax.fill_between(wps['Season'], wps['Wickets'], alpha=0.15, color=ACC2)
                ax.plot(wps['Season'], wps['Wickets'], color=ACC2, marker='s', linewidth=2.5, markersize=6)
                for x,y in zip(wps['Season'], wps['Wickets']): ax.text(x, y+0.2, str(y), ha='center', color=TEXT, fontsize=7)
                ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
                ax.set_title(f'{sel_player} — Wickets per Season', color=TEXT, fontweight='bold')
                ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Wickets', color=MUTED)
                for sp in ax.spines.values(): sp.set_color('#30363d')
                ax.set_xticks(wps['Season']); ax.set_xticklabels(wps['Season'], rotation=45)
                fig.patch.set_facecolor(BG); plt.tight_layout()
                st.pyplot(fig); plt.close()

        # Runs per team
        st.markdown("#### 🏏 Runs Scored Against Each Team")
        rpt = p_bat.groupby('team_bowling')['batter_runs'].sum().sort_values(ascending=False)
        if not rpt.empty:
            fig, ax = plt.subplots(figsize=(10,3.5), facecolor=BG)
            colors_rpt = [TEAM_COLORS.get(t, ACC1) for t in rpt.index]
            bars = ax.bar(rpt.index, rpt.values, color=colors_rpt, edgecolor='none', width=0.65)
            for bar,val in zip(bars, rpt.values):
                ax.text(bar.get_x()+bar.get_width()/2, val+5, str(val), ha='center', color=TEXT, fontsize=7.5, fontweight='bold')
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
            ax.set_title('Runs vs Each Team', color=TEXT, fontweight='bold')
            ax.set_ylabel('Runs', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

    # ─────────────────────────────────────────────
    # SUB-TAB 2 : TEAM DETAILS
    # ─────────────────────────────────────────────
    with sub[1]:
        all_team_names = sorted(valid['match_winner'].dropna().unique().tolist())
        sel_team = st.selectbox("Select Team", all_team_names, key='td_team')
        t_color  = TEAM_COLORS.get(sel_team, ACC1)

        t_matches = matches[(matches['team1']==sel_team) | (matches['team2']==sel_team)]
        t_valid   = t_matches[t_matches['result']=='win']
        t_wins    = t_valid[t_valid['match_winner']==sel_team]
        t_losses  = t_valid[t_valid['match_winner']!=sel_team]
        t_no_res  = t_matches[t_matches['result']!='win']

        total_matches  = len(t_matches)
        total_wins     = len(t_wins)
        total_losses   = len(t_losses)
        no_result      = len(t_no_res)
        win_pct        = round(total_wins / total_matches * 100, 1) if total_matches > 0 else 0

        # IPL titles
        finals_ids  = finals['id'].tolist()
        title_years = valid[(valid['match_id'].isin(finals_ids)) & (valid['match_winner']==sel_team)]['season'].tolist()

        # Runs scored & conceded
        t_deliv_bat  = deliv[deliv['team_batting']==sel_team]
        t_deliv_bowl = deliv[deliv['team_bowling']==sel_team]
        runs_scored   = int(t_deliv_bat['total_runs'].sum())
        runs_conceded = int(t_deliv_bowl['total_runs'].sum())
        wickets_taken = int(t_deliv_bowl['is_wicket'].sum())
        wickets_lost  = int(t_deliv_bat['is_wicket'].sum())

        # Seasons participated
        seasons_in = sorted(t_matches['season'].unique().tolist())

        # Toss stats
        toss_won  = len(t_matches[t_matches['toss_winner']==sel_team])
        toss_pct  = round(toss_won / total_matches * 100, 1) if total_matches > 0 else 0

        # Top scorer for team
        top_scorer_s = t_deliv_bat.groupby('batter')['batter_runs'].sum().idxmax() if len(t_deliv_bat) > 0 else 'N/A'
        top_scorer_r = int(t_deliv_bat.groupby('batter')['batter_runs'].sum().max()) if len(t_deliv_bat) > 0 else 0
        top_wicket_s = t_deliv_bowl[t_deliv_bowl['is_wicket']].groupby('bowler')['is_wicket'].count().idxmax() if int(t_deliv_bowl['is_wicket'].sum()) > 0 else 'N/A'
        top_wicket_w = int(t_deliv_bowl[t_deliv_bowl['is_wicket']].groupby('bowler')['is_wicket'].count().max()) if int(t_deliv_bowl['is_wicket'].sum()) > 0 else 0

        st.markdown(f"### <span style='color:{t_color}'>{sel_team}</span>", unsafe_allow_html=True)
        title_str = ', '.join(map(str, title_years)) if title_years else 'None'
        st.markdown(f"<div class='insight-box'>🏆 IPL Titles: <b>{len(title_years)}</b> &nbsp;|&nbsp; 🗓️ Won in: <b>{title_str}</b> &nbsp;|&nbsp; 📅 Seasons: <b>{seasons_in[0]} – {seasons_in[-1]}</b></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # KPI row 1
        st.markdown("#### 📊 Match Record")
        mc1,mc2,mc3,mc4,mc5 = st.columns(5)
        for col, val, lbl, color in [
            (mc1, total_matches,        "Matches Played",  t_color),
            (mc2, total_wins,           "Wins",            ACC3),
            (mc3, total_losses,         "Losses",          '#ef4444'),
            (mc4, no_result,            "No Result/Ties",  MUTED),
            (mc5, f"{win_pct}%",        "Win %",           ACC1),
        ]:
            col.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{color}">{val}</p><p class="metric-label">{lbl}</p></div>', unsafe_allow_html=True)

        # KPI row 2
        st.markdown("#### 🏏 Batting & Bowling")
        rc1,rc2,rc3,rc4,rc5,rc6 = st.columns(6)
        for col, val, lbl, color in [
            (rc1, f"{runs_scored:,}",   "Runs Scored",    ACC1),
            (rc2, f"{runs_conceded:,}", "Runs Conceded",  '#ef4444'),
            (rc3, f"{wickets_taken}",   "Wickets Taken",  ACC2),
            (rc4, f"{wickets_lost}",    "Wickets Lost",   ACC4),
            (rc5, f"{toss_won}",        "Toss Wins",      ACC3),
            (rc6, f"{toss_pct}%",       "Toss Win %",     ACC1),
        ]:
            col.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{color}">{val}</p><p class="metric-label">{lbl}</p></div>', unsafe_allow_html=True)

        # Top performers
        st.markdown("<br>", unsafe_allow_html=True)
        tp1, tp2 = st.columns(2)
        tp1.markdown(f'<div class="insight-box">🏏 <b>Top Scorer:</b> {top_scorer_s} — {top_scorer_r:,} runs</div>', unsafe_allow_html=True)
        tp2.markdown(f'<div class="insight-box">🎯 <b>Top Wicket-Taker:</b> {top_wicket_s} — {top_wicket_w} wickets</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Wins per season chart
        col1, col2 = st.columns(2)
        with col1:
            wps_t = t_wins.groupby('season').size().reset_index(name='Wins')
            fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
            ax.fill_between(wps_t['season'], wps_t['Wins'], alpha=0.15, color=t_color)
            ax.plot(wps_t['season'], wps_t['Wins'], color=t_color, marker='o', linewidth=2.5, markersize=6)
            for x,y in zip(wps_t['season'], wps_t['Wins']): ax.text(x, y+0.1, str(y), ha='center', color=TEXT, fontsize=7)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            ax.set_title(f'{sel_team} — Wins per Season', color=TEXT, fontweight='bold')
            ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Wins', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.set_xticks(wps_t['season']); ax.set_xticklabels(wps_t['season'], rotation=45)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

        with col2:
            rps_t = t_deliv_bat.groupby('season_id')['total_runs'].sum().reset_index()
            rps_t.columns = ['Season','Runs']
            fig, ax = plt.subplots(figsize=(7,3.5), facecolor=BG)
            ax.fill_between(rps_t['Season'], rps_t['Runs'], alpha=0.15, color=ACC3)
            ax.plot(rps_t['Season'], rps_t['Runs'], color=ACC3, marker='s', linewidth=2.5, markersize=6)
            for x,y in zip(rps_t['Season'], rps_t['Runs']): ax.text(x, y+50, f'{y//1000}K', ha='center', color=TEXT, fontsize=7)
            ax.set_facecolor(CARD); ax.tick_params(colors=TEXT, labelsize=8)
            ax.set_title(f'{sel_team} — Runs Scored per Season', color=TEXT, fontweight='bold')
            ax.set_xlabel('Season', color=MUTED); ax.set_ylabel('Runs', color=MUTED)
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.set_xticks(rps_t['Season']); ax.set_xticklabels(rps_t['Season'], rotation=45)
            fig.patch.set_facecolor(BG); plt.tight_layout()
            st.pyplot(fig); plt.close()

        # Season-by-season record table
        st.markdown("#### 📋 Season-by-Season Record")
        season_rec = []
        for s in seasons_in:
            sm = t_matches[t_matches['season']==s]
            sw = t_wins[t_wins['season']==s]
            sl = t_losses[t_losses['season']==s]
            sr = t_deliv_bat[t_deliv_bat['season_id']==s]['total_runs'].sum()
            title = '🏆' if s in title_years else ''
            season_rec.append({'Season': s, 'Played': len(sm), 'Won': len(sw), 'Lost': len(sl), 'Runs': int(sr), 'Title': title})
        rec_df = pd.DataFrame(season_rec)
        st.dataframe(rec_df, use_container_width=True, hide_index=True,
            column_config={
                'Won':  st.column_config.ProgressColumn('Won',  max_value=int(rec_df['Played'].max()), format='%d'),
                'Lost': st.column_config.ProgressColumn('Lost', max_value=int(rec_df['Played'].max()), format='%d'),
            })

# ── Footer ────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
# PAGE: LIVE PREDICTOR
# ═══════════════════════════════════════════════════════════════
elif page == "🔴 Live Predictor":
    st.markdown('<p class="section-header">🔴 Live Match Predictor</p>', unsafe_allow_html=True)
    st.markdown("Fetches **live IPL scores** from Cricbuzz and predicts the winner using current match state + historical IPL win rates.")
    st.markdown("<br>", unsafe_allow_html=True)

    api_key = RAPIDAPI_KEY

    # ── Helper functions
    def fetch_live_matches(key):
        url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
        headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()

    def parse_live_matches(data):
        matches_list = []
        for type_group in data.get('typeMatches', []):
            for series_group in type_group.get('seriesMatches', []):
                series_wrapper = series_group.get('seriesAdWrapper', {})
                series_name = series_wrapper.get('seriesName', '')
                if 'IPL' not in series_name and 'Indian Premier' not in series_name:
                    continue
                for m in series_wrapper.get('matches', []):
                    mi = m.get('matchInfo', {})
                    ms = m.get('matchScore', {})
                    t1     = mi.get('team1', {}).get('teamName', 'Team 1')
                    t2     = mi.get('team2', {}).get('teamName', 'Team 2')
                    status = mi.get('status', '')
                    state  = mi.get('state', '')
                    mid    = mi.get('matchId', '')
                    venue  = mi.get('venueInfo', {}).get('ground', 'Unknown')
                    city   = mi.get('venueInfo', {}).get('city', '')
                    desc   = mi.get('matchDesc', '')

                    def fmt_score(sc):
                        inn = sc.get('inngs1', {})
                        if not inn: return 'Yet to bat'
                        r = inn.get('runs', 0); w = inn.get('wickets', 0); ov = inn.get('overs', 0)
                        return f"{r}/{w} ({ov} ov)"

                    t1_score = ms.get('team1Score', {})
                    t2_score = ms.get('team2Score', {})

                    matches_list.append({
                        'match_id': mid, 'desc': desc,
                        'team1': t1, 'team2': t2,
                        'score1': fmt_score(t1_score),
                        'score2': fmt_score(t2_score),
                        'status': status, 'state': state,
                        'venue': venue, 'city': city,
                        'series': series_name,
                        't1_raw': t1_score, 't2_raw': t2_score,
                    })
        return matches_list

    def win_probability(team1, team2, t1_raw, t2_raw):
        # Historical win rates
        wr = {}
        for team in valid['match_winner'].dropna().unique():
            played = len(matches[(matches['team1']==team)|(matches['team2']==team)])
            won    = len(valid[valid['match_winner']==team])
            wr[team] = won / played if played > 0 else 0.5

        def best_match_wr(name):
            name_l = name.lower()
            for k in wr:
                if any(w in k.lower() for w in name_l.split() if len(w) > 3):
                    return wr[k]
            return 0.5

        t1_wr = best_match_wr(team1)
        t2_wr = best_match_wr(team2)
        base  = t1_wr / (t1_wr + t2_wr)  # historical base probability for t1

        inn1 = t1_raw.get('inngs1', {})
        inn2 = t2_raw.get('inngs1', {})

        r1 = inn1.get('runs', 0);  w1 = inn1.get('wickets', 0);  ov1 = float(inn1.get('overs', 0))
        r2 = inn2.get('runs', 0);  w2 = inn2.get('wickets', 0);  ov2 = float(inn2.get('overs', 0))

        is_2nd_innings = bool(inn2)

        if not is_2nd_innings:
            # 1st innings: project final score
            balls_done = int(ov1) * 6 + round((ov1 % 1) * 10)
            balls_left = max(0, 120 - balls_done)
            crr = r1 / (balls_done / 6) if balls_done > 0 else 8.0
            proj = r1 + crr * (balls_left / 6)
            wkts_factor = (10 - w1) / 10
            score_factor = min(proj / 175, 1.2)
            t1_prob = 0.5 * base + 0.3 * score_factor * wkts_factor + 0.2 * base
            t1_prob = min(max(t1_prob, 0.08), 0.92)
        else:
            # 2nd innings chase
            target     = r1 + 1
            runs_need  = target - r2
            balls_done2= int(ov2) * 6 + round((ov2 % 1) * 10)
            balls_left2= max(1, 120 - balls_done2)
            wkts_left2 = 10 - w2
            rrr = runs_need / (balls_left2 / 6)
            crr2= r2 / (balls_done2 / 6) if balls_done2 > 0 else 0
            momentum   = min(max((crr2 - rrr + 2) / 6, 0), 1)  # 0=hard chase, 1=easy
            wkts_factor2 = wkts_left2 / 10
            t2_prob = 0.35 * (1 - base) + 0.40 * momentum + 0.25 * wkts_factor2
            t2_prob = min(max(t2_prob, 0.08), 0.92)
            t1_prob = 1 - t2_prob

        return round(t1_prob * 100, 1), round((1 - t1_prob) * 100, 1)

    def draw_prob_bar(t1, t2, p1, p2, c1, c2):
        fig, ax = plt.subplots(figsize=(10, 1.0), facecolor=BG)
        ax.barh([0], [p1], color=c1, height=0.55)
        ax.barh([0], [p2], left=[p1], color=c2, height=0.55)
        if p1 > 8:
            ax.text(p1/2, 0, f"{t1[:14]}  {p1}%", ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        if p2 > 8:
            ax.text(p1 + p2/2, 0, f"{p2}%  {t2[:14]}", ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        ax.set_xlim(0, 100); ax.axis('off')
        fig.patch.set_facecolor(BG); plt.tight_layout(pad=0)
        st.pyplot(fig); plt.close()

    # ─────────────────────────────────────────────
    live_tab, demo_tab = st.tabs(["🔴 Live Matches", "🧪 Demo / Simulate"])

    # ── LIVE TAB
    with live_tab:
        col_btn, col_auto = st.columns([2,1])
        with col_btn:
            fetch_btn = st.button("🔄 Fetch Live IPL Matches", use_container_width=True)
        with col_auto:
            auto_refresh = st.checkbox("⏱️ Auto-refresh every 60s")

        if auto_refresh:
            import time
            st.caption("Auto-refreshing... (stop by unchecking above)")

        if fetch_btn or auto_refresh:
            try:
                with st.spinner("Fetching from Cricbuzz..."):
                    raw        = fetch_live_matches(api_key)
                    live_list  = parse_live_matches(raw)

                if not live_list:
                    st.warning("⚠️ No live IPL matches right now. Check back during an IPL match window.")
                    st.info(f"📊 Total live matches across all cricket: {sum(len(sg.get('seriesAdWrapper',{}).get('matches',[])) for tg in raw.get('typeMatches',[]) for sg in tg.get('seriesMatches',[]))}")
                else:
                    st.success(f"✅ {len(live_list)} live IPL match(es) found!")
                    for m in live_list:
                        c1 = TEAM_COLORS.get(m['team1'], ACC2)
                        c2 = TEAM_COLORS.get(m['team2'], ACC1)
                        p1, p2 = win_probability(m['team1'], m['team2'], m['t1_raw'], m['t2_raw'])
                        winner = m['team1'] if p1 >= p2 else m['team2']
                        wc     = c1 if p1 >= p2 else c2

                        # Match card
                        st.markdown(f"""
                        <div style="background:{CARD};border:1px solid #30363d;border-radius:14px;padding:20px;margin:12px 0;">
                            <div style="font-size:0.75rem;color:{MUTED};margin-bottom:10px;">
                                🏟️ {m['venue']}, {m['city']} &nbsp;·&nbsp; {m['desc']} &nbsp;·&nbsp; {m['series']}
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">
                                <div style="text-align:center;flex:1;">
                                    <div style="font-size:1.05rem;font-weight:800;color:{c1}">{m['team1']}</div>
                                    <div style="font-size:1.6rem;font-weight:900;color:{TEXT};margin-top:4px">{m['score1']}</div>
                                </div>
                                <div style="text-align:center;">
                                    <div style="font-size:1.3rem;color:{MUTED};font-weight:700">VS</div>
                                </div>
                                <div style="text-align:center;flex:1;">
                                    <div style="font-size:1.05rem;font-weight:800;color:{c2}">{m['team2']}</div>
                                    <div style="font-size:1.6rem;font-weight:900;color:{TEXT};margin-top:4px">{m['score2']}</div>
                                </div>
                            </div>
                            <div style="text-align:center;margin-top:10px;font-size:0.82rem;color:{ACC1};font-weight:600">{m['status']}</div>
                        </div>""", unsafe_allow_html=True)

                        # Win probability bar
                        draw_prob_bar(m['team1'], m['team2'], p1, p2, c1, c2)

                        # Probability cards
                        pc1, pc2 = st.columns(2)
                        pc1.markdown(f"""
                        <div style="background:linear-gradient(135deg,{c1}22,{c1}11);border:2px solid {c1};
                        border-radius:10px;padding:14px;text-align:center;">
                            <div style="font-size:0.85rem;color:{c1};font-weight:700">{m['team1']}</div>
                            <div style="font-size:2rem;font-weight:900;color:{c1}">{p1}%</div>
                            <div style="font-size:0.72rem;color:{MUTED}">Win Probability</div>
                        </div>""", unsafe_allow_html=True)
                        pc2.markdown(f"""
                        <div style="background:linear-gradient(135deg,{c2}22,{c2}11);border:2px solid {c2};
                        border-radius:10px;padding:14px;text-align:center;">
                            <div style="font-size:0.85rem;color:{c2};font-weight:700">{m['team2']}</div>
                            <div style="font-size:2rem;font-weight:900;color:{c2}">{p2}%</div>
                            <div style="font-size:0.72rem;color:{MUTED}">Win Probability</div>
                        </div>""", unsafe_allow_html=True)

                        st.markdown(f"<div class='insight-box' style='margin-top:10px;'>🏆 <b>Predicted Winner:</b> <span style='color:{wc}'>{winner}</span> &nbsp;—&nbsp; <b>{max(p1,p2)}%</b> probability</div>", unsafe_allow_html=True)
                        st.markdown("---")

                if auto_refresh:
                    import time; time.sleep(60); st.rerun()

            except requests.exceptions.HTTPError as e:
                if '403' in str(e) or '401' in str(e):
                    st.error("🔒 Invalid API key or not subscribed to Cricbuzz on RapidAPI.")
                elif '429' in str(e):
                    st.error("⏱️ Rate limit hit. Free tier = 100 req/day.")
                else:
                    st.error(f"API error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown(f"""
        <div class='insight-box'>
        💡 <b>How prediction works:</b> Live score (runs, wickets, overs) →
        current run rate vs required run rate → wickets in hand factor →
        blended with <b>historical IPL win rates</b> from 2008–2025 dataset.
        </div>""", unsafe_allow_html=True)

    # ── DEMO TAB
    with demo_tab:
        st.markdown("#### 🧪 Simulate Any Match State")
        all_team_names = sorted(valid['match_winner'].dropna().unique().tolist())
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            d_team1  = st.selectbox("🔵 Team 1 (Batting First)", all_team_names, key='demo_t1')
            d_runs1  = st.number_input("1st Innings Runs", 0, 300, 165, key='demo_r1')
            d_wkts1  = st.number_input("1st Innings Wickets", 0, 10, 6, key='demo_w1')
            d_overs1 = st.number_input("1st Innings Overs", 0.0, 20.0, 20.0, step=0.1, key='demo_o1')
        with demo_col2:
            d_team2  = st.selectbox("🔴 Team 2 (Chasing)", [t for t in all_team_names if t != d_team1], key='demo_t2')
            d_runs2  = st.number_input("2nd Innings Runs", 0, 300, 87, key='demo_r2')
            d_wkts2  = st.number_input("2nd Innings Wickets", 0, 10, 3, key='demo_w2')
            d_overs2 = st.number_input("2nd Innings Overs", 0.0, 20.0, 11.2, step=0.1, key='demo_o2')

        if st.button("🚀 Predict", use_container_width=True, key='demo_predict'):
            t1_raw_d = {'inngs1': {'runs': d_runs1, 'wickets': d_wkts1, 'overs': d_overs1}}
            t2_raw_d = {'inngs1': {'runs': d_runs2, 'wickets': d_wkts2, 'overs': d_overs2}} if d_runs2 > 0 or d_overs2 > 0 else {}
            p1d, p2d = win_probability(d_team1, d_team2, t1_raw_d, t2_raw_d)
            c1d = TEAM_COLORS.get(d_team1, ACC2)
            c2d = TEAM_COLORS.get(d_team2, ACC1)
            winner_d = d_team1 if p1d >= p2d else d_team2
            wcd = c1d if p1d >= p2d else c2d

            target_d = d_runs1 + 1
            runs_need_d = target_d - d_runs2
            balls_done_d = int(d_overs2)*6 + round((d_overs2 % 1)*10)
            balls_left_d = max(1, 120 - balls_done_d)
            rrr_d = round(runs_need_d / (balls_left_d / 6), 2)
            crr_d = round(d_runs2 / (balls_done_d / 6), 2) if balls_done_d > 0 else 0

            st.markdown("<br>", unsafe_allow_html=True)

            # Match state summary
            ms1, ms2, ms3, ms4 = st.columns(4)
            for col, val, lbl, color in [
                (ms1, target_d,       "Target",       ACC1),
                (ms2, runs_need_d,    "Runs Needed",  '#ef4444'),
                (ms3, f"{crr_d}",     "CRR",          ACC3),
                (ms4, f"{rrr_d}",     "RRR",          ACC2),
            ]:
                col.markdown(f'<div class="metric-card"><p class="metric-value" style="color:{color}">{val}</p><p class="metric-label">{lbl}</p></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            draw_prob_bar(d_team1, d_team2, p1d, p2d, c1d, c2d)

            rc1, rc2 = st.columns(2)
            rc1.markdown(f"""
            <div style="background:linear-gradient(135deg,{c1d}22,{c1d}11);border:2px solid {c1d};
            border-radius:10px;padding:16px;text-align:center;">
                <div style="font-size:0.9rem;color:{c1d};font-weight:700">{d_team1}</div>
                <div style="font-size:2.2rem;font-weight:900;color:{c1d}">{p1d}%</div>
                <div style="font-size:0.72rem;color:{MUTED}">Win Probability</div>
            </div>""", unsafe_allow_html=True)
            rc2.markdown(f"""
            <div style="background:linear-gradient(135deg,{c2d}22,{c2d}11);border:2px solid {c2d};
            border-radius:10px;padding:16px;text-align:center;">
                <div style="font-size:0.9rem;color:{c2d};font-weight:700">{d_team2}</div>
                <div style="font-size:2.2rem;font-weight:900;color:{c2d}">{p2d}%</div>
                <div style="font-size:0.72rem;color:{MUTED}">Win Probability</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"<div class='insight-box' style='margin-top:12px;'>🏆 <b>Predicted Winner:</b> <span style='color:{wcd}'>{winner_d}</span> &nbsp;—&nbsp; <b>{max(p1d,p2d)}%</b> probability</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#8b949e; font-size:0.78rem; padding:10px'>
    🏏 IPL Analytics Dashboard &nbsp;|&nbsp; Built with Python · pandas · Scikit-learn · Streamlit
    &nbsp;|&nbsp; Dataset: Kaggle IPL 2008–2025 &nbsp;|&nbsp; <b style='color:#f97316'>Placement Project</b>
</div>
""", unsafe_allow_html=True)
