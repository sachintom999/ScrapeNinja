import scrapy
import json
from kafka import KafkaConsumer,KafkaProducer
from termcolor import cprint

class KafkaSpider(scrapy.Spider):
    name = "102"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # To prevent hitting servers too fast
        "CONCURRENT_REQUESTS": 5  # Adjust based on load
    }
    
    # custom_settings = {
    # "DOWNLOAD_DELAY": 0.5,  # Reduce delay for faster processing
    # "CONCURRENT_REQUESTS": 10,  # Allow more simultaneous requests
    # "RETRY_TIMES": 3  # Retry failed requests
    # }

    
    start_urls = ["https://producthunt.com/","https://udemy.com/"]

    def __init__(self, *args, **kwargs):
        super(KafkaSpider, self).__init__(*args, **kwargs)
        


    def parse(self, response):
        if response.status in [301, 302, 403, 429, 503]:
            self.logger.warning(f"🚨 Possible blocking detected! Status Code: {response.status}")
            self.logger.warning(f"Headers: {response.headers}")
            return  # Stop parsing if blocked

        title = response.xpath("//title/text()").get(default="No title found")
        cprint(f"Scraped {response.url} - Title: {title}","green")
