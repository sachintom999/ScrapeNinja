

import scrapy

class JA3Spider(scrapy.Spider):
    name = "s2"
    start_urls = ["https://tools.scrapfly.io/api/fp/ja3?extended=1"]

    def parse(self, response):
        json_data = response.json()
        self.logger.info(f"🟢JA3 Fingerprint: {json_data['ja3']}")
        self.logger.info(f"🟢JA3 Digest: {json_data['ja3_digest']}")
        self.logger.info(f"🟢TLS Version: {json_data['tls']['version']}")
