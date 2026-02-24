from dotenv import load_dotenv
import os
import socket
from typing import Optional
from urllib.parse import urlparse, urlunparse

load_dotenv()


def _is_running_in_docker() -> bool:
    return os.path.exists("/.dockerenv")


def _replace_hostname(url: str, from_host: str, to_host: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname != from_host:
        return url

    auth_part = ""
    if parsed.username:
        auth_part = parsed.username
        if parsed.password:
            auth_part += f":{parsed.password}"
        auth_part += "@"

    port_part = f":{parsed.port}" if parsed.port else ""
    netloc = f"{auth_part}{to_host}{port_part}"
    return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))


def _is_host_reachable(host: str, port: int, timeout_sec: float = 0.4) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except OSError:
        return False


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

    # Local host mapping: Docker service names won't resolve when backend runs directly on host OS.
    if ENV != "production" and not _is_running_in_docker():
        DATABASE_URL = _replace_hostname(DATABASE_URL, "resume_postgres", "localhost")

    if ENV != "production":
        parsed_db_url = urlparse(DATABASE_URL)
        if parsed_db_url.scheme.startswith("postgresql"):
            db_host = parsed_db_url.hostname or "localhost"
            db_port = parsed_db_url.port or 5432
            if not _is_host_reachable(db_host, db_port):
                DATABASE_URL = f"sqlite:///./{os.getenv('DB_FILENAME','dev.db')}"

    # For production require a JWT secret; for development use a default but warn
    JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is not set")
    
    try:
        JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    except ValueError:
       raise ValueError("JWT_EXPIRE_MINUTES must be an integer")

    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    if ENV != "production" and not _is_running_in_docker():
        ELASTICSEARCH_URL = _replace_hostname(ELASTICSEARCH_URL, "resume_elasticsearch", "localhost")

settings = Settings()
