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

# FIX: Convert date to plain date object to avoid PyArrow serialization error
df["date"] = pd.to_datetime(df["date"]).dt.date

# ========================
# TITLE
# ========================
st.title("📊 Crypto Market Analysis Dashboard")
st.markdown("Analyze Bitcoin returns using sentiment and holiday data.")

# ========================
# METRICS
# ========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Daily Return", f"{df['btc_daily_return'].mean():.4f}")
col2.metric("Avg Volume", f"{df['btc_volume'].mean():,.0f}")
col3.metric("Positive Days (%)", f"{df['positive_return'].mean()*100:.2f}%")
col4.metric("Holiday Days", f"{df['is_holiday'].sum()}")

st.divider()

# ========================
# OVERVIEW
# ========================
st.header("📌 Project Overview")
st.write("""
This dashboard explores how Bitcoin returns relate to sentiment and holidays.

A new feature (**is_holiday**) was added using the `holidays` Python library,
allowing comparison between holiday and non-holiday trading behavior.

The goal is to move beyond visualization into statistical testing.
""")

# ========================
# DATA PREVIEW
# ========================
with st.expander("📂 View Dataset"):
    st.dataframe(df.head(10))
    st.write(df.describe())

# ========================
# VISUALS
# ========================
st.header("📈 Visual Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("BTC Returns Over Time")
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["btc_daily_return"], linewidth=0.8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Return")
    ax.axhline(0, color="red", linestyle="--", linewidth=0.7)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Volume vs Returns")
    fig, ax = plt.subplots()
    ax.scatter(df["btc_volume"], df["btc_daily_return"], alpha=0.5, color="steelblue")
    ax.set_xlabel("Volume")
    ax.set_ylabel("Return")
    st.pyplot(fig)

# FIX: Boxplot — dynamically match tick count to label count
st.subheader("Holiday vs Non-Holiday Returns")
fig, ax = plt.subplots()
df.boxplot(column="btc_daily_return", by="is_holiday", ax=ax)
ticks = ax.get_xticks()
labels = ["Non-Holiday (0)", "Holiday (1)"]
ax.set_xticks(ticks[:len(labels)])
ax.set_xticklabels(labels[:len(ticks)])
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
# 1. ONE-SAMPLE T-TEST
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
    st.success("✅ Reject H0 → Mean return is significantly different from 0")
else:
    st.warning("⚠️ Fail to Reject H0 → No significant difference from 0")

st.markdown(f"**Interpretation:** With p = {p_val:.4f}, there is insufficient evidence that BTC average return differs from zero.")

# ------------------------
# 2. TWO-SAMPLE T-TEST
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

if len(holiday) >= 2 and holiday.std() > 0:
    t_stat2, p_val2 = stats.ttest_ind(holiday, non_holiday, equal_var=False)
    col1, col2 = st.columns(2)
    col1.metric("T-Statistic", f"{t_stat2:.4f}")
    col2.metric("P-Value", f"{p_val2:.4f}")
    if p_val2 < alpha:
        st.success("✅ Reject H0 → Returns differ significantly")
    else:
        st.warning("⚠️ Fail to Reject H0 → No significant difference")
    st.markdown(f"**Interpretation:** With only {len(holiday)} holiday observations, results should be interpreted cautiously.")
else:
    st.error(f"⚠️ Not enough holiday samples ({len(holiday)}) to perform this test. Re-run create_gold.py to fix holiday detection.")

# ------------------------
# 3. CHI-SQUARE TEST
# ------------------------
st.subheader("3️⃣ Chi-Square Test")
st.markdown("""
**Hypothesis**
- H0: Variables are independent
- H1: Variables are related

**Assumptions**
- Expected frequency ≥ 5 in each cell
""")

contingency = pd.crosstab(df["positive_return"], df["is_holiday"])
st.dataframe(contingency)

chi2, p, dof, expected = stats.chi2_contingency(contingency)

col1, col2 = st.columns(2)
col1.metric("Chi²", f"{chi2:.4f}")
col2.metric("P-Value", f"{p:.4f}")

if (expected < 5).any():
    st.error("⚠️ Assumption violated: Some expected cell frequencies are < 5. Results may be unreliable due to limited holiday samples.")
else:
    if p < alpha:
        st.success("✅ Reject H0 → Relationship exists between variables")
    else:
        st.warning("⚠️ Fail to Reject H0 → Variables appear independent")

# ------------------------
# 4. VARIANCE COMPARISON
# ------------------------
st.subheader("4️⃣ Variance Comparison")

if len(holiday) >= 2 and holiday.var(ddof=1) > 0 and non_holiday.var(ddof=1) > 0:
    f_stat = holiday.var(ddof=1) / non_holiday.var(ddof=1)
    st.metric("F-Statistic", f"{f_stat:.4f}")
    if f_stat > 1.5 or f_stat < 0.67:
        st.success("👉 Variability differs between groups")
    else:
        st.info("👉 Variability is similar between groups")
else:
    st.error(f"⚠️ Cannot compute F-Statistic: insufficient or zero-variance holiday data ({len(holiday)} samples).")

# ------------------------
# 5. CORRELATION ANALYSIS
# ------------------------
st.subheader("5️⃣ Correlation Analysis")
st.markdown("""
**Hypothesis**
- H0: No correlation between volume and return
- H1: Correlation exists
""")

corr, p_val = stats.pearsonr(df["btc_volume"], df["btc_daily_return"])

col1, col2 = st.columns(2)
col1.metric("Pearson Correlation", f"{corr:.4f}")
col2.metric("P-Value", f"{p_val:.4f}")

if p_val < alpha:
    st.success("✅ Reject H0 → Significant correlation exists")
else:
    st.warning("⚠️ Fail to Reject H0 → No significant correlation")

st.markdown(f"**Interpretation:** A weak correlation of {corr:.4f} suggests volume and return have little linear relationship.")

st.divider()

# ========================
# KEY INSIGHTS
# ========================
st.header("📌 Key Insights")
st.info("""
- Bitcoin returns fluctuate over time with no significant deviation from zero
- Holiday vs non-holiday differences could not be robustly tested due to limited holiday samples
- Volume and return show no significant linear correlation
- Results do not imply causation — observational data only
""")

# ========================
# LIMITATIONS
# ========================
st.header("⚠️ Limitations")
st.warning("""
- Crypto trades 24/7 → holidays may have limited effect on market behavior
- Only 5 Canadian holidays in the dataset → insufficient for group comparisons
- Observational data → causation cannot be inferred
- External factors (news, macroeconomics) not included
- Some statistical assumptions (normality, expected frequency) may not fully hold
""")