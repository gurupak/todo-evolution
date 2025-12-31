# Multi-stage Dockerfile for FastAPI backend with UV package manager
# Optimized for production deployment on Kubernetes

# Stage 1: Builder
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /app

# Install UV package manager and clean up pip cache
RUN pip install --no-cache-dir uv && \
    rm -rf /root/.cache/pip

# Copy all necessary files for package installation
COPY pyproject.toml ./
COPY README.md ./
COPY src/ ./src/

# Install dependencies using UV (editable install for development)
RUN uv pip install --system --no-cache -e . && \
    find /usr/local/lib/python3.13 -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.13 -type f -name '*.pyc' -delete 2>/dev/null || true

# Stage 2: Runtime
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Create non-root user (UID 1000)
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Copy installed dependencies from builder
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder --chown=appuser:appuser /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser src/ ./src/

# Switch to non-root user
USER 1000

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "src.todo_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
