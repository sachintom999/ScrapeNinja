import scrapy
import json
from kafka import KafkaConsumer,KafkaProducer
from termcolor import cprint
import time

class KafkaSpider(scrapy.Spider):
    name = "101"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # To prevent hitting servers too fast
        "CONCURRENT_REQUESTS": 5  # Adjust based on load
    }
    
    # custom_settings = {
    # "DOWNLOAD_DELAY": 0.5,  # Reduce delay for faster processing
    # "CONCURRENT_REQUESTS": 10,  # Allow more simultaneous requests
    # "RETRY_TIMES": 3  # Retry failed requests
    # }

    
    # start_urls = ["https://quotes.toscrape.com/page/1/","https://quotes.toscrape.com/page/2/"]

    def __init__(self, *args, **kwargs):
        super(KafkaSpider, self).__init__(*args, **kwargs)
        
        
        self.kafka_producer = create_kafka_producer()



    def start_requests(self):
        """
        Reads URLs from Kafka and generates Scrapy requests.
        """
        kafka_consumer = KafkaConsumer(
            "crawl_requests",
            # bootstrap_servers="localhost:9092",
            bootstrap_servers="foundry-kafka:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,  # Ensure manual commit
            group_id="scrapy_group"  # Enable multiple workers in the same group
        )

        for message in kafka_consumer:
            url = message.value.get("url")
            if url:
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    meta={"kafka_message": message, "kafka_consumer": kafka_consumer}  # Pass message and consumer
                )




    # def parse(self, response):
    #     """
    #     Process the response and commit Kafka offset.
    #     """
    #     page_title = response.xpath("//title/text()").get()
    #     cprint(f"\n\n Scraped URL: {response.url} | Title: {page_title}", "green")

    #     result = {
    #         "text": response.url, 
    #         "url": response.url, 
    #         "title": page_title, 
    #         "author": "Jane Austen", 
    #         "tags": ["aliteracy", "books", "classic", "humor"]
    #     }

    #     # Send result to Kafka
    #     future = self.kafka_producer.send("crawl_results", result)
    #     future.get(timeout=10)
    #     self.kafka_producer.flush()
    #     cprint(f"✔ Response Sent to Kafka\n\n", "green")

    #     # Commit Kafka offset
    #     kafka_message = response.meta["kafka_message"]
    #     kafka_consumer = response.meta["kafka_consumer"]
    #     kafka_consumer.commit()

    #     yield {"url": response.url, "title": page_title}

    def parse(self, response):
        """
        Process the response and commit Kafka offset.
        """
        page_title = response.xpath("//title/text()").get()
        cprint(f"\n\n Scraped URL: {response.url} | Title: {page_title}", "green")

        result = {
            "text": response.url, 
            "url": response.url, 
            "title": page_title, 
            "author": "Jane Austen", 
            "tags": ["aliteracy", "books", "classic", "humor"]
        }

        # ✅ Convert to JSON string and encode as bytes
        result_bytes = json.dumps(result).encode("utf-8")

        # Send result to Kafka
        future = self.kafka_producer.send("crawl_results", value=result_bytes)
        future.get(timeout=10)
        self.kafka_producer.flush()
        cprint(f"✔ Response Sent to Kafka\n\n", "green")

        # Commit Kafka offset
        kafka_message = response.meta["kafka_message"]
        kafka_consumer = response.meta["kafka_consumer"]
        kafka_consumer.commit()

        yield {"url": response.url, "title": page_title}


def create_kafka_producer():
    for i in range(10):  # Retry 10 times
        try:
            print(f"Attempt {i+1}: Connecting to Kafka...")
            producer = KafkaProducer(bootstrap_servers="foundry-kafka:9092")
            print("✅ Successfully connected to Kafka!")
            return producer
        except Exception as e:
            print(f"❌ Failed to connect to Kafka (Attempt {i+1}/10). Retrying in 5s...")
            time.sleep(5)  # Wait before retrying
    raise Exception("❌ Kafka is unreachable after multiple retries.")
