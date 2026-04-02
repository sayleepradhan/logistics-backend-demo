from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server started ...")
    yield
    print("Server stopped ...")


app = FastAPI(lifespan=lifespan_handler)

@app.get("/")
def read_root():
    return {"detail": "Server is running ..."}