"""
Database configuration and ORM models.

Uses SQLAlchemy's async engine backed by aiosqlite writing to a local `test.db` file.
`expire_on_commit=False` keeps ORM attributes accessible after a commit without
requiring an extra round-trip to refresh them.

Models:
  Post  — A user-created post consisting of a caption and a hosted media file.

Exports used by app.py:
  create_db_and_tables()  Called at startup to auto-create any missing tables.
  get_async_session()     FastAPI dependency that opens and yields a scoped
                          AsyncSession, committing or rolling back on exit.
"""
from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session