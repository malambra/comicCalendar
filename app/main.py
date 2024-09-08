from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.v1 import event_routes as event_routes_v1
from app.routes.v1 import auth_routes as auth_routes_v1
from starlette.responses import FileResponse
import textwrap


app = FastAPI(
    title="Comic Calendar API",
    description="API para gestionar eventos de cómics. Permite listar, buscar y actualizar eventos.",
    version="1.0.0",
    terms_of_service="https://github.com/malambra/comicCalendar/blob/main/terms.md",
    contact={
        "name": "developer",
        "url": "https://github.com/malambra/comicCalendar",
        "email": "alambra.manolo@gmail.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
## Lista de dominios permitidos
# origins = [
#    "http://localhost:3000",  # Ejemplo de dominio permitido
#    "https://miapp.com",  # Añade aquí más dominios según sea necesario
# ]

# Añadir GZipMiddleware con un nivel de compresión de 4
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ruta para servir un solo fichero estático
@app.get("/static-events", include_in_schema=False)
async def static_file():
    return FileResponse("events.json")

@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root():
    message = """
    <div style="text-align: center; font-family: Arial, sans-serif; color: #f5f5f5; background-color: #1a1a2e; padding: 20px; border-radius: 10px;">
        <h2 style="color: #ffcc00;">Welcome to Comic Calendar API</h2>
        <p>The default version is <strong>v1</strong></p>
        <p>To read the documentation 
            <a href="/docs" style="text-decoration: none; color: #ffcc00;">/docs</a>
        </p>
        <p>To access web 
            <a href="https://eventoscomic.com" style="text-decoration: none; color: #ffcc00;">https://eventoscomic.com</a>
        </p>
        <br>
        <a href="https://github.com/malambra/comicCalendar" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="30" height="30" style="border-radius: 50%;"> 
        </a>
    </div>
    """
    formatted_message = textwrap.dedent(message).replace("\n", "<br>")
    return formatted_message


app.include_router(event_routes_v1.router, tags=["events"])
app.include_router(auth_routes_v1.router, tags=["auth"])
