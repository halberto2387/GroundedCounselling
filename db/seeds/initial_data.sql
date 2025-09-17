-- Sample data for GroundedCounselling platform
-- This file contains seed data for development and testing

-- Insert sample users
INSERT INTO users (
    id, 
    email, 
    hashed_password, 
    first_name, 
    last_name, 
    phone, 
    role, 
    is_active, 
    is_verified,
    created_at,
    updated_at
) VALUES 
-- Admin user
(
    'admin-user-id-1234567890',
    'admin@groundedcounselling.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYMeAOm.6VKhAWO', -- password: admin123
    'Admin',
    'User',
    '+1234567890',
    'ADMIN',
    true,
    true,
    NOW(),
    NOW()
),
-- Sample counsellor
(
    'counsellor-user-id-1234567890',
    'dr.smith@groundedcounselling.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYMeAOm.6VKhAWO', -- password: counsellor123
    'Dr. Jane',
    'Smith',
    '+1234567891',
    'COUNSELLOR',
    true,
    true,
    NOW(),
    NOW()
),
-- Sample patient
(
    'patient-user-id-1234567890',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYMeAOm.6VKhAWO', -- password: patient123
    'John',
    'Doe',
    '+1234567892',
    'PATIENT',
    true,
    true,
    NOW(),
    NOW()
);

-- Insert specialist profile for the counsellor
INSERT INTO specialists (
    id,
    user_id,
    bio,
    specializations,
    credentials,
    languages,
    hourly_rate,
    is_available,
    is_accepting_new_clients,
    years_experience,
    total_sessions,
    average_rating,
    total_reviews,
    license_number,
    license_state,
    education,
    created_at,
    updated_at
) VALUES (
    'specialist-id-1234567890',
    'counsellor-user-id-1234567890',
    'Dr. Jane Smith is a licensed clinical psychologist with over 10 years of experience helping individuals overcome anxiety, depression, and trauma. She specializes in cognitive-behavioral therapy (CBT) and mindfulness-based interventions.',
    ARRAY['Anxiety', 'Depression', 'PTSD', 'CBT', 'Mindfulness'],
    ARRAY['Ph.D. in Clinical Psychology', 'Licensed Clinical Psychologist', 'Certified CBT Therapist'],
    ARRAY['English', 'Spanish'],
    150.00,
    true,
    true,
    10,
    0,
    NULL,
    0,
    'PSY12345',
    'CA',
    'Ph.D. in Clinical Psychology from UCLA, M.A. in Psychology from USC',
    NOW(),
    NOW()
);

-- Insert availability for the specialist
INSERT INTO availability (
    id,
    specialist_id,
    day_of_week,
    start_time,
    end_time,
    is_active,
    is_recurring,
    created_at,
    updated_at
) VALUES 
-- Monday
(
    gen_random_uuid(),
    'specialist-id-1234567890',
    0, -- Monday
    '09:00:00',
    '17:00:00',
    true,
    true,
    NOW(),
    NOW()
),
-- Tuesday
(
    gen_random_uuid(),
    'specialist-id-1234567890',
    1, -- Tuesday
    '09:00:00',
    '17:00:00',
    true,
    true,
    NOW(),
    NOW()
),
-- Wednesday
(
    gen_random_uuid(),
    'specialist-id-1234567890',
    2, -- Wednesday
    '09:00:00',
    '17:00:00',
    true,
    true,
    NOW(),
    NOW()
),
-- Thursday
(
    gen_random_uuid(),
    'specialist-id-1234567890',
    3, -- Thursday
    '09:00:00',
    '17:00:00',
    true,
    true,
    NOW(),
    NOW()
),
-- Friday
(
    gen_random_uuid(),
    'specialist-id-1234567890',
    4, -- Friday
    '09:00:00',
    '15:00:00',
    true,
    true,
    NOW(),
    NOW()
);

-- Insert a sample booking
INSERT INTO bookings (
    id,
    client_id,
    specialist_id,
    start_time,
    duration_minutes,
    status,
    client_notes,
    specialist_notes,
    hourly_rate,
    total_cost,
    is_paid,
    created_at,
    updated_at,
    confirmed_at
) VALUES (
    'booking-id-1234567890',
    'patient-user-id-1234567890',
    'specialist-id-1234567890',
    NOW() + INTERVAL '7 days',
    60,
    'CONFIRMED',
    'Looking forward to discussing my anxiety management strategies.',
    'Initial consultation - focus on assessment and goal setting.',
    150.00,
    150.00,
    true,
    NOW(),
    NOW(),
    NOW()
);

-- Insert a sample session for the booking
INSERT INTO sessions (
    id,
    booking_id,
    status,
    video_room_id,
    recording_consent,
    created_at,
    updated_at
) VALUES (
    'session-id-1234567890',
    'booking-id-1234567890',
    'SCHEDULED',
    'room-' || EXTRACT(EPOCH FROM NOW())::bigint,
    false,
    NOW(),
    NOW()
);

-- Insert audit log entry
INSERT INTO audit_logs (
    id,
    user_id,
    action,
    resource_type,
    resource_id,
    ip_address,
    user_agent,
    new_values,
    created_at
) VALUES (
    gen_random_uuid(),
    'admin-user-id-1234567890',
    'system.seed',
    'Database',
    'initial_seed',
    '127.0.0.1',
    'Seed Script',
    '{"message": "Initial seed data created", "tables": ["users", "specialists", "availability", "bookings", "sessions"]}',
    NOW()
);