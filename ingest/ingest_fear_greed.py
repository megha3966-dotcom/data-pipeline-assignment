import requests, json
from datetime import datetime
import os

url = "https://api.alternative.me/fng/"
params = {
    "limit": 365,
    "format": "json"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

# Create folder if not exists
os.makedirs("data/bronze/fear_greed", exist_ok=True)

# Create timestamp filename
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/fear_greed/fng_{ts}.json"

# Save file
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")