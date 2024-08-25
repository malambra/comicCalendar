import json
import os
from collections import defaultdict
from datetime import datetime

# Construir la ruta al archivo events.json en la carpeta superior
file_path = os.path.join(os.path.dirname(__file__), '..', 'events.json')

# Leer el archivo events.json
with open(file_path, 'r', encoding='utf-8') as f:
    events = json.load(f)

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

# Obtener el rango completo de años
todos_los_años = set()
for años in eventos_totales_por_comunidad_y_año.values():
    todos_los_años.update(años.keys())
for años in eventos_totales_por_provincia_y_año.values():
    todos_los_años.update(años.keys())
for tipos in eventos_por_comunidad_tipo_y_año.values():
    for años in tipos.values():
        todos_los_años.update(años.keys())
for tipos in eventos_por_provincia_tipo_y_año.values():
    for años in tipos.values():
        todos_los_años.update(años.keys())

año_min = min(todos_los_años)
año_max = max(todos_los_años)
rango_completo = list(range(año_min, año_max + 1))

# Función para rellenar años faltantes con 0
def rellenar_años_faltantes(data, rango_completo):
    for key, años in data.items():
        for año in rango_completo:
            if año not in años:
                años[año] = 0

# Rellenar años faltantes en todos los diccionarios
rellenar_años_faltantes(eventos_totales_por_comunidad_y_año, rango_completo)
rellenar_años_faltantes(eventos_totales_por_provincia_y_año, rango_completo)

for comunidad, tipos in eventos_por_comunidad_tipo_y_año.items():
    for tipo, años in tipos.items():
        rellenar_años_faltantes({tipo: años}, rango_completo)

for provincia, tipos in eventos_por_provincia_tipo_y_año.items():
    for tipo, años in tipos.items():
        rellenar_años_faltantes({tipo: años}, rango_completo)

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
