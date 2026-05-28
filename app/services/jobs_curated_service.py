from collections import Counter


class JobsCuratedService:

    @staticmethod
    def build_by_category(jobs):
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
        counter = Counter(
            (job.get("publication_date") or "")[:10] or "unknown"
            for job in jobs
        )
        return [
            {"date": k, "total_jobs": v}
            for k, v in counter.items()
        ]