from fastapi import FastAPI
from app.app import router as fraud_router  # ✅ Absolute import

app = FastAPI(title="Fraud Detection API", version="1.0")

app.include_router(fraud_router, prefix="/api")  # Or remove prefix

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is live."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
