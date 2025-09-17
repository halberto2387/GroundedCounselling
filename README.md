# GroundedCounselling

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

- Node.js 18+ with pnpm
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (or use Docker)
- Redis (or use Docker)

### Local Development

1. **Clone and install dependencies:**

```bash
git clone https://github.com/halberto2387/GroundedCounselling.git
cd GroundedCounselling
pnpm install
```

2. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your local configuration
```

3. **Start services with Docker:**

```bash
docker-compose up -d postgres redis
```

4. **Run database migrations:**

```bash
cd services/api
alembic upgrade head
```

5. **Start development servers:**

```bash
# Terminal 1: API
cd services/api
uvicorn app.main:app --reload --port 8000

# Terminal 2: Worker
cd services/worker
python worker/main.py

# Terminal 3: Web
cd apps/web
pnpm dev
```

6. **Access the application:**
   - Web: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

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

### Web App Development

The Next.js web application is located in `apps/web` and includes:

**Features:**
- Next.js 14 with App Router and TypeScript
- Tailwind CSS with design system integration
- Theming support with light/dark modes
- Internationalization (i18next) with English default
- Video calling integration (Jitsi Meet)
- Sentry monitoring and error tracking
- Security headers and CSP configuration

**Available Pages:**
- `/` - Homepage with company branding
- `/services` - Service offerings overview
- `/specialists` - Practitioner directory with profiles
- `/specialists/[id]` - Individual specialist details
- `/book` - Appointment booking (placeholder)
- `/blog` - Mental health resources and articles
- `/account` - User account management
- `/admin` - Administrative interface (access controlled)
- `/cms` - Content management system
- `/auth/*` - Authentication pages (signin, signup, 2FA)

**Development Commands:**
```bash
# Start development server
cd apps/web
pnpm dev

# Run tests
pnpm test

# Run e2e tests (requires dev server)
pnpm test:e2e

# Build for production
pnpm build

# Start production server
pnpm start
```

### Docker Deployment

The web application can be containerized using the provided Dockerfile:

```bash
# Build Docker image
docker build -f infra/docker/web.Dockerfile -t grounded-counselling-web .

# Run container
docker run -p 3000:3000 grounded-counselling-web
```

**Note:** When using Docker Compose, the web service will be available at http://localhost:3000

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