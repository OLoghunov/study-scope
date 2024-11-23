from fastapi import FastAPI
from src.books.routes import booksRouter
from contextlib import asynccontextmanager
from src.db.main import initDb


@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Server is starting...")
    await initDb()
    yield
    print("Server has been stopped")

version = "0.1"

app = FastAPI(
    title="Library",
    description="A REST API for online library",
    version=version,
    lifespan=lifeSpan
)

app.include_router(booksRouter, prefix="/api/{version}/books", tags=["books"])