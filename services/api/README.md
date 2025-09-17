# FastAPI Backend for GroundedCounselling

A production-ready FastAPI backend with async SQLAlchemy, JWT authentication, and comprehensive API documentation.

## Features

- **FastAPI** with async/await support
- **SQLAlchemy 2.0** with async sessions
- **Alembic** for database migrations
- **JWT Authentication** with refresh tokens
- **Role-based Access Control (RBAC)**
- **Comprehensive API Documentation** with OpenAPI
- **Rate Limiting** with SlowAPI
- **Structured Logging** with structlog
- **Error Tracking** with Sentry
- **Testing** with pytest and async support

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis

### Installation

1. **Create virtual environment:**

```bash
cd services/api
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
# Edit .env with your database and other configuration
```

4. **Run database migrations:**

```bash
alembic upgrade head
```

5. **Start the development server:**

```bash
uvicorn app.main:app --reload --port 8000
```

6. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff app/ tests/

# Type checking
mypy app/
```

### Database Operations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## API Structure

### Authentication Endpoints

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/change-password` - Change password

### User Endpoints

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (admin only)

### Specialist Endpoints

- `GET /api/v1/specialists/` - List specialists
- `GET /api/v1/specialists/{specialist_id}` - Get specialist details
- `POST /api/v1/specialists/` - Create specialist profile
- `PUT /api/v1/specialists/{specialist_id}` - Update specialist profile

### Booking Endpoints

- `GET /api/v1/bookings/` - List user's bookings
- `POST /api/v1/bookings/` - Create new booking
- `GET /api/v1/bookings/{booking_id}` - Get booking details
- `PUT /api/v1/bookings/{booking_id}` - Update booking
- `DELETE /api/v1/bookings/{booking_id}` - Cancel booking

## Database Models

### Core Models

- **User** - Authentication and basic profile
- **Specialist** - Counsellor profiles and professional information
- **Booking** - Session bookings and scheduling
- **Session** - Actual counselling sessions
- **Availability** - Specialist availability schedules
- **AuditLog** - System activity tracking

## Security Features

### Authentication

- JWT access tokens (15 minutes default)
- JWT refresh tokens (1 week default)
- Password hashing with bcrypt
- 2FA support (TOTP ready)

### Authorization

- Role-based access control (Patient, Counsellor, Admin, Super Admin)
- Permission-based resource access
- User context isolation

### Security Headers

- CORS configuration
- Trusted host middleware
- Rate limiting (60 requests/minute default)

## Configuration

All configuration is handled through environment variables. See `.env.example` for available options.

### Key Settings

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Secret for signing access tokens
- `JWT_REFRESH_SECRET` - Secret for signing refresh tokens
- `SENTRY_DSN` - Sentry error tracking DSN

## Deployment

### Production Checklist

1. Set strong JWT secrets
2. Configure production database
3. Set up Redis for caching
4. Configure Sentry for error tracking
5. Set environment to "production"
6. Configure CORS origins
7. Set up SSL/TLS termination

### Environment Variables

Ensure all required environment variables are set for production deployment.

## Contributing

1. Follow PEP 8 style guidelines
2. Write tests for new features
3. Update documentation as needed
4. Use type hints consistently
5. Follow conventional commit messages

## License

Apache License 2.0 - See the [LICENSE](../../LICENSE) file for details.