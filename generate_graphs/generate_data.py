import json, os
from collections import defaultdict
from datetime import datetime

# Construir la ruta al archivo events.json en la carpeta superior
file_path = os.path.join(os.path.dirname(__file__), '..', 'events.json')

# Leer el archivo events.json
with open(file_path, 'r', encoding='utf-8') as f:
    events = json.load(f)

## Cargar el archivo JSON original
#with open('events.json', 'r', encoding='utf-8') as f:
#    events = json.load(f)

# Inicializar diccionarios para almacenar los datos
eventos_totales_por_comunidad_y_año = defaultdict(lambda: defaultdict(int))
eventos_totales_por_provincia_y_año = defaultdict(lambda: defaultdict(int))
eventos_por_comunidad_tipo_y_año = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
eventos_por_provincia_tipo_y_año = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

# Procesar los eventos
for event in events:
    comunidad = event['community']
    provincia = event['province']
    tipo = event['type']
    fecha_inicio = datetime.strptime(event['start_date'], '%Y-%m-%d %H:%M:%S%z')
    año = fecha_inicio.year
    
    # Incrementar el total de eventos por comunidad y año
    eventos_totales_por_comunidad_y_año[comunidad][año] += 1
    
    # Incrementar el total de eventos por provincia y año
    eventos_totales_por_provincia_y_año[provincia][año] += 1
    
    # Incrementar los eventos por comunidad, tipo y año
    eventos_por_comunidad_tipo_y_año[comunidad][tipo][año] += 1
    
    # Incrementar los eventos por provincia, tipo y año
    eventos_por_provincia_tipo_y_año[provincia][tipo][año] += 1

# Convertir defaultdicts a diccionarios normales antes de guardar
datos_a_guardar = {
    "eventos_totales_por_comunidad_y_año": {comunidad: dict(años) for comunidad, años in eventos_totales_por_comunidad_y_año.items()},
    "eventos_totales_por_provincia_y_año": {provincia: dict(años) for provincia, años in eventos_totales_por_provincia_y_año.items()},
    "eventos_por_comunidad_tipo_y_año": {comunidad: {tipo: dict(años) for tipo, años in tipos.items()} for comunidad, tipos in eventos_por_comunidad_tipo_y_año.items()},
    "eventos_por_provincia_tipo_y_año": {provincia: {tipo: dict(años) for tipo, años in tipos.items()} for provincia, tipos in eventos_por_provincia_tipo_y_año.items()}
}

# Guardar los datos procesados en un archivo JSON
with open('events_by_year.json', 'w', encoding='utf-8') as f:
    json.dump(datos_a_guardar, f, ensure_ascii=False, indent=4)

print("Datos guardados en 'events_by_year.json'")

