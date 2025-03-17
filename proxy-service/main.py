# proxy-service/main.py
from fastapi import FastAPI
import random

app = FastAPI()

PROXIES = [
    "http://proxy1:8000",
    "http://proxy2:8000",
    "http://proxy3:8000",
]

@app.get("/get-proxy")
def get_proxy():
    return {"proxy": random.choice(PROXIES)}
