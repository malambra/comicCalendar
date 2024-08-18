import json
import os
import subprocess
import sys
import argparse

# URL del servidor y endpoint de autenticación
server_url = 'http://localhost:8000/v1'
auth_endpoint = f'{server_url}/token'
events_endpoint = f'{server_url}/events/'

# Credenciales autenticación
username = 'admin'
password = 'password'

# Obtener el token de acceso
def get_access_token():
    response = subprocess.run(
        ['curl', '-X', 'POST', auth_endpoint, '-d', f'username={username}&password={password}'],
        capture_output=True,
        text=True
    )
    if response.returncode != 0:
        print(f"Error obteniendo el token: {response.stderr}")
        return None

    try:
        token_info = json.loads(response.stdout)
        return token_info.get('access_token')
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")
        return None

# Enviar evento
def send_event(event, token):
    if 'id' in event:
        del event['id']
        
    print(json.dumps(event))
    response = subprocess.run(
        [
            'curl', '-X', 'POST', events_endpoint,
            '-H', 'accept: application/json',
            '-H', f'Authorization: Bearer {token}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(event),
            '-v'  # Agregar la opción -v para salida detallada
        ],
        capture_output=True,
        text=True
    )
    if response.returncode != 0:
        print(f"Error enviando el evento: {response.stderr}")
    else:
        print(f"Respuesta del servidor: {response.stdout}")

# Leer el archivo JSON y enviar eventos
def main(input_file_path):
    if not os.path.exists(input_file_path):
        print(f"El archivo {input_file_path} no existe.")
        return

    with open(input_file_path, 'r') as file:
        try:
            events = json.load(file)
            print(f"Archivo JSON cargado correctamente: {events}")
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            return

    token = get_access_token()
    if not token:
        print("No se pudo obtener el token de acceso.")
        return

    for event in events:
        send_event(event, token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enviar eventos a un servidor.')
    parser.add_argument('input_file_path', type=str, help='Ruta del archivo JSON con los eventos a enviar')
    args = parser.parse_args()
    
    main(args.input_file_path)