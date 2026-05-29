-- =========================================
-- EXTENSÃO UUID
-- =========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- BRONZE (RAW LAYER)
-- =========================================
CREATE TABLE IF NOT EXISTS jobs_raw (
    id SERIAL PRIMARY KEY,

    -- ingestion controlado pela aplicação (NÃO default)
    ingestion_id UUID NOT NULL,

    title TEXT,
    company TEXT,
    source_name TEXT,
    source_type TEXT,
    source_url TEXT,
    location TEXT,

    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- guarda TUDO do scraper sem perda de dados
    payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_ingestion_id
ON jobs_raw(ingestion_id);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_company
ON jobs_raw(company);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_payload
ON jobs_raw USING GIN (payload);

-- =========================================
-- SILVER (PROCESSADOS / NORMALIZADOS)
-- =========================================
CREATE TABLE IF NOT EXISTS jobs_processed (
    id SERIAL PRIMARY KEY,

    raw_job_id INTEGER REFERENCES jobs_raw(id),
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
    id SERIAL PRIMARY KEY,

    ingestion_id UUID,

    title TEXT,
    company TEXT,
    job_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_company
ON jobs_curated(company);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_ingestion_id
ON jobs_curated(ingestion_id);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_job_url
ON jobs_curated(job_url);

-- =========================================
-- DIM COMPANY
-- =========================================
CREATE TABLE IF NOT EXISTS dim_company (
    id SERIAL PRIMARY KEY,

    name TEXT UNIQUE NOT NULL,

    logo_url TEXT,
    website TEXT,
    url TEXT
);

-- =========================================
-- PIPELINE RUNS (OBSERVABILIDADE)
-- =========================================
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,

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