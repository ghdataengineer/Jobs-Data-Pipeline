import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlencode

from app.ingestion.providers.base_provider import BaseProvider


class LinkedInScraper(BaseProvider):

    BASE_URL = "https://www.linkedin.com/jobs/search"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def fetch_jobs(self) -> list:

        keyword = os.getenv(
            "JOB_KEYWORDS",
            "data engineer"
        )

        location = os.getenv(
            "JOB_LOCATION",
            "Brasil"
        )

        max_jobs = int(
            os.getenv(
                "MAX_JOBS",
                200
            )
        )

        jobs = []
        start = 0

        while len(jobs) < max_jobs:

            params = {
                "keywords": keyword,
                "location": location,
                "start": start,
            }

            url = (
                f"{self.BASE_URL}?"
                f"{urlencode(params)}"
            )

            print(f"[SCRAPER] Coletando: {url}")

            response = requests.get(
                url,
                headers=self.HEADERS,
                timeout=30
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            cards = soup.select(".base-card")

            if not cards:
                print(
                    "[SCRAPER] Nenhuma vaga encontrada."
                )
                break

            for card in cards:

                title_el = card.select_one(
                    ".base-search-card__title"
                )

                company_el = card.select_one(
                    ".base-search-card__subtitle"
                )

                location_el = card.select_one(
                    ".job-search-card__location"
                )

                link_el = card.select_one(
                    "a.base-card__full-link"
                )

                job = {
                    "title": (
                        title_el.text.strip()
                        if title_el else None
                    ),
                    "company_name": (
                        company_el.text.strip()
                        if company_el else None
                    ),
                    "location": (
                        location_el.text.strip()
                        if location_el else None
                    ),
                    "job_url": (
                        link_el["href"]
                        if link_el else None
                    ),
                    "source_type": "scraping",
                }

                jobs.append(job)

                if len(jobs) >= max_jobs:
                    break

            print(
                f"[SCRAPER] Total coletado: "
                f"{len(jobs)}"
            )

            start += 25

        return jobs