from pydantic import BaseModel
from typing import List, Dict


class SkillGapResult(BaseModel):
    job_id: int
    resume_id: int
    missing_skills: List[str]
    recommendations: Dict[str, str]
