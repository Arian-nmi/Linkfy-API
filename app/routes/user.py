from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schema, database, auth


router = APIRouter()

@router.post("/register", response_model=schema.UserResponse)
def register(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="A user with this email already exists.")

    hashed_pwd = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schema.Token)
def login(user: schema.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email or Password is incorrect")

    access_token = auth.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}