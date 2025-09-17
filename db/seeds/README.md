# Database Seeds

This directory contains seed data for the GroundedCounselling database.

## Files

- `initial_data.sql` - Basic seed data for development and testing

## Seed Data Includes

### Users
- **Admin User**
  - Email: admin@groundedcounselling.com
  - Password: admin123
  - Role: Admin

- **Sample Counsellor**
  - Email: dr.smith@groundedcounselling.com
  - Password: counsellor123
  - Role: Counsellor

- **Sample Patient**
  - Email: john.doe@example.com
  - Password: patient123
  - Role: Patient

### Specialist Profile
- Complete specialist profile for Dr. Jane Smith
- Specializations: Anxiety, Depression, PTSD, CBT, Mindfulness
- Availability: Monday-Friday with varying hours

### Sample Data
- Availability slots for the specialist
- Sample booking between patient and specialist
- Sample session linked to the booking
- Audit log entry

## Usage

### Manual Import

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d grounded_counselling

# Run the seed file
\i db/seeds/initial_data.sql
```

### Via Docker

```bash
# Copy seed file to container
docker cp db/seeds/initial_data.sql gc-postgres:/tmp/

# Execute in container
docker exec -i gc-postgres psql -U postgres -d grounded_counselling -f /tmp/initial_data.sql
```

### Via API Container

```bash
# Access API container
docker-compose exec api bash

# Run migrations first
alembic upgrade head

# Then run seeds (manual import)
```

## Development Notes

- All passwords are hashed using bcrypt
- UUIDs are generated for primary keys
- Timestamps use NOW() for current time
- Sample data is realistic but fictional

## Production Warning

**Do not use these seeds in production!** 

This data is for development and testing only. Production databases should be seeded with appropriate production data and strong passwords.

## Customization

To add more seed data:

1. Create new `.sql` files in this directory
2. Follow the existing pattern for data insertion
3. Ensure foreign key relationships are maintained
4. Update this README with new seed information