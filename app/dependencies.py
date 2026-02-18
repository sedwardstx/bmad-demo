"""FastAPI dependencies for dependency injection."""

import logging
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
