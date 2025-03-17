import os
import time
import subprocess
from kafka import KafkaConsumer
from termcolor import cprint

# Kafka Config
KAFKA_TOPIC = "crawl_requests"
KAFKA_BROKER = "localhost:9092"
KAFKA_GROUP_ID = "scrapy_group"

# Worker Scaling Config
MAX_QUEUE_SIZE = 5    # Spawn a new worker if pending messages > 5
MIN_QUEUE_SIZE = 1    # Kill a worker if pending messages < 1
MAX_WORKERS = 5       # Max allowed Scrapy workers

# Track worker processes
workers = []





def get_kafka_queue_size():
    from kafka import KafkaAdminClient, KafkaConsumer

    # Kafka details
    BOOTSTRAP_SERVERS = "localhost:9092"
    CONSUMER_GROUP = "scrapy_group"
    TOPIC = "crawl_requests"

    # Initialize Kafka Admin Client
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

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
        print(f"Partition {partition.partition}: Lag = {partition_lag}")

    print(f"Total Kafka Queue Size (Lag): {total_lag}")
    
    return total_lag
        
        
    
    
    
    
    
    
def get_kafka_queue_size1():
    """Fetch pending messages in Kafka topic."""
    try:
        cmd = f"docker exec -it kafka kafka-consumer-groups --bootstrap-server {KAFKA_BROKER} \
               --group {KAFKA_GROUP_ID} --describe"
        # cprint(f'\n\n{cmd=}',"yellow")
               
        output = subprocess.check_output(cmd, shell=True, text=True)
        # cprint(f'{output=}',"yellow")

        # Extract lag count from Kafka output
        for line in output.split("\n"):
            if KAFKA_TOPIC in line:
                # cprint(f'\n\n{line=}',"green")
                parts = line.split()
                cprint(f'\n\n{parts=}',"green")
                if "lag" in parts[-3].lower():
                    cprint(f'37',"red")
                    # cprint(f'\n\n{int(parts[-1])=}',"green")
                    return int(parts[-1])  # Last column is lag count

    except Exception as e:
        cprint(f"⚠️ Error fetching Kafka queue size: {e}", "red")
    
    return 0  # Default to 0 if error occurs

def start_worker():
    """Start a new Scrapy worker process."""
    if len(workers) >= MAX_WORKERS:
        cprint("⚠️ Max workers reached. Not spawning more.", "yellow")
        return
    
    cprint(f"🚀 Spawning new Scrapy worker - {len(workers)} 🟠...", "green")
    process = subprocess.Popen(["scrapy", "crawl", "101", "-s", "LOG_LEVEL=ERROR"])
    workers.append(process)

# def stop_worker():
#     """Kill the oldest worker process."""
#     if workers:
#         cprint(f"🛑 Stopping worker...{len(workers)}", "red")
#         worker = workers.pop(0)
#         worker.terminate()
#         worker.wait(timeout=10)  # Graceful shutdown


def stop_worker():
    """Kill the oldest worker process."""
    if workers:
        cprint(f"🛑 Stopping worker... {len(workers)}", "red")
        worker = workers.pop(0)

        worker.terminate()  # Send SIGTERM
        try:
            worker.wait(timeout=5)  # Wait for graceful shutdown
        except subprocess.TimeoutExpired:
            cprint("⚠️ Worker did not exit in time, forcing kill.", "yellow")
            worker.kill()  # Force kill if not exiting
            worker.wait()  # Ensure process is fully cleaned up


def clean_dead_workers():
    """Remove workers that have crashed or exited."""
    global workers
    workers = [w for w in workers if w.poll() is None]  # Keep only running processes

def manage_workers():
    """Main loop to monitor Kafka and scale workers."""
    while True:
        queue_size = get_kafka_queue_size()
        cprint(f"📊 Kafka Queue Size: {queue_size}", "blue")

        clean_dead_workers()  # Remove crashed workers

        if queue_size > MAX_QUEUE_SIZE:
            start_worker()
        
        if queue_size < MIN_QUEUE_SIZE and len(workers) > 1:
            stop_worker()

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    cprint("🔄 Worker Manager Started!", "cyan")
    manage_workers()


# ------


