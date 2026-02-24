# Interview Notes: AI Resume Analyzer & Job Matcher

## 1. 30-Second Project Pitch
This project is a full-stack resume intelligence platform. Users register/login, upload PDF resumes, run AI analysis to extract skills and experience, create jobs, search jobs via Elasticsearch, and calculate resume-job match and skill gaps. FastAPI handles the backend, React handles the frontend, PostgreSQL stores source-of-truth data, and Elasticsearch handles search relevance.

## 2. Architecture Summary
- Layered backend: `api` -> `services` -> `models/schemas` -> `db/core`
- Frontend: component-state navigation with pages for login, upload/analyze, create job, and search jobs
- Data architecture:
  - PostgreSQL: users, resumes, jobs
  - Elasticsearch: searchable index for jobs and analyzed resumes
- Auth: JWT bearer tokens with password hashing (bcrypt via `passlib`)

## 3. Key Backend Flows

Auth:
- `POST /api/auth/register` creates user with hashed password
- `POST /api/auth/login` verifies credentials and returns JWT

Resume flow:
- `POST /api/resumes/upload` accepts PDF, validates type/size (10MB), extracts text with `pdfplumber`, stores resume
- `POST /api/resumes/{id}/analyze` calls Gemini model (`gemini-flash-lite-latest`), stores `skills` and `experience_years`, indexes resume in Elasticsearch

Job flow:
- `POST /api/jobs` creates job for current user and indexes it in Elasticsearch
- `DELETE /api/jobs/{id}` enforces owner-only delete and removes ES document
- `GET /api/search/jobs` supports keyword, location, skills, pagination, sorting

Matching flow:
- `GET /api/match/resume/{resume_id}/job/{job_id}`
- `GET /api/gap/resume/{resume_id}/job/{job_id}`

## 4. Design Decisions You Can Defend
- Postgres + Elasticsearch:
  - Postgres is reliable transactional storage.
  - Elasticsearch gives fast fuzzy full-text search and relevance scoring.
- Skills stored as JSON:
  - Easy to persist structured extracted skills and re-use for ES indexing.
- Service layer:
  - Keeps route handlers thin and business logic testable/reusable.
- Token auth via dependency:
  - Shared `get_current_user` enforces auth consistently across protected routes.

## 5. Practical Tradeoffs / Current Limitations
- Table creation uses `Base.metadata.create_all` on startup, not Alembic migrations yet.
- `admin/reindex/jobs` is token-protected but lacks strict role-based admin checks.
- Frontend has a service method for top resumes (`/match/job/{id}/top-resumes`) but backend route is not implemented.
- No refresh-token/session strategy yet; auth is simple bearer token in localStorage.

## 6. Common Interview Questions (with concise answers)

Q: Why not use only PostgreSQL for search?
A: PostgreSQL can search, but Elasticsearch handles fuzzy multi-field matching and relevance ranking better at scale for job discovery use cases.

Q: How is resume text extracted?
A: `pdfplumber` reads PDF text. Scanned/non-text PDFs return a clear error (`PDF contains no extractable text`).

Q: How is AI output validated?
A: Gemini response is parsed as JSON and validated using Pydantic schema `ResumeAnalysisResult`.

Q: How do you enforce authorization?
A: JWT in `Authorization: Bearer <token>`, decoded in `get_current_user`, and owner checks for protected resources (for example resume analysis and job deletion).

Q: What would you improve first for production?
A: Add Alembic migrations, role-based auth, secure secret management/rotation, tighter CORS, rate limiting, and stronger token strategy (refresh tokens or httpOnly cookies).

## 7. Demo Script (2-3 minutes)
1. Register + login from frontend and confirm token stored.
2. Upload a real PDF resume and run analysis.
3. Create a job with clear required skills.
4. Search jobs by skill keyword and location.
5. Run resume-job match and skill gap endpoints.
6. Show `/api/health/full` for DB/Elasticsearch status.
