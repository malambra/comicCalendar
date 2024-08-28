# Notify

Las notificaciones se realizan via Telegram. Los usuarios pueden gernerar multiples suscripciones.

## Proceso.

Cada intervalo de tiempo definido:
- El bot recorre el fichero de preferencias y para cada usuario
    - Para cada evento en el fichero de la última insercion **events_to_add.json**
        - Compara la fecha de modificación del fichero y la de la última notificación al usuario. 
            - En caso de que el fichero, sea más reciente, notifica el evento y actualiza la fecha de notificación.

## Pre-Requisitos

- Creación de un bot de telegram y obtencion del Token.
- Instala de **python-telegram-bot** y **python-telegram-bot[job-queue]**
- Configuración del token en el fichero **.env**
- Configuración de tiempo de programación, por defecto cada **6h**

## QuickStart

### Entorno local.

Para lanzar el bot es necesario arrancar el proceso main.py
```bash
python3 main.py
```

### Producción

El servicio se ha dockerizado para desplegarlo con el docker-compose general, por lo que bastará:
```bash
docker-compose build
docker-compose up -d
```

Para levantar el container **notify**

## Acciones disponibles

El bot porporciona a los usuarios, distintas acciones.

**/start** : Con esta accion se lanza un asistente que solicita al usuario:
- De que tipo de eventos desea ser notificado.
- De que Comunidad Autonoma y Provincia quiere las notificaciones.

Esta acción se puede lanzar tantas veces como se requiera para crear multiple suscripciones.

**/check** : Con esta acción el usuario, obtiene un listado de todas sus suscripciones.

**/delete** : Con esta acción se lanza el mismo asistente que se usó para crear suscripciones, pero en este caso se eliminara la suscripción indicada.

**/clean** : Con esta acción se eliminaran todas las suscripciones del usuario.

**/about** : Con esta acción se obtiene informacion general.

**/help** : Con esta accion se obtiene una ayuda de las acciones disponibles.