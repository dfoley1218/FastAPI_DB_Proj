"""
FastAPI application — route definitions.

Endpoints:
  POST /upload  Accepts a multipart form (file + caption). Writes a Post record
                to the database and returns the saved row as JSON.
                File upload to ImageKit is stubbed with placeholder values for now.

  GET  /feed    Returns all posts ordered newest-first as a JSON array.

The `lifespan` context manager runs once on startup: it calls `create_db_and_tables`
so the SQLite schema is automatically created before the first request arrives.
"""
from select import select

from fastapi import FastAPI, File, UploadFile, Form, Depends
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    
    post = Post(
        caption=caption,
        url="dummyurl",
        file_type="photo",
        file_name="dummyname"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.fetchall()]
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return posts_data
