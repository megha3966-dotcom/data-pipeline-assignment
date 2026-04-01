import pandas as pd

# Load Silver data
btc = pd.read_csv("data/silver/btc_clean.csv")
fng = pd.read_csv("data/silver/fng_clean.csv")

# Join on date
df = pd.merge(btc, fng, on="date", how="inner")

# Create derived features
df["btc_daily_return"] = df["btc_close"].pct_change()

# Binary variable (VERY IMPORTANT for stats)
df["positive_return"] = (df["btc_daily_return"] > 0).astype(int)

# Drop missing values
df = df.dropna()

# Save Gold dataset
df.to_csv("data/gold/crypto_sentiment.csv", index=False)

print("✅ Gold dataset created successfully")