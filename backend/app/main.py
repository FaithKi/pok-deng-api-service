from fastapi import FastAPI

# from app.routes import wallets, transactions

app = FastAPI()

# app.include_router(wallets.router)
# app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "This is Pok-Deng API"}

