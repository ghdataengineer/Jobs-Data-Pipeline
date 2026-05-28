import os

from app.ingestion.providers.api.remotive_provider import RemotiveProvider
from app.ingestion.providers.api.adzuna_provider import AdzunaProvider
from app.ingestion.providers.scraping.linkedin_scraper import LinkedInScraper
from app.ingestion.providers.scraping.infojobs_scraper import InfoJobsScraper
from app.ingestion.providers.scraping.glassdoor_scraper import GlassdoorScraper

_API_PROVIDERS = {
    "remotive": RemotiveProvider,
    "adzuna":   AdzunaProvider,
}

_SCRAPING_PROVIDERS = {
    "linkedin":  LinkedInScraper,
    "infojobs":  InfoJobsScraper,
    "glassdoor": GlassdoorScraper,
}


class ProviderFactory:

    @staticmethod
    def get_provider():
        source = os.getenv("DATA_SOURCE", "api").lower()

        if source == "api":
            name = os.getenv("API_PROVIDER", "remotive").lower()
            cls = _API_PROVIDERS.get(name)
            if not cls:
                raise ValueError(f"API provider desconhecido: '{name}'. Disponíveis: {list(_API_PROVIDERS)}")
            return cls()

        if source == "scraping":
            name = os.getenv("SCRAPING_PROVIDER", "linkedin").lower()
            cls = _SCRAPING_PROVIDERS.get(name)
            if not cls:
                raise ValueError(f"Scraping provider desconhecido: '{name}'. Disponíveis: {list(_SCRAPING_PROVIDERS)}")
            return cls()

        raise ValueError(f"DATA_SOURCE inválido: '{source}'. Use 'api' ou 'scraping'.")