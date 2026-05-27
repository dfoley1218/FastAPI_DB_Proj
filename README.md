# FastAPI Post Feed API

A lightweight REST API built with FastAPI and SQLAlchemy that lets clients upload media posts and retrieve a chronological feed. Designed as a learning project for async Python web development with a local SQLite database.

---

## Features

- **File upload endpoint** — accepts a multipart form with a file and caption, persists a post record to the database
- **Feed endpoint** — returns all posts ordered newest-first
- **Async throughout** — FastAPI + SQLAlchemy async engine + aiosqlite; no blocking I/O on the request thread
- **Auto schema creation** — the database table is created on startup if it does not exist; no migration tooling required
- **ImageKit-ready** — environment variables for [ImageKit](https://imagekit.io/) CDN are in place for wiring up real file hosting

---

## Tech Stack

| Layer | Library |
|---|---|
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ASGI server | [Uvicorn](https://www.uvicorn.org/) |
| ORM | [SQLAlchemy](https://docs.sqlalchemy.org/) (async) |
| Database driver | [aiosqlite](https://github.com/omnilib/aiosqlite) |
| Data validation | [Pydantic](https://docs.pydantic.dev/) (bundled with FastAPI) |
| Image hosting | [ImageKit Python SDK](https://github.com/imagekit-developer/imagekit-python) |
| Package manager | [uv](https://github.com/astral-sh/uv) |

---

## Project Structure

```
APItut/
├── main.py            # Entry point — launches Uvicorn
├── pyproject.toml     # Project metadata and dependencies
├── .env               # ImageKit credentials (not committed)
└── app/
    ├── app.py         # FastAPI app instance and route handlers
    ├── db.py          # SQLAlchemy engine, ORM models, session factory
    └── schemas.py     # Pydantic schemas for request validation
```

---

## How It Works

### Startup

`main.py` launches Uvicorn pointing at `app.app:app`. FastAPI's `lifespan` context manager fires `create_db_and_tables()` before the first request, creating the `posts` table in `test.db` if it doesn't already exist.

### Database Model

The single `Post` model lives in `app/db.py`:

| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key, auto-generated |
| `caption` | Text | User-supplied description |
| `url` | String | Hosted file URL (ImageKit or placeholder) |
| `file_type` | String | e.g. `"photo"`, `"video"` |
| `file_name` | String | Original or stored filename |
| `created_at` | DateTime | Set automatically on insert |

### Session Management

`get_async_session()` is a FastAPI dependency injected into each route handler. It opens a scoped `AsyncSession` using the configured `async_sessionmaker`, yields it for use in the handler, then cleans up when the response is sent.

---

## API Endpoints

### `POST /upload`

Upload a new post.

**Request** — `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | binary | yes | The media file to upload |
| `caption` | string | yes | Text caption for the post |

**Response** — the newly created `Post` row as JSON.

```json
{
  "id": "a3f1c2d4-...",
  "caption": "Hello world",
  "url": "dummyurl",
  "file_type": "photo",
  "file_name": "dummyname",
  "created_at": "2026-05-27T12:00:00"
}
```

> **Note:** `url` and `file_name` are currently stubbed with placeholder strings. ImageKit upload logic is the next step.

---

### `GET /feed`

Retrieve all posts, newest first.

**Response** — JSON array of post objects.

```json
[
  {
    "id": "a3f1c2d4-...",
    "caption": "Hello world",
    "url": "dummyurl",
    "file_type": "photo",
    "file_name": "dummyname",
    "created_at": "2026-05-27T12:00:00"
  }
]
```

---

## Setup & Running

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Install dependencies

```bash
uv sync
```

### Configure environment

Create a `.env` file in the project root (or copy `.env.example`):

```env
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=https://ik.imagekit.io/your_id
```

### Run the server

```bash
python main.py
```

The server starts at `http://localhost:8000` with hot-reload enabled.

### Interactive docs

FastAPI generates interactive API docs automatically:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Roadmap

- [ ] Wire up ImageKit SDK to store uploaded files and replace placeholder `url`/`file_name` values
- [ ] Add user authentication with `fastapi-users` (dependency already installed)
- [ ] Validate file type and size before accepting uploads
- [ ] Paginate the `/feed` endpoint
- [ ] Migrate from SQLite to PostgreSQL for production use
