from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AI Resume Analyzer & Job Matcher")
    ENV: str = os.getenv("ENV", "development")

    # Provide a sensible default for local development (sqlite file)
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        if ENV == "production":
            raise ValueError("DATABASE_URL environment variable is not set")
        # development fallback
        DATABASE_URL = f"sqlite:///./{os.getenv('DB_FILENAME','dev.db')}"

    # Normalize DATABASE_URL: if credentials contain extra '@' (e.g., in password),
    # URL-encode those '@' characters so SQLAlchemy can parse the URL.
    try:
        if "@" in DATABASE_URL:
            scheme_split = DATABASE_URL.split("://", 1)
            if len(scheme_split) == 2:
                scheme, rest = scheme_split
                # If more than one '@' in the rest, then password likely contains '@'
                if rest.count("@") > 1:
                    creds, host_part = rest.rsplit("@", 1)
                    safe_creds = creds.replace("@", "%40")
                    DATABASE_URL = f"{scheme}://{safe_creds}@{host_part}"
    except Exception:
        # If normalization fails, keep the original URL and let engine raise a clear error later
        pass

    # For production require a JWT secret; for development use a default but warn
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        if ENV == "production":
            raise ValueError("JWT_SECRET_KEY environment variable is not set")
        # development fallback (not secure for prod)
        JWT_SECRET_KEY = os.getenv("DEV_JWT_SECRET", "dev-secret")
    
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

settings = Settings()
