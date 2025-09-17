````markdown
# API Documentation

Documentation for the GroundedCounselling API service.

## Overview

The GroundedCounselling API is built with FastAPI and provides comprehensive endpoints for managing users, specialists, bookings, and sessions in a mental health platform.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 7+

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

3. **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your database and API keys
```

4. **Run migrations:**

```bash
alembic upgrade head
```

5. **Start the server:**

```bash
uvicorn app.main:app --reload --port 8000
```

6. **Access the documentation:**
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## Authentication

The API uses JWT-based authentication with access and refresh tokens.

### Login Flow

1. **Login** - `POST /api/v1/auth/login`
   - Provide email and password
   - Receive access token (15 min) and refresh token (7 days)

2. **Use Access Token** - Include in Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

3. **Refresh Token** - `POST /api/v1/auth/refresh`
   - Provide refresh token when access token expires
   - Receive new access and refresh tokens

### Example Usage

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use authenticated endpoint
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer <access_token>"
```

## Core Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration  
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/change-password` - Change password

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (admin only)

### Specialists
- `GET /api/v1/specialists/` - List specialists
- `GET /api/v1/specialists/{specialist_id}` - Get specialist details
- `POST /api/v1/specialists/` - Create specialist profile
- `PUT /api/v1/specialists/{specialist_id}` - Update specialist profile

### Bookings
- `GET /api/v1/bookings/` - List user's bookings
- `POST /api/v1/bookings/` - Create new booking
- `GET /api/v1/bookings/{booking_id}` - Get booking details
- `PUT /api/v1/bookings/{booking_id}` - Update booking
- `DELETE /api/v1/bookings/{booking_id}` - Cancel booking

## Data Models

### User Model
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "role": "patient|counsellor|admin|super_admin",
  "is_active": true,
  "is_verified": true,
  "is_2fa_enabled": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Specialist Model
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "bio": "Professional biography",
  "specializations": ["Anxiety", "Depression"],
  "credentials": ["Ph.D. Psychology"],
  "languages": ["English", "Spanish"],
  "hourly_rate": 150.00,
  "is_available": true,
  "is_accepting_new_clients": true,
  "years_experience": 10,
  "average_rating": 4.8,
  "total_reviews": 25,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Booking Model
```json
{
  "id": "uuid",
  "client_id": "uuid",
  "specialist_id": "uuid", 
  "start_time": "2024-01-15T10:00:00Z",
  "duration_minutes": 60,
  "status": "pending|confirmed|cancelled|completed",
  "client_notes": "Looking forward to the session",
  "total_cost": 150.00,
  "is_paid": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Error Handling

The API returns standard HTTP status codes with JSON error responses:

### Error Response Format
```json
{
  "detail": "Error message description",
  "code": "ERROR_CODE", 
  "field": "field_name" // For validation errors
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default**: 60 requests per minute per IP
- **Authenticated**: Higher limits for authenticated users
- **Headers**: Rate limit info in response headers

### Rate Limit Headers
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

## Pagination

List endpoints support pagination with query parameters:

### Query Parameters
- `skip` - Number of records to skip (default: 0)
- `limit` - Maximum records to return (default: 20, max: 100)

### Response Format
```json
{
  "items": [...],
  "total": 150,
  "skip": 0,
  "limit": 20
}
```

## Filtering and Sorting

Many endpoints support filtering and sorting:

### Specialists Filtering
```bash
GET /api/v1/specialists/?specialization=Anxiety&is_available=true
```

### Bookings Filtering
```bash
GET /api/v1/bookings/?status=confirmed&start_date=2024-01-01
```

## WebSocket Support

Real-time features use WebSocket connections:

### Session Communication
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/session/{session_id}');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle real-time session updates
};
```

## Security

### HTTPS Only
- All production traffic must use HTTPS
- API redirects HTTP to HTTPS in production

### CORS Configuration
- Configured for specific origins
- Credentials included for authenticated requests

### Input Validation
- All inputs validated with Pydantic
- SQL injection prevention with parameterized queries
- XSS prevention with output encoding

### Audit Logging
- All API actions logged for compliance
- User actions tracked with IP and user agent
- Sensitive data redacted in logs

## Monitoring and Health

### Health Check
```bash
GET /health
```

Returns service status and dependencies:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "production",
  "dependencies": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

### Metrics Endpoint
```bash
GET /metrics  # Prometheus format
```

## SDK Generation

Automatically generate TypeScript SDK:

```bash
# From the API directory
npm run generate:sdk

# This creates TypeScript client in packages/sdk
```

### Using the Generated SDK

```typescript
import { GroundedCounsellingClient } from '@grounded-counselling/sdk';

const client = new GroundedCounsellingClient('http://localhost:8000');

// Login
const { access_token } = await client.login('user@example.com', 'password');
client.setAuthToken(access_token);

// Get current user
const user = await client.getCurrentUser();

// List specialists
const specialists = await client.getSpecialists({ 
  specialization: 'Anxiety' 
});
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Database Operations

```bash
# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback migration  
alembic downgrade -1

# View migration history
alembic history
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

## Deployment

### Environment Variables

Required environment variables for production:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379/0

# JWT Secrets (generate secure values)
JWT_SECRET=your-secret-key
JWT_REFRESH_SECRET=your-refresh-secret

# External APIs
RESEND_API_KEY=your-resend-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### Docker Deployment

```bash
# Build image
docker build -f ../../infra/docker/api.Dockerfile -t gc-api .

# Run container
docker run -p 8000:8000 --env-file .env gc-api
```

### Production Checklist

- [ ] Set strong JWT secrets
- [ ] Configure production database
- [ ] Set up Redis for caching
- [ ] Configure external API keys
- [ ] Set up monitoring (Sentry)
- [ ] Configure CORS origins
- [ ] Set up SSL/TLS
- [ ] Configure rate limiting
- [ ] Set up backups
- [ ] Configure log aggregation

## Support

### Getting Help

- **Documentation**: This file and inline code documentation
- **API Docs**: Interactive documentation at `/docs`
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

### Troubleshooting

Common issues and solutions:

#### Database Connection Issues
```bash
# Check database connectivity
python -c "from app.db.session import engine; print('DB connected')"

# Verify migrations
alembic current
```

#### Authentication Issues
```bash
# Test JWT token generation
python -c "from app.core.security import create_access_token; print(create_access_token({'sub': 'test'}))"
```

#### Redis Connection Issues
```bash
# Test Redis connectivity
python -c "import redis; r=redis.from_url('redis://localhost:6379'); r.ping()"
```

---

**Version**: 1.0  
**Last Updated**: January 2024  
**Team**: Backend Engineering
````