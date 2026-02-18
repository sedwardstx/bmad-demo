"""Application configuration loaded from .env file."""

import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bmad_demo.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-to-a-random-secret")
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
