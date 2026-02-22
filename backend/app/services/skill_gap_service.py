from typing import Dict, List
from app.models.resume import Resume
from app.models.job import Job


SKILL_CATEGORIES = {
    "python": "backend",
    "fastapi": "backend",
    "django": "backend",
    "react": "frontend",
    "node.js": "backend",
    "docker": "devops",
    "kubernetes": "devops",
    "aws": "cloud",
    "postgresql": "database",
    "mysql": "database",
    "mongodb": "database",
    "tensorflow": "ai/ml",
    "scikit-learn": "ai/ml",
}


class SkillGapService:
    @staticmethod
    def categorize(skill: str) -> str:
        return SKILL_CATEGORIES.get(skill, "general")

    @staticmethod
    def priority(skill: str, category: str) -> str:
        if category in {"backend", "devops", "cloud"}:
            return "High"
        if category in {"database", "frontend"}:
            return "Medium"
        return "Low"

    @staticmethod
    def build_recommendation(skill: str) -> Dict[str, str]:
        category = SkillGapService.categorize(skill)
        priority = SkillGapService.priority(skill, category)

        return {
            "category": category,
            "priority": priority,
            "action": (
                f"Build a small project using {skill}, "
                f"add it to GitHub, and mention it in your resume."
            ),
        }

    @staticmethod
    def analyze_gap(resume: Resume, job: Job):
        resume_skills = {s.strip().lower() for s in resume.skills.split(",")}
        job_skills = {s.strip().lower() for s in job.required_skills.split(",")}

        missing = sorted(list(job_skills - resume_skills))

        recommendations = {
            skill: SkillGapService.build_recommendation(skill)
            for skill in missing
        }

        return {
            "missing_skills": missing,
            "recommendations": recommendations,
        }
