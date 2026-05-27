"""
Entry point for the FastAPI application.

Starts the Uvicorn ASGI server pointing at the `app` object inside app/app.py.
`reload=True` watches for file changes and restarts automatically during development.
Run with: python main.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)