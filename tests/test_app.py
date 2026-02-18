"""Tests for application startup, root route, database init, and static files."""

from sqlalchemy import inspect, create_engine

from app.database import Base
import app.models  # noqa: F401


def test_root_redirects_to_setup_when_no_user(client):
    """Root / should redirect to /setup when no user exists (302)."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/setup"


def test_root_redirects_to_login_when_user_exists(client, db_session):
    """Root / should redirect to /login when a user exists (302)."""
    from app.models.user import User

    user = User(username="testuser", hashed_password="fakehash")
    db_session.add(user)
    db_session.commit()

    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"


def test_base_metadata_creates_user_table():
    """Base.metadata.create_all() should create the users table from registered models."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables

    engine.dispose()


def test_static_css_served(client):
    """Static CSS file should be accessible at /static/css/style.css."""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200


def test_static_js_served(client):
    """Static JS file should be accessible at /static/js/app.js."""
    response = client.get("/static/js/app.js")
    assert response.status_code == 200


def test_setup_page_renders(client):
    """GET /setup should return 200 and render the setup template."""
    response = client.get("/setup")
    assert response.status_code == 200
    assert "Setup" in response.text


def test_database_file_not_accessible(client):
    """SQLite database file must not be served via any web route (NFR10 / AC #6)."""
    response = client.get("/bmad_demo.db")
    assert response.status_code == 404

    response = client.get("/static/../bmad_demo.db")
    assert response.status_code == 404
