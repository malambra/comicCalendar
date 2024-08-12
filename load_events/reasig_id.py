import json

# Cargar el archivo JSON
with open('events.json', 'r', encoding='utf-8') as file:
    events = json.load(file)

# Reasignar IDs secuencialmente
for index, event in enumerate(events, start=1):
    event['id'] = index

# Guardar el archivo JSON con los IDs reasignados
with open('events_reasignados.json', 'w', encoding='utf-8') as file:
    json.dump(events, file, ensure_ascii=False, indent=4)

print("IDs reasignados secuencialmente y guardados en 'events_reasignados.json'")
