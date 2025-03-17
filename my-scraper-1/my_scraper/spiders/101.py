import scrapy
import json
from kafka import KafkaConsumer,KafkaProducer
from termcolor import cprint

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
        
        
        self.kafka_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            linger_ms=500,  # Prevents immediate closing
            acks=1  # Ensures delivery before closing
        )



    def start_requests(self):
        """
        Reads URLs from Kafka and generates Scrapy requests.
        """
        kafka_consumer = KafkaConsumer(
            "crawl_requests",
            bootstrap_servers="localhost:9092",
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
    #     Process the response and send data to Kafka.
    #     """
    #     page_title = response.xpath("//title/text()").get()

    #     cprint(f"Scraped URL: {response.url} | Title: {page_title}", "green")

    #     # Kafka message format
    #     result = {
    #         "text": response.url, 
    #         "author": "Jane Austen", 
    #         "tags": ["aliteracy", "books", "classic", "humor"]
    #     }

    #     # Send message to Kafka
    #     future = self.kafka_producer.send("crawl_results", result)
    #     future.get(timeout=10)  # Ensure the message is actually sent
    #     self.kafka_producer.flush()  # Force send messages immediately
    #     cprint(f"✔ Sent to Kafka: {result}", "green")

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

        # Send result to Kafka
        future = self.kafka_producer.send("crawl_results", result)
        future.get(timeout=10)
        self.kafka_producer.flush()
        cprint(f"✔ Response Sent to Kafka\n\n", "green")

        # Commit Kafka offset
        kafka_message = response.meta["kafka_message"]
        kafka_consumer = response.meta["kafka_consumer"]
        kafka_consumer.commit()

        yield {"url": response.url, "title": page_title}
