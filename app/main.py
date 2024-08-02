from app.routes import event_routes, auth_routes
from fastapi import FastAPI

app = FastAPI(
    title="Comic Calendar API",
    description="API para gestionar eventos de cómics. Permite listar, buscar y actualizar eventos.",
    version="1.0.0"
)

app.include_router(event_routes.router, tags=["events"])
app.include_router(auth_routes.router, tags=["auth"])