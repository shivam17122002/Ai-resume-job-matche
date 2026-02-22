from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.resume import ResumeCreate
from app.services.resume_service import ResumeService
from app.services.resume_parser import parse_pdf
from app.services.resume_analyzer_service import ResumeAnalyzerService
from app.services.job_match_service import JobMatchService
from app.services.job_service import JobService
from app.schemas.job import JobCreate
from app.services.skill_gap_service import SkillGapService
from app.services.job_search_service import JobSearchService
from elasticsearch import Elasticsearch
from app.core.elasticsearch import get_es_client
from app.services.resume_search_service import ResumeSearchService
import logging
from fastapi import Header
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import create_access_token, decode_access_token, verify_password





router = APIRouter(prefix="/api", tags=["api"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str | None = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")

    token = parts[1]
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("user_id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = UserService.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return user


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@router.get("/health/full")
def full_health(db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es_client)):
    """Comprehensive health check for DB and Elasticsearch"""
    status_obj = {"db": True, "elasticsearch": True}

    # DB: simple query
    try:
        db.execute("SELECT 1")
    except Exception as e:
        logging.exception("DB health check failed: %s", e)
        status_obj["db"] = False

    # ES: ping
    try:
        if not es.ping():
            status_obj["elasticsearch"] = False
    except Exception:
        status_obj["elasticsearch"] = False

    return {"status": status_obj}

@router.post("/resumes/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Extract text from PDF
    try:
        text = parse_pdf(file)
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Resume parsing failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to parse resume")

    # Create schema object
    resume_data = ResumeCreate(
        filename=file.filename,
        content=text,
        skills=None,
        experience_years=None,
    )

    # Save to DB with authenticated user
    resume = ResumeService.create_resume(db=db, resume=resume_data, user_id=getattr(current_user, "id", 1))

    return {
        "id": resume.id,
        "filename": resume.filename,
        "message": "Resume uploaded successfully",
    }
    
@router.post("/resumes/{resume_id}/analyze")
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    es: Elasticsearch = Depends(get_es_client),
    current_user = Depends(get_current_user),
):
    resume = ResumeService.get_resume(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # ensure only owner can analyze
    if getattr(current_user, "id", None) != getattr(resume, "user_id", None):
        raise HTTPException(status_code=403, detail="Not authorized to analyze this resume")

    try:
        analysis = ResumeAnalyzerService.analyze_resume(resume.content)
    except Exception as e:
        logging.exception("AI analysis failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

    ResumeService.update_analysis(db=db, resume_id=resume_id, skills=analysis.skills, experience_years=analysis.experience_years)

    # 🔹 Index analyzed resume (safe & idempotent)
    ResumeSearchService.create_index(es)
    updated_resume = ResumeService.get_resume(db, resume_id)

    try:
        ResumeSearchService.create_index(es)
        ResumeSearchService.index_resume(es, updated_resume)
    except Exception as e:
        logging.exception("Elasticsearch resume indexing failed: %s", e)

    return {
        "resume_id": resume_id,
        "role": analysis.role,
        "skills": analysis.skills,
        "experience_years": analysis.experience_years,
    }

@router.post("/jobs")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    es: Elasticsearch = Depends(get_es_client),
    current_user = Depends(get_current_user),
):
    JobSearchService.create_index(es)
    created_job = JobService.create_job(db, job, owner_id=getattr(current_user, "id", None))

    try:
        JobSearchService.index_job(es, created_job)
    except Exception as e:
        logging.exception("Elasticsearch job indexing failed: %s", e)

    return created_job


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es_client), current_user = Depends(get_current_user)):
    # ensure owner deletes
    deleted = JobService.delete_job_for_owner(db, job_id, getattr(current_user, "id", None))
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found or not owned by user")

    try:
        JobSearchService.delete_job(es, job_id)
    except Exception:
        logging.exception("Failed to delete job from Elasticsearch: %s", job_id)

    return {"detail": "Job deleted"}


@router.post("/admin/reindex/jobs")
def reindex_jobs(db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es_client), current_user = Depends(get_current_user)):
    # Basic protection; in a real app check admin role
    jobs = db.query(JobService.__orig_bases__[0].__args__[0] if False else None).all() if False else db.query.__self__ if False else None
    # Fallback: query Job model directly
    from app.models.job import Job as JobModel
    jobs = db.query(JobModel).all()

    JobSearchService.reindex_all(es, jobs)
    return {"detail": "Reindex started", "jobs": len(jobs)}


@router.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = UserService.get_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    created = UserService.create_user(db, user)
    return created


@router.post("/auth/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = UserService.get_by_email(db, form_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    from app.core.security import verify_password as verify_pwd

    if not verify_pwd(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/match/resume/{resume_id}/job/{job_id}")
def match_resume_to_job(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    resume = ResumeService.get_resume(db, resume_id)
    if not resume or not resume.skills:
        raise HTTPException(status_code=404, detail="Resume not found or not analyzed")

    job = JobService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    result = JobMatchService.match_resume_to_job(resume, job)
    return result


@router.get("/gap/resume/{resume_id}/job/{job_id}")
def skill_gap_analysis(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    resume = ResumeService.get_resume(db, resume_id)
    if not resume or not resume.skills:
        raise HTTPException(status_code=404, detail="Resume not found or not analyzed")

    job = JobService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    gap = SkillGapService.analyze_gap(resume, job)

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "missing_skills": gap["missing_skills"],
        "recommendations": gap["recommendations"],
    }

@router.get("/search/jobs")
def search_jobs(
    q: str | None = None,
    location: str | None = None,
    skills: list[str] | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "relevance",
    order: str = "desc",
    es: Elasticsearch = Depends(get_es_client),
):
    return JobSearchService.search(
        es=es,
        query=q,
        location=location,
        skills=skills,
        page=page,
        size=size,
        sort_by=sort_by,
        order=order,
    )


    

    



    
