from fastapi import FastAPI

from app.routes import game_route

app = FastAPI()

app.include_router(game_route.router)

@app.get("/")
def read_root():
    return {"message": "This is Pok-Deng API"}

