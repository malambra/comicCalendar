# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-telegram-bot[job-queue]

# Exponer el puerto (opcional, si tu bot necesita escuchar en un puerto específico)
# EXPOSE 8000

# Ejecutar el script principal
CMD ["python", "main.py"]