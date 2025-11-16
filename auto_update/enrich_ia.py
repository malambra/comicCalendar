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
        {
            "role": "system",
            "content": (
                "Eres un asistente experto en eventos relacionados con el mundo del cómic. "
                "Tu tarea es analizar descripciones de eventos y clasificarlos con precisión "
                "en una de las siguientes categorías, devolviendo el resultado en formato JSON "
                "con un solo campo 'type'."
            ),
        },
        {
            "role": "user",
            "content": (
                "Clasifica el siguiente evento de cómic en una de estas categorías:\n\n"
                "1. **Convención**: Grandes eventos o salones dedicados al cómic, manga o cultura pop "
                "(por ejemplo: Salón del Cómic, Comic-Con, Japan Weekend).\n"
                "2. **Feria**: Eventos de venta o intercambio de cómics, fanzines o merchandising, "
                "normalmente con puestos o stands comerciales.\n"
                "3. **Firma**: Sesión de firmas o encuentro con autores/as donde firman ejemplares de sus obras.\n"
                "4. **Presentación**: Acto formal en el que se presenta una obra, cómic o libro, generalmente con los autores presentes.\n"
                "5. **Taller**: Actividad formativa o práctica (por ejemplo, dibujo, guion, ilustración, creación de cómics, etc.).\n"
                "6. **Exposición**: Muestra artística o exhibición de obras relacionadas con el cómic (originales, ilustraciones, etc.).\n"
                "7. **Club de lectura**: Actividad donde un grupo de personas, con o sin moderación, se reúne para leer y/o discutir cómics.\n"
                "8. **Otros**: Cualquier evento que no encaje claramente en las categorías anteriores.\n\n"
                "Devuelve únicamente un JSON con el formato:\n"
                "{ \"type\": \"<categoría>\" }\n\n"
                "Descripción del evento:\n"
                f"{description}"
            ),
        },
    ]

    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=60,
                temperature=0.2,
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