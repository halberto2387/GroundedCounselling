# Background Worker for GroundedCounselling

A Redis Queue (RQ) based background worker for handling asynchronous tasks in the GroundedCounselling platform.

## Features

- **Email Tasks** - Send emails via Resend API
- **SMS Tasks** - Send SMS messages via Twilio
- **Notification Tasks** - Multi-channel notifications
- **Report Generation** - Analytics and performance reports
- **Structured Logging** - JSON logging with structlog
- **Error Tracking** - Sentry integration
- **Graceful Shutdown** - Signal handling for clean worker shutdown

## Quick Start

### Prerequisites

- Python 3.11+
- Redis server
- Resend API key (for emails)
- Twilio credentials (for SMS)

### Installation

1. **Create virtual environment:**

```bash
cd services/worker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -e ".[dev]"
```

3. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your Redis URL and API credentials
```

### Running the Worker

```bash
# Start the worker
python worker/main.py

# Or with specific environment
ENVIRONMENT=production python worker/main.py
```

## Task Queues

The worker processes tasks from multiple queues:

- **default** - General purpose tasks
- **email** - Email sending tasks
- **sms** - SMS sending tasks  
- **notifications** - Multi-channel notifications
- **reports** - Report generation tasks

## Available Tasks

### Email Tasks

```python
from worker.tasks.email import send_email, send_welcome_email

# Send generic email
result = send_email(
    to_email="user@example.com",
    subject="Test Email",
    html_content="<h1>Hello!</h1>",
)

# Send welcome email
result = send_welcome_email(
    user_email="newuser@example.com",
    user_name="John Doe",
)
```

### SMS Tasks

```python
from worker.tasks.sms import send_sms, send_2fa_code_sms

# Send SMS
result = send_sms(
    phone_number="+1234567890",
    message="Hello from GroundedCounselling!",
)

# Send 2FA code
result = send_2fa_code_sms(
    phone_number="+1234567890",
    code="123456",
)
```

### Notification Tasks

```python
from worker.tasks.notifications import send_booking_notifications

# Send booking confirmation
result = send_booking_notifications(
    user_data={"email": "user@example.com", "name": "John", "phone": "+1234567890"},
    booking_data={"id": "booking-123", "specialist_name": "Dr. Smith", "start_time": "2024-01-15 10:00"},
    notification_preferences={"email": True, "sms": True},
)
```

### Report Tasks

```python
from worker.tasks.reports import generate_specialist_performance_report
from datetime import datetime

# Generate specialist report
result = generate_specialist_performance_report(
    specialist_id="specialist-123",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31),
)
```

## Enqueueing Tasks

Tasks can be enqueued from the main application:

```python
import redis
from rq import Queue

# Connect to Redis
redis_conn = redis.from_url("redis://localhost:6379/0")

# Create queue
email_queue = Queue("email", connection=redis_conn)

# Enqueue task
job = email_queue.enqueue(
    "worker.tasks.email.send_welcome_email",
    user_email="newuser@example.com",
    user_name="John Doe",
)
```

## Configuration

### Environment Variables

- `REDIS_URL` - Redis connection URL
- `RESEND_API_KEY` - Resend API key for emails
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_PHONE_NUMBER` - Twilio phone number
- `SENTRY_DSN` - Sentry DSN for error tracking
- `ENVIRONMENT` - Environment (development/production)
- `DEBUG` - Debug mode flag
- `LOG_LEVEL` - Logging level

### Worker Configuration

- `WORKER_NAME` - Worker instance name
- `WORKER_QUEUES` - Comma-separated list of queues to process

## Monitoring

### Worker Dashboard

RQ provides a web dashboard for monitoring:

```bash
pip install rq-dashboard
rq-dashboard --redis-url redis://localhost:6379/0
```

Access at http://localhost:9181

### Logging

All tasks log structured JSON output:

```json
{
  "event": "Email sent successfully",
  "level": "info",
  "timestamp": "2024-01-01T12:00:00Z",
  "email_id": "msg_123",
  "logger": "worker.tasks.email"
}
```

### Error Tracking

Errors are automatically reported to Sentry when configured.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black worker/ tests/

# Lint code  
ruff worker/ tests/

# Type checking
mypy worker/
```

## Deployment

### Production Considerations

1. **Multiple Workers** - Run multiple worker processes for scalability
2. **Process Manager** - Use supervisord or systemd for process management
3. **Health Checks** - Monitor worker health and queue lengths
4. **Error Handling** - Ensure robust error handling and retries
5. **Resource Limits** - Set appropriate memory and CPU limits

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY worker/ worker/
CMD ["python", "worker/main.py"]
```

### Scaling

- Run multiple worker processes
- Use different queues for task prioritization
- Monitor queue lengths and scale accordingly
- Consider using RQ Scheduler for periodic tasks

## License

Apache License 2.0 - See the [LICENSE](../../LICENSE) file for details.