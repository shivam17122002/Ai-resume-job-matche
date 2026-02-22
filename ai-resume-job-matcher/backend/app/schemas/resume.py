from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ResumeBase(BaseModel):
    filename: str
    content: str
    skills: Optional[List[str]] = None
    experience_years: Optional[float] = None


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
