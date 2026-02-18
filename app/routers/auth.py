"""Auth routes — login, logout, and first-run setup."""

import logging
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/setup")
def setup_page(request: Request):
    """First-run setup page (placeholder — implemented in Story 1.2)."""
    return templates.TemplateResponse(request, "setup.html")
