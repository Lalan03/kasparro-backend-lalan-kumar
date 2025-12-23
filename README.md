# Kasparro ETL & Backend System

A production-grade ETL pipeline and FastAPI backend that ingests data from multiple sources, performs incremental processing, deduplication, observability, and exposes APIs for downstream consumption.

---

## 1. System Architecture

Sources
 ├── Public API
 ├── CSV File
 └── Third Source
        ↓
Raw Data Layer
        ↓
Incremental ETL (Checkpointed)
        ↓
Unified Data Model
        ↓
FastAPI Backend
        ↓
Consumers / Monitoring



## 2. 🗂 Project Structure

.
├── api/
│   ├── main.py
│   ├── routes.py
│   └── dependencies/
│       └── auth.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── models.py
│
├── ingestion/
│   ├── api_source.py
│   ├── csv_source.py
│   ├── third_source.py
│   └── etl_runner.py
│
├── schemas/
│   └── unified.py
│
├── services/
│   ├── metrics.py
│   ├── rate_limiter.py
│   └── schema_drift.py
│
├── tests/
│   ├── test_api.py
│   └── test_etl.py
│
├── data/
│   └── sample.csv
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md



## 3. Features

### ETL Capabilities
- Multi-source ingestion (API, CSV, Third source)
- Raw data persistence for traceability
- Incremental ingestion using checkpoints
- Deduplication at unified layer
- Idempotent ETL re-runs
- Partial / success / failure classification
- ETL audit logging

### Backend Capabilities
- Health monitoring
- Paginated data API
- ETL statistics API
- Prometheus metrics exposure
- API key authentication

### Reliability & Observability
- Rate-limited API ingestion
- Retry with exponential backoff
- Prometheus counters & histograms
- Startup ETL execution (non-blocking)

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
- `unified_data` (deduplicated output)

---

## 5. API Endpoints

### Health Check



## 6. Author
- Lalan Kumar
