import json

from app.db.postgres import get_connection


class JobsRepository:

    @staticmethod
    def save_jobs_raw(jobs):
        conn = get_connection()
        cursor = conn.cursor()
        inserted = 0

        try:
            for job in jobs:
                payload = json.dumps(job)
                cursor.execute("""
                    INSERT INTO jobs_raw (source_name, source_url, payload, ingestion_time)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """, (
                    job.get("source_name"),
                    job.get("source_url"),
                    payload,
                ))
                inserted += cursor.rowcount

            conn.commit()
            print(f"\nInserted RAW jobs: {inserted}")
            return inserted

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_curated(records: list):
        if not records:
            return

        conn = get_connection()
        cursor = conn.cursor()
        inserted = 0

        try:
            for record in records:
                category = record.get("category")
                company  = record.get("company")
                total    = record.get("total_jobs", 0)

                # Só envia date se for uma data válida (YYYY-MM-DD), senão NULL
                raw_date = record.get("date")
                if raw_date and raw_date != "unknown" and len(raw_date) == 10:
                    job_date = raw_date
                else:
                    job_date = None

                cursor.execute("""
                    INSERT INTO jobs_curated (category, company, job_date, total_jobs)
                    VALUES (%s, %s, %s, %s)
                """, (category, company, job_date, total))
                inserted += cursor.rowcount

            conn.commit()
            print(f"Inserted CURATED records: {inserted}")
            return inserted

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()