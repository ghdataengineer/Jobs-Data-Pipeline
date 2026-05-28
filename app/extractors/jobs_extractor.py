from app.ingestion.factory.provider_factory import ProviderFactory
from app.services.jobs_normalization_service import JobsNormalizationService


class JobsExtractor:

    def __init__(self, max_jobs: int):
        self.max_jobs = max_jobs

    def extract(self):
        provider = ProviderFactory.get_provider()

        print(f"\n🚀 Provider ativo: {provider.__class__.__name__}")

        raw_jobs = provider.fetch_jobs()

        if not raw_jobs:
            print("⚠️  Nenhum job retornado pelo provider")
            return []

        source_url  = provider.get_source_url()
        source_name = provider.__class__.__name__

        all_jobs = []
        for job in raw_jobs[:self.max_jobs]:
            try:
                normalized = JobsNormalizationService.normalize_job(
                    job=job,
                    source_name=job.get("source_name", source_name),
                    source_url=job.get("source_url", source_url),
                )
                all_jobs.append(normalized)
            except Exception as e:
                print(f"❌ Erro ao normalizar job: {e}")
                print(f"   Job: {job}")

        print(f"\n📊 Total de jobs processados: {len(all_jobs)}")
        return all_jobs