import json
import argparse
import os
from icalendar import Calendar
import datetime
import pytz

# Lista de provincias españolas
provincias = [
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz",
    "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón",
    "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa",
    "Huelva", "Huesca", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida",
    "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra",
    "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife",
    "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza",
]

madrid_tz = pytz.timezone('Europe/Madrid')

def get_province(location):
    for province in provincias:
        if province in location:
            return province
    return "Desconocida"

def convert_to_madrid_tz(dt):
    if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        # Si es una fecha sin tiempo, asumir que es medianoche en UTC
        dt = datetime.datetime.combine(dt, datetime.time.min)
        dt = pytz.utc.localize(dt)
    else:
        # Asegurarse de que el datetime está en UTC
        dt = dt.replace(tzinfo=pytz.utc)
    # Convertir a la zona horaria de Madrid
    return dt.astimezone(madrid_tz)

def ics_to_json(ics_file):
    with open(ics_file, "r") as f:
        gcal = Calendar.from_ical(f.read())

    events = []
    event_id = 1

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary"))

            start_dt = component.get("dtstart").dt
            end_dt = component.get("dtend")
            create_dt = component.get("created").dt if component.get("created") else datetime.datetime.now(pytz.utc)

            # Convertir start_dt a la zona horaria de Madrid
            start_dt = convert_to_madrid_tz(start_dt)
            start_date = start_dt.strftime("%Y-%m-%d %H:%M:%S")

            # Convertir create_dt a la zona horaria de Madrid
            create_dt = convert_to_madrid_tz(create_dt)
            create_date = create_dt.strftime("%Y-%m-%d %H:%M:%S")

            if end_dt is not None:
                # Convertir end_dt a la zona horaria de Madrid
                end_dt = convert_to_madrid_tz(end_dt.dt)
                end_date = end_dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                end_date = start_date  # Si no hay dtend, usar la misma fecha que dtstart

            location = str(component.get("location"))
            description = str(component.get("description"))

            province = get_province(location)

            community = "Desconocida"
            city = "Desconocida"
            type = "Desconocido"

            event = {
                "id": event_id,
                "summary": summary,
                "start_date": start_date,
                "end_date": end_date,
                "create_date": create_date,
                "province": province,
                "address": location,
                "description": description,
                "community": community,
                "city": city,
                "type": type,
            }
            events.append(event)
            event_id += 1

    return json.dumps(events, indent=4, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Convertir un archivo ICS a JSON.")
    parser.add_argument("ics_file", help="El archivo ICS a convertir.")
    args = parser.parse_args()

    json_output = ics_to_json(args.ics_file)

    # Crear el nombre del archivo de salida
    json_file = os.path.splitext(args.ics_file)[0] + '.json'

    # Guardar el JSON en el archivo de salida
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_output)

if __name__ == "__main__":
    main()