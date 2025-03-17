import scrapy
from kafka import KafkaConsumer, KafkaProducer
import json
import requests

KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'
REQUEST_TOPIC = "crawl_requests"
RESULTS_TOPIC = "crawl_results"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

class MySpider(scrapy.Spider):
    name = "my_spider"

    def __init__(self):
        self.consumer = KafkaConsumer(
            REQUEST_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8"))
        )

    def start_requests(self):
        for message in self.consumer:
            url = message.value["url"]
            proxy = requests.get("http://proxy-service:8000/get-proxy").json()["proxy"]
            yield scrapy.Request(url, callback=self.parse, meta={"proxy": proxy})

    def parse(self, response):
        data = {"url": response.url, "content": response.text}
        producer.send(RESULTS_TOPIC, data)
