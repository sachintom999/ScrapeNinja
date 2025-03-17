# import scrapy
# from scrapy_playwright.page import PageMethod
# from termcolor import cprint

# class MySpider(scrapy.Spider):
#     name = "s3"
#     start_urls = ["https://example.com"]

#     custom_settings = {
#         "PLAYWRIGHT_BROWSER_TYPE": "chromium",
#         "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},  # Run headless
#     }

#     async def parse(self, response):
#         cprint(f'15 in parse...',"red")
#         # Extract headers
#         headers = response.request.headers.to_unicode_dict()

#         # Extract cookies
#         cookies = {cookie["name"]: cookie["value"] for cookie in response.headers.getlist('Set-Cookie')}
#         res = { "headers": headers, "cookies": cookies }
#         cprint(f'\n\n{res=}',"red")
        

#         yield {
#             "headers": headers,
#             "cookies": cookies
#         }


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
