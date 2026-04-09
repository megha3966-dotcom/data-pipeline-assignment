import pandas as pd
import holidays

# Load Silver data
btc = pd.read_csv("data/silver/btc_clean.csv")
fng = pd.read_csv("data/silver/fng_clean.csv")

# Merge datasets
df = pd.merge(btc, fng, on="date", how="inner")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Create BTC return
df["btc_daily_return"] = df["btc_close"].pct_change()

# Binary return
df["positive_return"] = (df["btc_daily_return"] > 0).astype(int)

# HOLIDAYS (NEW SOURCE)
ca_holidays = holidays.CountryHoliday('CA')

df["is_holiday"] = df["date"].isin(ca_holidays).astype(int)

# Optional holiday name
df["holiday_name"] = df["date"].apply(
    lambda x: ca_holidays.get(x) if x in ca_holidays else None
)

# New feature
df["high_volatility"] = (abs(df["btc_daily_return"]) > 0.03).astype(int)

# Clean
df = df.dropna()

# Save
df.to_csv("data/gold/crypto_sentiment.csv", index=False)

print("✅ Gold dataset updated with holidays")