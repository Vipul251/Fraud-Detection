import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime

API_URL = "https://fraud-detection-2-iv4i.onrender.com/"
DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            step INTEGER,
            type TEXT,
            amount REAL,
            oldbalanceOrg REAL,
            newbalanceOrig REAL,
            oldbalanceDest REAL,
            newbalanceDest REAL,
            prediction TEXT,
            fraud_probability REAL
        )
    """)
    conn.commit()
    conn.close()

def log_prediction(data, prediction_result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (timestamp, step, type, amount, oldbalanceOrg, newbalanceOrig,
                                 oldbalanceDest, newbalanceDest, prediction, fraud_probability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        data["step"],
        data["type"],
        data["amount"],
        data["oldbalanceOrg"],
        data["newbalanceOrig"],
        data["oldbalanceDest"],
        data["newbalanceDest"],
        prediction_result["prediction"],
        prediction_result["fraud_probability"]
    ))
    conn.commit()
    conn.close()

def make_prediction(data):
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            api_result = response.json()
            # Map keys to expected Streamlit keys
            return {
                "prediction": api_result["prediction"],
                "fraud_probability": api_result["probability_fraud"],
                "model_version": api_result.get("model_version", "N/A")
            }
        else:
            st.error(f"❌ Server Error: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"⚠️ Backend not reachable:\n{e}")
    return None

def main():
    st.set_page_config(page_title="Fraud Detection", page_icon="🕵️‍♂️", layout="centered")
    st.title("🛡️ Real-Time Fraud Detection System")

    tab1, tab2 = st.tabs(["🔍 Single Prediction", "📁 Batch Upload"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            step = st.number_input("Step", min_value=1, value=1)
            type_ = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT", "DEBIT", "PAYMENT", "CASH_IN"])
            amount = st.number_input("Amount", min_value=0.0)

        with col2:
            oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0)
            newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0)
            oldbalanceDest = st.number_input("Old Balance (Dest)", min_value=0.0)
            newbalanceDest = st.number_input("New Balance (Dest)", min_value=0.0)

        if st.button("🚀 Predict Now"):
            data = {
                "step": step,
                "type": type_,
                "amount": amount,
                "oldbalanceOrg": oldbalanceOrg,
                "newbalanceOrig": newbalanceOrig,
                "oldbalanceDest": oldbalanceDest,
                "newbalanceDest": newbalanceDest
            }

            with st.spinner("Predicting..."):
                result = make_prediction(data)

            if result:
                st.success(f"Prediction: **{result['prediction']}**")
                st.metric("Fraud Probability", f"{result['fraud_probability']*100:.2f}%")
                st.caption(f"Model Version: v{result['model_version']}")
                log_prediction(data, result)

    with tab2:
        uploaded_file = st.file_uploader("Upload a CSV file with transaction data", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("📄 Uploaded Data Preview:", df.head())

            if st.button("📊 Predict All"):
                results = []
                for i, row in df.iterrows():
                    row_data = row.to_dict()
                    result = make_prediction(row_data)
                    if result:
                        row_data.update({
                            "prediction": result["prediction"],
                            "fraud_probability": result["fraud_probability"]
                        })
                        log_prediction(row_data, result)
                        results.append(row_data)

                if results:
                    output_df = pd.DataFrame(results)
                    st.success("✅ Batch predictions completed!")
                    st.dataframe(output_df)

                    csv = output_df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")
    # Footer
    st.markdown("""<hr style="margin-top: 2rem; margin-bottom: 1rem;">""", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "<small>© 2025 Vipul Bhatt. All rights reserved.</small>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    init_db()
    main()

