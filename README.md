# 📊 Crypto Market Analysis Pipeline (Assignment 4)

## 📌 Project Overview

This project extends Assignment 3 by enhancing the data pipeline and building an
interactive Streamlit dashboard for statistical analysis.

The pipeline follows a **medallion architecture**:

| Layer | Description |
|-------|-------------|
| 🥉 Bronze | Raw API data |
| 🥈 Silver | Cleaned datasets |
| 🥇 Gold | Final dataset for analysis |

In Assignment 4, an additional data source (**holidays**) is introduced to improve analysis.

---

## 🔄 Pipeline Overview
Public APIs → Bronze → Silver → Gold → Streamlit App → Statistical Analysis

text

- **Extract** → Binance & Fear & Greed APIs
- **Transform** → Cleaning and feature engineering
- **Load** → Final dataset for analysis

---

## 📡 Data Sources

- **Binance API** — Bitcoin price and volume data
- **Fear & Greed Index API** — Market sentiment indicator
- **Holidays** *(NEW)* — Generated using the `python-holidays` library; used to analyze behavior on holidays vs. non-holidays

---

## ⚙️ Feature Engineering

New variables added:

| Variable | Description |
|-------------------|-------------------------------|
| `btc_daily_return` | Daily return |
| `positive_return` | Binary outcome |
| `is_holiday` | Holiday indicator *(new)* |
| `high_volatility` | High movement days |

---

## 📊 Statistical Analysis

The Streamlit app includes the following tests, each with a **hypothesis, assumptions, decision, and interpretation**:

- One-sample t-test
- Two-sample t-test
- Chi-square test
- Variance comparison
- Correlation analysis

---

## 🖥️ Streamlit Dashboard

To run the app:

```bash
streamlit run app/streamlit_app.py
```

The dashboard includes:

- Data preview
- Visualizations
- Statistical tests
- Insights and limitations

---

## 📁 Project Structure
📦 project-root
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
├── ingest/
├── transform/
├── app/
├── README.md
├── analysis_preview.md
├── assignment4_analysis_plan.md
└── assignment4_reflection.md

text

---

## 🤖 AI Usage

ChatGPT was used to:

- Assist with pipeline design
- Debug issues (timestamp conversion, Streamlit errors)
- Help implement statistical tests
- Improve dashboard UI and explanations

> All outputs were reviewed and verified for correctness.

---

## 🎯 Conclusion

This project demonstrates how raw data can be transformed into meaningful insights
through data engineering and statistical analysis. The addition of holidays provides
a new dimension for understanding market behavior.