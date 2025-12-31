from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

# Variáveis globais
app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@app.get("/db-check")
def check_db_conn() -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        return {"db": "disconnected", "error": str(e)}