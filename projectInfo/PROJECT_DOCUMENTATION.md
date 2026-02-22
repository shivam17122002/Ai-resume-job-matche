# AI Resume Analyzer & Job Matcher - Complete Project Documentation

## 📋 Project Overview

**Project Name:** AI Resume Analyzer & Job Matcher  
**Status:** Under Development (Foundation Phase Complete)  
**Last Updated:** January 31, 2026  
**Location:** `c:\Users\Lenovo\Projects\Resume_Analyzer\ai-resume-job-matcher`

### Purpose
A full-stack application that:
- Analyzes resumes using AI (OpenAI API)
- Matches resumes with job opportunities
- Provides skill gap analysis
- Searches jobs using Elasticsearch
- Stores data in PostgreSQL database

---

## 🏗️ Project Architecture

### Architecture Type: Microservices with Docker
```
┌─────────────────────────────────────────────────────┐
│        Frontend (React + TypeScript + Vite)         │
│     Running on: http://localhost:5173               │
└──────────────────┬──────────────────────────────────┘
                   │ CORS Enabled
                   │ API Calls
┌──────────────────▼──────────────────────────────────┐
│   Backend (FastAPI - Python)                        │
│   Running on: http://localhost:8000                 │
│   - REST APIs for Resume & Job management           │
│   - AI Processing with OpenAI                       │
│   - Database ORM with SQLAlchemy                    │
└──────────────┬─────────────────┬────────────────────┘
               │                 │
        ┌──────▼──────┐    ┌─────▼────────┐
        │ PostgreSQL  │    │ Elasticsearch│
        │ Port: 5432  │    │ Port: 9200   │
        └─────────────┘    └──────────────┘
```

---

## 📁 Complete Project Structure

```
ai-resume-job-matcher/
│
├── .gitignore                          # Git ignore rules (protects .env and credentials)
├── docker-compose.yml                  # Docker orchestration file
├── README.md                           # Project documentation
│
├── backend/                            # FastAPI Backend (Python)
│   ├── .env                            # Environment variables (PROTECTED in .gitignore)
│   ├── .env.example                    # Template for .env (SAFE to share)
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Docker image for backend
│   ├── venv/                           # Virtual environment (local development)
│   │
│   └── app/                            # Main application package
│       ├── __init__.py                 # Package initialization
│       ├── main.py                     # FastAPI application entry point
│       │                               # Features:
│       │                               # - CORS middleware configured
│       │                               # - Health check endpoint at /
│       │
│       ├── core/                       # Core configuration
│       │   ├── __init__.py
│       │   └── config.py               # Settings management
│       │                               # - Environment variable loading
│       │                               # - Validation with error handling
│       │                               # - Type hints for all settings
│       │
│       ├── db/                         # Database layer
│       │   ├── __init__.py
│       │   └── database.py             # SQLAlchemy setup
│       │                               # - Database engine configuration
│       │                               # - Session management
│       │                               # - Base ORM class
│       │
│       ├── models/                     # SQLAlchemy ORM Models
│       │   ├── __init__.py
│       │   ├── resume.py               # Resume database model
│       │   │                           # - Fields: id, user_id, filename, content,
│       │   │                           #           skills, experience_years
│       │   └── job.py                  # Job database model
│       │                               # - Fields: id, title, company, description,
│       │                               #           required_skills, location, salary, url
│       │
│       ├── schemas/                    # Pydantic validation schemas
│       │   ├── __init__.py
│       │   ├── resume.py               # Resume request/response schema
│       │   │                           # - ResumeBase, ResumeCreate, Resume
│       │   └── job.py                  # Job request/response schema
│       │                               # - JobBase, JobCreate, Job
│       │
│       ├── api/                        # API routes & endpoints
│       │   ├── __init__.py
│       │   └── routes.py               # API route handlers
│       │                               # - GET /api/health - Health check
│       │                               # - Database dependency injection
│       │
│       └── services/                   # Business logic layer
│           ├── __init__.py
│           ├── resume_service.py       # Resume operations
│           │                           # - create_resume()
│           │                           # - get_resume()
│           │                           # - get_user_resumes()
│           │                           # - delete_resume()
│           └── job_service.py          # Job operations
│                                       # - create_job()
│                                       # - get_job()
│                                       # - get_all_jobs()
│                                       # - delete_job()
│
└── frontend/                           # React + TypeScript Frontend
    ├── package.json                    # Node.js dependencies
    ├── tsconfig.json                   # TypeScript configuration
    ├── tsconfig.app.json               # App-specific TypeScript config
    ├── tsconfig.node.json              # Node-specific TypeScript config
    ├── vite.config.ts                  # Vite build configuration
    ├── eslint.config.js                # ESLint rules
    ├── index.html                      # HTML entry point
    │
    ├── public/                         # Static public assets
    │
    └── src/                            # React source code
        ├── main.tsx                    # Entry point (React DOM initialization)
        ├── App.tsx                     # Main App component (Currently: Vite starter template)
        ├── App.css                     # App styles
        ├── index.css                   # Global styles
        └── assets/                     # Images and other assets
```

