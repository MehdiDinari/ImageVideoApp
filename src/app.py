# src/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

# On importe les schémas Pydantic pour la validation
from schema import PostCreate, PostRead
# On importe la configuration DB
from db import create_db_and_tables


# Configuration du cycle de vie (Démarrage)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Démarrage de la base de données...")
    await create_db_and_tables()  # Pas d'argument 'app' ici
    yield


app = FastAPI(lifespan=lifespan)

# Simulation de base de données (Dictionnaire temporaire)
text_posts = {
    1: {
        "id": 1,
        "title": "New Post",
        "content": "This is my first post"
    },
    2: {
        "id": 2,
        "title": "Learning FastAPI",
        "content": "FastAPI is incredibly fast 🚀"
    }
}


@app.get("/hello")
def read_root():
    return {"message": "Hello Mehdi 🎉 FastAPI fonctionne !"}


@app.get("/posts", response_model=list[PostRead])
def read_posts(limit: int = None):
    posts_list = list(text_posts.values())
    if limit:
        return posts_list[:limit]
    return posts_list


@app.get("/posts/{id}", response_model=PostRead)
def read_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="No such post")
    return text_posts[id]


# Correction : Ajout du "/" devant posts et utilisation des Schémas
@app.post("/posts", response_model=PostRead)
def create_post(post: PostCreate):
    # Génération d'un ID simple pour l'exemple dictionnaire
    new_id = max(text_posts.keys()) + 1 if text_posts else 1

    new_post_data = {
        "id": new_id,
        "title": post.title,
        "content": post.content
    }

    text_posts[new_id] = new_post_data
    return new_post_data