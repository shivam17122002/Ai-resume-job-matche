# Project Interview Notes — AI Resume Analyzer & Job Matcher

Summary:
- Backend: FastAPI, SQLAlchemy, Pydantic, PostgreSQL (or sqlite for dev), Elasticsearch for full-text job search.
- Frontend: React 19 + TypeScript + Vite, Tailwind CSS for UI.
- Auth: JWT using `python-jose`, passwords hashed with `passlib[bcrypt]`.
- AI: optional Gemini/OpenAI integration for resume analysis (controlled by `GEMINI_API_KEY`).

Architecture:
- Layered: `models` → `schemas` → `services` → `api/routes` → `core` (config, ES client, security) → `db`.
- PostgreSQL is source of truth for jobs/resumes/users; Elasticsearch provides search and ranking.

Key Endpoints:
- `POST /api/auth/register` — body `{email, password}` → returns created user (no token).
- `POST /api/auth/login` — body `{email, password}` → returns `{access_token, token_type}`.
- `POST /api/resumes/upload` — multipart file (pdf) — requires `Authorization: Bearer <token>` — extracts text, stores resume.
- `POST /api/resumes/{id}/analyze` — runs AI analysis, saves skills array (JSON) and experience. Indexes into ES.
- `POST /api/jobs` — create job, requires auth; owner_id saved; job is indexed into ES.
- `GET /api/search/jobs` — params `q, location, skills[], page, size` — uses multi_match with fuzziness and title boosting.
- `DELETE /api/jobs/{id}` — owner-only delete (removes from DB and ES).

Important implementation notes:
- Skills stored as `JSON` (maps to Postgres JSONB) for efficient queries and to feed ES as keyword arrays.
- ES mapping: `title` text (with `raw` keyword), `description` text, `required_skills` keyword, `location` keyword, `salary` keyword.
- Job search uses `multi_match` (title^3 boosting) and `terms` filter for skills; uses `fuzziness: AUTO` for resilient matching.
- Resume parsing uses `pdfplumber` with 10MB limit; scanned PDFs without text will error.
- JWT secret is required in production (`JWT_SECRET_KEY`).

Deployment checklist / commands:
- Build and run with Docker Compose: `docker compose up --build`.
- For production backend: build image, run with Gunicorn + Uvicorn workers (suggested `gunicorn -k uvicorn.workers.UvicornWorker app.main:app -w 4`).
- Use Alembic to manage DB migrations: `alembic init alembic`, then `alembic revision --autogenerate -m "init"`, `alembic upgrade head`.

Common interview questions & short answers:
- Q: Why use Elasticsearch alongside Postgres?
  A: Postgres is the source of truth and supports relational queries; ES provides advanced full-text search, fuzziness, relevance scoring, and faster search over large text fields.

- Q: How are skills stored and why?
  A: Stored as JSON/JSONB in Postgres and as keyword arrays in ES. This allows structural queries (terms) and efficient indexing for skill-based filters.

- Q: How is authentication implemented?
  A: Passwords hashed with bcrypt via `passlib`. JWTs are created with `python-jose`, stored client-side (localStorage) and sent in `Authorization` header. Backend validates token and loads user via dependency injection.

- Q: How does resume analysis work?
  A: Text extracted from PDF using `pdfplumber`, then sent to AI model (Gemini/OpenAI) to extract skills, experience years and role; result validated with Pydantic `ResumeAnalysisResult` before saving.

- Q: How to ensure security in production?
  A: Use strong JWT secrets (env), HTTPS, rate limiting, CORS restrictions, store tokens securely (prefer refresh tokens + httpOnly cookies), avoid storing secrets in repo, and enable ES security in production.

- Q: How to run migrations?
  A: Install `alembic` and configure `alembic.ini` with `sqlalchemy.url` pointing to `DATABASE_URL`. Use `alembic revision --autogenerate` then `alembic upgrade head`.

Prep tips for demo:
- Demonstrate upload→analyze→index→search flow: upload a PDF, wait for analysis, search by skill to surface job, show match score.
- Show the DB (psql) that skills stored as JSON and ES index documents via `_search` API.
