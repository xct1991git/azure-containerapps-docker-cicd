from fastapi import FastAPI
import os
import platform

app = FastAPI(title="Cloud Native Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "azure-container-apps-demo",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "platform": platform.system()
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "code": 200}
