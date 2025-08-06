import lightgbm as lgb
import numpy as np

print("LightGBM version:", lgb.__version__)

# Create a small dummy dataset
X_train = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y_train = np.array([0, 1, 0, 1])

# Prepare dataset for LightGBM
train_data = lgb.Dataset(X_train, label=y_train)

# Train a simple model
params = {
    'objective': 'binary',
    'verbose': -1,
    'metric': 'binary_logloss'
}

model = lgb.train(params, train_data, num_boost_round=5)

# Make a prediction
X_test = np.array([[2, 3], [4, 5]])
preds = model.predict(X_test)

print("Predictions:", preds)
