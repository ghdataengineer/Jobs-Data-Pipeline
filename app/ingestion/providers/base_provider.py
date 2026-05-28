from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def fetch_jobs(self) -> list:
        pass

    def get_source_url(self) -> str:
        return getattr(self, "BASE_URL", None) or getattr(self, "URL", "unknown")