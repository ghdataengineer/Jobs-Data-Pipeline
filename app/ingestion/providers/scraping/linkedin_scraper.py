import requests
from bs4 import BeautifulSoup

from app.ingestion.providers.base_provider import BaseProvider


class LinkedInScraper(BaseProvider):

    URL = "https://www.linkedin.com/jobs/search?keywords=data%20engineer"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def fetch_jobs(self) -> list:
        response = requests.get(self.URL, headers=self.HEADERS, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []

        for card in soup.select(".base-card"):
            title_el   = card.select_one(".base-search-card__title")
            company_el = card.select_one(".base-search-card__subtitle")
            location_el = card.select_one(".job-search-card__location")
            link_el    = card.select_one("a.base-card__full-link")

            jobs.append({
                "title":        title_el.text.strip() if title_el else None,
                "company_name": company_el.text.strip() if company_el else None,
                "location":     location_el.text.strip() if location_el else None,
                "job_url":      link_el["href"] if link_el else None,
                "source_type":  "scraping",
            })

        return jobs