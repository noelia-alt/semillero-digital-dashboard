from fastapi import FastAPI
from config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "client_id": settings.google_client_id,
        "message": "FastAPI + Google OAuth listo 🚀"
    }
