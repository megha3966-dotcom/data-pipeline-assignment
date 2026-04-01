import json
import pandas as pd
import glob

files = glob.glob("data/bronze/fear_greed/*.json")

if not files:
    print("❌ No files found in bronze/fear_greed")
    exit()

latest_file = max(files)

with open(latest_file, "r") as f:
    raw = json.load(f)

data = raw["data"]

df = pd.DataFrame(data)

# FIX HERE
df["timestamp"] = df["timestamp"].astype(int)

df["date"] = pd.to_datetime(df["timestamp"], unit="s").dt.date
df["fear_greed_value"] = df["value"].astype(int)
df["fear_greed_label"] = df["value_classification"]

df = df[["date", "fear_greed_value", "fear_greed_label"]]

df.to_csv("data/silver/fng_clean.csv", index=False)

print("✅ fng_clean.csv created successfully")