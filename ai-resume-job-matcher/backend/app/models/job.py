from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy import JSON
from sqlalchemy.sql import func
from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    company = Column(String(255), index=True)
    description = Column(Text)
    # store required skills as JSON/JSONB where supported
    required_skills = Column(JSON, nullable=True)
    location = Column(String(255), index=True)
    owner_id = Column(Integer, index=True, nullable=True)
    salary = Column(String(100))
    url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


Index('ix_jobs_title_location_created_at', Job.title, Job.location, Job.created_at)
