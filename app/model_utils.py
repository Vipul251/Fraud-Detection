import os
import joblib
import lightgbm as lgb

def load_model_artifacts():
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, '../models/fraud_model.txt')  # Saved using LightGBM
    label_encoder_path = os.path.join(base_path, '../models/label_encoder_type.pkl')
    threshold_path = os.path.join(base_path, '../models/best_threshold.pkl')

    model = lgb.Booster(model_file=model_path)  # ✅ Correct way to load LightGBM model from .txt
    label_encoder = joblib.load(label_encoder_path)
    best_threshold = joblib.load(threshold_path)

    return model, label_encoder, best_threshold
