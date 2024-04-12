import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database settings
DATABASE_NAME = os.getenv("DATABASE_NAME")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET")

# API settings
API_ENDPOINT = os.getenv("API_ENDPOINT")