---

## 🔧 Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11 | Programming language |
| FastAPI | Latest | REST API framework |
| Uvicorn | Latest | ASGI server |
| SQLAlchemy | Latest | ORM (Object-Relational Mapping) |
| Pydantic | Latest | Data validation |
| PostgreSQL | 15 | Relational database |
| psycopg2-binary | Latest | PostgreSQL adapter |
| python-dotenv | Latest | Environment variables |
| python-multipart | Latest | File upload support |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19.2.0 | UI library |
| React-DOM | 19.2.0 | React rendering |
| TypeScript | 5.9.3 | Type-safe JavaScript |
| Vite | 7.2.4 | Build tool |
| ESLint | 9.39.1 | Code linting |

### Infrastructure
| Service | Version | Port | Purpose |
|---------|---------|------|---------|
| PostgreSQL | 15 | 5432 | Main database |
| Elasticsearch | 8.11.0 | 9200 | Full-text search engine |
| Docker | Latest | - | Containerization |
| Docker Compose | Latest | - | Container orchestration |

---

## 📦 Dependencies

### Backend (requirements.txt)
```
fastapi           # REST API framework
uvicorn           # ASGI server
python-multipart  # File upload handling
pydantic          # Data validation
sqlalchemy        # ORM
psycopg2-binary   # PostgreSQL connection
python-dotenv     # Environment variable management
```

### Frontend (package.json)
```
dependencies:
  - react: ^19.2.0
  - react-dom: ^19.2.0

devDependencies:
  - @vitejs/plugin-react: ^5.1.1
  - typescript: ~5.9.3
  - vite: ^7.2.4
  - eslint: ^9.39.1
  - @types/react: ^19.2.5
  - @types/react-dom: ^19.2.3
  - typescript-eslint: ^8.46.4
```

---

## 🐳 Docker & Container Setup

### Docker Compose Configuration (docker-compose.yml)

#### Backend Service
- **Image:** Built from `./backend/Dockerfile`
- **Container Name:** `resume_backend`
- **Port:** 8000 (exposed to host)
- **Environment:** Loads from `./backend/.env`
- **Dependencies:** Waits for PostgreSQL and Elasticsearch
- **Volumes:** Mounts backend directory for hot-reload development
- **Command:** `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

#### PostgreSQL Service
- **Image:** postgres:15
- **Container Name:** `resume_postgres`
- **Port:** 5432
- **Database:** resume_db
- **User:** resume_user
- **Password:** resume_pass
- **Volume:** Named volume `pgdata` for persistent data

#### Elasticsearch Service
- **Image:** elasticsearch:8.11.0
- **Container Name:** `resume_elasticsearch`
- **Port:** 9200
- **Config:** Single-node cluster, security disabled (for development)
- **Memory:** -Xms512m -Xmx512m
- **Volume:** Named volume `esdata` for persistent data

### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
EXPOSE 8000
```

