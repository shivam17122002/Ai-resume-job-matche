# AI Resume Analyzer & Job Matcher

Lightweight full-stack app: FastAPI backend, React + Vite frontend, PostgreSQL, Elasticsearch. Supports resume upload (PDF), AI-based skill extraction, job CRUD, search, and match scoring.

Quick start (dev):

1. Copy backend env example:

```bash
cp backend/.env.example backend/.env
# edit backend/.env to set JWT secret and any Postgres details
```

2. Start with Docker Compose (recommended):

```bash
docker compose up --build
```

3. Frontend (if not using Docker):

```bash
cd frontend
npm install
npm run dev
```

API highlights:
- `POST /api/auth/register` — register
- `POST /api/auth/login` — obtain JWT
- `POST /api/resumes/upload` — upload PDF (requires Bearer token)
- `POST /api/resumes/{id}/analyze` — run AI analysis (requires token)
- `POST /api/jobs` — create job (requires token)
- `GET /api/search/jobs` — search ES

Notes:
- Fill secrets in `backend/.env` before production. Do not commit secrets.
- Use Alembic for DB migrations (see INTERVIEW.md for commands).
