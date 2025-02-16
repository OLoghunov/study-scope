from fastapi import FastAPI

from src.books.routes import booksRouter
from src.auth.routes import authRouter
from src.reviews.routes import reviewRouter
from src.tags.routes import tagsRouter
from .errors import registerAllErrors
from .middleware import registerMiddleware

version = "0.1"

app = FastAPI(
    title="Study-Scope",
    description="A REST API for online library",
    version=version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    openapi_url=f"/api/{version}/openapi.json",
    contact={
        "email":"loghunov1@gmail.com"
    }
)

registerAllErrors(app)

registerMiddleware(app)

app.include_router(booksRouter, prefix="/api/{version}/books", tags=["books"])
app.include_router(authRouter, prefix="/api/{version}/auth", tags=["auth"])
app.include_router(reviewRouter, prefix="/api/{version}/reviews", tags=["reviews"])
app.include_router(tagsRouter, prefix="/api/{version}/tags", tags=["tags"])
