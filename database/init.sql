-- =========================================
-- DATABASE INIT - JOBS DATA PLATFORM
-- COMPATÍVEL + ENRIQUECIDO
-- =========================================

-- =========================================
-- EXTENSÃO (UUID opcional)
-- =========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- RAW LAYER (BRONZE)
-- =========================================

CREATE TABLE IF NOT EXISTS jobs_raw (
    id SERIAL PRIMARY KEY,

    ingestion_id UUID NOT NULL DEFAULT uuid_generate_v4(),

    source_name TEXT,
    source_type TEXT,
    source_url TEXT,

    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_ingestion_id
ON jobs_raw(ingestion_id);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_payload
ON jobs_raw USING GIN (payload);

-- =========================================
-- SILVER LAYER (PROCESSADOS)
-- =========================================

CREATE TABLE IF NOT EXISTS jobs_processed (
    id SERIAL PRIMARY KEY,

    raw_job_id INTEGER REFERENCES jobs_raw(id),

    title TEXT,
    company TEXT,
    location TEXT,
    category TEXT,
    publication_date DATE,
    job_url TEXT,

    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_company
ON jobs_processed(company);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_location
ON jobs_processed(location);

CREATE INDEX IF NOT EXISTS idx_jobs_processed_category
ON jobs_processed(category);

-- =========================================
-- GOLD LAYER (CURATED / AGG)
-- =========================================

CREATE TABLE IF NOT EXISTS jobs_curated (
    id SERIAL PRIMARY KEY,

    category TEXT,
    company TEXT,
    job_date DATE,

    total_jobs INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_category
ON jobs_curated(category);

CREATE INDEX IF NOT EXISTS idx_jobs_curated_company
ON jobs_curated(company);

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