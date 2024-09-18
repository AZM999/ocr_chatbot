from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()   # fastapi instance

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")
def root():
    return {"message" : "hello from fastapi! -- added something"}


@app.get("/posts")
def get_posts():
    return {"data": "some dummy data"}

@app.post("/createpost")
def create_post(new_post: Post):
    print (new_post.dict())
    return {"data": new_post.content}