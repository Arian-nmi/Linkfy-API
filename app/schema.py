from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ------------------ User ------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# ------------------ Token ------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# ------------------ Shorten ------------------

class ShortenCreate(BaseModel):
    full_url: str

class ShortenResponse(BaseModel):
    id: int
    full_url: str
    short_code: str
    click_count: int

    class Config:
        orm_mode = True