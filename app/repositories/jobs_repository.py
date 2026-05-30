import uuid

from psycopg2.extras import execute_values, Json

from app.db.postgres import get_connection


class JobsRepository:

    # =========================================
    # RAW LAYER (BRONZE)
    # =========================================
    @staticmethod
    def save_jobs_raw(jobs):

        if not jobs:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        ingestion_id = str(uuid.uuid4())

        try:

            values = []

            for job in jobs:

                values.append((
                    ingestion_id,
                    job.get("title"),
                    job.get("company"),
                    job.get("source_name"),
                    job.get("source_type"),
                    job.get("source_url"),
                    job.get("location"),
                    Json(job)
                ))

            execute_values(
                cursor,
                """
                INSERT INTO jobs_raw (
                    ingestion_id,
                    title,
                    company,
                    source_name,
                    source_type,
                    source_url,
                    location,
                    payload
                )
                VALUES %s
                """,
                values
            )

            conn.commit()

            print(f"\n[RAW] Inserted jobs: {len(values)}")
            print(f"[RAW] Ingestion ID: {ingestion_id}")

            return ingestion_id

        except Exception as e:

            conn.rollback()
            print(f"[RAW] Error: {e}")
            raise

        finally:

            cursor.close()
            conn.close()

    # =========================================
    # SILVER LAYER (NORMALIZADO)
    # =========================================
    @staticmethod
    def insert_processed(records: list):

        if not records:
            return 0

        conn = get_connection()
        cursor = conn.cursor()

        try:

            values = []

            for record in records:

                title = record.get("title")
                company = record.get("company")
                location = record.get("location")
                job_url = record.get("job_url")

                if isinstance(company, dict):
                    company = company.get("name") or company.get("company")

                if not title or not company:
                    continue

                values.append((
                    title,
                    company,
                    location,
                    job_url
                ))

            if not values:
                return 0

            execute_values(
                cursor,
                """
                INSERT INTO jobs_processed (
                    title,
                    company,
                    location,
                    job_url
                )
                VALUES %s
                """,
                values
            )

            conn.commit()

            inserted = len(values)

            print(f"[SILVER] Inserted records: {inserted}")

            return inserted

        except Exception as e:

            conn.rollback()
            print(f"[SILVER] Error: {e}")
            raise

        finally:

            cursor.close()
            conn.close()

    # =========================================
    # GOLD LAYER (CURATED / ANALYTICS)
    # =========================================
    @staticmethod
    def insert_curated(records: list):

        if not records:
            return 0

        conn = get_connection()
        cursor = conn.cursor()

        try:

            values = []

            for record in records:

                title = record.get("title")
                company = record.get("company")
                job_url = record.get("job_url")

                if isinstance(company, dict):
                    company = company.get("name") or company.get("company")

                if not title or not company or not job_url:
                    continue

                values.append((
                    title,
                    company,
                    job_url
                ))

            if not values:
                return 0

            execute_values(
                cursor,
                """
                INSERT INTO jobs_curated (
                    title,
                    company,
                    job_url
                )
                VALUES %s
                ON CONFLICT (job_url)
                DO NOTHING
                """,
                values
            )

            inserted = cursor.rowcount

            conn.commit()

            print(f"[CURATED] Inserted records: {inserted}")
            print(f"[CURATED] Ignored duplicates: {len(values) - inserted}")

            return inserted

        except Exception as e:

            conn.rollback()
            print(f"[CURATED] Error: {e}")
            raise

        finally:

            cursor.close()
            conn.close()