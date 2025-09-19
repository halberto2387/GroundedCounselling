import { GroundedCounsellingClient, type UserCreate, type SpecialistCreate, type BookingCreate } from './index';

/**
 * Example usage of the GroundedCounselling SDK
 * This demonstrates the basic workflow for using the API client
 */
export async function exampleUsage() {
  // Initialize the client with the API base URL
  const client = new GroundedCounsellingClient('http://localhost:8000');

  try {
    // 1. Health Check
    const health = await client.health();
    return { success: true, health };

  } catch (error) {
    return { success: false, error };
  }
}

/**
 * Example data structures
 */
export const exampleUserData: UserCreate = {
  email: 'therapist@example.com',
  password: 'SecurePassword123!'
};

export const exampleSpecialistData: SpecialistCreate = {
  bio: 'Licensed therapist specializing in anxiety and depression.',
  specializations: ['Anxiety', 'Depression', 'CBT'],
  hourly_rate: 120.50,
  years_experience: 8,
  is_available: true
};

export const exampleBookingData: BookingCreate = {
  specialist_id: 123,
  start_time: '2024-01-15T10:00:00',
  duration_minutes: 60,
  notes: 'First therapy session'
};

/**
 * Example usage patterns
 */
export const usageExamples = {
  // Basic client setup
  setup: `
import { GroundedCounsellingClient } from '@grounded-counselling/sdk';
const client = new GroundedCounsellingClient('http://localhost:8000');
`,

  // Authentication flow
  auth: `
// Register user
const user = await client.register({
  email: 'user@example.com',
  password: 'password123'
});

// Login
const loginResult = await client.login('user@example.com', 'password123');
client.setAuthToken(loginResult.access_token);
`,

  // Specialist operations
  specialist: `
// Get specialists with filters
const specialists = await client.getSpecialists({
  limit: 10,
  specialization: 'Anxiety'
});

// Get specific specialist
const specialist = await client.getSpecialist('123');
`,

  // Booking operations
  booking: `
// Create booking
const booking = await client.createBooking({
  specialist_id: 123,
  start_time: '2024-01-15T10:00:00',
  duration_minutes: 60,
  notes: 'Therapy session'
});

// Get user bookings
const bookings = await client.getBookings({ status: 'confirmed' });
`
};