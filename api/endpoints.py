from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, HttpUrl
from api import database

import random
import string
from typing import Optional

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

# Create Shorten URL on the DB
@router.post("/pog")
def shorten_url(url_request: ShortenURLRequest, vanity_url: Optional[str] = None):
    if vanity_url:
        # Check if the specified vanity URL already exists in the database
        if random_string_exists(vanity_url):
            raise HTTPException(status_code=400, detail="Vanity URL already exists")
        # Insert the mapping between the vanity URL and the destination URL into the database
        database.execute_query("INSERT INTO urls (shorturl, destination) VALUES (?, ?)", (vanity_url, str(url_request.url)))
        return {"message": "Shortened URL created successfully",
                "shortened_url": url_request.url,
                "vanity_url": vanity_url}, status.HTTP_201_CREATED
    else:
        # Generate a random string
        random_string = generate_random_string()
        while random_string_exists(random_string):
            random_string = generate_random_string()
        # Insert the mapping between the random string and the URL into the database
        database.execute_query("INSERT INTO urls (shorturl, destination) VALUES (?, ?)", (random_string, str(url_request.url)))
        return {
            "message": "Shortened URL created successfully",
            "shortened_url": url_request.url,
            "link": random_string}, status.HTTP_201_CREATED

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

# PATCH - Update the destination of an existing Vanity URL
@router.patch("/pog/{vanity_url}")
def patch_url(vanity_url: str, update_request: ShortenURLRequest):
    if not random_string_exists(vanity_url):
        raise HTTPException(status_code=404, detail="Vanity URL doesn't exist.")
    else:
        new_destination_url = update_request.url
        # Logic to update the destination URL in the database goes here
        return {"Patch": vanity_url, "New Destination URL": new_destination_url}