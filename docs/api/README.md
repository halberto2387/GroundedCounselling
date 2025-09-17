# API Documentation

## Overview

The GroundedCounselling API is a FastAPI-based backend service that provides secure, HIPAA-compliant endpoints for managing counselling practice operations.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Local Development with Docker

The easiest way to run the API locally is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/halberto2387/GroundedCounselling.git
cd GroundedCounselling

# Copy environment variables
cp services/api/.env.example services/api/.env
cp apps/web/.env.example apps/web/.env
cp services/worker/.env.example services/worker/.env

# Start all services
docker-compose -f infra/docker/docker-compose.yml up -d

# Check service health
docker-compose -f infra/docker/docker-compose.yml ps
```

The API will be available at:
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Manual Development Setup

If you prefer to run the API outside of Docker:

```bash
# Navigate to API directory
cd services/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install uv
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local configuration

# Start database and Redis (if not using Docker)
docker-compose -f ../../infra/docker/docker-compose.yml up -d postgres redis

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

The API requires several environment variables. Copy `services/api/.env.example` to `services/api/.env` and configure:

### Required Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_REFRESH_SECRET`: Secret key for refresh tokens

### Optional Variables
- `RESEND_API_KEY`: For email notifications
- `TWILIO_*`: For SMS notifications
- `STRIPE_*`: For payment processing
- `AWS_*`: For file storage

## Docker Configuration

The API includes a multi-stage Dockerfile optimized for production:

```dockerfile
# Build and run with Docker
docker build -f infra/docker/api.Dockerfile -t grounded-api .
docker run -p 8000:8000 --env-file services/api/.env grounded-api
```

### Docker Compose Services

The `docker-compose.yml` includes:

- **postgres**: PostgreSQL 15 with health checks
- **redis**: Redis 7 for caching and job queues
- **api**: FastAPI application
- **worker**: Background job processor
- **web**: Next.js frontend

### Health Checks

The API container includes health checks:

```bash
# Check API health
curl http://localhost:8000/health

# Docker health status
docker-compose -f infra/docker/docker-compose.yml ps
```

## Development Workflow

### Database Migrations

```bash
# Create a new migration
cd services/api
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Testing

```bash
# Run tests
cd services/api
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Linting with ruff
ruff check .

# Formatting with black
black .

# Type checking with mypy
mypy .
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile
- `DELETE /api/v1/users/me` - Delete user account

### Specialists
- `GET /api/v1/specialists` - List specialists
- `GET /api/v1/specialists/{id}` - Get specialist details
- `POST /api/v1/specialists` - Create specialist profile
- `PUT /api/v1/specialists/{id}` - Update specialist profile

### Bookings
- `GET /api/v1/bookings` - List user bookings
- `POST /api/v1/bookings` - Create new booking
- `GET /api/v1/bookings/{id}` - Get booking details
- `PUT /api/v1/bookings/{id}` - Update booking
- `DELETE /api/v1/bookings/{id}` - Cancel booking

For complete API documentation, visit http://localhost:8000/docs when running the server.

## Security Considerations

- All endpoints require proper authentication except registration and login
- JWT tokens expire after 15 minutes (configurable)
- Refresh tokens are rotated on each use
- Rate limiting is applied to prevent abuse
- All sensitive data is encrypted at rest and in transit
- CORS is configured for the frontend domain only

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Ensure PostgreSQL is running and accessible
   - Check DATABASE_URL environment variable
   - Verify database exists and migrations are applied

2. **Redis connection errors**
   - Ensure Redis is running and accessible
   - Check REDIS_URL environment variable

3. **Import errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify virtual environment is activated

### Logs and Debugging

```bash
# View API logs
docker-compose -f infra/docker/docker-compose.yml logs api

# Debug with interactive Python
cd services/api
python -c "from app.main import app; print('API loaded successfully')"
```

## Contributing

1. Create a feature branch from `develop`
2. Make your changes following the coding standards
3. Add tests for new functionality
4. Run the full test suite
5. Update documentation as needed
6. Submit a pull request

See the main [Contributing Guidelines](../../.github/CONTRIBUTING.md) for more details.