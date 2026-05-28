import os
import requests

from app.ingestion.providers.base_provider import BaseProvider


class AdzunaProvider(BaseProvider):

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID", "")
        self.app_key = os.getenv("ADZUNA_APP_KEY", "")
        self.country = os.getenv("ADZUNA_COUNTRY", "br")

    def fetch_jobs(self) -> list:
        if not self.app_id or not self.app_key:
            raise ValueError("ADZUNA_APP_ID e ADZUNA_APP_KEY precisam estar no .env")

        url = self.BASE_URL.format(country=self.country)
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": 50,
            "what": "data engineer",
            "content-type": "application/json",
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for item in data.get("results", []):
            jobs.append({
                "title": item.get("title"),
                "company_name": item.get("company", {}).get("display_name"),
                "location": item.get("location", {}).get("display_name"),
                "description": item.get("description"),
                "url": item.get("redirect_url"),
                "publication_date": item.get("created"),
                "category": item.get("category", {}).get("label"),
                "source_type": "api",
            })

        return jobs