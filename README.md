# comicCalendar
comicCalendar, es una **api** desarrollada con FastAPI, para gestionar eventos relacionados con el mundo del cómic.

El proyecto nace de la necesidad de un "friki" de tener un punto centralizado en el que poder consultar los eventos por distintos campos, fecha, provincia, etc. y estar informado de que me interesa visitar.

Si tienes esta misma necesidad, aparte de ser otro "friki", eres libre de usar el código o el servicio como consideres, dentro de los términos publicados en [términos](terms.md)

#### API
La **API** está disponible en: https://api.eventoscomic.com

La **documentación de la API**: https://api.eventoscomic.com/docs

#### FRONT
El **front** está disponible en:  https://eventoscomic.es y https://eventoscomic.com

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

Para desplegar el proyecto de forma local, puedes seguir los siguientes pasos...

### Install requirements

Los requerimientos de la **API**, están definidos en el fichero requirements.

```bash
pip install -r requirements.txt
```
### Create user

Las operaciones de creación, actualización o eliminación de eventos requieren autenticación. Para lo que deberás crear uno o varios usuarios en un fichero **.htpasswd** en la raíz del proyecto.

```bash
htpasswd -c .htpasswd admin
```
### Bulid docker image

La imagen docker, con la **API** y el servidor **uvicorn**, se debe construir de la siguiente manera.

```bash
docker build -t comiccalendar .
```

En el caso de usar docker-compose, debes adaptar el fichero docker-compose.yml y construir la imagen desde el.

```bash
docker-compose build
```

### Run docker image

El contenedor docker, con la API y el servidor uvicorn, se debe ejecutar de la siguiente manera.

```bash
docker run -d -p 8000:8000 comiccalendar
```
En el caso de usar docker-compose, la ejecución la realiza directamente, docker-compose.

```bash
 docker-compose up -d
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
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── v1
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── event_routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_operations.py
├── events.json
├── README.md
├── requirements.txt
├── LICENSE
├── Dockerfile
├── docker-compose.yml
├── load_events
│   ├── basic.ics
│   ├── ics_to_json.py
```
 
## Estructura del Proyecto

### comicCalendar/
Directorio raíz del proyecto.

#### app/
Directorio de la **API**

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`main.py`**: Punto de entrada de la **API**, metadatos, includes de routers y definición de CORS.

#### app/auth/
Directorio para las funciones relacionadas con la autenticación.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`auth.py`**: Definición de la función de autenticación y de la ruta del fichero **.htpasswd** usado.

#### app/models/
Directorio para los modelos de datos.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`events.py`**: Definición de los distintos modelos de datos para los eventos.

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

### events.json
Archivo JSON para almacenar los eventos.

### LICENSE
Licencia aplicada al proyecto.

### requirements.txt
Definición de dependencias.

### Dockerfile
Definición de la imagen de la API.

### docker-compose.yml
Fichero de orquestacion par docker-compose.

### .htpasswd
Credenciales de usuarios con permisos de moificación, creación y eliminación de eventos.

### README.md
Documentación del proyecto.

### load_events
Directorio para realizar la precarga de datos.

### basic.ics
Calendario de google con los datos iniciales.

### ics_to_json.py
Script python para la conversión de eventos de ics a json

### Configuración de CORS
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

## Contribuciones
¡Toda ayuda será buen recibida!, así que si quieres contribuir:

- Haz un **fork** del proyecto.

- Crea una nueva rama. 
```bash
git switch -c "tu_rama"
```

- Realiza tus cambios y haz **add** y **commit**
```bash
git commit -am 'feat: Agrega nueva funcionalidad'
```

- Haz **push** de tus cambios.
```bash
git push origin tu_rama
```

- Abre un **Pull Request**.

### Convención commits

Podemos usar múltiples commits, aunque seguir algún convencionalismo siempre ayuda.

Por ejemplo, el de [Angular](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)

- **feat**: Una nueva característica para el usuario.

- **fix**: Arregla un bug que afecta al usuario.

- **perf**: Cambios que mejoran el rendimiento del sitio.

- **build**: Cambios en el sistema de build, tareas de despliegue o instalación.

- **ci**: Cambios en la integración continua.

- **docs**: Cambios en la documentación.

- **refactor**: Refactorización del código como cambios de nombre de variables o funciones.

- **style**: Cambios de formato, tabulaciones, espacios o puntos y coma, etc; no afectan al usuario.

- **test**: Añade tests o refactoriza uno existente.

## Precarga de datos
Actualmente he encontrado este [calendario](https://calendar.google.com/calendar/ical/8crhqvvts7t9ll97v62adearug%40group.calendar.google.com/public/basic.ics) de google, que esta siendo mantenido, en su mayoría por [emea75](https://www.instagram.com/emea75), lo que me ha permitido hacer una precarga de datos, para usarlos desde la **API**

```bash
python ics_to_json.py > events.json
```

