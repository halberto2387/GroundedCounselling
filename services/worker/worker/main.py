import os
import signal
import sys
from typing import List

import redis
from rq import Worker, Queue, Connection
from rq.job import Job

from worker.config import settings
from worker.tasks import email, sms, notifications, reports
from worker.logging_setup import setup_logging, get_logger

logger = get_logger(__name__)


def create_queues() -> List[Queue]:
    """Create RQ queues."""
    redis_conn = redis.from_url(settings.REDIS_URL)
    
    queues = []
    for queue_name in settings.WORKER_QUEUES:
        queue = Queue(queue_name, connection=redis_conn)
        queues.append(queue)
        logger.info(f"Created queue: {queue_name}")
    
    return queues


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)


def main():
    """Main worker entry point."""
    # Set up logging
    setup_logging()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info(f"Starting {settings.WORKER_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Redis URL: {settings.REDIS_URL}")
    logger.info(f"Queues: {', '.join(settings.WORKER_QUEUES)}")
    
    # Create Redis connection
    redis_conn = redis.from_url(settings.REDIS_URL)
    
    # Create queues
    queues = create_queues()
    
    # Test Redis connection
    try:
        redis_conn.ping()
        logger.info("Redis connection successful")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # Create and start worker
    try:
        with Connection(redis_conn):
            worker = Worker(
                queues,
                name=settings.WORKER_NAME,
                log_job_description=settings.DEBUG,
            )
            
            logger.info("Worker started, waiting for jobs...")
            worker.work()
            
    except KeyboardInterrupt:
        logger.info("Worker interrupted, shutting down...")
    except Exception as e:
        logger.error(f"Worker error: {e}")
        sys.exit(1)
    finally:
        logger.info("Worker shutdown complete")


if __name__ == "__main__":
    main()