from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class JobBase(BaseModel):
    title: str
    company: str
    description: str
    required_skills: Optional[List[str]] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    url: Optional[str] = None


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
