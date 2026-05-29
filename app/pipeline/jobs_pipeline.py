import os
from datetime import datetime

from app.extractors.jobs_extractor import JobsExtractor
from app.services.jobs_curated_service import JobsCuratedService
from app.utils.file_utils import save_json
from app.repositories.jobs_repository import JobsRepository
from app.repositories.company_repository import CompanyRepository


class JobsPipeline:

    def __init__(self, max_jobs: int, storage_path: str = "data_lake"):
        self.max_jobs = max_jobs
        self.storage_path = storage_path

    def run(self):

        try:
            # =========================
            # EXTRACT
            # =========================
            extractor = JobsExtractor(self.max_jobs)
            clean_jobs = extractor.extract() or []

            date = datetime.now().strftime("%Y-%m-%d")

            print(f"\n===== CLEAN =====")
            print(f"JOBS: {len(clean_jobs)}")

            # =========================
            # STORAGE (RAW + CLEAN)
            # =========================
            raw_path = f"{self.storage_path}/raw/jobs_{date}.json"
            clean_path = f"{self.storage_path}/clean/jobs_{date}.json"

            os.makedirs(os.path.dirname(raw_path), exist_ok=True)

            save_json(clean_jobs, raw_path)
            save_json(clean_jobs, clean_path)

            # =========================
            # CURATED (SIMPLIFICADO)
            # =========================
            curated_jobs = JobsCuratedService.build(clean_jobs) or []

            print("\n🚨 CURATED")
            print("JOBS:", len(curated_jobs))

            curated_dir = f"{self.storage_path}/curated"
            os.makedirs(curated_dir, exist_ok=True)

            save_json(curated_jobs, f"{curated_dir}/jobs_{date}.json")

            # =========================
            # COMPANIES NORMALIZATION
            # =========================
            company_list = []

            for j in clean_jobs:

                company = j.get("company")

                # dict
                if isinstance(company, dict):
                    company = company.get("name") or company.get("company")

                # list
                elif isinstance(company, list):
                    company = next(
                        (c for c in company if isinstance(c, str) and c.strip()),
                        None
                    )

                # string final
                if isinstance(company, str) and company.strip():
                    company_list.append({
                        "name": company.strip(),
                        "logo_url": None,
                        "website": None,
                        "url": None
                    })

            unique_companies = list(
                {c["name"]: c for c in company_list}.values()
            )

            if unique_companies:
                CompanyRepository.insert_companies(unique_companies)

            # =========================
            # POSTGRES (GOLD LAYER)
            # =========================
            print("\n🚀 SALVANDO NO POSTGRES...")

            inserted_curated = 0

            if curated_jobs:
                inserted_curated = JobsRepository.insert_curated(curated_jobs)

            # =========================
            # FINAL REPORT
            # =========================
            print("\n📊 RESUMO FINAL")
            print("CLEAN:", len(clean_jobs))
            print("COMPANIES:", len(unique_companies))
            print("CURATED:", inserted_curated)

            print("\n✅ PIPELINE FINALIZADO COM SUCESSO")

        except Exception as e:
            print("\n❌ PIPELINE FAILED")
            print(f"ERROR: {e}")
            raise