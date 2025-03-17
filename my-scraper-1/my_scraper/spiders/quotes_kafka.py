import json
from kafka import KafkaProducer,KafkaConsumer
from termcolor import cprint
from scrapy_redis.spiders import RedisSpider
from time import sleep
import scrapy

class KafkaQuotesSpider(RedisSpider):
    name = "s1"
    
    # The redis key where to read URLs from
    redis_key = "crawl_requests"
    
    # Custom settings
    custom_settings = {
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'db': 0,
        },
        'LOG_LEVEL': 'INFO',
        'REDIS_START_URLS_BATCH_SIZE': 10,
        'REDIS_START_URLS_AS_SET': False,
        'SCHEDULER_IDLE_BEFORE_CLOSE': 30,
        "DOWNLOAD_DELAY": 5,  # To prevent hitting servers too fast
        "CONCURRENT_REQUESTS": 2  # Adjust based on load
        
    }
    
    custom_settings = {
    
}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Connect to Kafka
        self.kafka_producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            linger_ms=500,  # Prevents immediate closing
            acks=1  # Ensures delivery before closing
        )

        
        cprint("✅KafkaQuotesSpider initialized","green")
    
    


    def parse(self, response):
        
        try:
        
            cprint(f"\n\n\n\n🟢Successfully processing: {response.url}","green")
            sleep(3)
            result = {'text': response.url, 'author': 'Jane Austen', 'tags': ['aliteracy', 'books', 'classic', 'humor']}
            self.kafka_producer.send("crawl_results", result)
            cprint(f"Sent to Kafka: ","green")
        except Exception as e:
            cprint(f'\n\n{e=}',"error")
      

    def closed(self, reason):
        cprint(f"Spider closed due to: {reason}", "red")
        self.kafka_producer.close()
        cprint("🚨 Kafka producer closed.", "green")
    
    def error_handler(self, failure):
        """
        Handles request failures.
        """
        cprint(f"🚨 Req ffailed.", "red")
        cprint(failure, "red")
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(failure.value)




