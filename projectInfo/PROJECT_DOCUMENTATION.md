# AI Resume Analyzer & Job Matcher - Project Documentation

Last updated: February 24, 2026
Root path: `c:\Users\Lenovo\Projects\Resume_Analyzer`

## 1. Overview
This project provides:
- User registration and login (JWT)
- Resume upload (PDF) and AI analysis
- Job creation and deletion
- Job search with Elasticsearch
- Resume-to-job match scoring and skill gap analysis

## 2. High-Level Architecture
Frontend (React + Vite) -> Backend API (FastAPI) -> PostgreSQL + Elasticsearch

- PostgreSQL stores users, resumes, jobs.
- Elasticsearch indexes jobs (and analyzed resumes) for fast search.
- Gemini is called during resume analysis to extract skills, experience, and role.

## 3. Current Repository Structure
```
Resume_Analyzer/
|- backend/
|  |- app/
|  |  |- api/routes.py
|  |  |- core/
|  |  |- db/
|  |  |- models/
|  |  |- schemas/
|  |  |- services/
|  |- Dockerfile
|  |- requirements.txt
|- frontend/
|  |- src/
|  |  |- api/client.ts
|  |  |- pages/
|  |  |- services/
|  |  |- components/
|- projectInfo/
|  |- INTERVIEW.md
|  |- PROJECT_DOCUMENTATION.md
|- docker-compose.yml
|- README.md
```

## 4. Backend Details

### 4.1 Stack
- FastAPI
- SQLAlchemy ORM
- Pydantic schemas
- python-jose (JWT)
- passlib[bcrypt]
- pdfplumber
- google-generativeai
- elasticsearch (8.11 client)

### 4.2 Config Behavior (`app/core/config.py`)
- Reads env variables from `backend/.env`.
- Requires `JWT_SECRET_KEY`.
- Uses `DATABASE_URL`, with development fallback to SQLite if Postgres host is unreachable.
- Rewrites docker hostnames (`resume_postgres`, `resume_elasticsearch`) to `localhost` when backend runs outside Docker in development.

### 4.3 App Startup (`app/main.py`)
- Configures logging and CORS.
- Includes API router under `/api`.
- Creates missing DB tables on startup via `Base.metadata.create_all`.
- Exposes `GET /` health endpoint.

### 4.4 API Endpoints (`app/api/routes.py`)

Health:
- `GET /api/health`
- `GET /api/health/full`

Auth:
- `POST /api/auth/register`
- `POST /api/auth/login`

Resume:
- `POST /api/resumes/upload` (auth required, PDF-only, <=10MB)
- `POST /api/resumes/{resume_id}/analyze` (auth required, owner-only)

Jobs:
- `POST /api/jobs` (auth required)
- `DELETE /api/jobs/{job_id}` (auth required, owner-only)
- `POST /api/admin/reindex/jobs` (auth required; currently no strict admin role check)

Search:
- `GET /api/search/jobs`
  - query params: `q`, `location`, `skills`, `page`, `size`, `sort_by`, `order`

Matching:
- `GET /api/match/resume/{resume_id}/job/{job_id}`
- `GET /api/gap/resume/{resume_id}/job/{job_id}`

### 4.5 Data Models
`users`:
- `id`, `email`, `hashed_password`, `is_active`, `created_at`

`resumes`:
- `id`, `user_id`, `filename`, `content`, `skills` (JSON), `experience_years`, timestamps

`jobs`:
- `id`, `title`, `company`, `description`, `required_skills` (JSON), `location`, `owner_id`, `salary`, `url`, `created_at`

### 4.6 Search Indexing
Job index: `jobs`
- Fields include `title`, `company`, `description`, `required_skills`, `location`, `salary`
- Search uses `multi_match` with title boost (`title^3`) and fuzziness `AUTO`
- Skill filtering via `terms` query

Resume indexing is performed after analysis for searchable skill/content use cases.

## 5. Frontend Details

### 5.1 Stack
- React 19 + TypeScript
- Axios API client with auth interceptor
- Tailwind CSS

### 5.2 Pages/Features
- `Login.tsx`: register/login using backend auth
- `ResumeUpload.tsx`: upload + analyze workflow
- `JobCreate.tsx`: create job posting
- `JobSearch.tsx`: search jobs and render results via `JobCard`

### 5.3 API Client
- Base URL: `VITE_API_URL` or `http://localhost:8000/api`
- Adds `Authorization: Bearer <token>` from `localStorage`

## 6. Docker Setup

`docker-compose.yml` services:
- `backend` on `8000`
- `postgres` on `5432`
- `elasticsearch` on `9200`

Backend starts with:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 7. Local Runbook

### 7.1 Docker (recommended)
```bash
docker compose up --build
```

### 7.2 Frontend local dev
```bash
cd frontend
npm install
npm run dev
```

### 7.3 Backend local dev (without Docker)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 8. Required Environment Variables
Set these in `backend/.env`:
- `ENV`
- `APP_NAME`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`
- `ELASTICSEARCH_URL`
- `GEMINI_API_KEY` (needed for analyze endpoint)
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

## 9. Known Issues / Gaps
- No Alembic migrations yet; schema is startup-created.
- Secrets have existed in tracked files previously; rotate credentials/keys.
- `frontend/src/services/matchService.ts` has `topResumesForJob`, but backend route is missing.
- `POST /api/admin/reindex/jobs` should enforce admin role in production.

## 10. Recommended Next Improvements
1. Add Alembic migrations and migration CI checks.
2. Add role-based access control for admin endpoints.
3. Add tests for auth, upload/analyze, search, and matching.
4. Implement missing top-resumes endpoint or remove unused client call.
5. Introduce refresh token flow and stronger client auth storage strategy.
