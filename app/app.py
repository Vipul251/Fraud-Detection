from fastapi import APIRouter, HTTPException
import pandas as pd
import logging
from app.schema import Transaction
from app.model_utils import load_model_artifacts
router = APIRouter()
# Load model and preprocessing objects
model, label_encoder, best_threshold = load_model_artifacts()

logging.basicConfig(level=logging.INFO)

@router.post("/predict")
def predict_fraud(txn: Transaction):
    try:
        logging.info(f"Input received: {txn.dict()}")

        encoded_type = label_encoder.transform([txn.type])[0]

        df = pd.DataFrame([{
            "step": txn.step,
            "type": encoded_type,
            "amount": txn.amount,
            "oldbalanceOrg": txn.oldbalanceOrg,
            "newbalanceOrig": txn.newbalanceOrig,
            "oldbalanceDest": txn.oldbalanceDest,
            "newbalanceDest": txn.newbalanceDest
        }])

        # ✅ Use model.predict instead of predict_proba
        prob_fraud = model.predict(df)[0]
        prob_non_fraud = 1 - prob_fraud
        is_fraud = int(prob_fraud >= best_threshold)

        result = {
            "probability_non_fraud": round(prob_non_fraud, 4),
            "probability_fraud": round(prob_fraud, 4),
            "prediction": "FRAUD" if is_fraud else "NOT FRAUD",
            "model_version": "1.0",
            "status": "success"
        }
        logging.info(f"Prediction result: {result}")
        return result

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
