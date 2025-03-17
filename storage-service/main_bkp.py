# # storage-service/main.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# import psycopg2
# import json

# app = FastAPI()

# # Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname="scraper_db",
#     user="user",
#     password="password",
#     host="postgres",
#     port="5432"
# )
# cursor = conn.cursor()

# class ScrapeResult(BaseModel):
#     url: str
#     data: dict

# @app.post("/store")
# def store_data(result: ScrapeResult):
#     cursor.execute("INSERT INTO results (url, data) VALUES (%s, %s)", 
#                    (result.url, json.dumps(result.data)))
#     conn.commit()
#     return {"status": "success"}



import time
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
import json
from kafka import KafkaConsumer

app = FastAPI()

# Retry connecting to PostgreSQL
def connect_to_db():
    retries = 5
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                dbname="scraper_db",
                user="user",
                password="password",
                host="postgres",
                port="5432"
            )
            return conn
        except psycopg2.OperationalError:
            print(f"Postgres not ready, retrying {i+1}/{retries}...")
            time.sleep(5)
    raise Exception("Failed to connect to Postgres after retries")

conn = connect_to_db()
cursor = conn.cursor()

cursor.execute("""
   CREATE TABLE IF NOT EXISTS scrapes (
	id SERIAL PRIMARY KEY,
	url text NOT NULL,
	title text NULL
);
""")
conn.commit()


consumer = KafkaConsumer(
    "crawl_results",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


class ScrapeResult(BaseModel):
    url: str
    data: dict

@app.post("/store")
def store_data(result: ScrapeResult):
    cursor.execute("INSERT INTO results (url, data) VALUES (%s, %s)", 
                   (result.url, json.dumps(result.data)))
    conn.commit()
    return {"status": "success"}
