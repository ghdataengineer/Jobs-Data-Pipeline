from collections import Counter


class JobsCuratedService:

    @staticmethod
    def build(jobs):

        curated = []

        for job in jobs:

            title = job.get("title")
            company = job.get("company")
            job_url = job.get("job_url")

            publication_date = job.get("publication_date")
            category = job.get("category")

            # =========================
            # NORMALIZA COMPANY
            # =========================
            if isinstance(company, dict):
                company = company.get("name") or company.get("company")

            elif isinstance(company, list):
                company = next(
                    (c for c in company if isinstance(c, str) and c.strip()),
                    None
                )

            # =========================
            # VALIDAÇÃO BÁSICA
            # =========================
            if not isinstance(title, str) or not title.strip():
                continue

            if not isinstance(company, str) or not company.strip():
                continue

            curated.append({
                "title": title.strip(),
                "company": company.strip(),
                "job_url": job_url,
                "publication_date": publication_date,
                "category": category
            })

        return curated

    # =====================================================
    # (OPCIONAL) MÉTRICAS SEPARADAS — NÃO USAR NO POSTGRES
    # =====================================================

    @staticmethod
    def build_by_category(jobs):

        from collections import Counter

        counter = Counter(
            job.get("category") or "unknown"
            for job in jobs
        )

        return [
            {"category": k, "total_jobs": v}
            for k, v in counter.items()
        ]

    @staticmethod
    def build_by_company(jobs):

        from collections import Counter

        counter = Counter(
            job.get("company") or "unknown"
            for job in jobs
        )

        return [
            {"company": k, "total_jobs": v}
            for k, v in counter.items()
        ]

    @staticmethod
    def build_by_date(jobs):

        from collections import Counter

        counter = Counter(
            (job.get("publication_date") or "")[:10] or "unknown"
            for job in jobs
        )

        return [
            {"date": k, "total_jobs": v}
            for k, v in counter.items()
        ]