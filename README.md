# AI Resume Analyzer & Job Matcher

Full-stack application for resume parsing, AI-powered skill extraction, job posting, Elasticsearch-based search, and resume-to-job matching.

## Tech Stack
- Backend: FastAPI, SQLAlchemy, PostgreSQL (or SQLite fallback in local dev), Elasticsearch
- AI: Gemini (`google-generativeai`)
- Auth: JWT (`python-jose`) + password hashing (`passlib[bcrypt]`)
- Frontend: React 19, TypeScript, Vite, Tailwind CSS
- Infra: Docker Compose

## Project Structure
```
Resume_Analyzer/
|- backend/
|  |- app/
|  |  |- api/routes.py
|  |  |- core/{config.py,security.py,elasticsearch.py}
|  |  |- db/database.py
|  |  |- models/{user.py,resume.py,job.py}
|  |  |- services/
|- frontend/
|  |- src/{pages,components,services,types}
|- projectInfo/
|  |- INTERVIEW.md
|  |- PROJECT_DOCUMENTATION.md
|- docker-compose.yml
```

## Prerequisites
- Docker + Docker Compose
- Node.js 18+ (for local frontend run)
- Python 3.11+ (for local backend run)

## Environment Configuration
Create `backend/.env` with at least:
- `ENV=development`
- `APP_NAME=AI Resume Analyzer & Job Matcher`
- `DATABASE_URL=postgresql://<user>:<password>@resume_postgres:5432/resume_db`
- `JWT_SECRET_KEY=<strong-secret>`
- `JWT_ALGORITHM=HS256`
- `JWT_EXPIRE_MINUTES=60`
- `ELASTICSEARCH_URL=http://resume_elasticsearch:9200`
- `GEMINI_API_KEY=<optional-but-required-for-analyze-endpoint>`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

Important: rotate any previously exposed secrets and never commit real keys.

## Run with Docker (Recommended)
```bash
docker compose up --build
```

Services:
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Elasticsearch: `http://localhost:9200`
- PostgreSQL: `localhost:5432`

## Run Frontend Locally
```bash
cd frontend
npm install
npm run dev
```
Frontend default URL: `http://localhost:5173`

## API Overview

Health:
- `GET /` - backend health
- `GET /api/health`
- `GET /api/health/full` (checks DB + Elasticsearch)

Auth:
- `POST /api/auth/register`
- `POST /api/auth/login`

Resume:
- `POST /api/resumes/upload` (Bearer token, PDF only, max 10MB)
- `POST /api/resumes/{resume_id}/analyze` (Bearer token, owner only)

Jobs:
- `POST /api/jobs` (Bearer token)
- `DELETE /api/jobs/{job_id}` (Bearer token, owner only)
- `GET /api/search/jobs` (`q`, `location`, `skills`, `page`, `size`, `sort_by`, `order`)
- `POST /api/admin/reindex/jobs` (protected, currently token-based)

Matching:
- `GET /api/match/resume/{resume_id}/job/{job_id}`
- `GET /api/gap/resume/{resume_id}/job/{job_id}`

## Current Frontend Features
- Login/Register page
- Resume upload + analyze flow
- Job create form
- Job search page and result cards

Navigation is component-state based (no React Router yet).

## Known Gaps / Notes
- `frontend/src/services/matchService.ts` includes `topResumesForJob`, but backend route is not implemented.
- No Alembic migrations yet; tables are created on startup via `Base.metadata.create_all`.
- Admin reindex route does not yet enforce role-based authorization.

## Documentation
- Detailed technical docs: `projectInfo/PROJECT_DOCUMENTATION.md`
- Interview prep notes: `projectInfo/INTERVIEW.md`
