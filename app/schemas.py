"""
Pydantic schemas for request/response validation.

PostCreate  Validates the body of a post-creation request.
            Not yet wired into the upload endpoint — placeholder for when
            the multipart form is refactored to use JSON body validation.
"""
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str