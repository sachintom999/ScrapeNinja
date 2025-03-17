from kafka import KafkaProducer
import json
from termcolor import cprint

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

urls = [
    "http://quotes.toscrape.com/page/5/",
    "http://quotes.toscrape.com/page/6/",
]

for url in urls:
    producer.send("crawl_requests", {"url": url})
    cprint(f"✅ Sent URL to Kafka: {url}","yellow")

producer.close()
