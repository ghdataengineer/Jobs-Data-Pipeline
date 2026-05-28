from app.ingestion.providers.base_provider import BaseProvider


class GlassdoorScraper(BaseProvider):

    URL = "https://www.glassdoor.com.br/Vaga/vagas.htm?sc.keyword=data+engineer"

    def fetch_jobs(self) -> list:
        # TODO: implementar
        return []