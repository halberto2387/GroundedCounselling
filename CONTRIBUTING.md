# Contributing to GroundedCounselling

Thank you for your interest in contributing to GroundedCounselling! This document provides guidelines and information for contributors.

## 🔒 Security and Compliance

GroundedCounselling is designed for healthcare applications and must maintain strict security and compliance standards:

- **HIPAA Compliance**: All code must consider HIPAA requirements for protected health information (PHI)
- **Data Security**: Encrypt sensitive data at rest and in transit
- **Audit Trail**: Maintain comprehensive audit logs for all user actions
- **Access Controls**: Implement proper role-based access control (RBAC)

## 🛠️ Development Setup

### Prerequisites

- Node.js 18+ with pnpm
- Python 3.11+
- Docker and Docker Compose
- Git

### Getting Started

1. **Fork and clone the repository**
```bash
git clone https://github.com/your-username/GroundedCounselling.git
cd GroundedCounselling
```

2. **Install dependencies**
```bash
pnpm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
cp services/api/.env.example services/api/.env
cp apps/web/.env.example apps/web/.env
# Edit files with your local configuration
```

4. **Start development environment**
```bash
docker-compose -f infra/docker/docker-compose.yml up -d
# OR for manual setup:
pnpm dev
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] **Tests**: All tests pass (`pnpm test`)
- [ ] **Linting**: Code passes linting (`pnpm lint`)
- [ ] **Type Checking**: TypeScript types are valid (`pnpm type-check`)
- [ ] **Documentation**: Update documentation if needed
- [ ] **Security Review**: Consider security implications
- [ ] **Accessibility**: Ensure WCAG 2.1 AA compliance for UI changes
- [ ] **Privacy**: Review data handling for privacy compliance

### Pull Request Template

Use the provided PR template and ensure you:

1. **Describe the change**: Clear description of what and why
2. **Link issues**: Reference related issues
3. **Screenshots**: Include screenshots for UI changes
4. **Testing**: Describe how the change was tested
5. **Security**: Note any security considerations
6. **Breaking Changes**: Highlight any breaking changes

### Code Review Process

1. **Automated Checks**: CI must pass (linting, tests, type-checking)
2. **Code Review**: At least one maintainer review required
3. **Security Review**: Security-sensitive changes need additional review
4. **Compliance Check**: Healthcare-related changes need compliance review

## 🎨 Code Style

### Frontend (TypeScript/React)

- **ESLint**: Follow the configured ESLint rules
- **Prettier**: Code formatting is handled by Prettier
- **Components**: Use shadcn/ui components where possible
- **Accessibility**: Follow ARIA guidelines and test with screen readers
- **Performance**: Optimize for performance (lazy loading, code splitting)

### Backend (Python/FastAPI)

- **Black**: Code formatting with Black
- **Ruff**: Linting with Ruff
- **MyPy**: Type checking with MyPy
- **Async/Await**: Use async patterns for I/O operations
- **Dependencies**: Minimize dependencies, prefer standard library

### General

- **Commit Messages**: Follow Conventional Commits
- **Variable Names**: Use descriptive, clear names
- **Comments**: Comment complex logic, not obvious code
- **Error Handling**: Proper error handling and logging

## 🔍 Testing Guidelines

### Frontend Testing

- **Unit Tests**: Jest + React Testing Library
- **Component Tests**: Test user interactions and accessibility
- **E2E Tests**: Playwright for critical user journeys
- **Visual Tests**: Include visual regression testing for UI components

### Backend Testing

- **Unit Tests**: pytest for individual functions
- **Integration Tests**: Test API endpoints with test database
- **Security Tests**: Test authentication and authorization
- **Performance Tests**: Test under load for critical endpoints

### Healthcare-Specific Testing

- **Data Privacy**: Test data encryption and access controls
- **Audit Logging**: Verify all user actions are logged
- **Compliance**: Test HIPAA compliance requirements
- **Emergency Access**: Test break-glass access procedures

## 📚 Documentation

### Code Documentation

- **TypeScript**: Use JSDoc for public APIs
- **Python**: Use Google-style docstrings
- **README**: Update README files for new features
- **ADRs**: Document significant architectural decisions

### User Documentation

- **User Guides**: Update user-facing documentation
- **API Docs**: FastAPI automatically generates OpenAPI docs
- **Deployment**: Document deployment procedures
- **Troubleshooting**: Add common issues and solutions

## 🚨 Security Guidelines

### Code Security

- **Input Validation**: Validate all inputs server-side
- **SQL Injection**: Use parameterized queries
- **XSS Prevention**: Sanitize outputs and use CSP headers
- **Authentication**: Implement proper session management
- **Authorization**: Check permissions for every action

### Data Security

- **Encryption**: Encrypt PHI data at rest and in transit
- **Key Management**: Use proper key rotation and storage
- **Data Minimization**: Collect only necessary data
- **Retention**: Follow data retention policies
- **Backup**: Secure backup procedures

### Infrastructure Security

- **HTTPS**: All communications over HTTPS
- **Headers**: Implement security headers
- **Dependencies**: Keep dependencies updated
- **Monitoring**: Monitor for security incidents
- **Logging**: Log security events without exposing sensitive data

## 🎯 Issue Guidelines

### Bug Reports

Include:
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details**
- **Screenshots/logs** (without sensitive data)

### Feature Requests

Include:
- **User story**: Who, what, why
- **Acceptance criteria**
- **Mockups/wireframes** if applicable
- **Security considerations**
- **Compliance requirements**

### Security Issues

**DO NOT** create public issues for security vulnerabilities.
Email security@groundedcounselling.com instead.

## 📞 Getting Help

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Create issues for bugs and feature requests
- **Chat**: Join our community chat (link in README)
- **Documentation**: Check docs/ folder for detailed guides

## 📄 License

By contributing to GroundedCounselling, you agree that your contributions will be licensed under the Apache License 2.0.

## 🙏 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md**: Listed alphabetically
- **Release Notes**: Mentioned for significant contributions
- **Documentation**: Credited for documentation improvements

Thank you for helping make GroundedCounselling better! 🎉