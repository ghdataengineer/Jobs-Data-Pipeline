from app.ingestion.factory.provider_factory import ProviderFactory
from app.services.jobs_normalization_service import JobsNormalizationService


class IngestionEngine:

    def run(self):
        provider = ProviderFactory.get_provider()
        raw_jobs = provider.fetch_jobs()

        source_url  = provider.get_source_url()
        source_name = provider.__class__.__name__

        normalized_jobs = []
        for job in raw_jobs:
            normalized_job = JobsNormalizationService.normalize_job(
                job=job,
                source_name=job.get("source_name", source_name),
                source_url=job.get("source_url", source_url),
            )
            normalized_jobs.append(normalized_job)

        return normalized_jobs