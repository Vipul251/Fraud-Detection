import requests

url = "http://127.0.0.1:8000/api/predict"
data = {
    "step": 1,
    "type": "TRANSFER",
    "amount": 10000,
    "oldbalanceOrg": 15000,
    "newbalanceOrig": 5000,
    "oldbalanceDest": 0,
    "newbalanceDest": 10000
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response:", response.json())
