from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate
from typing import List, Optional

class ResumeService:
    @staticmethod
    def create_resume(db: Session, resume: ResumeCreate, user_id: int):
        """Create a new resume"""
        db_resume = Resume(
            user_id=user_id,
            filename=resume.filename,
            content=resume.content,
            skills=resume.skills,
            experience_years=resume.experience_years
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        return db_resume

    @staticmethod
    def get_resume(db: Session, resume_id: int):
        """Get resume by ID"""
        return db.query(Resume).filter(Resume.id == resume_id).first()

    @staticmethod
    def get_user_resumes(db: Session, user_id: int):
        """Get all resumes for a user"""
        return db.query(Resume).filter(Resume.user_id == user_id).all()

    @staticmethod
    def delete_resume(db: Session, resume_id: int):
        """Delete a resume"""
        db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if db_resume:
            db.delete(db_resume)
            db.commit()
        return db_resume
    
    @staticmethod
    def update_analysis(
        db,
        resume_id: int,
        skills: List[str],
        experience_years: Optional[float],
    ):
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return None

        # store skills as native JSON list
        resume.skills = skills
        resume.experience_years = experience_years

        db.commit()
        db.refresh(resume)
        return resume
