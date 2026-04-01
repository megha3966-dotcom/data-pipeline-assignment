# Statistical Analysis Preview

## 📌 Research Question

Is the average daily Bitcoin return different from zero, and does it differ between Fear and Greed market conditions?

---

## 📊 Outcome Variable

* btc_daily_return (continuous variable)

---

## 👥 Grouping Variable

* fear_greed_label (Fear vs Greed)

---

## 🔘 Binary Variable

* positive_return

  * 1 = positive return
  * 0 = negative return

This is used for proportion-based testing.

---

## 🧪 Hypotheses

### 1. One-sample t-test

* H0: Mean BTC return = 0
* H1: Mean BTC return ≠ 0

---

### 2. Two-sample t-test

* H0: Mean return (Fear) = Mean return (Greed)
* H1: Mean return differs between groups

---

### 3. Proportion z-test

* H0: Proportion of positive returns is the same for Fear and Greed
* H1: Proportion differs

---

## 📈 Selected Tests

* One-sample t-test → to test overall return vs zero
* Two-sample t-test → compare Fear vs Greed
* Proportion z-test → compare positive return rates

---

## 🎯 Why This Works

The dataset includes:

* A continuous variable → btc_daily_return
* A grouping variable → fear_greed_label
* A binary variable → positive_return

This makes it suitable for all required statistical tests in Part 2.
