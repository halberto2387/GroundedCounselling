// Export the main client
export { GroundedCounsellingClient } from './client';
export { default } from './client';

// Export types
export * from './types';

// Type aliases for easier use
import type { components } from './types';

export type User = components['schemas']['UserOut'];
export type UserCreate = components['schemas']['UserCreate'];
export type Specialist = components['schemas']['SpecialistOut'];
export type SpecialistCreate = components['schemas']['SpecialistCreate'];
export type Booking = components['schemas']['BookingOut'];
export type BookingCreate = components['schemas']['BookingCreate'];
export type Session = components['schemas']['SessionOut'];
export type SessionCreate = components['schemas']['SessionCreate'];
export type Availability = components['schemas']['AvailabilityOut'];
export type AvailabilityCreate = components['schemas']['AvailabilityCreate'];