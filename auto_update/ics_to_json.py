import json
import argparse
import os
from icalendar import Calendar
import datetime  # Importar el módulo datetime

# Lista de provincias españolas
provincias = [
    "Álava",
    "Albacete",
    "Alicante",
    "Almería",
    "Asturias",
    "Ávila",
    "Badajoz",
    "Baleares",
    "Barcelona",
    "Burgos",
    "Cáceres",
    "Cádiz",
    "Cantabria",
    "Castellón",
    "Ciudad Real",
    "Córdoba",
    "Cuenca",
    "Gerona",
    "Granada",
    "Guadalajara",
    "Guipúzcoa",
    "Huelva",
    "Huesca",
    "Jaén",
    "La Coruña",
    "La Rioja",
    "Las Palmas",
    "León",
    "Lérida",
    "Lugo",
    "Madrid",
    "Málaga",
    "Murcia",
    "Navarra",
    "Orense",
    "Palencia",
    "Pontevedra",
    "Salamanca",
    "Segovia",
    "Sevilla",
    "Soria",
    "Tarragona",
    "Santa Cruz de Tenerife",
    "Teruel",
    "Toledo",
    "Valencia",
    "Valladolid",
    "Vizcaya",
    "Zamora",
    "Zaragoza",
]


def get_province(location):
    for province in provincias:
        if province in location:
            return province
    return "Desconocida"


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

            # Manejar tanto datetime.date como datetime.datetime
            if isinstance(start_dt, datetime.date):
                start_date = str(start_dt)
            else:
                start_date = str(start_dt.date())

            if end_dt is not None:
                end_dt = end_dt.dt
                if isinstance(end_dt, datetime.date):
                    end_date = str(end_dt)
                else:
                    end_date = str(end_dt.date())
            else:
                end_date = (
                    start_date  # Si no hay dtend, usar la misma fecha que dtstart
                )

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
