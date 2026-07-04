from fastapi import FastAPI

from app.routes import game

app = FastAPI()

app.include_router(game.router)

@app.get("/")
def read_root():
    return {"message": "This is Pok-Deng API"}

