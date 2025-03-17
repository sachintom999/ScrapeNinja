import os
import redis
import time
import subprocess
from termcolor import cprint

# Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Define scaling thresholds
# MAX_QUEUE_SIZE = 1000  # Spawn new worker if queue > 1000
# MIN_QUEUE_SIZE = 50    # Kill worker if queue < 50
# MAX_WORKERS = 5        # Avoid infinite workers

MAX_QUEUE_SIZE = 2   # Spawn a new worker if queue > 10
MIN_QUEUE_SIZE = 1    # Kill a worker if queue < 2
MAX_WORKERS = 5


# Track worker processes
workers = []

def get_queue_length():
    """Check the number of URLs in Redis queue"""
    return redis_client.llen("crawl_requests")

def start_worker():
    """Start a new Scrapy worker process"""
    if len(workers) >= MAX_WORKERS:
        cprint("⚠️ Max workers reached. Not spawning more.", "yellow")
        return
    
    cprint(f"🚀 Spawning new Scrapy worker - {len(workers)} 🟠...", "green")
    process = subprocess.Popen(["scrapy", "crawl", "s1","-s LOG_LEVEL=ERROR"])
    workers.append(process)

def stop_worker():
    """Kill the oldest worker process"""
    if workers:
        cprint(f"🛑 Stopping worker...{len(workers)}", "red")
        worker = workers.pop(0)
        worker.terminate()

def manage_workers():
    """Main loop to monitor Redis queue and scale workers"""
    while True:
        queue_size = get_queue_length()
        cprint(f"📊 Queue Size: {queue_size}", "blue")

        if queue_size > MAX_QUEUE_SIZE:
            start_worker()
        
        if queue_size < MIN_QUEUE_SIZE and len(workers) > 1:
            stop_worker()

        time.sleep(2)  # Check every 5 seconds

if __name__ == "__main__":
    cprint("🔄 Worker Manager Started!", "cyan")
    manage_workers()
