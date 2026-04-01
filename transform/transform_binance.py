import json
import pandas as pd
import glob

# Get latest file
files = glob.glob("data/bronze/binance/*.json")
latest_file = max(files)

# Load JSON
with open(latest_file, "r") as f:
    raw = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(raw, columns=[
    "open_time","open","high","low","close","volume",
    "close_time","qav","trades","tb_base","tb_quote","ignore"
])

# Clean data
df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.date
df["btc_close"] = df["close"].astype(float)
df["btc_volume"] = df["volume"].astype(float)

# Keep needed columns
df = df[["date", "btc_close", "btc_volume"]]

# Save
df.to_csv("data/silver/btc_clean.csv", index=False)

print("BTC Silver data saved")