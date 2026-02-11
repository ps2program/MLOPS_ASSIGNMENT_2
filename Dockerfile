# Multi-stage Dockerfile for Cats vs Dogs Classifier

# Stage 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create models directory and copy model if available
RUN mkdir -p models
COPY models/best_model.pt* models/

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Set environment variables
ENV MODEL_PATH=models/best_model.pt
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.inference.app:app", "--host", "0.0.0.0", "--port", "8000"]

