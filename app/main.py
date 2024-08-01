from app.routes import event_routes
from fastapi import FastAPI

app = FastAPI()

app.include_router(event_routes.router)