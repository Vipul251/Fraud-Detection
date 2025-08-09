🛡️ Fraud Detection System
📌 Overview
A real-time fraud detection system built from scratch using Python, Scikit-learn, and Streamlit.
This project leverages machine learning classification models to detect fraudulent financial transactions based on patterns in the data.
Designed with both batch and single prediction capabilities, it includes a simple Streamlit front-end and a FastAPI back-end.

🎯 Motivation 
Fraudulent transactions cause billions in losses annually.
I wanted to design, train, and deploy a fraud detection system end-to-end to:

Understand real-world ML pipeline challenges.

Learn model training, optimization, and deployment.

Implement imbalanced data handling and feature engineering for practical fraud detection.

Provide fast and interpretable predictions for decision-making.

🛠 Tech Stack
Languages & Libraries

Python 3.11

Pandas, NumPy (data handling)

Scikit-learn (modeling & evaluation)

Imbalanced-learn (SMOTE oversampling)

Matplotlib, Seaborn (visualization)

Streamlit (frontend UI)

FastAPI (backend API)

Tools

Git & GitHub

VS Code

Render / Local deployment

🔍 Project Workflow
1️⃣ Data Preparation
Reasoning: Fraud detection datasets are highly imbalanced; I applied SMOTE [Lightgbm] to balance the dataset.

Actions:
Loaded CSV dataset using Pandas.
Removed duplicates and handled missing values.
Applied scaling to numerical features.

2️⃣ Feature Engineering
Reasoning: The right features drastically improve detection accuracy.
Actions:
Extracted transaction type as categorical.
Created derived features (e.g., balance differences before and after transactions).

3️⃣ Model Training
Reasoning: Chose models that handle imbalanced data well (e.g., Random Forest, Logistic Regression).
Actions:
Trained multiple classifiers.
Tuned hyperparameters with GridSearchCV.
Selected the best model based on F1-score and AUC-ROC.

4️⃣ Model Evaluation
Reasoning: Accuracy alone is misleading for imbalanced datasets.

Actions:
Evaluated precision, recall, F1-score, ROC curve.
Plotted confusion matrix for model interpretability.

5️⃣ API & UI Development
Reasoning: To make predictions accessible via a web interface.
Actions:
Built FastAPI endpoint /api/predict for model inference.
Integrated Streamlit app for single & batch predictions.
Connected frontend to backend API.

6️⃣ Deployment
Reasoning: To simulate real-world usage and share results.

Actions:
Packaged dependencies in requirements.txt.
Deployed backend API on Render.
Hosted frontend locally / on Streamlit Cloud.

📂 Project Structure
bash
Copy
Edit
Fraud-Detection/
│── data/                # Dataset
│── models/              # Trained model files
│── api/                 # FastAPI backend
│── streamlit_app.py     # Streamlit frontend
│── train_model.py       # Model training script
│── requirements.txt
│── README.md
🚀 How to Run Locally
bash
Copy
Edit
# 1. Clone repo
git clone https://github.com/Vipul251/Fraud-Detection.git
cd Fraud-Detection

# 2. Create virtual environment & activate
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train model (optional)
python train_model.py

# 5. Run FastAPI backend
uvicorn api.main:app --reload --port 8001

# 6. Run Streamlit frontend
streamlit run streamlit_app.py

✅ Model detects fraudulent transactions with high recall, minimizing false negatives.

📌 Future Improvements
Deploy both API & frontend to a single cloud environment.

Integrate real-time transaction streaming with Kafka.

Add explainable AI (XAI) methods for feature importance.


For contribution feel free to reach at contact.vipulbhatt@gmail.com
