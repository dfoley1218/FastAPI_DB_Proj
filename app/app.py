from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate

app = FastAPI()

text_posts = {1: {"title": "New Post", "content": "This is a new post"}}

@app.get("/posts")
def get_all_posts(limit: int = 10):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

# post endpoint
@app.post("/posts")
def create_post(post: PostCreate) -> PostCreate:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = {"title": post.title, "content": post.content}
    return new_post



