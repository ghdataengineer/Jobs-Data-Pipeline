from datetime import datetime


class JobsTransformer:

    @staticmethod
    def transform(job):

        return {
            "title": (job.get("title") or "").strip(),

            "company": (
                job.get("company_name")
                or job.get("company")
                or "unknown"
            ).strip(),

            "category": job.get("category") or "unknown",

            "source_name": job.get("source_name"),

            "source_url": job.get("source_url"),

            "ingestion_time": job.get("ingestion_time_utc"),

            "processed_at": datetime.utcnow().isoformat()
        }