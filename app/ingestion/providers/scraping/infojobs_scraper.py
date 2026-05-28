from app.ingestion.providers.base_provider import BaseProvider


class InfoJobsScraper(BaseProvider):

    URL = "https://www.infojobs.com.br/empregos.aspx?keyword=data+engineer"

    def fetch_jobs(self) -> list:
        # TODO: implementar
        return []