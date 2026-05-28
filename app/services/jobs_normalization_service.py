from datetime import datetime, timezone


class JobsNormalizationService:

    @staticmethod
    def normalize_job(job: dict, source_name: str, source_url: str) -> dict:
        return {
            "source_name":        source_name,
            "source_url":         source_url,
            "source_type":        job.get("source_type") or "api",
            "ingestion_time_utc": datetime.now(timezone.utc).isoformat(),

            "title": (
                job.get("title") or job.get("job_title")
            ),
            "company": (
                job.get("company_name") or job.get("company")
            ),
            "location": (
                job.get("candidate_required_location") or job.get("location")
            ),
            "category":         job.get("category"),
            "description":      job.get("description"),
            "job_url": (
                job.get("url") or job.get("job_url") or job.get("link")
            ),
            "publication_date": (
                job.get("publication_date") or job.get("date")
            ),
        }