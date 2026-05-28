import requests

from app.ingestion.providers.base_provider import BaseProvider


class RemotiveProvider(BaseProvider):

    BASE_URL = "https://remotive.com/api/remote-jobs"

    def fetch_jobs(self) -> list:
        response = requests.get(self.BASE_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        jobs = data.get("jobs", [])
        for job in jobs:
            job.setdefault("source_type", "api")
        return jobs