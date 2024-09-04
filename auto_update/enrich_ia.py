import os
import sys
import json
import openai
import argparse
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath('../app/utils'))
from validate_data import provinces


# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Configura la API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_type(description):
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
            resultado = response['choices'][0]['message']['content'].strip()
            print(f"Respuesta de la API (get_type): {resultado}")  # Mensaje de depuración
            try:
                event_type_info = json.loads(resultado)
                return event_type_info.get('type', 'Desconocido')
            except json.JSONDecodeError as e:
                print(f"Error decodificando JSON: {e}")
                return 'Desconocido'
        except openai.error.RateLimitError as e:
            print(f"Rate limit alcanzado: {e}. Reintentando en {2 ** i} segundos...")
            time.sleep(2 ** i)
    return 'Desconocido'

def get_location_info(address):
    # Convertir la lista de provincias y comunidades a un formato JSON
    provinces_json = json.dumps(provinces, ensure_ascii=False)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Determina la provincia, comunidad y ciudad del siguiente evento basado en su descripción:\n\n{address}\n\nUsa la siguiente lista de provincias y comunidades:\n\n{provinces_json}\n\nProporciona el resultado en el formato JSON con los campos 'province', 'community' y 'city'."}
    ]

    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50,
            )
            resultado = response['choices'][0]['message']['content'].strip()
            print(f"Respuesta de la API (get_location_info): {resultado}")  # Mensaje de depuración
            try:
                location_info = json.loads(resultado)
                return {
                    'province': location_info.get('province', 'Desconocida'),
                    'community': location_info.get('community', 'Desconocida'),
                    'city': location_info.get('city', 'Desconocida')
                }
            except json.JSONDecodeError as e:
                print(f"Error decodificando JSON: {e}")
                return {'province': 'Desconocida', 'community': 'Desconocida', 'city': 'Desconocida'}
        except openai.error.RateLimitError as e:
            print(f"Rate limit alcanzado: {e}. Reintentando en {2 ** i} segundos...")
            time.sleep(2 ** i)
    return {'province': 'Desconocida', 'community': 'Desconocida', 'city': 'Desconocida'}

def add_location_info(events):
    for event in events:
        location_info = get_location_info(event['address'])
        event.update(location_info)
    return events

def enrich_events(input_file_path, output_file_path):
    if not os.path.exists(input_file_path):
        print(f"El archivo {input_file_path} no existe.")
        return

    if os.stat(input_file_path).st_size == 0:
        print(f"El archivo {input_file_path} está vacío.")
        return

    with open(input_file_path, 'r') as file:
        try:
            events = json.load(file)
            print(f"Archivo JSON cargado correctamente: {events}")
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            return

    for event in events:
        description = event.get('description', '')
        address = event.get('address', '')
        event['type'] = get_type(description)
        location_info = get_location_info(address)
        event.update(location_info)

    with open(output_file_path, 'w') as file:
        json.dump(events, file, ensure_ascii=False, indent=4)
        print(f"Archivo JSON enriquecido guardado en {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Procesa un archivo JSON y genera un archivo JSON con información enriquecida.')
    parser.add_argument('input_json', type=str, help='El archivo JSON de entrada a procesar')
    parser.add_argument('output_json', type=str, help='El archivo JSON de salida con la información enriquecida')
    args = parser.parse_args()

    input_file_path = args.input_json
    output_file_path = args.output_json

    enrich_events(input_file_path, output_file_path)

if __name__ == "__main__":
    main()