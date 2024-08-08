from fastapi import APIRouter, HTTPException, Response, status, Depends, Header
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import URL 
from settings import API_ENDPOINT, JWT_SECRET
import random
import string
from typing import Optional

router = APIRouter()

# Helper functions

def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def random_string_exists(random_string, db: Session):
    return db.query(URL).filter(URL.shorturl == random_string).first() is not None

# Middleware to check JWT token
async def check_token(token: Optional[str] = Header(None)):
    if not token or token != JWT_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

# Root endpoint
@router.get("/")
def root():
    return {"Hello, World!"}

class ShortenURLRequest(BaseModel):
    url: HttpUrl

@router.post(API_ENDPOINT)
def shorten_url(url_request: ShortenURLRequest, vanity_url: Optional[str] = None, token: str = Depends(check_token), db: Session = Depends(get_db)):
    if vanity_url:
        if random_string_exists(vanity_url, db):
            raise HTTPException(status_code=400, detail="Vanity URL already exists")
        new_url = URL(shorturl=vanity_url, destination=str(url_request.url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return {
            "message": "Shortened URL created successfully",
            "shortened_url": url_request.url,
            "vanity_url": vanity_url
        }, status.HTTP_201_CREATED
    else:
        random_string = generate_random_string()
        while random_string_exists(random_string, db):
            random_string = generate_random_string()
        new_url = URL(shorturl=random_string, destination=str(url_request.url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return {
            "message": "Shortened URL created successfully",
            "shortened_url": url_request.url,
            "link": random_string
        }, status.HTTP_201_CREATED

@router.get(f"{API_ENDPOINT}/{{url}}", status_code=307)
def redirect_to_destination(random_string: str, response: Response, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.shorturl == random_string).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    response.headers["Location"] = url_entry.destination
    return

@router.patch(f"{API_ENDPOINT}/{{vanity_url}}")
def patch_url(vanity_url: str, update_request: ShortenURLRequest, token: str = Depends(check_token), db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.shorturl == vanity_url).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Vanity URL doesn't exist.")
    
    new_destination_url = update_request.url
    url_entry.destination = str(new_destination_url)  # Ensure the URL is converted to a string if necessary
    db.commit()
    db.refresh(url_entry)
    return {"message": "URL updated successfully", "New Destination URL": new_destination_url}