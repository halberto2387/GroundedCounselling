# GroundedCounselling Development Environment

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Initial Setup - Required Every Time
1. **Install pnpm globally:**
   ```bash
   npm install -g pnpm
   ```

2. **Install all dependencies:**
   ```bash
   pnpm install --no-frozen-lockfile
   ```
   - Takes ~30 seconds
   - Use `--no-frozen-lockfile` to handle workspace dependencies correctly

### Build and Development Commands
- **Build all packages:** `pnpm build` 
  - Takes ~5 seconds. NEVER CANCEL. Set timeout to 60+ seconds for safety.
  - Builds TypeScript packages in packages/sdk and packages/ui
  
- **Type checking:** `pnpm type-check` 
  - Takes ~4 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
  
- **Linting:** `pnpm lint` 
  - Takes ~3 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
  - Note: Shows TypeScript version warnings but works correctly
  
- **Generate SDK types:** `pnpm generate:sdk` 
  - Takes ~3 seconds
  - Creates fallback types when API server is not running (expected behavior)
  
- **Run tests:** `pnpm test` 
  - Takes ~2 seconds (no tests currently configured)

### Project Structure
This is a **partial monorepo** with only the packages/ directory present. The repository structure mentioned in README.md includes missing directories:

```
├── packages/              # ✅ Present - shared packages
│   ├── ui/                # Design system and components  
│   ├── sdk/               # TypeScript API client
│   └── config/            # Shared ESLint, Prettier, TS config
├── apps/                  # ❌ Missing - Next.js frontend
├── services/              # ❌ Missing - FastAPI backend, worker
├── docs/                  # ❌ Missing - documentation
├── db/                    # ❌ Missing - migrations, seeds  
├── infra/                 # ❌ Missing - Docker configuration
└── .github/               # ❌ Missing - workflows and templates
```

**Important:** Only work with the packages/ directory. Do not attempt to run commands that expect apps/ or services/ directories.

### Known Working Configuration
- **Node.js:** v20.19.5
- **npm:** 10.8.2  
- **pnpm:** 8.15.0
- **Package manager:** pnpm (required)

### Validation Steps
ALWAYS run these commands in order after making code changes:
1. `pnpm type-check` - Validate TypeScript
2. `pnpm build` - Build all packages  
3. `pnpm lint` - Check code style

### Timing Expectations and Timeouts
- **CRITICAL:** NEVER CANCEL any build or lint command
- `pnpm install`: 30 seconds - Set timeout to 120+ seconds
- `pnpm build`: 5 seconds - Set timeout to 60+ seconds  
- `pnpm type-check`: 4 seconds - Set timeout to 30+ seconds
- `pnpm lint`: 3 seconds - Set timeout to 30+ seconds
- `pnpm generate:sdk`: 3 seconds - Set timeout to 30+ seconds

### Common Issues and Solutions

**1. ESLint configuration errors:**
- Fixed in current setup with simplified TypeScript parser configuration
- Uses basic `eslint:recommended` with TypeScript parser

**2. Build failures:**
- Ensure `pnpm install --no-frozen-lockfile` was run first
- Check that all packages have their dependencies installed

**3. TypeScript version warnings in ESLint:**
- Expected behavior - ESLint warns about TS 5.9.2 vs supported 5.4.0
- Does not affect functionality, warnings can be ignored

**4. Missing API server for SDK generation:**
- Expected behavior - generates fallback types when API unavailable
- Creates types in `packages/sdk/src/types.ts`

### Package Details

**packages/ui:**
- Design system with Radix UI components
- Uses Tailwind CSS and class-variance-authority
- Exports: Button, Input, Card, Badge, Alert, ThemeProvider
- Build target: ES2022

**packages/sdk:**  
- TypeScript client for GroundedCounselling API
- Axios-based HTTP client
- Auto-generates types from OpenAPI spec (with fallback)
- Build target: ES2020

**packages/config:**
- Shared ESLint, Prettier, and TypeScript configurations
- Used by other packages for consistent code style

### Environment Variables
See `.env.example` for complete list. Key variables include:
- `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` (for SDK generation)
- Database, Redis, JWT, and other service configurations

### Docker and Deployment
No Docker configuration present in this repository clone. Commands like `pnpm docker:up` will fail as docker-compose.yml is missing.

### Contributing Workflow
1. Make changes to packages/
2. Run validation commands: `pnpm type-check && pnpm build && pnpm lint`
3. Commit changes with conventional commit format
4. Always validate that build succeeds before committing

### What Does NOT Work
- **Docker commands:** No docker-compose.yml file present
- **App/service commands:** Only packages exist in this repository  
- **Database migrations:** No db/ directory or Alembic configuration
- **Full application running:** Frontend and backend services are not present

### Manual Validation Scenarios
Since only packages are present, validation is limited to:
1. **Build validation:** Ensure all packages build successfully
2. **Type validation:** Ensure TypeScript compilation passes
3. **Lint validation:** Ensure code style is consistent
4. **SDK generation:** Test that fallback types are created properly

**Note:** Cannot perform end-to-end application testing as frontend/backend are not present in this repository clone.