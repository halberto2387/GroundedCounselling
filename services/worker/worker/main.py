"""
Minimal RQ Worker implementation for GroundedCounselling.
This is a placeholder implementation for Docker testing.
"""

import os
import time
import redis
from rq import Worker, Queue

def main():
    """Main worker function"""
    print("Starting GroundedCounselling Worker...")
    
    # Connect to Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_conn = redis.from_url(redis_url)
    
    # Create queues
    queues = [Queue('default', connection=redis_conn)]
    
    print(f"Connected to Redis: {redis_url}")
    print(f"Listening on queues: {[q.name for q in queues]}")
    
    # Start worker
    worker = Worker(queues, connection=redis_conn)
    worker.work()

if __name__ == "__main__":
    main()