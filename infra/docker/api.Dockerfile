# Python FastAPI Dockerfile with uvicorn
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install UV for faster Python package installation
RUN pip install uv

# Copy requirements first for better caching
COPY services/api/requirements.txt ./
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY services/api/ ./

# Create non-root user
RUN useradd --create-home --shell /bin/bash api && \
    chown -R api:api /app
USER api

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]