from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, HttpUrl
from api import database

import random
import string

router = APIRouter()

# Helper funcs

# Generates a random String with 6 numbers/letters
def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Check if the random string already exists in the database
def random_string_exists(random_string):
    result = database.execute_query("SELECT COUNT(*) FROM urls WHERE shorturl = ?", (random_string,))
    return result[0][0] > 0

# Root endpoint
@router.get("/")
def root():
    return {"Hello, World!"}

# Create link endpoint
class ShortenURLRequest(BaseModel):
    url: HttpUrl

@router.post("/pog")
def shorten_url(url_request: ShortenURLRequest):
    random_string = generate_random_string()
    # Check if the generated random string already exists in the database
    while random_string_exists(random_string):
        random_string = generate_random_string()
    # Insert the mapping between the random string and the URL into the database, url_request must be converted to String so it's supported by SQLite
    database.execute_query("INSERT INTO urls (shorturl, destination) VALUES (?, ?)", (random_string, str(url_request.url)))
    return {"shortened_url": url_request.url, "link": random_string}

# Access shortened url
@router.get("/pog/{random_string}", status_code=307)  # Use 307 Temporary Redirect
def redirect_to_destination(random_string: str, response: Response):
    # Retrieve the destination URL corresponding to the random string from the database
    result = database.execute_query("SELECT destination FROM urls WHERE shorturl = ?", (random_string,))
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Extract the destination URL from the database result
    destination_url = result[0][0]
    
    # Set the Location header in the response to redirect the client
    response.headers["Location"] = destination_url
    
    # Return an empty response (status code 307 will be used for redirection)
    return