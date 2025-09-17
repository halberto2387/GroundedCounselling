# CI/CD Quickstart Guide

This guide helps you configure the GitHub repository for optimal CI/CD operation with all workflows and automation features.

## Prerequisites

Before running the CI workflows successfully, you need to configure repository settings and secrets.

## Repository Settings

### 1. Workflow Permissions

Navigate to your repository's **Settings → Actions → General → Workflow permissions** and select:

- **Read and write permissions** 
- Check **Allow GitHub Actions to create and approve pull requests**

This allows workflows to:
- Create issues and manage labels
- Write to projects and milestones
- Commit changes back to the repository

### 2. Create Personal Access Token (PAT)

For full functionality of the Repository Seeding workflow, create a classic Personal Access Token:

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `project` (Full control of projects)
   - `workflow` (Update GitHub Action workflows)
4. Copy the generated token

### 3. Add Repository Secret

Add the PAT as a repository secret:

1. Go to **Repository → Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `PROJECTS_TOKEN`
4. Value: [paste your PAT here]
5. Click **Add secret**

## Workflow Overview

### Web CI (`web-ci.yml`)
- **Triggers**: Push/PR to `main`, `develop`, feature branches affecting web app
- **Purpose**: Lint, type-check, test, and build the Next.js frontend
- **Dependencies**: Node.js 20, pnpm 8, with caching enabled
- **Environment variables**: Safe defaults for `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_JITSI_DOMAIN`

### API CI (`api-ci.yml`)  
- **Triggers**: Push/PR to `main`, `develop`, feature branches affecting API
- **Purpose**: Lint (ruff/black/mypy), run Alembic migrations, test with pytest
- **Services**: PostgreSQL 16, Redis 7
- **Database**: Uses `postgresql+asyncpg://` connection string for async support

### Label Sync (`label-sync.yml`)
- **Triggers**: Push to `main` affecting `.github/labels.yml`, or manual dispatch
- **Purpose**: Synchronize repository labels with configuration
- **Permissions**: `issues: write`, `pull-requests: write`

### Repository Seeding (`setup-seed.yml`)
- **Triggers**: Manual dispatch only (workflow_dispatch)
- **Purpose**: Create milestones M0-M7, GitHub project, and initial issues
- **Permissions**: `issues: write`, `projects: write`, `contents: read`
- **Token**: Uses `PROJECTS_TOKEN` secret, falls back to `GITHUB_TOKEN`

## Running Repository Seeding

After configuring the `PROJECTS_TOKEN` secret:

1. Go to **Actions** tab in your repository
2. Click **Repository Seeding** workflow
3. Click **Run workflow** 
4. Configure the inputs:
   - **Create milestones M0-M7**: `true` (recommended)
   - **Create GitHub Project**: `true` (requires admin permissions)
   - **Create initial backlog issues**: `true` (recommended)
5. Click **Run workflow**

The workflow will:
- Create milestones M0 through M7 for project phases
- Create a GitHub Projects v2 board for development tracking
- Seed initial issues from `.github/seeds/issues.yml`
- Skip duplicates if items already exist

## Troubleshooting

### Common Issues

**Permission denied errors**:
- Verify workflow permissions are set to "Read and write"
- Ensure `PROJECTS_TOKEN` secret is configured correctly
- Check that your PAT has the required scopes

**API CI failures**:
- Ensure services (PostgreSQL, Redis) are healthy before running tests
- Check that database connection string uses `postgresql+asyncpg://` for async support
- Verify Alembic migrations are properly configured

**Web CI build failures**:
- Missing environment variables are provided with safe defaults
- Build failures may indicate actual code issues, not CI configuration

**Label sync failures**:
- Verify `.github/labels.yml` exists and is valid YAML
- Check that workflow has `issues: write` permissions

### Getting Help

- Check the **Actions** tab for detailed logs of workflow runs
- Review the specific step that failed for error messages
- Ensure all prerequisites from this guide are completed
- For persistent issues, check the repository's issue tracker

## Next Steps

Once CI is stabilized:
1. All pushes to `main`/`develop` will trigger appropriate CI checks
2. Repository seeding creates your project structure and initial backlog
3. Label synchronization keeps your labels organized
4. Manual workflows can be run as needed from the Actions UI

The CI system now provides a solid foundation for collaborative development with automated quality checks and project management integration.