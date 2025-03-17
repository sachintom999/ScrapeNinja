import scrapy

class MySpider(scrapy.Spider):
    name = "s3"
    start_urls = ["https://example.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies={"session": "abcd1234"},  # Example cookie
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info(f"Response received from {response.url}")
