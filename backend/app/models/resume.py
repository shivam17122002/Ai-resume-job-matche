from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Index
from sqlalchemy import JSON
from sqlalchemy.sql import func
from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String(255), index=True)
    content = Column(Text, nullable=False)
    # store skills as JSON/JSONB where supported
    skills = Column(JSON, nullable=True)
    experience_years = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# additional indexes for fast lookup
Index('ix_resumes_user_id_created_at', Resume.user_id, Resume.created_at)
    