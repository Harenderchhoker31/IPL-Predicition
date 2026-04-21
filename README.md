# 🏏 IPL Data Analytics Dashboard (2008–2025)

> **A full-stack data analytics + machine learning project built for placement/internship portfolios.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-orange?logo=scikit-learn)](https://scikit-learn.org)
[![pandas](https://img.shields.io/badge/pandas-2.2-green?logo=pandas)](https://pandas.pydata.org)

---

## 📌 Project Overview

An end-to-end data analytics pipeline on the **Indian Premier League (IPL)** dataset spanning **18 seasons (2008–2025)**. Covers:

- 🔍 **Exploratory Data Analysis** — cleaning, merging 6 relational CSV files
- 📊 **16 Custom Visualisations** — dark-theme charts, heatmaps, pie charts
- 🤖 **Machine Learning** — 3 models trained to predict match winners
- 🌐 **Streamlit Web App** —  interactive dashboard with live ML prediction
- 📄 **Professional PDF Report** — 15-page placement-ready report

---

## 📊 Dataset

| File | Rows | Description |
|------|------|-------------|
| all_ipl_matches_data.csv | 1,169 | Match-level data |
| all_ball_by_ball_data.csv | 278,205 | Ball-by-ball data |
| all_players-data-updated.csv | 772 | Player profiles |
| all_teams_data.csv | 16 | Team IDs & names |
| all_team_aliases.csv | 46 | Team name aliases |
| IPL_finals.csv | 18 | Finals match IDs |

**Source:** [Kaggle — IPL Seasons 2008–2025](https://www.kaggle.com/datasets/slidescope/ipl-seasons-2008-to-2025-dataset)

---

## 🔑 Key Findings

| Metric | Finding |
|--------|---------|
| 🏆 Most Wins | Mumbai Indians — 151 wins |
| 🏏 Top Batsman | Virat Kohli — 8,671 runs |
| 🎯 Top Bowler | YS Chahal — 229 wickets |
| ⭐ Most POTM | AB de Villiers — 25 awards |
| 🪙 Toss Impact | Only 51.6% win rate (near-random!) |
| 🤖 Best ML Model | Random Forest — 50.2% CV accuracy |

> **Note on ML:** 50% accuracy in a 14-team classification is strong — random baseline is ~7%.

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ipl-data-analytics-2008-2025.git
cd ipl-data-analytics-2008-2025

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add data files
mkdir data
# Copy all 6 CSV files into the data/ folder

# 4. Run the app
streamlit run app.py
```

---

## 🌐 Live Demo

👉 **[Click here to open the live dashboard](YOUR_STREAMLIT_LINK_HERE)**

---

## 📁 Project Structure

```
ipl-data-analytics-2008-2025/
├── app.py                        ← Streamlit web app
├── requirements.txt              ← Python dependencies
├── IPL_Analytics_Colab.ipynb     ← Full analysis notebook
├── IPL_Analytics_Report.pdf      ← Professional PDF report
├── data/
│   ├── all_ipl_matches_data.csv
│   ├── all_ball_by_ball_data.csv
│   ├── all_players-data-updated.csv
│   ├── all_teams_data.csv
│   ├── all_team_aliases.csv
│   └── IPL_finals.csv
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Use |
|------|-----|
| **Python 3.10+** | Core language |
| **pandas** | Data manipulation & EDA |
| **NumPy** | Numerical computation |
| **Matplotlib / Seaborn** | Visualisations |
| **Scikit-learn** | ML models (RF, GB, LR) |
| **Streamlit** | Interactive web dashboard |
| **ReportLab** | PDF generation |

---

## 📄 Resume Bullet Points

```
• Built end-to-end IPL analytics pipeline in Python on a 6-file relational dataset
  (1,169 matches, 278K+ deliveries, 18 seasons: 2008–2025)

• Performed EDA, data cleaning, and feature engineering using pandas — including
  ID-to-name mapping, missing value treatment, and season normalisation

• Generated 16 professional dark-theme visualisations using Matplotlib and Seaborn

• Trained 3 ML classification models (Random Forest, Gradient Boosting, Logistic
  Regression) with 5-fold cross-validation and feature importance analysis

• Deployed interactive analytics dashboard on Streamlit Cloud with live ML prediction
```

---

## 📸 Screenshots

> *(Add screenshots of your Streamlit app here after deploying)*

---

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

*⭐ Star this repo if it helped you!*
