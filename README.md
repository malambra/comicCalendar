# comicCalendar
Calendario de eventos relacionados con el comic.

## QuickStart

#### Install requirements

Los requerimientos de la API, estan definidos en el fichero requirements.

```bash
pip install -r requirements.txt
```
#### Create user

Las operaciones de creacion, actualizacion o eliminación de eventos, requieren autenticación.

```bash
htpasswd -c .htpasswd admin
```
#### Bulid docker image

La imagen docker, con la API y el servidor uvicorn, se debe contruir de la siguiente manera.
Esta construcción la realiza directamente, docker-compose, por lo que solo es necesario para pruebas concretas.

```bash
docker build -t comiccalendar .
```
#### Run docker image

El contenedor docker, con la API y el servidor uvicorn, se debe ejecutar de la siguiente manera.
Esta ejecución la realiza directamente, docker-compose, por lo que solo es necesario para pruebas concretas.

```bash
docker run -d -p 8000:8000 comiccalendar
```

#### Ejecute uvicorn server - Manualmente

Lanzamiento manuel del servidor uvicorn.

```bash
# Desde raiz del proyecto
uvicorn app.main:app --reload
```

## Esquema
```
comicCalendar/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── event_routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   ├── crud.py
├── events.json
```
 
## Estructura del Proyecto

### comicCalendar/
Directorio raíz del proyecto.

#### app/
Directorio principal de la aplicación.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`main.py`**: Punto de entrada de la aplicación FastAPI.

#### app/auth/
Directorio para los modelos de datos.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`auth.py`**: Definición de la función de autenticación y de la ruta del fichero **.htpasswd** usado.

#### app/models/
Directorio para los modelos de datos.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`events.py`**: Definición del modelo de datos para los eventos.

#### app/routes/
Directorio para los enrutadores de la API.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`event_routes.py`**: Enrutador para las rutas relacionadas con eventos.

#### app/utils/
Directorio para utilidades y funciones auxiliares.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`file_operations.py`**: Funciones para operaciones con archivos, como cargar y guardar eventos.

### events.json
Archivo JSON para almacenar los datos de eventos.
