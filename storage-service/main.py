import json
import psycopg2
from kafka import KafkaConsumer
import os
from termcolor import cprint
from fastapi import FastAPI

app = FastAPI()

# Database connection details (Using Docker network)
DB_NAME = "scraper_db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "postgres"  # Docker service name
DB_PORT = "5432"

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cprint("✅ Connected to PostgreSQL database", "green")
except Exception as e:
    cprint(f"❌ Error connecting to PostgreSQL: {e}", "red")
    exit(1)

# Ensure the table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scrapes (
        id SERIAL PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT NULL
    );
""")
conn.commit()

# Kafka Configuration
KAFKA_BROKER = "foundry-kafka:9092"  # Use Docker service name
TOPIC_NAME = "crawl_results"

# Kafka Consumer
try:
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",  # Read from the beginning if needed
        enable_auto_commit=True,
        group_id="storage_group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")))
    cprint(f"✅ Connected to Kafka topic '{TOPIC_NAME}'", "green")
except Exception as e:
    cprint(f"❌ Error connecting to Kafka: {e}", "red")
    exit(1)

cprint(f"📥 Listening for messages on '{TOPIC_NAME}'...", "yellow")


for message in consumer:
    data = message.value
    url = data.get("url", "Unknown URL")
    title = data.get("title", "-- No title found --")

    print(f"📌 Saving to database: {url} - {title}")

    try:
        cursor.execute(
            "INSERT INTO scrapes (url, title) VALUES (%s, %s)",
            (url, title)
        )
        conn.commit()
        cprint("✅ Data inserted successfully", "green")
    except Exception as e:
        conn.rollback()
        cprint(f"❌ Error inserting data: {e}", "red")


cursor.close()
conn.close()
