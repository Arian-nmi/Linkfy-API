from fastapi import FastAPI
from app.routes import shorten, user
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="Linkify API",
    description="An API for shortening links with FastAPI",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app.include_router(user.router, prefix="/auth", tags=["Auth"])
app.include_router(shorten.router, prefix="/shorten", tags=["Shorten"])

@app.get("/")
def root():
    return {"message": "Hello this is Linkify API"}