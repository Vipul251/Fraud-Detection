import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_curve
import numpy as np

# Load dataset
DATA_PATH = "data/Fraud.csv"
df = pd.read_csv(DATA_PATH)
df_clean = df.drop(['nameOrig', 'nameDest'], axis=1)
le_type = LabelEncoder()
df_clean['type'] = le_type.fit_transform(df_clean['type'])
df_clean = df_clean[~df_clean['isFraud'].isna()]

X = df_clean.drop(['isFraud', 'isFlaggedFraud'], axis=1)
y = df_clean['isFraud']

# Train-test split
X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# Train model
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val)
params = {
    'objective': 'binary',
    'metric': 'auc',
    'learning_rate': 0.05,
    'scale_pos_weight': pos_weight,
    'boosting_type': 'gbdt',
    'verbose': -1,
    'seed': 42
}

bst = lgb.train(params, train_data, num_boost_round=1000, valid_sets=[val_data],
                callbacks=[lgb.early_stopping(stopping_rounds=50), lgb.log_evaluation(period=100)])

# Threshold tuning
y_pred_proba = bst.predict(X_val)
# Ensure inputs are numpy arrays
y_val_np = np.array(y_val)
y_pred_proba_np = np.array(y_pred_proba)
precision, recall, thresholds = precision_recall_curve(y_val_np, y_pred_proba_np)
idx = np.where(recall >= 0.9)[0]
best_idx = idx[np.argmax(precision[idx])]
best_threshold = thresholds[best_idx]

# Save artifacts
bst.save_model("models/fraud_model.txt")
joblib.dump(le_type, "models/label_encoder_type.pkl")
joblib.dump(best_threshold, "models/best_threshold.pkl")
print("Model and artifacts saved.")