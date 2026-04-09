import pandas as pd
import holidays
import datetime

# ========================
# LOAD SILVER DATA
# ========================
btc = pd.read_csv("data/silver/btc_clean.csv")
fng = pd.read_csv("data/silver/fng_clean.csv")

# ========================
# FIX DATE FORMAT — normalize strips time component
# ========================
btc["date"] = pd.to_datetime(btc["date"]).dt.normalize()
fng["date"] = pd.to_datetime(fng["date"]).dt.normalize()

# ========================
# SORT DATA (REQUIRED FOR ASOF)
# ========================
btc = btc.sort_values("date").reset_index(drop=True)
fng = fng.sort_values("date").reset_index(drop=True)

# ========================
# DEBUG — CHECK DATE RANGES BEFORE MERGE
# ========================
print("BTC date range:", btc["date"].min(), "→", btc["date"].max())
print("FNG date range:", fng["date"].min(), "→", fng["date"].max())
print("BTC rows:", len(btc))
print("FNG rows:", len(fng))

# ========================
# MERGE USING ASOF
# ========================
df = pd.merge_asof(
    btc,
    fng,
    on="date",
    direction="backward"
)

# ========================
# HANDLE MISSING SENTIMENT VALUES
# ========================
df["fear_greed_value"] = df["fear_greed_value"].ffill()
df["fear_greed_label"] = df["fear_greed_label"].ffill()

# ========================
# CREATE RETURNS
# ========================
df["btc_daily_return"] = df["btc_close"].pct_change()
df["positive_return"] = (df["btc_daily_return"] > 0).astype(int)

# ========================
# ADD HOLIDAYS — FIX: use pd.Timestamp(x).date() for reliable matching
# ========================
ca_holidays = holidays.CountryHoliday('CA')

df["is_holiday"] = df["date"].apply(
    lambda x: 1 if pd.Timestamp(x).date() in ca_holidays else 0
)

df["holiday_name"] = df["date"].apply(
    lambda x: ca_holidays.get(pd.Timestamp(x).date(), None)
)

# ========================
# ADD VOLATILITY FEATURE
# ========================
df["high_volatility"] = (abs(df["btc_daily_return"]) > 0.03).astype(int)

# ========================
# DEBUG — CHECK NaN COUNTS BEFORE DROPPING
# ========================
print("\nNaN count per column:")
print(df.isnull().sum())

# ========================
# TARGETED DROPNA — only drop where critical columns are missing
# ========================
df = df.dropna(subset=["btc_close", "fear_greed_value", "btc_daily_return"])

# ========================
# VERIFY HOLIDAY DETECTION
# ========================
print("\nTotal holidays found:", df["is_holiday"].sum())
print("\nHoliday dates found:")
print(df[df["is_holiday"] == 1][["date", "holiday_name"]])

# Manual sanity check for a known holiday in range
test_date = datetime.date(2025, 12, 25)
print("\nChristmas 2025 in ca_holidays:", test_date in ca_holidays)

# ========================
# GROUP SIZE CHECK — for two-sample tests
# ========================
holiday_group = df[df["is_holiday"] == 1]["btc_daily_return"]
non_holiday_group = df[df["is_holiday"] == 0]["btc_daily_return"]

print(f"\nHoliday samples:     {len(holiday_group)}")
print(f"Non-holiday samples: {len(non_holiday_group)}")

if len(holiday_group) < 2:
    print("⚠️  WARNING: Not enough holiday samples for two-sample t-test or variance comparison.")
elif holiday_group.std() == 0:
    print("⚠️  WARNING: Holiday group has zero variance. F-statistic cannot be computed.")
else:
    print("✅ Group sizes are sufficient for two-sample tests.")

# ========================
# FINAL DEBUG CHECK
# ========================
print("\nFINAL rows:", len(df))
print(df.head())

# ========================
# SAVE GOLD DATA
# ========================
df.to_csv("data/gold/crypto_sentiment.csv", index=False)

print("\n✅ Gold dataset created successfully with aligned data!")