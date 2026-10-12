import logging
from app.db.base import Base
from app.db.session import engine
# Import all models to ensure they are registered with Base.metadata before creating tables
from app.models.user import User  # noqa: F401

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Create database tables defined by SQLAlchemy ORM models."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
        raise e
