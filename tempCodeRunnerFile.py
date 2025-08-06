rom fastapi import FastAPI
from app.app import router as fraud_router  # ✅ Absolute import

app = FastAPI(title="Fraud Detection API", version="1.0")

app.include_router(fraud_router, prefix="/api")  # Or remove prefix

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is live."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
