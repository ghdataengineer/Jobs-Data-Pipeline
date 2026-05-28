from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.db.postgres import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    title = Column(String(255))

    company = Column(String(255))

    location = Column(String(255))

    category = Column(String(255))

    description = Column(Text)

    job_url = Column(Text, unique=True)

    source_name = Column(String(100))

    source_type = Column(String(50))

    source_url = Column(Text)

    publication_date = Column(String(100))

    ingestion_time_utc = Column(String(100))