from fastapi import FastAPI
from app.routes import shorten, user


app = FastAPI(
    title="Linkify API",
    description="An API for shortening links with FastAPI",
    version="1.0.0"
)

app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(shorten.router, prefix="/shorten", tags=["Shorten"])

@app.get("/")
def root():
    return {"message": "Hello this is Linkify API"}