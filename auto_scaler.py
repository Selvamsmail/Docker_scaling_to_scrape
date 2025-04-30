import docker
import pika
import time

RABBIT_HOST = 'localhost'  # Must match container name or DNS name in Docker network
QUEUE_NAME = 'url_queue'
MAX_WORKERS = 3
MIN_WORKERS = 500
URLS_PER_WORKER = 1  # Change based on how heavy the jobs are
IMAGE_NAME = 'my-python-worker'
NETWORK_NAME = 'scraper-net'

client = docker.from_env()

def get_queue_length():
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = conn.channel()
    q = channel.queue_declare(queue=QUEUE_NAME, durable=True, passive=True)
    conn.close()
    return q.method.message_count

def get_active_workers():
    return [c for c in client.containers.list() if IMAGE_NAME in c.image.tags]

def scale_workers(target_count):
    current = get_active_workers()
    diff = target_count - len(current)
    
    if diff > 0:
        timestamp = int(time.time())
        for i in range(diff):
            container_name = f"worker_{timestamp}_{i}"
            client.containers.run(
                IMAGE_NAME,
                name=container_name,
                network=NETWORK_NAME,
                detach=True
            )
            print(f"Started {container_name}")
    elif diff < 0:
        for c in current[:abs(diff)]:
            c.kill()
            c.remove()
            print(f"Stopped {c.name}")

def main():
    while True:
        queue_size = get_queue_length()
        target_workers = min(MAX_WORKERS, max(MIN_WORKERS, (queue_size // URLS_PER_WORKER) + 1))
        print(f"Queue size: {queue_size}, Target workers: {target_workers}")
        scale_workers(target_workers)
        time.sleep(10)

if __name__ == "__main__":
    main()
