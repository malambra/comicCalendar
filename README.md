# comicCalendar
## Qué es...
comicCalendar, es una **api** desarrollada con FastAPI, para gestionar eventos relacionados con el mundo del cómic.

El proyecto nace de la necesidad de un "friki", de tener un punto centralizado en el que poder consultar los eventos por distintos campos... fecha, provincia, etc. y estar informado de lo que me interesa visitar.

Si tienes esta misma necesidad, aparte de ser otro "friki", eres libre de usar el código o la **API** como consideres, dentro de los términos publicados en [términos](terms.md)

Si quieres disfrutar de tus eventos sin complicarte, te sigiero que uses la web de [https://eventoscomic.com](https://eventoscomic.com)

#### API
- URL de la **API** está disponible en: https://api.eventoscomic.com

- Documentación de la **API**: https://api.eventoscomic.com/docs

- Repositorio **Github**: https://github.com/malambra/comicCalendar

#### FRONT
- URL en producción:  https://eventoscomic.com

- Repositorio **Github**: https://github.com/Raixs/ComicCalendarWeb

## Características
La **API** se auto explica en su [documentación](https://api.eventoscomic.com/docs)

Las funcionalidades más destacadas son:
- Listado ordenado por fecha
- Obtención de evento por **Id**
- Consulta de eventos por cualquier combinación de los siguientes campos:
    - Provincia
    - Comunidad
    - Ciudad
    - Fecha ( YYYY-MM-DD )
    - Tipo ( Evento | Firma )
    - Titulo ( String contenido en el titulo )

## QuickStart
Para ejecutar el proyecto basta con:

- Clona el proyecto

```bash
git clone git@github.com:malambra/comicCalendar.git
```

- Creación de usuario.

Las operaciones de creación, actualización o eliminación de eventos requieren autenticación. Para lo que deberás crear uno o varios usuarios en un fichero **.htpasswd** en la raíz del proyecto.

```bash
htpasswd -c .htpasswd admin
```

- Creación de fichero de variables .env

Creamos el fichero .env
```bash
vim .env
```

Creamos un valor random para el SECRET_JWT
```bash
openssl rand -hex 32
```

Con el siguiente contenido, adaptando nuestros valores.
```bash
#JWT
SECRET_KEY="xxxxxx"

#OPENAI
OPENAI_API_KEY="sk-xxx"

#Add events
USER_API="HTPASSWD_USER"
PASSWORD_API="HTPASSWD_PASSWORD"
SERVER_URL="http://localhost:8000/v1"

#Notify Telegram
TELEGRAM_TOKEN=xxxxxxx
TELEGRAM_TIMER_SECONDS=30
```

- Construimos y arrancamos el proyecto.
```bash
docker-compose build
docker-compose up -d
```

- Copiamos el fichero de eventos al volumen.
```bash
docker cp ./events.json comiccalendar:/code/events.json
```

## Entorno de desarrollo
Aquí dejo algunos tips para desplegar el proyecto de forma local, de cara ha realizar futuros desarrllos...

### Install requirements

Los requerimientos de la **API**, están definidos en el fichero requirements.

```bash
pip install -r requirements.txt
```

### Creation python Virtual env
Es recomendable crear un virtualEnv sobre el que trabajar.

#### Crea venv
```bash
python3.11 -m venv .venv
```

#### Carga venv
```bash
source .venv/bin/activate
```
### Docker Image
#### Bulid docker image

La imagen docker, con la **API** y el servidor **uvicorn**, se debe construir de la siguiente manera.

```bash
docker build -t comiccalendar .
```

#### Run docker image

El contenedor docker, con la API y el servidor uvicorn, se debe ejecutar de la siguiente manera.

```bash
docker run -d -p 8000:8000 comiccalendar
```

### Ejecute uvicorn server - Manualmente

Si durante la fase de desarrollo, te resulta más cómodo, levantar el servidor **uvicorn**, para que refresque los cambios sin construir la imagen, puedes lanzarlo de la siguiente manera.

```bash
# Desde raiz del proyecto
uvicorn app.main:app --reload
```

## Esquema

La **API**, tiene la siguiente estructura, con el fin de hacerla lo más *mantenible* y *escalable* posible
```
comicCalendar/
├── .env
├── .htpasswd
├── .gitignore
├── .github
│   ├── workflows
│   │   ├── lint_ruf.yml
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── README.md
├── TERMS.md
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── events.py
│   │   └── users.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── auth_routes.py
│   │       └── event_routes.py
│   ├── static
│   │   └── graphs
│   └── utils
│       ├── __init__.py
│       ├── file_operations.py
│       └── validate_data.py
│       └── cache.py
├── auto_update
│   ├── README.md
│   ├── add_events.py
│   ├── enrich_dates.py
│   ├── enrich_ia.py
│   ├── ics_to_json.py
│   └── new_events.py
├── docker-compose.yml
├── events.json
├── generate_graphs
│   ├── README.md
│   ├── generate_data.py
│   ├── generate_graf_totals_top.py
│   └── generate_graf_year.py
├── load_events
│   ├── basic.ics
│   ├── enrich_dates.py
│   ├── enrich_ia.py
│   ├── ics_to_json.py
│   └── reasig_id.py
└── requirements.txt
```
 
## Estructura del Proyecto

### comicCalendar/
Directorio raíz del proyecto.

### .env
Variables de entorno necesarias.

### .htpasswd
Credenciales de usuarios con permisos de moificación, creación y eliminación de eventos.

### .github/workflows
Directorio para las actions

- **`lint_ruff.yml`**: Action de linter con ruff, que es uno de los linters más rápidos actualmente.

### CODE_OF_CONDUCT.md
Codigo de conducta

### CONTRIBUTING.md
Normas para facilitar las contribuciones.

### Dockerfile
Definición de la imagen de la api.

### LICENSE
Definición de la licencia aplicada al proyecto.

### README.md
Información relevante del proyecto.

### TERMS.md
Terminos de uso de la API.

### app/
Directorio de la **API**

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`main.py`**: Punto de entrada de la **API**, metadatos, includes de routers y definición de CORS.

#### app/auth/
Directorio para las funciones relacionadas con la autenticación.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`auth.py`**: Definición de la función de autenticación, de la ruta del fichero **.htpasswd** usado, de la creacion del token jwt y del algoritmo de cifrado usado.

#### app/models/
Directorio para los modelos de datos.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`events.py`**: Definición de los distintos modelos de datos para los eventos.
- **`users.py`**: Definición de los distintos modelos de datos para la autenticacion de usuarios.

#### app/routes/
Directorio para los **enrutadores** de la **API**

#### app/routes/v1
Directorio para la versión v1.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`auth_routes.py`**: Enrutador para las rutas relacionadas con gestión eventos.
- **`event_routes.py`**: Enrutador para las rutas relacionadas con queries sobre eventos.

#### app/utils/
Directorio para utilidades y funciones auxiliares.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`file_operations.py`**: Funciones para operaciones con archivos, como cargar y guardar eventos.
- **`cache.py`**: Funciones para carga de eventos en cache.

#### app/static/graphs
Directorio para los html con las gráficas generadas.

#### auto_update
Directorio con los scripts necesarios para insertar y enriquecer los nuevos eventos generados en el calendario.

- **`README.md`**: Documentación acerca de la funcionalidad.
- **`add_events.py`**: Script encargado de invocar a la API, para añadir los nuevos eventos.
- **`enrich_dates.py`**: Script encargado de normalizar fechas para añadir la hora en caso de no estar disponible.
- **`enrich_ia.py`**: Script encargado de enriquecer los eventos para definir el tipo, comunidad y provincia.
- **`ics_to_json.py`**: Script encargado de convertir a json los calendarios ics.
- **`new_events.py`**: Script encargado de la descarga del nuevo ics y la generacin uno nuevo con los nuevos eventos.

### docker-compose.yml
Fichero de orquestacion par docker-compose.

### events.json
Archivo JSON para almacenar los eventos.

### generate_graphs

- **`README.md`**: Documentación acerca de la funcionalidad.
- **`generate_data.py`**: Script para generar el json con los datos necesarios para la creacón de gráficas.
- **`generate_graf_totals_top.py`**: Script para generar gráficas totales.
- **`generate_graf_year.py`**: Script para generar gráficas de evoluciones anuales.

### load_events
Directorio para realizar la precarga inicial de datos.

## tests
Directorio con las coberturas de tests unitarios usando pytest.

### requirements.txt
Definición de dependencias.



## Configuración de CORS
Para el control de CORS, se usa la librería
```python
from fastapi.middleware.cors import CORSMiddleware
```
Como muestra la configuración aplicada para desarrollo, podemos controlar los orígenes, métodos y headers.

```python
## Lista de dominios permitidos
#origins = [
#    "http://localhost:3000",  # Ejemplo de dominio permitido
#    "https://miapp.com",  # Añade aquí más dominios según sea necesario
#]

# Configuración de CORS 
app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,  
    allow_origins=["*"],  
    allow_credentials=True,
    #allow_methods=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],  
)
```
Para verificar las cabeceras podemos realizar la siguiente petición

```bash
curl -i -H "Origin: http://example.com" http://localhost:8000/docs  
```

En la respuesta debemos encontrar la cabecera:
```bash
access-control-allow-origin: *
```
## Tests - PyTests
Para lanzar los tests definidos, debemos tener instaladas las siguientes dependencias:
```bash
 pip3.11 install pytest
 pip3.11 install python-jose
 pip3.11 install passlib
```
Para la ejecución de los tests, lanzaremos **pytest**
```bash
PYTHONPATH=./ pytest
```

## Contribuciones
¡Toda ayuda será buen recibida!, así que si quieres contribuir, hazlo lo mas ordenado posible. [guía](CONTRIBUTING.md)

## Precarga de datos
Actualmente he encontrado este [calendario](https://calendar.google.com/calendar/ical/8crhqvvts7t9ll97v62adearug%40group.calendar.google.com/public/basic.ics) de google, que esta siendo mantenido, en su mayoría por [emea75](https://www.instagram.com/emea75), lo que me ha permitido hacer una precarga de datos, para usarlos desde la **API**

```bash
python ics_to_json.py > events.json
```

## ToDo
- [ &check; ] (app) Añadir los eventos totales devueltos.
- [ &check; ] (app) Añadir versionado a la api.
- [ &check; ] (app) Cambio del modelo de datos para incorporar comunidad, ciudad y tipo.
- [ &check; ] (app) Añadir capacidades de filtrado para nuevos campos.
- [ &check; ] (app) Normalizar fechas YYYY-MM-DD hh:mm:ss
- [ &check; ] (app) Add data update por evento
- [ &check; ] (app) Permitir busqueda por summary
- [ ] (app) Controlar duplicados
- [ &check; ] (app) sort por id de mayor a menos en events
- [ ] (app) Notificar eventos insertados desde la web
- [ &check; ] (app) Normalizar Comunidades y Provincias segun INE
- [ &check; ] (app) Activar compresion en la respuesta de la api
- [ ] (app) Activar cache para las respuestas de la api
- [ &check; ] (app) Cambios formato notificaciones.
- [] (app) Cambios formato notificaciones - clean html.
- [ &check; ] (app) Activar cache para la carga de los eventos de events.json
- [ &check; ] (app) Definicion de tests unitarios con pytest
- [ &check; ] (app) Cambio autenticacion a OAuth2
- [ ] (app) Control de edicion por Usuario y Evento
- [ &check; ] (app) Control e entrada de provincias y comunidades con enums
- [ &check; ] (app) Incrementar duracion token a 120min
- [ &check; ] (app) Mostrar fecha ultimo update en endpoint /events
- [ &check; ] (app) Busqueda por rango de fechas
- [ &check; ] (app) Uso de usuario no ROOT en dockerfile
- [ &check; ] (app) Notificación de nuevos eventos via Telegram
- [ ] (app) Gestion con bbdd en lugar de json
- [ &check; ] (app) Graficado de información agregada de datos de eventos
- [ &check; ] (app) No regenerar _id
- [ &check; ] (infra) Automatizar mecanismos de obtencion y enriquecimiento de datos.
- [ &check; ] (infra) Gestion de backups.
- [ &check; ] (infra) Añadida action linter con ruff.
- [ &check; ] (infra) Uso de volumenes para events.json, etc...
- [ &check; ] (infra) Añadir autorestart a los contenedores


## Agradecimientos

A los creadores y mantenedores, del calendario de eventos, del que he obtenido los datos para la precarga.

En especial a **dos de sus mantenedores**, con los que he podido hablar:
- Eme A: [emea75](https://www.instagram.com/emea75)
- Guillermo Velasco: [@illustraworks](https://instagram.com/illustraworks)

## Desarrolladores
Proyecto desarrollado por:
- Frontend [@raixs](https://github.com/Raixs)
- Backend  [@malambra](https://github.com/malambra)
- UX/UI [@hdetinta](https://github.com/hdetinta)

## Contexto
Consulta los archivos [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [LICENSE](LICENSE) y [TERMS](TERMS.md) para obtener más informacion acerca del proyecto.
