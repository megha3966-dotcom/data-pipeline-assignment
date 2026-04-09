# 📊 Assignment 4 Analysis Plan

## 📌 Objective

To extend the Assignment 3 dataset and perform statistical analysis using an additional data source.

---

## 📡 New Data Source

- Canadian holidays generated using the `holidays` Python library
- Joined with dataset using the `date` column

---

## 🔗 Join Strategy

| Property | Detail |
|----------------|------------------------|
| Key | `date` |
| Type | Left join |
| Missing values | Treated as non-holidays |

---

## 🧱 New Variables

| Variable | Description |
|------------------|--------------------------------------|
| `is_holiday` | Binary: 1 = holiday, 0 = not |
| `high_volatility` | Binary based on return threshold |

---

## 📊 Statistical Tests

1. **One-Sample T-Test** — Tests if average return differs from zero
2. **Two-Sample T-Test** — Compares returns on holidays vs. non-holidays
3. **Chi-Square Test** — Tests independence between `positive_return` and `is_holiday`
4. **Variance Test** — Compares volatility between groups
5. **Correlation** — Relationship between BTC volume and BTC return

---

## 📈 Visualizations

- Time series (returns)
- Boxplot (holiday vs. non-holiday)
- Scatter plot (volume vs. return)
- Bar chart (positive returns)

---

## 🎯 Expected Outcome

- Identify differences in returns across conditions
- Explore relationships between variables
- Provide statistical justification for findings