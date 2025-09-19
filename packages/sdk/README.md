# GroundedCounselling SDK

A TypeScript SDK for the GroundedCounselling API - a secure, HIPAA-compliant platform for counselling practice management.

## Installation

```bash
npm install @grounded-counselling/sdk
# or
yarn add @grounded-counselling/sdk
# or
pnpm add @grounded-counselling/sdk
```

## Quick Start

```typescript
import { GroundedCounsellingClient } from '@grounded-counselling/sdk';

// Initialize the client
const client = new GroundedCounsellingClient('http://localhost:8000');

// Test connectivity
const health = await client.health();
console.log('API Status:', health);
```

## Authentication

### User Registration

```typescript
import { type UserCreate } from '@grounded-counselling/sdk';

const userData: UserCreate = {
  email: 'therapist@example.com',
  password: 'SecurePassword123!'
};

const user = await client.register(userData);
console.log('Registered user:', user);
```

### Login & Token Management

```typescript
// Login
const loginResult = await client.login('therapist@example.com', 'SecurePassword123!');

// Set authentication token for future requests
client.setAuthToken(loginResult.access_token);

// Get current user info
const currentUser = await client.getCurrentUser();

// Remove token (logout)
client.removeAuthToken();
```

## Specialist Management

### Create Specialist Profile

```typescript
import { type SpecialistCreate } from '@grounded-counselling/sdk';

const specialistData: SpecialistCreate = {
  bio: 'Licensed therapist specializing in anxiety and depression.',
  specializations: ['Anxiety', 'Depression', 'CBT'],
  hourly_rate: 120.50,
  years_experience: 8,
  is_available: true,
  license_number: 'LIC123456'
};

const specialist = await client.createSpecialistProfile(specialistData);
```

### Find Specialists

```typescript
// Get all specialists with pagination
const specialists = await client.getSpecialists({
  skip: 0,
  limit: 10
});

// Search specialists by specialization
const anxietySpecialists = await client.getSpecialists({
  specialization: 'Anxiety',
  limit: 5
});

// Get specific specialist
const specialist = await client.getSpecialist('123');
```

## Booking Management

### Create Booking

```typescript
import { type BookingCreate } from '@grounded-counselling/sdk';

const bookingData: BookingCreate = {
  specialist_id: 123,
  start_time: '2024-01-15T10:00:00',
  duration_minutes: 60,
  notes: 'First therapy session'
};

const booking = await client.createBooking(bookingData);
```

### Manage Bookings

```typescript
// Get user's bookings
const myBookings = await client.getBookings({
  status: 'confirmed',
  limit: 20
});

// Get specific booking
const booking = await client.getBooking('456');

// Update booking
const updatedBooking = await client.updateBooking('456', {
  notes: 'Updated session notes'
});

// Cancel booking
await client.cancelBooking('456');
```

## Session Management

### Create Session

```typescript
import { type SessionCreate } from '@grounded-counselling/sdk';

const sessionData: SessionCreate = {
  booking_id: 456,
  session_notes: 'Patient showed significant improvement...',
  homework_assigned: 'Practice breathing exercises daily'
};

const session = await client.createSession(sessionData);
```

## Availability Management

### Set Specialist Availability

```typescript
import { type AvailabilityCreate } from '@grounded-counselling/sdk';

const availability: AvailabilityCreate = {
  day_of_week: 'MONDAY',
  start_time: '09:00:00',
  end_time: '17:00:00',
  is_available: true
};

const schedule = await client.createAvailability(availability);
```

## Error Handling

```typescript
try {
  const user = await client.getCurrentUser();
} catch (error) {
  if (error.response?.status === 401) {
    console.log('Authentication required');
    // Redirect to login
  } else if (error.response?.status === 404) {
    console.log('Resource not found');
  } else {
    console.error('API Error:', error.message);
  }
}
```

## TypeScript Types

The SDK provides comprehensive TypeScript types for all API operations:

```typescript
import {
  type User,
  type UserCreate,
  type Specialist,
  type SpecialistCreate,
  type Booking,
  type BookingCreate,
  type Session,
  type SessionCreate,
  type Availability,
  type AvailabilityCreate,
  type paths,  // All API paths
  type components  // All schemas
} from '@grounded-counselling/sdk';
```

## Configuration

### Custom Base URL

```typescript
const client = new GroundedCounsellingClient('https://api.groundedcounselling.com');
```

### Custom Axios Configuration

```typescript
const client = new GroundedCounsellingClient('http://localhost:8000', {
  timeout: 10000,
  headers: {
    'X-Custom-Header': 'value'
  }
});
```

### Custom Requests

```typescript
// For endpoints not covered by the client methods
const customResponse = await client.request({
  method: 'GET',
  url: '/api/v1/custom-endpoint',
  params: { custom: 'param' }
});
```

## API Reference

### Client Methods

- `health()` - Check API health status
- `register(userData)` - Register new user
- `login(email, password)` - User login
- `refreshToken(token)` - Refresh access token
- `logout()` - User logout
- `getCurrentUser()` - Get current user info
- `updateProfile(data)` - Update user profile
- `getSpecialists(params?)` - List specialists
- `getSpecialist(id)` - Get specific specialist
- `createSpecialistProfile(data)` - Create specialist profile
- `createBooking(data)` - Create new booking
- `getBookings(params?)` - List bookings
- `getBooking(id)` - Get specific booking
- `updateBooking(id, data)` - Update booking
- `cancelBooking(id)` - Cancel booking
- `createSession(data)` - Create session record
- `createAvailability(data)` - Set availability

### Authentication Methods

- `setAuthToken(token)` - Set bearer token
- `removeAuthToken()` - Remove authentication

### Generic Request Method

- `request(config)` - Make custom API requests

## Development

### Building the SDK

```bash
pnpm build
```

### Generating Types

```bash
pnpm run generate
```

This will regenerate TypeScript types from the latest OpenAPI specification.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@groundedcounselling.com or open an issue on GitHub.