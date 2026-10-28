from fastapi import FastAPI
from fastapi.params import Body
from fastapi import HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

my_posts = [{"Title":"Best pizzas in town","Content":"Here's a comprehensive list of best pizzas in town","published":True,"rating":4, "id":1},
         {"Title":"Best coffee shops in town","Content":"Have you ever asked yourself which coffee shops are the best in town? here's a list","published":True,"rating":4,"id":2}]

@app.get("/")
def read_root():
    return {"message": "Here's my api!"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

@app.get("/posts/{id}")
def get_post(id: int):
        post = find_post(int(id))

        if not post:
            raise HTTPException(
                status_code = 404,
                detail = f"Post with id:{id} not found"
            )
        return {"post detail":post}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
        for i, p in enumerate(my_posts):
            if p["id"]==id:
                return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = find_index_post(int(id))

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} does not exist."
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(int(id))

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} does not exist."
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}