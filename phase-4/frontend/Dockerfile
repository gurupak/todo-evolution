# Multi-stage Dockerfile for Next.js 15 App Router with standalone output
# Optimized for production deployment on Kubernetes

# Stage 1: Dependencies
FROM node:22-alpine AS deps

# Install dependencies only when needed
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# Stage 2: Builder
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Set environment for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV NEXT_PUBLIC_BACKEND_URL=http://todo-app-backend:8000
ENV NEXT_PUBLIC_FRONTEND_URL=http://todo.local
ENV NEXT_PUBLIC_API_URL=/api/proxy
ENV NEXT_PUBLIC_APP_URL=http://todo.local

# Build Next.js application with standalone output
RUN npm run build

# Stage 3: Runtime
FROM node:22-alpine AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user (use existing group if 1000 is taken)
RUN addgroup --system appuser || true && \
    adduser --system --ingroup appuser appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Copy standalone output from builder
COPY --from=builder --chown=appuser:appuser /app/.next/standalone ./
COPY --from=builder --chown=appuser:appuser /app/.next/static ./.next/static

# Switch to non-root user
USER 1000

# Expose application port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode === 200) process.exit(0); process.exit(1);})" || exit 1

# Run application
CMD ["node", "server.js"]
