from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import event_routes, auth_routes


app = FastAPI(
    title="Comic Calendar API",
    description="API para gestionar eventos de cómics. Permite listar, buscar y actualizar eventos.",
    version="1.0.0"
)
## Lista de dominios permitidos
#origins = [
#    "http://localhost:3000",  # Ejemplo de dominio permitido
#    "https://miapp.com",  # Añade aquí más dominios según sea necesario
#]

# Configuración de CORS 
app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,  
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    #allow_methods=["*"],  # Permite todos los métodos
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],  # Permite todas las cabeceras
)

app.include_router(event_routes.router, tags=["events"])
app.include_router(auth_routes.router, tags=["auth"])