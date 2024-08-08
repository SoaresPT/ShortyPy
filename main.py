import uvicorn
from fastapi import FastAPI
from api.endpoints import router as api_router
from app.database import create_tables

app = FastAPI()

# Initialize database tables
create_tables()

# Include API endpoints
app.include_router(api_router)