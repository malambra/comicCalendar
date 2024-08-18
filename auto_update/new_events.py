from icalendar import Calendar, Event
import copy, os, requests, subprocess

def load_calendar(file_path):
    with open(file_path, 'r') as file:
        return Calendar.from_ical(file.read())

def get_event_key(event):
    return (str(event.get('UID')), str(event.get('SUMMARY')))

def find_discrepant_events(cal1, cal2):
    events1 = {get_event_key(event): event for event in cal1.walk('VEVENT')}
    events2 = {get_event_key(event): event for event in cal2.walk('VEVENT')}
    
    discrepant_events = []
    
    for key, event in events1.items():
        if key not in events2:
            discrepant_events.append(event)
    
    for key, event in events2.items():
        if key not in events1:
            discrepant_events.append(event)
    
    return discrepant_events

def create_discrepant_calendar(events):
    new_cal = Calendar()
    new_cal.add('prodid', '-//Discrepant Events Calendar//mxm.dk//')
    new_cal.add('version', '2.0')
    
    for event in events:
        new_cal.add_component(copy.deepcopy(event))
    
    return new_cal

def save_calendar(calendar, file_path):
    with open(file_path, 'wb') as file:
        file.write(calendar.to_ical())

def rotate_calendars():
    #Delete calendar basicOLD.ics
    old_calendar='basicOLD.ics'
    if os.path.exists(old_calendar):
        os.remove(old_calendar)

    #Crear un archivo  vacio si no existe
    current_calendar='basic.ics'
    if not os.path.exists(current_calendar):
        content = """BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Eventos Cómic España
X-WR-TIMEZONE:Europe/Madrid
X-WR-CALDESC:Salones\, exposiciones\, jornadas\, firmas y otros eventos dedicados a la historieta en España.
 Se admite añadir vuestros propios eventos\, previa solicitud a: eventosdecomic@gmail.com
END:VCALENDAR"""
        with open(current_calendar, 'w', encoding='utf-8') as file:
            file.write(content)
    
    #Rename basic.ics a basicOLD.ics
    os.rename(current_calendar, old_calendar)
    
    #Donwload basic.ics
    print("- Downloading basic.ics calendar...")
    url='https://calendar.google.com/calendar/ical/8crhqvvts7t9ll97v62adearug%40group.calendar.google.com/public/basic.ics'
    response=requests.get(url)
    if response.status_code == 200:
        with open(current_calendar, 'wb') as file:
            file.write(response.content)

def main():
    print("")
    print("Executing Steps:")
    print("---------------------------------------")
    # Rotar calendarios
    print("- Rename calendars...")
    rotate_calendars()

    # Cargar los calendarios
    cal1 = load_calendar('basicOLD.ics')
    cal2 = load_calendar('basic.ics')

    # Encontrar eventos discrepantes
    print("- Find discrepants events...")
    discrepant_events = find_discrepant_events(cal1, cal2)

    # Crear un nuevo calendario con los eventos discrepantes
    print("- Creating new calendar with discrepants events...")
    discrepant_calendar = create_discrepant_calendar(discrepant_events)

    # Guardar el nuevo calendario
    print("- Saving new calendar...")
    save_calendar(discrepant_calendar, 'discrepant_events.ics')

    #Convertimos a json el nuevo calendario
    #result = subprocess.run(['python3', 'ics_to_json.py', 'discrepant_events.ics'], capture_output=True, text=True)
    try:
        print("- Exporting new calendar from ics to json...")
        result = subprocess.run(['python3.11', 'ics_to_json.py', 'discrepant_events.ics'], capture_output=True, text=True)
        result.check_returncode()  # Esto lanzará una excepción si el comando falló
    except subprocess.CalledProcessError as e:
        print(f"- Error al ejecutar el script: {e}")
        print(f"- Salida estándar: {e.stdout}")
        print(f"- Salida de error: {e.stderr}")
    except Exception as e:
        print(f"- Excepción inesperada: {e}")
    
    #Normalizamos fechas
    try:
        print("- Normalize dates in new calendar...")
        result = subprocess.run(['python3.11', 'enrich_dates.py', 'discrepant_events.json', 'discrepant_events_dates.json'], capture_output=True, text=True)
        result.check_returncode()  # Esto lanzará una excepción si el comando falló
    except subprocess.CalledProcessError as e:
        print(f"- Error al ejecutar el script: {e}")
        print(f"- Salida estándar: {e.stdout}")
        print(f"- Salida de error: {e.stderr}")
    except Exception as e:
        print(f"- Excepción inesperada: {e}")

    #IA Enrich de datos
    try:
        print("- Invoke IA to complete needed parans type, province, community and city...")
        result = subprocess.run(['python3.11', 'enrich_ia.py', 'discrepant_events_dates.json', 'events_to_add.json'], capture_output=True, text=True)
        result.check_returncode()  # Esto lanzará una excepción si el comando falló
    except subprocess.CalledProcessError as e:
        print(f"- Error al ejecutar el script: {e}")
        print(f"- Salida estándar: {e.stdout}")
        print(f"- Salida de error: {e.stderr}")
    except Exception as e:
        print(f"- Excepción inesperada: {e}")

    #Add new events
    try:
        print("- Invoke API to add new events...")
        result = subprocess.run(['python3.11', 'add_events.py', 'events_to_add.json'], capture_output=True, text=True)
        result.check_returncode()  # Esto lanzará una excepción si el comando falló
    except subprocess.CalledProcessError as e:
        print(f"- Error al ejecutar el script: {e}")
        print(f"- Salida estándar: {e.stdout}")
        print(f"- Salida de error: {e.stderr}")
    except Exception as e:
        print(f"- Excepción inesperada: {e}")
    
if __name__ == "__main__":
    main()
