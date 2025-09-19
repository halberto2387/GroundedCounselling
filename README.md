# GroundedCounselling

[![API CI](https://github.com/halberto2387/GroundedCounselling/actions/workflows/api-ci.yml/badge.svg)](https://github.com/halberto2387/GroundedCounselling/actions/workflows/api-ci.yml)
[![Web CI](https://github.com/halberto2387/GroundedCounselling/actions/workflows/web-ci.yml/badge.svg)](https://github.com/halberto2387/GroundedCounselling/actions/workflows/web-ci.yml)
[![Label Sync](https://github.com/halberto2387/GroundedCounselling/actions/workflows/label-sync.yml/badge.svg)](https://github.com/halberto2387/GroundedCounselling/actions/workflows/label-sync.yml)

A production-ready counselling practice management system built with modern web technologies.

## 🏗️ Architecture

This monorepo contains:

- **apps/web**: Next.js frontend with App Router, Tailwind CSS, and shadcn/ui
- **services/api**: FastAPI backend with async SQLAlchemy and Alembic migrations  
- **services/worker**: RQ-based background job processor
- **packages/ui**: Shared design system and components
- **packages/sdk**: TypeScript client generated from API OpenAPI spec
- **packages/config**: Shared configuration (ESLint, Prettier, TypeScript)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ with pnpm (for local development without Docker)
- Python 3.11+ (for local development without Docker)

### Docker Development (Recommended)

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/halberto2387/GroundedCounselling.git
cd GroundedCounselling

# Copy environment files
cp .env.example .env
cp services/api/.env.example services/api/.env
cp apps/web/.env.example apps/web/.env
cp services/worker/.env.example services/worker/.env

# Start all services
docker-compose -f infra/docker/docker-compose.yml up -d

# Check service status
docker-compose -f infra/docker/docker-compose.yml ps
```

**Access the application:**
- Web App: http://localhost:3000
- API Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Database: localhost:5432 (postgres/postgres)
- Redis: localhost:6379

**Common Docker commands:**
```bash
# View logs
docker-compose -f infra/docker/docker-compose.yml logs -f

# Stop services
docker-compose -f infra/docker/docker-compose.yml down

# Rebuild after code changes
docker-compose -f infra/docker/docker-compose.yml up --build
```

### Local Development (Manual Setup)

If you prefer to run services manually without Docker:

1. **Install dependencies:**

```bash
# Install pnpm globally
npm install -g pnpm

# Install workspace dependencies
pnpm install
```

2. **Start infrastructure services:**

```bash
# Start only database and Redis with Docker
docker-compose -f infra/docker/docker-compose.yml up -d postgres redis
```

3. **Set up environment variables:**

```bash
cp .env.example .env
cp services/api/.env.example services/api/.env
cp apps/web/.env.example apps/web/.env
cp services/worker/.env.example services/worker/.env
# Edit files with your local configuration
```

4. **Run database migrations:**

```bash
cd services/api
# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install uv
uv pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

5. **Start development servers:**

```bash
# Terminal 1: API
cd services/api
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Worker
cd services/worker
source venv/bin/activate
python worker/main.py

# Terminal 3: Web (when available)
cd apps/web
pnpm dev
```

## 🛠️ Development

### Commands

```bash
# Install dependencies
pnpm install

# Run linting
pnpm lint

# Run type checking
pnpm type-check

# Run tests
pnpm test

# Build all packages
pnpm build

# Generate SDK from API
pnpm generate:sdk
```

### Project Structure

```
├── apps/
│   └── web/                    # Next.js frontend
├── services/
│   ├── api/                    # FastAPI backend
│   └── worker/                 # Background job processor
├── packages/
│   ├── ui/                     # Design system
│   ├── sdk/                    # TypeScript API client
│   └── config/                 # Shared configuration
├── infra/
│   └── docker/                 # Docker configuration
├── db/
│   ├── migrations/             # Database migrations
│   └── seeds/                  # Database seeds
├── docs/                       # Documentation
└── .github/                    # GitHub workflows and templates
```

## ✅ Continuous Integration

The repository uses a layered CI approach to balance fast feedback with deeper validation:

- **Core API Lite CI** (`core-api-lite-ci.yml`): Runs on every push/PR touching API code. Uses an in-repo SQLite database to perform:
	- Dependency installation + Alembic migrations
	- Health endpoint + OpenAPI schema sanity checks
	- Minimal async DB CRUD smoke test (user insert)
	This provides a quick signal (<1 min typical) without relying on Postgres services.

- **Core API Extended CI** (`core-api-extended-ci.yml`): More comprehensive multi-job pipeline validating CRUD flows, service imports, and integration scenarios. Currently under stabilization; some steps may still assume Postgres-specific behavior.

- **API CI / Web CI**: Existing pipelines for broader API & web build/test validation.

- **SDK Sync** (`sdk-sync.yml`): Regenerates the TypeScript SDK from the live FastAPI OpenAPI schema (using in-process TestClient + SQLite) and fails if `packages/sdk/src/types.ts` drifts from the committed version. Ensures client consumers always have an up-to-date contract.

- **Specialist Filter Matrix** (`specialist-filter-matrix.yml`): Runs specialization filtering tests across SQLite and Postgres to guarantee dialect parity and guard against substring collision regressions.

### CI Roadmap
Planned improvements:
- Make all service queries dialect-portable (replace Postgres-only operators)
- Reintroduce richer CRUD and integration checks into Extended CI once portable
- Add auth/security endpoint smoke tests to Lite CI
- Consider Python and OS matrix when stability is confirmed
- Optional auto-commit for SDK regeneration (behind `AUTO_COMMIT_SDK` flag)
- Transition fully to normalized specialization association tables once backfill validated; remove legacy JSON list

If a PR only needs rapid confirmation that the API layer still starts and migrates, rely on the Lite workflow; for deeper assurance, consult the Extended run once stabilized.

## 🎨 Design System

The design system uses the following brand colors:

- **Primary (Evergreen)**: #2E6F4E
- **Surface (Sand)**: #F5F1EA
- **Text (Charcoal)**: #1E1E1E
- **Muted (Slate)**: #6B7280
- **Accent (Sky)**: #3BA6FF

Typography combines Inter (sans-serif) and Source Serif 4 (serif) for professional, accessible design.

## 📋 Features

### For Counsellors
- **Practice Management**: Client management, scheduling, session notes
- **Video Sessions**: Integrated video calling (Jitsi)
- **Billing**: Invoice generation and payment processing (Stripe)
- **Analytics**: Practice insights and reporting

### For Clients
- **Booking**: Find and book sessions with counsellors
- **Profile**: Manage personal information and preferences
- **Sessions**: Join video sessions and view history
- **Resources**: Access to mental health resources and content

### Technical Features
- **Authentication**: JWT with refresh tokens, 2FA support
- **Real-time**: WebSocket support for live features
- **Internationalization**: Multi-language support
- **Accessibility**: WCAG 2.1 AA compliant
- **Security**: HIPAA-ready with audit logging
- **Performance**: Optimized for speed and scalability

## 🔐 Security & Compliance

This application is designed with healthcare compliance in mind:

- **Data Encryption**: At rest and in transit
- **Audit Logging**: Comprehensive activity tracking
- **Access Controls**: Role-based permissions (RBAC)
- **Session Management**: Secure JWT implementation
- **Privacy**: GDPR and HIPAA considerations

## 🚢 Deployment

### Production Setup

**Frontend (Vercel):**
1. Connect your GitHub repository to Vercel
2. Configure environment variables
3. Deploy automatically on push to main

**Backend (Render):**
1. Connect your GitHub repository to Render
2. Configure environment variables
3. Set up auto-deploy from main branch

**Database (Neon):**
1. Create a PostgreSQL database on Neon
2. Configure DATABASE_URL in environment variables

**Redis (Upstash):**
1. Create a Redis instance on Upstash
2. Configure REDIS_URL in environment variables

### Environment Variables

See `.env.example` and service-specific `.env.example` files for required configuration.

## 📚 Documentation

- [Product Requirements](./docs/product/PRD.md)
- [Architecture Decisions](./docs/engineering/ADR-000-bootstrap.md)
- [Design System](./docs/design/system.md)
- [API Documentation](./docs/api/README.md)
- [Compliance](./docs/compliance/readiness.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please read our [contributing guidelines](.github/CONTRIBUTING.md) for details on our code of conduct and development process.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@groundedcounselling.com
- 📖 Documentation: [docs/](./docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/halberto2387/GroundedCounselling/issues)

---

Built with ❤️ for mental health professionals and their clients.

## ⚠️ Specializations Data Model Transition

The `specialists.specializations` JSON array column is being deprecated in favor of a normalized model:

- `specializations` (unique `slug`, `display_name`)
- `specialist_specializations` (association table)

During the transition both representations are written for backward compatibility. Reads now prefer the association tables when present, falling back to JSON otherwise. Tests in the Specialist Filter Matrix CI ensure exact matching (no substring collisions like `art` vs `heart`).

Planned removal of the legacy JSON field will occur after confirming 1:1 parity in production. If you add new code that filters by specializations, use service-layer methods instead of ad-hoc JSON queries to remain forward-compatible.

### Parity Verification

Before dropping or ignoring the legacy JSON field, run the parity check script in production or staging:

```bash
cd services/api
python -m scripts.check_specialization_parity --database-url "$DATABASE_URL"
```

Exit codes:
- 0: All specialists have identical counts (safe to proceed)
- 1: At least one mismatch (investigate before removing JSON field)

You can adjust sampling with `--sample 50` to view more mismatch examples.

### Automated Parity Workflow

A scheduled + manual GitHub Actions workflow (`specialization-parity.yml`) runs the parity script daily at 03:00 UTC and can be triggered on demand.

Configure repository secret:
- `DATABASE_URL` (points at the target environment—staging or prod readonly replica).

Manual run (GitHub UI → Actions → Specialization Parity Check → Run workflow) optionally allows overriding the database URL.

Failure of this workflow (non‑zero exit) signals remaining mismatches between legacy JSON counts and association rows; delay JSON field removal until green for several consecutive days.

#### Notifications & Trend

The workflow produces:
- `parity_report.json` artifact (retained 14 days) containing counts & sample mismatches.
- A GitHub job summary with the latest totals.

Optional webhook notifications (Slack / Teams) can be enabled by adding secrets:
- `SLACK_WEBHOOK_URL`
- `TEAMS_WEBHOOK_URL`

Placeholders are present; once secrets are added you can extend the workflow to actually POST payloads (currently simplified for linting environments).

#### Planned JSON Field Removal

A placeholder migration (`0006_drop_specialist_json_field_placeholder`) is included but guarded by a runtime error to prevent accidental execution. After stable parity (e.g., 7 consecutive green daily runs):
1. Edit the migration to remove the guard and call `op.drop_column('specialists', 'specializations')`.
2. Re-run migrations in staging; confirm application behavior.
3. Apply to production during a low-traffic window.
4. Remove legacy references in code (mirroring writes) and update documentation.