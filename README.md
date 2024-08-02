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

Lanzamiento manual del servidor uvicorn para ejecutar la api localmente.

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
│   │   ├── auth_routes.py
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
- **`auth_routes.py`**: Enrutador para las rutas relacionadas con gestion eventos.
- **`event_routes.py`**: Enrutador para las rutas relacionadas con queries sobre eventos.

#### app/utils/
Directorio para utilidades y funciones auxiliares.

- **`__init__.py`**: Archivo para marcar el directorio como un paquete Python.
- **`file_operations.py`**: Funciones para operaciones con archivos, como cargar y guardar eventos.

### events.json
Archivo JSON para almacenar los datos de eventos.

## Precarga de datos
Actualmente he encontrado este calendario de google y estoy intentando contactar con algunos de los mantenedores por mail y telegram.
```
wget https://calendar.google.com/calendar/ical/8crhqvvts7t9ll97v62adearug%40group.calendar.google.com/public/basic.ics
```

Para hacer una precarga, dado este fichero puedes ejecutar el script adjunto **ics_to_json.py** que recorre el ics *ics_file = 'basic.ics'
*, y lo convierte a json al formato esperado por la API.
Además intenta hacer match en una lista con las 50 provincias, en caso de que esten en el texto del ics. Las que no esten o esten
mal definidas apareceran como *Desconocida* y tendrás que adaptarlas a mano si quieres mostrar esta información.

```bash
python ics_to_json.py > events.json
```