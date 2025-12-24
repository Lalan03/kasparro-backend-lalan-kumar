# Kasparro ETL & Backend System

- A production-grade ETL pipeline and FastAPI backend that ingests data from multiple sources, performs incremental processing, deduplication, and observability, and exposes APIs for downstream consumption.

- This project is designed to meet Backend & ETL Systems assignment requirements, following industry-grade architecture and best practices.

---

## 1. System Architecture

Data Sources
 ├── Public API
 ├── CSV File
 └── Third Source (JSON)
        ↓
Raw Data Layer (Audit & Traceability)
        ↓
Incremental ETL (Checkpointed)
        ↓
Unified & Deduplicated Data Model
        ↓
FastAPI Backend
        ↓
Consumers / Monitoring / Metrics




### Key Design Principles

- Raw data is always preserved (P0 requirement)

- Incremental ingestion via checkpoints (P1 requirement)

- Idempotent ETL runs

- Observability through Prometheus metrics

- Clear separation of concerns


## 2. 🗂 Project Structure

.
├── api/
│   ├── main.py              # FastAPI app & startup ETL
│   ├── routes.py            # API endpoints
│   └── dependencies/
│       └── auth.py          # API key authentication
│
├── core/
│   ├── config.py            # Environment configuration
│   ├── database.py          # DB engine & session management
│   └── models.py            # SQLAlchemy models
│
├── ingestion/
│   ├── api_source.py        # Public API ingestion
│   ├── csv_source.py        # CSV ingestion
│   ├── third_source.py      # Third source ingestion
│   └── etl_runner.py        # ETL orchestration
│
├── schemas/
│   └── unified.py           # Pydantic schemas
│
├── services/
│   ├── metrics.py           # Prometheus metrics
│   ├── rate_limiter.py      # Rate limiting & retries
│   └── schema_drift.py      # Schema drift detection
│
├── tests/
│   ├── test_api.py
│   └── test_etl.py
│
├── data/
│   ├── sample.csv
│   └── third_source.json
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md


## 3. Features

### ETL Capabilities

- Multi-source ingestion (API, CSV, JSON)

- Raw data persistence for auditability

- Incremental ingestion using checkpoints

- Canonical normalization & deduplication

- Idempotent ETL re-runs

- Success / Partial / Failure classification

- ETL execution audit logging

### Backend Capabilities

- Health check endpoint

- Paginated data access API

- ETL statistics API

- Prometheus-compatible metrics

- API key–based authentication

### Reliability & Observability

- Rate-limited external API ingestion
- Retry with exponential backoff
- Prometheus counters & histograms
- Safe ETL execution on application startup
---

## 4. Data Model

### Raw Tables
- `raw_api_data`
- `raw_csv_data`
- `raw_third_source_data`

### Control Tables
- `etl_checkpoint`
- `etl_runs`

### Unified Table
- `etl_checkpoint`
- `etl_runs`
#### These tables support:
- `Incremental ingestion`
- `Auditing`
- `Operational transparency`

### Unified Table (Canonical Output)
- `unified_data`

| Column        | Purpose                                    |
| ------------- | ------------------------------------------ |
| `name`        | **Canonical entity identity (normalized)** |
| `value`       | Business value                             |
| `source`      | Metadata only (not part of identity)       |
| `ingested_at` | Timestamp                                  |


#### Design decision:
- Identity is enforced only on the canonical name
- Source is treated as metadata, not identity
- This ensures true unification across sources

---

## 5. Canonical Normalization Strategy
- All incoming records are normalized before insertion:
def normalize_name(name: str) -> str:
    return name.strip().lower()

## 6. API Endpoints
### Root
- Returns application status.

- `GET /`
### Response:
- `{ "status": "running" }`

### Health Check
- `GET /health`
### Response:
- `{`
  `"status": "ok",`
  `"last_etl": "success | partial | failed"`
`}`

### Data API (Authentication Required)
- `GET /data`
- `Headers:`
`  x-api-key: `<API_KEY>
`Query Params:`
`  limit, offset, source`

### ETL Statistics
- `GET /stats`

#### Response includes:
- `Last run timestamp`
- `Last success timestamp`
- `Last failure timestamp`

### Metrics
- `GET /metrics`
#### Prometheus-compatible metrics including:
- `etl_runs_total`
- `etl_failures_total`
- `etl_records_total`
- `etl_duration_seconds`

## 7. Security & Secrets
- No secrets are committed
- `.env` is git-ignored
- `.env.example` provided
- API protected via API key
- Database credentials injected via environment variables


## 8. Deployment
Live Deployment (Railway)
#### URL: 
- `https://kasparro-backend-lalan-kumar-production.up.railway.app`

#### Infrastructure
- FastAPI hosted on Railway
- PostgreSQL hosted on Railway
- Docker-based deployment
- Non-root container user

### Startup Behavior
- Database initialized
- Tables created if missing
- ETL executed safely on startup
- Failures do not block API availability

## 9. Running Locally
- `docker-compose up --build`

#### and:
- `http://localhost:8000
`
## 10. Environment Variables
### Create a .env file:
- `DATABASE_URL=postgresql://user:password@host:port/dbname`
- `API_KEY=your-secret-key`

## 11. Running the Project
### ▶️ Local (Python)
- pip install -r requirements.txt
- uvicorn api.main:app --reload
### 🐳 Docker
- docker-compose up --build



## 12. Testing
- pytest

### Tests cover:
- API endpoints
- ETL execution
- Incremental ingestion
- Failure handling

## 13. Author
- Lalan Kumar



