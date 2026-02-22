from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import router
from app.core.config import settings
import logging
from logging.config import dictConfig


# Basic logging configuration
LOGGING = {
    "version": 1,
    "formatters": {"default": {"fmt": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
    "root": {"level": "INFO", "handlers": ["console"]},
}

dictConfig(LOGGING)
logger = logging.getLogger(__name__)


# Create app
app = FastAPI(title=settings.APP_NAME)


# Apply CORS from env-friendly defaults
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
if settings.ENV != "production":
    origins.append("http://frontend:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables if missing (for development)
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured on startup")
    except Exception:
        logger.exception("Failed to create database tables on startup")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Include API routes
app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "Backend is running"}