---

## 🔐 Security & Configuration

### Environment Variables (.env)
```
# Application Settings
APP_NAME=AI Resume Analyzer & Job Matcher
ENV=development

# Database Connection
DATABASE_URL=postgresql://resume_user:resume_pass@localhost:5432/resume_db

# JWT Authentication
JWT_SECRET_KEY=super_secret_key_change_later
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# AI Services
OPENAI_API_KEY=your_openai_api_key_here

# Search Service
ELASTICSEARCH_URL=http://localhost:9200
```

### .env.example (Safe Template)
Provided for team members - doesn't contain real secrets.

### .gitignore (Protections)
```
.env                    # Real credentials (NEVER commit)
.env.local
.env.*.local
__pycache__/
node_modules/
*.pyc
.vscode/
.idea/
build/
dist/
.DS_Store
```

### Config.py (Settings Management)
- Loads environment variables with defaults
- Validates critical variables at startup
- Type hints for IDE support and validation
- Raises errors if required variables missing

---

## 🌐 API Endpoints

### Currently Implemented
| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| GET | `/` | Health check | ✅ Working |
| GET | `/api/health` | API health check | ✅ Working |

### CORS Configuration
**Enabled Origins:**
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (Alternative port)
- http://frontend:5173 (Docker network)

---

## 📊 Database Models

