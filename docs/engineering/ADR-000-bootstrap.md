# ADR-000: Bootstrap and Initial Architecture Decisions

**Status:** Accepted  
**Date:** 2024-09-17  
**Authors:** GroundedCounselling Team  

## Context

GroundedCounselling is a new healthcare technology platform designed to connect clients with mental health specialists through secure, HIPAA-compliant video sessions. The platform must support rapid development while maintaining security, scalability, and compliance with healthcare regulations.

## Decisions

### Technology Stack

#### Frontend
- **Next.js 14+** with App Router for the web application
- **TypeScript** for type safety and developer experience
- **Tailwind CSS** with **shadcn/ui** for consistent, accessible UI components
- **pnpm** for package management (faster than npm/yarn)

#### Backend
- **FastAPI** for the REST API (async, OpenAPI docs, excellent Python ecosystem)
- **Python 3.11+** for modern language features and performance
- **SQLAlchemy 2.0+** with async support for database ORM
- **Alembic** for database migrations
- **PostgreSQL 15+** for the primary database
- **Redis 7+** for caching and job queues

#### Background Processing
- **RQ (Redis Queue)** for background job processing
- Separate worker service for async tasks

#### Infrastructure
- **Docker** and **Docker Compose** for local development
- **GitHub Actions** for CI/CD
- **Vercel** for frontend deployment (keeping existing choice)
- **Render** for backend deployment (keeping existing choice)

### Repository Structure

Chose a **monorepo** structure to:
- Enable shared code and configurations
- Simplify dependency management
- Improve developer experience
- Support atomic changes across frontend/backend

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
├── docs/                       # Documentation
└── .github/                    # GitHub workflows and templates
```

### Development Environment

#### Docker-First Approach
- **Docker Compose** for local development to ensure consistency
- Multi-stage Dockerfiles for optimized production builds
- Health checks for all services
- Named volumes for data persistence

#### Package Management
- **pnpm** workspaces for the monorepo
- **UV** for fast Python package installation
- Lock files committed to ensure reproducible builds

### CI/CD Pipeline

#### Continuous Integration
- **GitHub Actions** for all CI/CD workflows
- Separate workflows for API and Web to optimize build times
- Concurrency groups to prevent duplicate runs
- Docker image building as part of CI to validate Dockerfiles

#### Quality Gates
- **Linting**: ESLint/Prettier for frontend, Ruff/Black for backend
- **Type Checking**: TypeScript for frontend, MyPy for backend
- **Testing**: Jest for frontend, pytest for backend
- **Security**: Dependency scanning and static analysis

### Security and Compliance

#### Healthcare Compliance
- HIPAA compliance requirements from day one
- Audit logging for all data access
- Encryption at rest and in transit
- Secure session management

#### Authentication
- **JWT tokens** with short expiration (15 minutes)
- **Refresh token rotation** for security
- **Role-based access control** (Client, Specialist, Admin)

## Rationale

### Why FastAPI?
- Excellent async support for high-performance APIs
- Automatic OpenAPI documentation generation
- Built-in validation with Pydantic
- Strong ecosystem for healthcare applications

### Why Next.js App Router?
- Server-side rendering for better SEO and performance
- Modern React patterns with Server Components
- Excellent developer experience
- Built-in optimizations

### Why Docker Compose for Development?
- Eliminates "works on my machine" issues
- Simplifies onboarding for new developers
- Matches production environment closely
- Easy to add new services (databases, monitoring, etc.)

### Why Monorepo?
- Simplified dependency management across services
- Atomic commits for full-stack features
- Shared tooling and configurations
- Better collaboration between frontend/backend teams

## Consequences

### Positive
- Consistent development environment across team
- Fast iteration with hot reload in Docker
- Type-safe API integration with generated TypeScript client
- Automated quality checks prevent bugs from reaching production
- Easy to scale with additional services

### Negative
- Initial setup complexity for new developers
- Docker resource usage on development machines
- Monorepo can become large over time
- Need to manage workspace dependencies carefully

## Implementation Notes

### Docker and CI Integration (Added 2024-09-17)

Based on the need for streamlined development and deployment, we've added:

1. **Dockerized Development Environment**
   - Multi-stage Dockerfiles for production-optimized builds
   - Docker Compose with health checks and proper service dependencies
   - Named volumes for data persistence and caching
   - Environment variable management through .env files

2. **GitHub Actions CI Workflows**
   - Separate workflows for API and Web to optimize build times
   - Python 3.11 with UV for fast package installation
   - Node 20 with pnpm for consistent frontend builds
   - Concurrency groups to prevent resource waste
   - Docker image building to validate deployment readiness

3. **Repository Hygiene Automation**
   - Issue and PR templates with healthcare-specific checklists
   - Automated label management with comprehensive labeling scheme
   - CODEOWNERS for code review requirements
   - Repository seeding workflow for milestones and initial issues

These additions support our core architectural principles while enabling:
- **Faster Onboarding**: New developers can start with `docker-compose up`
- **Consistent Environments**: Development mirrors production infrastructure
- **Quality Assurance**: Automated testing and validation in CI
- **Project Management**: Structured issue tracking and milestone management
- **Compliance Readiness**: Security and healthcare compliance considerations built-in

## Alternatives Considered

### Technology Alternatives
- **Django REST Framework** vs FastAPI → FastAPI chosen for async support and modern features
- **React SPA** vs Next.js → Next.js chosen for SEO and performance
- **npm/yarn** vs pnpm → pnpm chosen for speed and monorepo support
- **MySQL** vs PostgreSQL → PostgreSQL chosen for advanced features and JSON support

### Infrastructure Alternatives
- **Kubernetes** vs Docker Compose → Docker Compose chosen for simplicity in early stages
- **Self-hosted** vs Managed services → Hybrid approach with managed databases

## Status

This ADR is **Accepted** and reflects the current architectural decisions for GroundedCounselling. Future ADRs will document significant changes or additions to this foundation.

## Review

This ADR should be reviewed when:
- Significant performance issues arise
- Compliance requirements change
- Team size changes significantly
- New major features require architectural changes