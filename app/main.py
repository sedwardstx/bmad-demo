"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import init_db
from app.dependencies import get_db
from app.models.user import User
from app.routers.auth import router as auth_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_HERE = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — initialise database on startup."""
    init_db()
    yield


app = FastAPI(title="bmad-demo", lifespan=lifespan)

# Static files — served ONLY from app/static/ (SQLite DB is NOT in this tree)
app.mount("/static", StaticFiles(directory=_HERE / "static"), name="static")

# Routers
app.include_router(auth_router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    """Redirect to /setup if no user exists, otherwise to /login."""
    # TODO: Move DB query to auth_service.user_exists(db) in Story 1.2
    user_count = db.query(User).count()
    if user_count == 0:
        return RedirectResponse(url="/setup", status_code=302)
    return RedirectResponse(url="/login", status_code=302)
