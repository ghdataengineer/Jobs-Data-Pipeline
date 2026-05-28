from app.config import START_DATE, END_DATE, MAX_JOBS
from app.pipeline.jobs_pipeline import JobsPipeline
from app.wait_for_db import wait_for_db


def run():
    wait_for_db()

    print("=" * 50)
    print("INICIANDO PIPELINE DE VAGAS")
    print(f"START_DATE: {START_DATE}")
    print(f"END_DATE:   {END_DATE}")
    print(f"MAX_JOBS:   {MAX_JOBS}")
    print("=" * 50)

    pipeline = JobsPipeline(max_jobs=MAX_JOBS)
    pipeline.run()