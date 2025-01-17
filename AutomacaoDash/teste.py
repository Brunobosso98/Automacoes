import requests
import os

url = "https://market.csgo.com/api/v2/prices/orders/USD.json"
response = requests.get(url)

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "prices_orders_usd.json")

with open(json_path, "w") as file:
    file.write(response.text)

print("Download concluído!")
