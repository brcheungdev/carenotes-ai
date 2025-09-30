from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

from .config import settings


db = SQLAlchemy(session_options={'expire_on_commit': False})
engine = create_engine(settings.MYSQL_URL, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def get_session():
    return SessionLocal()
