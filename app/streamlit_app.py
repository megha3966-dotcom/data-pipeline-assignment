import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# ========================
# LOAD DATA
# ========================
df = pd.read_csv("data/gold/crypto_sentiment.csv")

# ========================
# TITLE
# ========================
st.title("📊 Crypto Market Analysis Dashboard")
st.markdown("Analyze Bitcoin returns using sentiment and holiday data")

# ========================
# METRICS
# ========================
col1, col2, col3 = st.columns(3)

col1.metric("Avg Return", f"{df['btc_daily_return'].mean():.4f}")
col2.metric("Avg Volume", f"{df['btc_volume'].mean():,.0f}")
col3.metric("Positive Days (%)", f"{df['positive_return'].mean()*100:.2f}%")

st.divider()

# ========================
# OVERVIEW
# ========================
st.header("📌 Project Overview")

st.write("""
This dashboard explores how Bitcoin returns relate to sentiment and holidays.

A new feature (**is_holiday**) was added using the holidays Python library,
allowing comparison between holiday and non-holiday trading behavior.

The goal is to move beyond visualization into statistical testing.
""")

# ========================
# DATA PREVIEW
# ========================
with st.expander("📂 View Dataset"):
    st.write(df.head())
    st.write(df.describe())

# ========================
# VISUALS
# ========================
st.header("📈 Visual Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("BTC Returns Over Time")
    st.line_chart(df["btc_daily_return"])

with col2:
    st.subheader("Volume vs Returns")
    fig, ax = plt.subplots()
    ax.scatter(df["btc_volume"], df["btc_daily_return"], alpha=0.5)
    ax.set_xlabel("Volume")
    ax.set_ylabel("Return")
    st.pyplot(fig)

# Boxplot
st.subheader("Holiday vs Non-Holiday Returns")

if "is_holiday" in df.columns:
    fig, ax = plt.subplots()
    df.boxplot(column="btc_daily_return", by="is_holiday", ax=ax)
    plt.title("Return Distribution by Holiday")
    plt.suptitle("")
    st.pyplot(fig)

st.divider()

# ========================
# STATISTICAL TESTS
# ========================
st.header("🧪 Statistical Analysis")

alpha = 0.05

holiday = df[df["is_holiday"] == 1]["btc_daily_return"]
non_holiday = df[df["is_holiday"] == 0]["btc_daily_return"]

# ------------------------
# 1. ONE SAMPLE T-TEST
# ------------------------
st.subheader("1️⃣ One-Sample T-Test")

st.markdown("""
**Hypothesis**
- H0: Mean BTC return = 0  
- H1: Mean BTC return ≠ 0  

**Assumptions**
- Normality  
- Independent observations  
""")

t_stat, p_val = stats.ttest_1samp(df["btc_daily_return"], 0)

col1, col2 = st.columns(2)
col1.metric("T-Statistic", f"{t_stat:.4f}")
col2.metric("P-Value", f"{p_val:.4f}")

if p_val < alpha:
    st.success("✅ Reject H0 → Mean return is different from 0")
else:
    st.warning("⚠️ Fail to Reject H0")

# ------------------------
# 2. TWO SAMPLE T-TEST
# ------------------------
st.subheader("2️⃣ Two-Sample T-Test (Holiday vs Non-Holiday)")

st.markdown("""
**Hypothesis**
- H0: Means are equal  
- H1: Means differ  

**Assumptions**
- Independent groups  
- Approximate normality  
""")

t_stat, p_val = stats.ttest_ind(holiday, non_holiday)

col1, col2 = st.columns(2)
col1.metric("T-Statistic", f"{t_stat:.4f}")
col2.metric("P-Value", f"{p_val:.4f}")

if p_val < alpha:
    st.success("✅ Reject H0 → Returns differ")
else:
    st.warning("⚠️ Fail to Reject H0")

# ------------------------
# 3. CHI-SQUARE TEST
# ------------------------
st.subheader("3️⃣ Chi-Square Test")

st.markdown("""
**Hypothesis**
- H0: Variables are independent  
- H1: Variables are related  

**Assumptions**
- Adequate expected frequency  
""")

contingency = pd.crosstab(df["positive_return"], df["is_holiday"])
chi2, p, _, _ = stats.chi2_contingency(contingency)

st.dataframe(contingency)

col1, col2 = st.columns(2)
col1.metric("Chi²", f"{chi2:.4f}")
col2.metric("P-Value", f"{p:.4f}")

if p < alpha:
    st.success("✅ Reject H0 → Relationship exists")
else:
    st.warning("⚠️ Fail to Reject H0")

# ------------------------
# 4. VARIANCE TEST
# ------------------------
st.subheader("4️⃣ Variance Comparison")

var1 = np.var(holiday, ddof=1)
var2 = np.var(non_holiday, ddof=1)

f_stat = var1 / var2

st.metric("F-Statistic", f"{f_stat:.4f}")

if f_stat > 1.5 or f_stat < 0.67:
    st.success("👉 Variability differs")
else:
    st.info("👉 Variability similar")

# ------------------------
# 5. CORRELATION
# ------------------------
st.subheader("5️⃣ Correlation Analysis")

st.markdown("""
**Hypothesis**
- H0: No correlation  
- H1: Correlation exists  
""")

corr, p_val = stats.pearsonr(df["btc_volume"], df["btc_daily_return"])

col1, col2 = st.columns(2)
col1.metric("Correlation", f"{corr:.4f}")
col2.metric("P-Value", f"{p_val:.4f}")

if p_val < alpha:
    st.success("✅ Reject H0 → Significant correlation")
else:
    st.warning("⚠️ Fail to Reject H0")

st.divider()

# ========================
# INTERPRETATION
# ========================
st.header("📌 Key Insights")

st.info("""
- Bitcoin returns fluctuate over time
- Holidays may influence trading patterns
- Some statistical relationships exist, but do not imply causation
""")

# ========================
# LIMITATIONS
# ========================
st.header("⚠️ Limitations")

st.warning("""
- Crypto trades 24/7 → holidays may have limited effect
- Observational data → cannot infer causation
- External factors not included
- Some statistical assumptions may not fully hold
""")