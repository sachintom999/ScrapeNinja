# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MyScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MyScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)




import tls_client
import scrapy
from termcolor import cprint
import logging

class TLSMiddleware:
    
    def __init__(self):
        self.session = tls_client.Session(client_identifier="chrome_116")
    

    
    def process_request(self, request, spider):
        try:
            cprint(f"🔴Using TLSMiddleware for URL: {request.url}","green")
            response = self.session.get(request.url)
            return scrapy.http.HtmlResponse(
                url=request.url,
                body=response.text,
                encoding='utf-8',
                request=request
            )
        except Exception as e:
            spider.logger.error(f"TLS Request failed: {e}")
            return None  # Let Scrapy retry the request




import redis
import json

class CookieMiddleware:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        cprint(f'\n\n{self.redis_client=}',"red")

    def process_request(self, request, spider):
        cprint(f'148 CookieMiddleware in process_request',"red")
        domain = request.url.split("/")[2]
        cookies = self.redis_client.get(f"{domain}_cookies")
        headers = self.redis_client.get(f"{domain}_headers")

        if cookies and headers:
            request.cookies = json.loads(cookies)
            request.headers.update(json.loads(headers))

    def process_response(self, request, response, spider):
        cprint(f'158 CookieMiddleware in process_Response..',"red")
        domain = request.url.split("/")[2]
        cookies = response.headers.getlist('Set-Cookie')

        if cookies:
            self.redis_client.set(f"{domain}_cookies", json.dumps(cookies), ex=86400)  # Store for 1 day
        
        cookies_dict = {cookie.split(b'=')[0].decode(): cookie.split(b'=')[1].decode() for cookie in cookies}
        self.redis_client.set(f"{domain}_cookies", json.dumps(cookies_dict), ex=86400)  # Store for 1 day


        return response



class RotateUserAgentMiddleware:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


PROXIES = [
    "http://12.34.56.78:8080",
    "http://98.76.54.32:3128",
]




import random

class RotateUserAgentMiddleware:
    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(spider.settings.get("USER_AGENTS"))



import random

class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta["proxy"] = random.choice(spider.settings.get("ROTATING_PROXY_LIST"))
