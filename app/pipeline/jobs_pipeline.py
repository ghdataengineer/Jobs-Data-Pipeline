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
        extractor  = JobsExtractor(self.max_jobs)
        clean_jobs = extractor.extract()

        date = datetime.now().strftime("%Y-%m-%d")

        print(f"\n===== CLEAN =====")
        print(f"JOBS: {len(clean_jobs)}")

        raw_path = f"{self.storage_path}/raw/jobs_{date}.json"
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        save_json(clean_jobs, raw_path)

        clean_path = f"{self.storage_path}/clean/jobs_{date}.json"
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        save_json(clean_jobs, clean_path)

        curated_by_category = JobsCuratedService.build_by_category(clean_jobs)
        curated_by_company  = JobsCuratedService.build_by_company(clean_jobs)
        curated_by_date     = JobsCuratedService.build_by_date(clean_jobs)

        print("\n🚨 CURATED")
        print("CATEGORY:", len(curated_by_category))
        print("COMPANY:",  len(curated_by_company))
        print("DATE:",     len(curated_by_date))

        curated_dir = f"{self.storage_path}/curated"
        os.makedirs(curated_dir, exist_ok=True)
        save_json(curated_by_category, f"{curated_dir}/category_{date}.json")
        save_json(curated_by_company,  f"{curated_dir}/company_{date}.json")
        save_json(curated_by_date,     f"{curated_dir}/date_{date}.json")

        company_list = []
        for j in clean_jobs:
            company = j.get("company")
            if isinstance(company, dict):
                company = company.get("name") or company.get("company")
            if isinstance(company, list):
                company = next((c for c in company if c), None)
            if not isinstance(company, str) or not company.strip():
                continue
            company_list.append({"name": company.strip(), "logo_url": None, "website": None, "url": None})

        unique_companies = list({c["name"]: c for c in company_list}.values())
        if unique_companies:
            CompanyRepository.insert_companies(unique_companies)

        print("\n🚀 SALVANDO CURATED NO POSTGRES...")
        if curated_by_category:
            JobsRepository.insert_curated(curated_by_category)
        if curated_by_company:
            JobsRepository.insert_curated(curated_by_company)
        if curated_by_date:
            JobsRepository.insert_curated(curated_by_date)

        print("\n📊 RESUMO FINAL")
        print("CLEAN:",     len(clean_jobs))
        print("COMPANIES:", len(unique_companies))
        print("\n✅ PIPELINE FINALIZADO COM SUCESSO")