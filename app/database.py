"""SQLAlchemy database engine, session, and initialization."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

logger = logging.getLogger(__name__)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base for all models."""
    pass


def init_db() -> None:
    """Create all tables from registered models."""
    import app.models  # noqa: F401 — ensure models are imported so Base knows about them

    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized — all tables created.")
