


import time
from kafka import KafkaAdminClient
import subprocess
from kafka.errors import NoBrokersAvailable

KAFKA_BOOTSTRAP_SERVERS = 'foundry-kafka:9092'
REQUEST_TOPIC = "crawl_requests"

def get_queue_size():
    retries = 5
    for i in range(retries):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
            partitions = admin_client.describe_topics([REQUEST_TOPIC])[0]["partitions"]
            return sum([p["partition_log_end_offset"] for p in partitions])
        except NoBrokersAvailable:
            print(f"Kafka not available, retrying in 5s... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("Kafka is still not available after retries")

# def scale_workers():
#     queue_size = get_queue_size()
#     num_workers = queue_size // 10  # 1 worker per 10 requests
#     # subprocess.run(["docker-compose", "up", "--scale", f"scraper-service={num_workers}"])
#     subprocess.run(["docker", "compose", "up", "--scale", f"scraper-service={num_workers}"])



# if __name__ == "__main__":
#     scale_workers()



import requests

def scale_workers():
    queue_size = get_queue_size()
    num_workers = queue_size // 10  # 1 worker per 10 requests
    requests.post("http://host.docker.internal:5001/scale", json={"num_workers": num_workers})

if __name__ == "__main__":
    scale_workers()