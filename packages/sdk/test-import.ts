// Quick test to verify SDK types are working
import { GroundedCounsellingClient, type User, type UserCreate } from './src/index';

// This file just tests that imports work correctly
// If this compiles, the SDK is properly set up

const client = new GroundedCounsellingClient('http://localhost:8000');

const userData: UserCreate = {
  email: 'test@example.com', 
  password: 'password123'
};

export { client, userData };