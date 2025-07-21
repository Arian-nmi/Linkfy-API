from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schema, database, auth
from fastapi.responses import RedirectResponse
import string, random


router = APIRouter()

def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@router.post("/create", response_model=schema.ShortenResponse)
def create_short_url(
        url: schema.ShortenCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    short_code = generate_short_code()

    while db.query(models.Link).filter(models.Link.short_code == short_code).first():
        short_code = generate_short_code()

    new_link = models.Link(
        full_url=url.full_url,
        short_code=short_code,
        owner=current_user
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link

@router.get("/s/{code}")
def redirect_to_url(code: str, db: Session = Depends(database.get_db)):
    link = db.query(models.Link).filter(models.Link.short_code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    link.click_count += 1
    db.commit()

    return RedirectResponse(link.full_url)