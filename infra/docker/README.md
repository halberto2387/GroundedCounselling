# Docker Development Environment

This directory contains Docker configurations for the GroundedCounselling development environment.

## Quick Start

```bash
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## Services

### PostgreSQL (postgres)
- **Image**: postgres:15-alpine
- **Port**: 5432
- **Database**: grounded_counselling
- **Credentials**: postgres/postgres
- **Health Check**: Built-in pg_isready

### Redis (redis)
- **Image**: redis:7-alpine
- **Port**: 6379
- **Health Check**: Built-in redis-cli ping

### API (api)
- **Build**: Python 3.11 with FastAPI
- **Port**: 8000
- **Endpoints**:
  - Health: http://localhost:8000/health
  - API Docs: http://localhost:8000/docs
  - Root: http://localhost:8000/
- **Dependencies**: postgres, redis
- **Health Check**: curl to /health endpoint

### Worker (worker)
- **Build**: Python 3.11 with RQ
- **Purpose**: Background job processing
- **Dependencies**: redis
- **No exposed ports**: Internal service

### Web (web)
- **Build**: Node 20 with Next.js
- **Port**: 3000
- **Dependencies**: api
- **Status**: Basic Next.js app (in development)

## Environment Variables

Copy the example environment files:

```bash
cp .env.example .env
cp services/api/.env.example services/api/.env
cp apps/web/.env.example apps/web/.env
cp services/worker/.env.example services/worker/.env
```

## Development Commands

```bash
# Build specific service
docker compose build api

# Start specific services
docker compose up -d postgres redis

# Restart a service
docker compose restart api

# View service logs
docker compose logs api

# Execute commands in running container
docker compose exec api bash
docker compose exec postgres psql -U postgres -d grounded_counselling

# Remove all containers and volumes
docker compose down -v
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 5432, 6379, 8000 are available
2. **Build failures**: Check Docker logs and network connectivity
3. **Database connection**: Wait for health checks to pass before starting dependent services

### Health Checks

All services include health checks. Wait for services to show "healthy" status:

```bash
docker compose ps
```

### Service Dependencies

The compose file ensures proper startup order:
1. postgres, redis (start first)
2. api (waits for postgres and redis to be healthy)
3. worker (waits for redis to be healthy)
4. web (waits for api to start)

## Production Considerations

These Dockerfiles are optimized for production with:
- Multi-stage builds to reduce image size
- Non-root users for security
- Health checks for reliability
- Proper signal handling
- Optimized layer caching