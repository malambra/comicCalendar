import json
import re

# Cargar el archivo JSON
with open('events.json', 'r', encoding='utf-8') as file:
    events = json.load(file)

# Función para agregar la hora si falta en la fecha
def add_time_if_missing(date_str, is_start):
    if date_str is None:
        return None
    # Verifica si el formato es solo fecha (sin hora)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        if is_start:
            return f"{date_str} 00:00:00+00:00"
        else:
            return f"{date_str} 23:59:59+00:00"
    return date_str

# Modificar las fechas
for event in events:
    event['start_date'] = add_time_if_missing(event.get('start_date'), is_start=True)
    event['end_date'] = add_time_if_missing(event.get('end_date'), is_start=False)

# Guardar el archivo JSON modificado
with open('events_modificado.json', 'w', encoding='utf-8') as file:
    json.dump(events, file, ensure_ascii=False, indent=4)

print("Fechas modificadas y guardadas en 'events_modificado.json'")