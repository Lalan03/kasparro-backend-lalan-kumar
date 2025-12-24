# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages only
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

# Create non-root user (MANDATORY for prod)
RUN useradd -m appuser
USER appuser

# Railway-compatible startup
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
