# Multi-stage Next.js Dockerfile with pnpm
FROM node:20-alpine AS base

# Allow overriding the npm registry (useful behind proxies/for mirrors)
ARG NPM_REGISTRY=https://registry.npmjs.org/
ENV npm_config_registry=${NPM_REGISTRY}
ENV npm_config_strict-ssl=false
ENV npm_config_fetch-retry-maxtimeout=120000
ENV npm_config_fetch-timeout=120000

# Install pnpm via npm from the configured registry (more controllable than corepack)
RUN npm config set registry ${NPM_REGISTRY} \
	&& npm config set strict-ssl false \
	&& npm config set fetch-retry-maxtimeout 120000 \
	&& npm config set fetch-timeout 120000 \
	&& npm install -g pnpm@8.15.0 --registry=${NPM_REGISTRY} \
	&& pnpm --version

# Dependencies stage
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/

# Ensure pnpm uses the same registry and relaxed SSL; then install
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN pnpm config set registry ${NPM_REGISTRY} \
	&& pnpm config set strict-ssl false \
	&& pnpm install --frozen-lockfile

# Build stage  
FROM base AS builder
WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules

# Copy source code
COPY . .

# Ensure public directory exists (Next.js app may omit it)
RUN mkdir -p /app/apps/web/public

# Build the web application
WORKDIR /app/apps/web
RUN pnpm build

# Runtime stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Add non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
# Ensure correct ownership and handle missing public by creating it in builder
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# In a monorepo, Next.js standalone often places server.js under apps/web
CMD ["node", "apps/web/server.js"]