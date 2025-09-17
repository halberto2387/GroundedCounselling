-- Initialize database for GroundedCounselling
-- This script is run when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if it doesn't exist (though it should be created by POSTGRES_DB)
-- SELECT 'CREATE DATABASE grounded_counselling' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'grounded_counselling')\gexec

-- Set timezone
SET timezone = 'UTC';

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'GroundedCounselling database initialized successfully';
END $$;