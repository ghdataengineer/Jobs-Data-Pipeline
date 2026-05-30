-- =========================================
-- EXTENSÃO UUID
-- =========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- BRONZE (RAW LAYER)
-- =========================================
CREATE TABLE IF NOT EXISTS jobs_raw (
    id BIGSERIAL PRIMARY KEY,

    ingestion_id UUID NOT NULL,

    title TEXT,
    company TEXT,
    source_name TEXT,
    source_type TEXT,
    source_url TEXT,
    location TEXT,

    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_ingestion_id
ON jobs_raw(ingestion_id);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_company
ON jobs_raw(company);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_payload
ON jobs_raw USING GIN(payload);

-- =========================================
-- SILVER (PROCESSADOS / NORMALIZADOS)
-- =========================================
CREATE TABLE IF NOT EXISTS jobs_processed (
    id BIGSERIAL PRIMARY KEY,

    raw_job_id BIGINT REFERENCES jobs_raw(id),

    ingestion_id UUID,

    title TEXT,
    company TEXT,
    location TEXT,

    job_url TEXT,
    source_url TEXT,

    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_company
ON jobs_processed(company);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_location
ON jobs_processed(location);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_ingestion_id
ON jobs_processed(ingestion_id);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_job_url
ON jobs_processed(job_url);

-- =========================================
-- GOLD (CURATED / ANALYTICS READY)
-- =========================================
CREATE TABLE IF NOT EXISTS jobs_curated (
    id BIGSERIAL PRIMARY KEY,
    ingestion_id UUID,
    title TEXT NOT NULL,
    company TEXT,
    job_url TEXT NOT NULL UNIQUE,
    status VARCHAR(30) DEFAULT 'NOVA',
    job_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_company
ON jobs_curated(company);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_title
ON jobs_curated(title);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_status
ON jobs_curated(status);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_created_at
ON jobs_curated(created_at);

-- =========================================
-- DIM COMPANY
-- =========================================
CREATE TABLE IF NOT EXISTS dim_company (
    id BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    logo_url TEXT,
    website TEXT,
    url TEXT
);

-- =========================================
-- PIPELINE RUNS (OBSERVABILIDADE)
-- =========================================
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id BIGSERIAL PRIMARY KEY,

    ingestion_id UUID,

    pipeline_name TEXT,
    source_name TEXT,

    status TEXT,

    total_extracted INTEGER DEFAULT 0,
    total_processed INTEGER DEFAULT 0,
    total_failed INTEGER DEFAULT 0,

    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP
);