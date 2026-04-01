# Data Pipeline for Statistical Analysis

## 📌 Project Overview

This project builds a data pipeline using a medallion architecture (Bronze → Silver → Gold). The pipeline collects cryptocurrency market data and sentiment data, cleans and transforms it, and produces a final dataset ready for statistical analysis.

This dataset will be used in Part 2 to perform hypothesis testing and build a Streamlit application.

---

## 🏗️ Architecture

Bronze → Silver → Gold

* **Bronze Layer**: Raw API data stored as JSON
* **Silver Layer**: Cleaned and structured data (CSV)
* **Gold Layer**: Final joined dataset with engineered features

---

## 📡 APIs Used

1. Binance API

   * Provides daily Bitcoin price and volume data

2. Alternative.me Fear & Greed Index

   * Provides daily market sentiment data

---

## ⚙️ How to Run the Project

### 1. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run ingestion scripts

```
python ingest/ingest_binance.py
python ingest/ingest_fear_greed.py
```

Run both scripts at least twice to generate multiple Bronze files.

---

### 4. Run transformation scripts

```
python transform/transform_binance.py
python transform/transform_fear_greed.py
```

---

### 5. Create Gold dataset

```
python transform/create_gold.py
```

---

## 📊 Final Dataset (Gold Layer)

The final dataset contains:

* date
* btc_close
* btc_volume
* fear_greed_value
* fear_greed_label
* btc_daily_return
* positive_return

---

## 📈 Feature Engineering

* **btc_daily_return**: Daily percentage return of Bitcoin
* **positive_return**: Binary variable (1 = positive return, 0 = negative)

These features are used for statistical tests such as:

* One-sample t-test
* Two-sample t-test
* Proportion z-test

---

## 🤖 AI Usage

I used ChatGPT to:

* Generate initial API request code
* Help structure the data pipeline
* Assist with debugging errors (timestamp conversion issue)

I verified:

* Data joins were correct
* Data types were properly converted
* Output dataset matched expected structure

---

## 📁 Project Structure

```
data-pipeline-assignment/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── ingest/
├── transform/
├── notebooks/
│
├── README.md
├── analysis_preview.md
├── requirements.txt
├── .env.example
├── .gitignore
```

---

## 🎯 Conclusion

This pipeline successfully transforms raw API data into an analysis-ready dataset, enabling statistical testing and visualization in the next stage of the project.
