from fastapi import FastAPI, HTTPException 
from datetime import datetime
from pydantic import BaseModel
from typing import Text, Optional
from uuid import uuid4

app = FastAPI()

posts = []

class Post(BaseModel):
    id: int
    title: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def read_posts():
    return posts

@app.post("/posts")
def create_post(post: Post):
    post.id = str(uuid4())
    posts.append(post)
    return posts[-1]

@app.get("/posts/{post_id}")
def read_post(post_id: str):
    for post in posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post.id == post_id:
            posts.pop(index)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}")
def update_post(post_id: str, postUpdate: Post):
    for index, post in enumerate(posts):
        if post.id == post_id:
            posts[index] = postUpdate
            posts[index].id = post_id
            return {"message": "Post updated successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

#pip install -r requirements.txt