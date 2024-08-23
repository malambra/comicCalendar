# Usar la imagen base oficial de Python en su versión slim
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /code

# Copiar requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código y ficheros necesarios al contenedor
COPY ./app /code/app
COPY ./auto_update /code/auto_update
COPY ./generate_graphs /code/generate_graphs
COPY ./load_events /code/load_events

# Crear grupo y usuario no ROOT con los IDs del host anfitrion
RUN groupadd -g 1000 celtha && useradd -u 1000 -g celtha -m celtha

# Cambiar propietario de los ficheros y directorios 
RUN chown -R celtha:celtha /code

# Cambiar al usuario no root
USER celtha

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
