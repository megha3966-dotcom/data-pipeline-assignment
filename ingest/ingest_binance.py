import requests, json
from datetime import datetime
import os

url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "1d",
    "limit": 365
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

# Create folder if not exists
os.makedirs("data/bronze/binance", exist_ok=True)

# Create timestamp filename
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/binance/btc_{ts}.json"

# Save file
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")