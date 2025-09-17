# Docker Infrastructure for GroundedCounselling

This directory contains Docker configuration for the GroundedCounselling platform.

## Services

### Core Services

- **postgres** - PostgreSQL 15 database
- **redis** - Redis 7 for caching and job queues
- **api** - FastAPI backend service
- **worker** - RQ background worker

### Optional Services

- **web** - Next.js frontend (uncomment when ready)

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running the Development Environment

1. **Start all services:**

```bash
cd infra/docker
docker-compose up -d
```

2. **View logs:**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

3. **Run database migrations:**

```bash
# Access the API container
docker-compose exec api bash

# Run migrations
alembic upgrade head
```

4. **Stop services:**

```bash
docker-compose down
```

## Service Configuration

### Database (PostgreSQL)

- **Port**: 5432
- **Database**: grounded_counselling
- **Username**: postgres
- **Password**: postgres
- **Data Volume**: postgres_data

### Cache (Redis)

- **Port**: 6379
- **Data Volume**: redis_data
- **Persistence**: AOF enabled

### API (FastAPI)

- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Environment**: Development

### Worker (RQ)

- **Queues**: default, email, sms, notifications, reports
- **Dashboard**: Install rq-dashboard for monitoring

## Development Workflow

### Starting Services

```bash
# Start core services only
docker-compose up -d postgres redis

# Start all services
docker-compose up -d
```

### Database Operations

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d grounded_counselling

# Run migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Description"
```

### Worker Operations

```bash
# View worker logs
docker-compose logs -f worker

# Access worker container
docker-compose exec worker bash

# Test task execution
docker-compose exec worker python -c "from worker.tasks.email import send_email; print('Worker ready')"
```

### API Operations

```bash
# View API logs
docker-compose logs -f api

# Access API container
docker-compose exec api bash

# Run tests
docker-compose exec api pytest

# Check API health
curl http://localhost:8000/health
```

## Production Considerations

### Security

1. **Change default passwords**
2. **Use environment files for secrets**
3. **Enable SSL/TLS termination**
4. **Configure firewall rules**
5. **Use non-root users in containers**

### Performance

1. **Resource limits** - Set CPU and memory limits
2. **Connection pooling** - Configure database connection pools
3. **Caching** - Optimize Redis configuration
4. **Load balancing** - Use nginx or similar for API load balancing

### Monitoring

1. **Health checks** - All services have health checks
2. **Logs** - Centralized logging with structured output
3. **Metrics** - Consider adding Prometheus/Grafana
4. **Alerts** - Set up monitoring alerts

## Customization

### Environment Variables

Create `.env` files for each service:

```bash
# services/api/.env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/grounded_counselling
REDIS_URL=redis://redis:6379/0
JWT_SECRET=your-production-secret
# ... other variables

# services/worker/.env
REDIS_URL=redis://redis:6379/0
RESEND_API_KEY=your-resend-key
TWILIO_ACCOUNT_SID=your-twilio-sid
# ... other variables
```

### Volume Mounts

For development, source code is mounted as volumes:

```yaml
volumes:
  - ../services/api:/app  # Live reload for API
  - ../services/worker:/app  # Live reload for worker
```

For production, remove volume mounts and use built images.

### Network Configuration

All services run on the `gc-network` bridge network for inter-service communication.

## Troubleshooting

### Common Issues

1. **Port conflicts** - Change exposed ports if needed
2. **Permission issues** - Ensure proper file permissions
3. **Database connection** - Check DATABASE_URL configuration
4. **Redis connection** - Verify REDIS_URL configuration

### Debugging

```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs [service-name]

# Access service shell
docker-compose exec [service-name] bash

# Restart specific service
docker-compose restart [service-name]

# Rebuild service
docker-compose build [service-name]
```

### Health Checks

All services include health checks:

```bash
# Check all health statuses
docker-compose ps

# Manual health check
curl http://localhost:8000/health  # API
docker-compose exec postgres pg_isready -U postgres  # PostgreSQL
docker-compose exec redis redis-cli ping  # Redis
```

## License

Apache License 2.0