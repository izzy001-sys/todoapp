"""
Configuration management for the application.
Loads environment variables from .env file and provides application settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ============================================
# Security Settings
# ============================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-123456")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ACCESS_COOKIE_NAME = os.getenv("ACCESS_COOKIE_NAME", "access_token")
AUTH_HEADER_PREFIX = os.getenv("AUTH_HEADER_PREFIX", "Bearer ")  # Note: includes trailing space

# ============================================
# Database Configuration
# ============================================
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", 
    "sqlite:///./todo_app.db"
)

# ============================================
# CORS Configuration
# ============================================
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
CORS_METHODS = os.getenv("CORS_METHODS", "*").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")

# ============================================
# Application Settings
# ============================================
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

