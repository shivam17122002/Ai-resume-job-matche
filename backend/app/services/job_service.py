from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate


class JobService:
    @staticmethod
    def create_job(db: Session, job: JobCreate, owner_id: int | None = None):
        """Create a new job"""
        db_job = Job(
            title=job.title,
            company=job.company,
            description=job.description,
            required_skills=job.required_skills,
            location=job.location,
            salary=job.salary,
            url=job.url,
            owner_id=owner_id,
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def get_job(db: Session, job_id: int):
        """Get job by ID"""
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 10):
        """Get all jobs with pagination"""
        return db.query(Job).offset(skip).limit(limit).all()

    @staticmethod
    def delete_job(db: Session, job_id: int):
        """Delete a job. Returns deleted job or None."""
        db_job = db.query(Job).filter(Job.id == job_id).first()
        if db_job:
            db.delete(db_job)
            db.commit()
        return db_job

    @staticmethod
    def delete_job_for_owner(db: Session, job_id: int, owner_id: int):
        db_job = db.query(Job).filter(Job.id == job_id, Job.owner_id == owner_id).first()
        if db_job:
            db.delete(db_job)
            db.commit()
        return db_job
