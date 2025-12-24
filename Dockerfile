# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .

RUN useradd -m appuser
USER appuser

CMD sh -c 'uvicorn api.main:app --host 0.0.0.0 --port ${PORT}'
