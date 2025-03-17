


import time
from kafka import KafkaAdminClient,KafkaConsumer
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


# def get_kafka_queue_size():
#     from kafka import KafkaAdminClient, KafkaConsumer

#     # Kafka details
#     BOOTSTRAP_SERVERS = 'foundry-kafka:9092'
#     CONSUMER_GROUP = "scrapy_group"
#     TOPIC = "crawl_requests"

#     # Initialize Kafka Admin Client
#     admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

#     # Get committed offsets for the consumer group
#     consumer_offsets = admin_client.list_consumer_group_offsets(CONSUMER_GROUP)

#     # Create a KafkaConsumer to get latest offsets (log end offsets)
#     consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)

#     total_lag = 0
#     for partition, offset_info in consumer_offsets.items():
#         latest_offset = consumer.end_offsets([partition])[partition]  # Get latest offset
#         committed_offset = offset_info.offset if offset_info.offset is not None else 0  # Get committed offset
#         partition_lag = latest_offset - committed_offset  # Calculate lag
#         total_lag += partition_lag
#         print(f"Partition {partition.partition}: Lag = {partition_lag}")

#     print(f"Total Kafka Queue Size (Lag): {total_lag}")
    
#     return total_lag
        


# def get_kafka_queue_size():
#     # Kafka details
#     # BOOTSTRAP_SERVERS = 'foundry-kafka:9092'
#     BOOTSTRAP_SERVERS = 'foundry-kafka:9092'
#     CONSUMER_GROUP = "scrapy_group"
#     TOPIC = "crawl_requests"

#     retries = 10  # Number of retries
#     for i in range(retries):
#         try:
#             print(f"🔄 Attempt {i+1}: Connecting to Kafka...")

#             # Initialize Kafka Admin Client
#             admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

#             # Get committed offsets for the consumer group
#             consumer_offsets = admin_client.list_consumer_group_offsets(CONSUMER_GROUP)

#             # Create a KafkaConsumer to get latest offsets (log end offsets)
#             consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)

#             total_lag = 0
#             for partition, offset_info in consumer_offsets.items():
#                 latest_offset = consumer.end_offsets([partition])[partition]  # Get latest offset
#                 committed_offset = offset_info.offset if offset_info.offset is not None else 0  # Get committed offset
#                 partition_lag = latest_offset - committed_offset  # Calculate lag
#                 total_lag += partition_lag
#                 print(f"✅ Partition {partition.partition}: Lag = {partition_lag}")

#             print(f"✅ Total Kafka Queue Size (Lag): {total_lag}")
#             return total_lag  # Return if successful

#         except NoBrokersAvailable:
#             print(f"⚠️ Kafka not available, retrying in 5s... ({i+1}/{retries})")
#             time.sleep(5)  # Wait before retrying

#     raise Exception("❌ Kafka is still not available after multiple retries")




import time
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.errors import NoBrokersAvailable, GroupCoordinatorNotAvailableError

def get_kafka_queue_size():
    BOOTSTRAP_SERVERS = "foundry-kafka:9092"  # Change this if needed
    CONSUMER_GROUP = "scrapy_group"
    TOPIC = "crawl_requests"

    retries = 10  # Number of retries
    for i in range(retries):
        try:
            print(f"🔄 Attempt {i+1}: Connecting to Kafka...")

            # Initialize Kafka Admin Client
            admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

            # Ensure consumer group is ready
            time.sleep(2)  # Give Kafka some time

            # Get committed offsets for the consumer group
            consumer_offsets = admin_client.list_consumer_group_offsets(CONSUMER_GROUP)

            # Create a KafkaConsumer to get latest offsets (log end offsets)
            consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)

            total_lag = 0
            for partition, offset_info in consumer_offsets.items():
                latest_offset = consumer.end_offsets([partition])[partition]  # Get latest offset
                committed_offset = offset_info.offset if offset_info.offset is not None else 0  # Get committed offset
                partition_lag = latest_offset - committed_offset  # Calculate lag
                total_lag += partition_lag
                print(f"✅ Partition {partition.partition}: Lag = {partition_lag}")

            print(f"✅ Total Kafka Queue Size (Lag): {total_lag}")
            return total_lag  # Return if successful

        except NoBrokersAvailable:
            print(f"⚠️ Kafka not available, retrying in 5s... ({i+1}/{retries})")
            time.sleep(5)  # Wait before retrying

        except GroupCoordinatorNotAvailableError:
            print(f"⚠️ GroupCoordinatorNotAvailableError, retrying in 5s... ({i+1}/{retries})")
            time.sleep(5)  # Wait before retrying

    raise Exception("❌ Kafka is still not available after multiple retries")




import requests

def scale_workers():
    # queue_size = get_queue_size()
    queue_size = get_kafka_queue_size()
    num_workers = queue_size // 5  # 1 worker per 5 requests
    requests.post("http://host.docker.internal:5001/scale", json={"num_workers": num_workers})



if __name__ == "__main__":
    while True:
        scale_workers()
        time.sleep(5)  # Check every 5 seconds