### Resume Model
```python
Table: resumes
- id (INT, Primary Key)
- user_id (INT, Foreign Key)
- filename (VARCHAR)
- content (TEXT)
- skills (TEXT, JSON format)
- experience_years (FLOAT)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Job Model
```python
Table: jobs
- id (INT, Primary Key)
- title (VARCHAR)
- company (VARCHAR)
- description (TEXT)
- required_skills (TEXT, JSON format)
- location (VARCHAR)
- salary (VARCHAR)
- url (VARCHAR)
- created_at (DATETIME)
```

---

## 🔄 Service Layer

### ResumeService (resume_service.py)
```python
Methods:
- create_resume(db, resume, user_id) → Resume object
- get_resume(db, resume_id) → Resume object
- get_user_resumes(db, user_id) → List[Resume]
- delete_resume(db, resume_id) → Deleted Resume object
```

### JobService (job_service.py)
```python
Methods:
- create_job(db, job) → Job object
- get_job(db, job_id) → Job object
- get_all_jobs(db, skip, limit) → List[Job]
- delete_job(db, job_id) → Deleted Job object
```

---

## ✅ Completed Tasks (January 31, 2026)

1. **✅ Security Fixes**
   - Removed exposed OpenAI API key from .env
   - Created .env.example template
   - Added .gitignore with comprehensive protections

2. **✅ CORS Configuration**
   - Added CORSMiddleware to FastAPI
   - Configured for local development and Docker environments
   - Enabled credentials and all HTTP methods for development

3. **✅ Environment Variable Validation**
   - Enhanced config.py with type hints
   - Added validation for critical variables
   - Implemented error handling with meaningful messages
   - Set defaults for optional variables

4. **✅ Database Configuration**
   - Updated database.py to use config settings
   - Removed hardcoded credentials
   - Proper SQLAlchemy setup with session management

5. **✅ Project Structure**
   - Added __init__.py files to all packages
   - Created ORM models (Resume, Job)
   - Created Pydantic schemas (Resume, Job)
   - Created API routes file with dependency injection
   - Created service layer with CRUD operations

6. **✅ Backend Foundation**
   - FastAPI app with middleware configured
   - Health check endpoints
   - Proper layered architecture (models → schemas → services → API)

---

## 🚀 TODO - Next Steps to Complete

### Phase 1: Backend API Completion
- [ ] Implement Resume upload endpoint (POST /api/resumes)
- [ ] Implement Resume retrieval endpoints (GET /api/resumes, GET /api/resumes/{id})
- [ ] Implement Job creation endpoint (POST /api/jobs)
- [ ] Implement Job search endpoint (GET /api/jobs/search)
- [ ] Add authentication/JWT endpoints (POST /api/auth/login, POST /api/auth/register)
- [ ] Add error handling and validation

### Phase 2: AI Integration
- [ ] Create resume parser service (extract text from PDF/DOC)
- [ ] Create resume analyzer service (use OpenAI API to extract skills, experience)
- [ ] Create job matcher service (compare resume with job descriptions)
- [ ] Create skill gap analyzer (identify missing skills)

### Phase 3: Search Integration
- [ ] Configure Elasticsearch indexing
- [ ] Create job indexing service
- [ ] Implement full-text search for jobs
- [ ] Add filters (location, salary range, skills)

### Phase 4: Frontend Development
- [ ] Replace Vite starter template with actual UI
- [ ] Create resume upload component
- [ ] Create job search/browse component
- [ ] Create match results display
- [ ] Create user dashboard
- [ ] Implement authentication UI
- [ ] Add styling and responsive design

### Phase 5: Testing & Deployment
- [ ] Unit tests for backend services
- [ ] Integration tests for API endpoints
- [ ] Frontend component tests
- [ ] Docker deployment verification
- [ ] CI/CD pipeline setup
- [ ] Production environment configuration

---

## 🏃 How to Run

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15 (if not using Docker)

### Option 1: Using Docker Compose (Recommended)
```bash
cd ai-resume-job-matcher
docker-compose up -d
```
This starts:
- Backend at http://localhost:8000
- Frontend at http://localhost:5173 (if you run dev separately)
- PostgreSQL at localhost:5432
- Elasticsearch at localhost:9200

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Environment Setup
1. Copy `.env.example` to `.env` in the backend directory
2. Update `.env` with your actual values:
   - `JWT_SECRET_KEY` - Generate a secure random key
   - `OPENAI_API_KEY` - Get from OpenAI dashboard
   - `DATABASE_URL` - Update if using custom DB

---

## 📝 Important Notes

1. **API Key Security**
   - The exposed OpenAI API key has been removed
   - Update `JWT_SECRET_KEY` and `OPENAI_API_KEY` in `.env` before production
   - Never commit `.env` files

2. **Database**
   - Default credentials in docker-compose should be changed for production
   - PostgreSQL runs on port 5432
   - Elasticsearch runs on port 9200 (no authentication in development)

3. **CORS**
   - Currently allows all methods and headers
   - Should be restricted for production
   - Frontend origins are configured for development

4. **Frontend**
   - Currently using Vite starter template
   - Needs to be replaced with actual application UI
   - TypeScript is configured and ready to use

5. **Python Version**
   - Project requires Python 3.11+
   - Uses modern Python features (type hints, pydantic v2)

---

## 🤝 Team Collaboration

### For New Team Members
1. Clone the repository
2. Copy `backend/.env.example` to `backend/.env`
3. Fill in required secrets (contact tech lead)
4. Run `docker-compose up -d`
5. Backend is ready at http://localhost:8000
6. Frontend development: `cd frontend && npm install && npm run dev`

### Code Organization
- **Services**: Business logic layer (one service per feature)
- **Models**: Database ORM models
- **Schemas**: Pydantic validation schemas
- **API**: Route handlers
- **DB**: Database configuration
- **Core**: Configuration management

---

## 📚 Additional Resources

- FastAPI Docs: http://localhost:8000/docs (when running)
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Elasticsearch Docs: https://www.elastic.co/guide/
- React Docs: https://react.dev
- Vite Docs: https://vite.dev

---

**Last Updated:** January 31, 2026  
**Status:** Foundation Complete - Ready for Feature Development
