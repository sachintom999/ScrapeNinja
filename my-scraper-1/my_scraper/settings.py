# Scrapy settings for my_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "my_scraper"

SPIDER_MODULES = ["my_scraper.spiders"]
NEWSPIDER_MODULE = "my_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "my_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1000

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "my_scraper.middlewares.MyScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "my_scraper.middlewares.MyScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "my_scraper.pipelines.MyScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}




# Enable Scrapy Cluster components
# SPIDER_MIDDLEWARES = {
#     'scrapy_cluster.middleware.ClusterMiddleware': 543,
# }

# SCHEDULER = "scrapy_cluster.scheduler.RedisScheduler"

KAFKA_BROKERS = ['localhost:9092']
REDIS_HOST = 'localhost'

DOWNLOADER_MIDDLEWARES = {
    # 'my_scraper.middlewares.RotateUserAgentMiddleware': 400,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'my_scraper.middlewares.RotateUserAgentMiddleware': 400,
     'my_scraper.middlewares.TLSMiddleware': 543,
    #  'my_scraper.middlewares.CookieMiddleware':543,
     'my_scraper.middlewares.ProxyMiddleware': 600,
    
}


ROTATING_PROXY_LIST_PATH = 'proxies.txt'


# DOWNLOADER_MIDDLEWARES.update({
#     'my_scraper.middlewares.ProxyMiddleware': 410,
# })

# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# })



KAFKA_BROKERS = ['localhost:9092']

# Scrapy will listen for crawl jobs here
KAFKA_TOPIC_PREFIX = "crawl_requests"

# Scrapy will store results here
KAFKA_PRODUCER_TOPIC = "crawl_results"

REDIS_START_URLS_BATCH_SIZE = 10






USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]


DOWNLOAD_DELAY = 2  # Wait 2 seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 5



ROTATING_PROXY_LIST = [
    "http://199.187.210.54:4145",
"http://135.148.10.161:64870",
"http://91.107.154.214:80",
"http://45.87.68.7:15321",
"http://89.110.78.230:80",
"http://174.75.211.222:4145",
"http://142.93.202.130:3128",
"http://47.89.184.18:3128",
"http://47.251.43.115:33333",
"http://72.195.34.42:4145",
"http://47.88.59.79:82",
"http://198.49.68.80:80",
"http://142.54.226.214:4145",
"http://184.178.172.18:15280",
"http://8.209.96.245:80",
"http://157.245.95.247:443",
"http://144.126.216.57:80",
"http://45.140.143.77:18080",
"http://66.29.128.244:20762",
"http://63.143.57.115:80",
"http://67.234.120.128:50079",
"http://81.169.213.169:8888",
"http://23.220.44.200:8080",
"http://206.81.31.215:80",
"http://165.232.129.150:80",
"http://100.1.53.24:5678",
"http://192.73.244.36:80",
"http://167.99.236.14:80",
"http://47.251.122.81:8888",
"http://147.78.182.131:8085",
"http://166.0.235.147:32722",
"http://64.20.59.204:8080",
"http://130.36.36.29:443",
"http://209.250.11.126:4450",
"http://192.111.137.34:18765",
"http://190.2.131.143:11122",
"http://38.91.107.229:56884",
"http://167.235.198.62:80",
"http://68.71.247.130:4145",
"http://45.58.233.115:3128",
"http://44.215.100.135:8118",
"http://71.248.185.27:8080",
"http://159.65.230.46:8888",
"http://184.181.217.201:4145",
"http://152.26.229.52:9443",
"http://7.250.254.68:1080",
"http://162.223.90.130:80",
"http://71.14.218.2:8080",
"http://213.239.221.24:8888",
"http://130.245.32.202:80",
"http://12.7.109.1:9812",
"http://67.205.177.122:32264",
"http://89.38.97.145:12208",
"http://4.14.120.230:39593",
"http://75.119.145.154:12416",
"http://67.213.210.62:56998",
"http://156.228.78.220:3128",
"http://161.123.33.135:6158",
"http://67.205.149.230:3128",
"http://163.207.253.45:5060",
"http://47.91.89.3:9080",
"http://184.178.172.11:4145",
"http://108.181.132.115:50825",
"http://44.40.19.31:1193",
"http://162.241.50.179:30828",
"http://192.252.220.89:4145",
"http://108.175.24.1:13135",
"http://142.54.231.38:4145",
"http://192.111.135.18:18301",
"http://192.111.137.37:18762",
"http://66.29.128.243:22572",
"http://74.208.51.197:5000",
"http://38.54.101.254:8060",
"http://153.62.129.51:8081",
"http://8.211.42.167:3128",
"http://162.240.217.45:59881",
"http://69.197.167.74:6526",
"http://142.54.232.6:4145",
"http://67.213.212.52:51299",
"http://157.89.46.130:8888",
"http://154.6.99.61:3128",
"http://43.130.169.32:22065",
"http://162.241.137.197:32145",
"http://192.151.150.174:3293",
"http://152.53.36.109:45030",
"http://208.180.122.158:80",
"http://184.174.56.80:5092",
"http://89.32.200.198:6654",
"http://206.155.214.128:80",
"http://37.221.193.221:36727",
"http://190.92.178.127:43661",
"http://155.100.41.254:3128",
"http://108.184.1.216:53854",
"http://65.49.2.84:52943",
"http://162.0.220.234:12644",
"http://104.37.135.145:4145",
"http://109.121.16.77:4991",
"http://170.106.184.175:8171",
"http://207.54.167.153:80",
"http://38.91.107.220:34616",
"http://156.228.105.198:3128",
"http://44.226.98.41:8080",
"http://72.167.150.81:53503",
"http://67.205.177.122:64252",
"http://29.235.136.234:59259",
"http://192.252.220.92:17328",
"http://104.238.100.115:45314",
"http://146.190.218.26:13108",
"http://167.87.82.30:8080",
"http://175.110.112.72:31954",
"http://108.181.132.118:47129",
"http://173.241.48.55:162",
"http://174.77.111.198:49547",
"http://65.49.68.84:44951",
"http://38.91.107.224:34844",
"http://72.195.34.58:4145",
"http://76.254.6.241:57023",
"http://199.58.185.9:4145",
"http://72.195.114.184:4145",
"http://107.181.168.145:4145",
"http://142.54.235.9:4145",
"http://94.249.221.93:49200",
"http://94.249.220.135:49200",

]
