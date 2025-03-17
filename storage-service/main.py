# storage-service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import json

app = FastAPI()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="scraper_db",
    user="user",
    password="password",
    host="postgres",
    port="5432"
)
cursor = conn.cursor()

class ScrapeResult(BaseModel):
    url: str
    data: dict

@app.post("/store")
def store_data(result: ScrapeResult):
    cursor.execute("INSERT INTO results (url, data) VALUES (%s, %s)", 
                   (result.url, json.dumps(result.data)))
    conn.commit()
    return {"status": "success"}
