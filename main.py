from fastapi import FastAPI
from api import database, endpoints

app = FastAPI()

database.create_tables()

app.include_router(endpoints.router)
