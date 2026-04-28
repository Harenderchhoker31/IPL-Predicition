# 🏏 IPL Analytics Dashboard 2008–2025
 
> An interactive data analytics and live prediction dashboard built on **18 seasons of IPL data** — covering 1,169 matches and 278,205 ball-by-ball deliveries.
 
🌐 **Live App:** [ipl-predicition.streamlit.app](https://ipl-predicition-9rhavjxzzgdejmayzduxpd.streamlit.app/)  
📓 **Colab Notebook:** `IPL_Analytics_Colab_Notebook.ipynb`  
📄 **Analytics Report:** `IPL_Analytics_Report_2008_2025.pdf`
 
---
 
## ✨ Features
 
### 🏠 Home & Overview
- KPI cards with key tournament stats
- IPL champions timeline (2008–2025)
- Key findings and data highlights
### 🏟️ Team Analysis
- All-time win records across all franchises
- Season heatmap and year-by-year performance trends
- Head-to-head matchup stats between any two teams
### 🧑‍🤝‍🧑 Player Analysis
- Top batsmen by runs, average, and strike rate
- Top bowlers by wickets, economy rate, and bowling average
- Player of the Match award leaders
### 📊 Match Insights
- Toss decision analysis and its impact on results
- Top venues by matches hosted and win rates
- Phase-wise (powerplay, middle, death) runs and wickets
- Dismissal type breakdown
### 🔴 Live Predictor
- Fetches live IPL scores from **Cricbuzz** in real time
- Predicts win probability using current match state
- Combines live data with historical head-to-head win rates
---
 
## 🛠️ Tech Stack
 
| Library | Version | Purpose |
|---|---|---|
| Streamlit | ≥1.38.0 | Web app framework |
| pandas | ≥2.2.2 | Data manipulation |
| NumPy | ≥2.0.0 | Numerical computing |
| Matplotlib | ≥3.9.0 | Data visualisation |
| Seaborn | ≥0.13.2 | Statistical charts |
| Cricbuzz API | — | Live match scores |
 
---
 
## 📁 Project Structure
 
```
IPL-Predicition/
├── data/                              # IPL match & ball-by-ball datasets
├── .devcontainer/                     # Dev container config
├── app.py                             # Main Streamlit application
├── patch_hero.py                      # Data patching / utility script
├── requirements.txt                   # Python dependencies
├── IPL_Analytics_Colab_Notebook.ipynb # EDA and model notebook
└── IPL_Analytics_Report_2008_2025.pdf # Full analytics report
```
 
---
 
## 🚀 Run Locally
 
### Prerequisites
- Python 3.10+
- pip
### Steps
 
```bash
# 1. Clone the repository
git clone https://github.com/Harenderchhoker31/IPL-Predicition.git
cd IPL-Predicition
 
# 2. Install dependencies
pip install -r requirements.txt
 
# 3. Launch the app
streamlit run app.py
```
 
The app will open at `http://localhost:8501`
 
---
 
## 📊 Data
 
The `data/` directory contains:
- **Match-level data** — results, venues, toss outcomes, winners (2008–2025)
- **Ball-by-ball data** — 278,205 deliveries with runs, wickets, and dismissal details
Data covers all **18 IPL seasons** and **1,169 matches**.
 
---
 
## 🚢 Deployment
 
This app is deployed on **Streamlit Community Cloud**.
 
To deploy your own instance:
1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo.
3. Set `app.py` as the entry point.
4. Click **Deploy**.
---
 
## 🤝 Contributing
 
Contributions are welcome!
 
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request
---
 
## 👤 Author
 
**Harenderchhoker31**
 
- GitHub: [@Harenderchhoker31](https://github.com/Harenderchhoker31)
---

