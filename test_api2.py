from fastapi.testclient import TestClient
from main import app  # import your FastAPI app object

client = TestClient(app)

def test_predict_valid_input():
    payload = {
        "step": 1,
        "type": "TRANSFER",
        "amount": 1000,
        "oldbalanceOrg": 5000,
        "newbalanceOrig": 4000,
        "oldbalanceDest": 1000,
        "newbalanceDest": 2000
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert "probability_fraud" in json_data
    assert json_data["prediction"] in ["FRAUD", "NOT FRAUD"]

def test_predict_missing_fields():
    payload = {"step": 1}  # Missing required fields
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422  # validation error
