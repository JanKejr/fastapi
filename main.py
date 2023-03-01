from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# TODO: Pridat lepsi databázi!

# Tohle je pouze testovací kolekce (postu)
my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, {"title": \
"favorie foods", "content": "I like pizza", "id": 2}]

# Funkce, ktera najde (post) podle jeho (id)
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
          print(p)
          return p

# Hlavni root stranka se zpravou (GET)
@app.get("/")
def root():
    return {"message": "Welcome to my API"}


# Stranka s (posty) (GET) - Vraci posty
# FASTAPI automaticky serializuje list do JSON formatu
@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Path parameter {id} - ziskat post podle id (Pozor na parametr)
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    try:
      post = find_post(id)
      if not post:
          response.status_code = status.HTTP_404_NOT_FOUND
          return {"message": f"post with id: {id} not found."}
      return {"post_detail": post}
    except:
        pass