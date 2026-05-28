import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion.ingestion_engine import IngestionEngine


engine = IngestionEngine()

jobs = engine.run()

print(f"Total jobs: {len(jobs)}")

print(jobs[:2])