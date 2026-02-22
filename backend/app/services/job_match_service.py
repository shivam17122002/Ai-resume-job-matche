from typing import Dict, List, Set
from app.models.resume import Resume
from app.models.job import Job


class JobMatchService:
    """
    Intelligent and explainable Resume ↔ Job matching logic.
    Deterministic, transparent, and production-safe.
    """

    @staticmethod
    def match_resume_to_job(resume: Resume, job: Job) -> Dict:
        # Defensive checks
        resume_skills: Set[str] = set(resume.skills or [])
        job_skills: Set[str] = set(job.required_skills or [])

        matched_skills: List[str] = list(resume_skills & job_skills)
        missing_skills: List[str] = list(job_skills - resume_skills)

        # ---------------------------
        # 1️⃣ Skill score (70%)
        # ---------------------------
        if job_skills:
            skill_score = (len(matched_skills) / len(job_skills)) * 70
        else:
            skill_score = 0

        # ---------------------------
        # 2️⃣ Experience score (20%)
        # ---------------------------
        experience_score = 0
        resume_exp = resume.experience_years or 0
        job_exp = getattr(job, "experience_years", None)

        if job_exp is not None:
            if resume_exp >= job_exp:
                experience_score = 20
            elif abs(resume_exp - job_exp) <= 1:
                experience_score = 10

        # ---------------------------
        # 3️⃣ Coverage bonus (10%)
        # ---------------------------
        coverage_bonus = 0
        if job_skills and len(matched_skills) / len(job_skills) >= 0.8:
            coverage_bonus = 10

        # ---------------------------
        # Final score
        # ---------------------------
        final_score = min(
            round(skill_score + experience_score + coverage_bonus, 2),
            100,
        )

        # ---------------------------
        # Verdict
        # ---------------------------
        if final_score >= 85:
            verdict = "Excellent Fit"
        elif final_score >= 70:
            verdict = "Good Fit"
        elif final_score >= 50:
            verdict = "Partial Fit"
        else:
            verdict = "Low Fit"

        # ---------------------------
        # Explanation (human-readable)
        # ---------------------------
        explanation = (
            f"Matched {len(matched_skills)} out of {len(job_skills)} required skills. "
            f"Experience score contributed {experience_score} points."
        )

        return {
            "match_score": final_score,
            "verdict": verdict,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "experience_analysis": {
                "resume_years": resume_exp,
                "job_required_years": job_exp,
                "experience_score": experience_score,
            },
            "explanation": explanation,
        }
