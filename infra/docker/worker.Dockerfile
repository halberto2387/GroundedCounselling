# Python RQ Worker Dockerfile
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
COPY services/worker/requirements.txt ./
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY services/worker/ ./

# Create non-root user
RUN useradd --create-home --shell /bin/bash worker && \
    chown -R worker:worker /app
USER worker

# Start worker
CMD ["python", "worker/main.py"]