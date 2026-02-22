from pydantic import BaseModel
from typing import List


class JobMatchResult(BaseModel):
    job_id: int
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
