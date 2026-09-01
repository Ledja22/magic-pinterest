from sqlalchemy import text
from .db import Base
from .db.session import get_engine

# Simple auto-migration/initialization for local dev

def init_db():
    engine = get_engine()
    # Ensure pgvector extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    # Create tables
    Base.metadata.create_all(bind=engine)
