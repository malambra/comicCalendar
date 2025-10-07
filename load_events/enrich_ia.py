import json
import os
import argparse
import time
from dotenv import load_dotenv
from icalendar import Calendar
import openai
from openai.error import RateLimitError

load_dotenv()
# Configura la API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_ics(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    calendar = Calendar.from_ical(content)
    events = []
    event_id = 1

    for component in calendar.walk():
        if component.name == "VEVENT":
            start_date = component.get('DTSTART').dt
            end_date = component.get('DTEND').dt if component.get('DTEND') else None
            event = {
                "id": event_id,
                "summary": str(component.get('SUMMARY')),
                "start_date": str(start_date),
                "end_date": str(end_date) if end_date else None,
                "create_date": str(component.get("CREATED").dt if component.get("CREATED") else datetime.datetime.now(pytz.utc)),
                "address": str(component.get('LOCATION')),
                "description": str(component.get('DESCRIPTION')),
                "type": get_type(str(component.get('DESCRIPTION')))
            }
            events.append(event)
            event_id += 1

    return events

def get_type(description):
    # Realiza una consulta a OpenAI para determinar el tipo de evento
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Determina si el siguiente evento es una 'Firma' (charlas o sesiones de firmas) o un 'Evento' (eventos grandes tipo salón) basada en su descripción:\n\n{description}\n\nProporciona el resultado en el formato JSON con el campo 'type'."}
    ]

    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50,
            )
            # Extrae el texto de la respuesta y convierte a JSON
            resultado = response['choices'][0]['message']['content'].strip()
            print(f"Respuesta de OpenAI para la descripción '{description}': {resultado}")  # Línea de depuración

            try:
                event_type_info = json.loads(resultado)
                return event_type_info.get('type', 'evento')
            except json.JSONDecodeError as e:
                print(f"Error decodificando JSON: {e}")
                return 'evento'
        except RateLimitError as e:
            print(f"Rate limit alcanzado: {e}. Reintentando en {2 ** i} segundos...")
            time.sleep(2 ** i)
    return 'evento'

def get_location_info(address):
    # Realiza una consulta a OpenAI para obtener la ciudad, provincia y comunidad
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Determina la ciudad, provincia y comunidad autónoma para la siguiente dirección en España:\n\n{address}\n\nProporciona el resultado en el formato JSON con los campos 'city', 'province' y 'community'."}
    ]

    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=100,
            )
            # Extrae el texto de la respuesta y convierte a JSON
            resultado = response['choices'][0]['message']['content'].strip()
            print(f"Respuesta de OpenAI para la dirección '{address}': {resultado}")  # Línea de depuración

            try:
                location_info = json.loads(resultado)
                return location_info.get('city', ''), location_info.get('province', ''), location_info.get('community', '')
            except json.JSONDecodeError as e:
                print(f"Error decodificando JSON: {e}")
                return '', '', ''
        except RateLimitError as e:
            print(f"Rate limit alcanzado: {e}. Reintentando en {2 ** i} segundos...")
            time.sleep(2 ** i)
    return '', '', ''

def add_location_info(events):
    for event in events:
        city, province, community = get_location_info(event['address'])
        event['city'] = city
        event['province'] = province
        event['community'] = community
    return events

def main():
    parser = argparse.ArgumentParser(description='Procesa un archivo ICS y genera un archivo JSON con información enriquecida.')
    parser.add_argument('ics_file', type=str, help='El archivo ICS a procesar')
    args = parser.parse_args()

    ics_file_path = args.ics_file
    json_file_path = os.path.splitext(ics_file_path)[0] + '.json'

    events = parse_ics(ics_file_path)
    events_with_location = add_location_info(events)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(events_with_location, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()