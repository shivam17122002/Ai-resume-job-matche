from pydantic import BaseModel
from typing import List, Optional


class ResumeAnalysisResult(BaseModel):
    skills: List[str]
    experience_years: Optional[float]
    role: Optional[str]
