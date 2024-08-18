# Auto Update
Para el auto update realizamos un proceso para descargar la ultima version del calendario y comprobar los eventos discrepantes con la ultima version cargada.

# Ficheros
```
auto_update \
├── README.md
├── add_events.py 5
├── basic.ics
├── basicOLD.ics
├── basicORIG.ics
├── discrepant_events.ics
├── discrepant_events.json
├── discrepant_events_dates.json
├── enrich_dates.py 3
├── enrich_ia.py 4
├── events_to_add.json
├── ics_to_json.py 2
└── new_events.py 1
```

## Ficheros.

#### new_events.py
Script inicial, encargado de orquestar las llamadas necesarias.

```bash
python3 new_events.py
```

Esta invocacion , genera un nuevo calendario que contiene las discrepancias. **discrepant_events.ics** y desencadena el resto del proceso.

#### ics_to_json.py
Hace un export del nuevo ics a json, usando el mismo nombre de fichero pero con extension json. Genera el fichero **discrepant_events.json**

```bash
python3 ics_to_json.py discrepant_events.ics
```

#### enrich_dates.py
Normaliza las fechas para añadir HH:mm:ss+ss a los eventos que no lo tienen. Genera el fichero **discrepant_events_dates.json**

```bash
python3 enrich_dates.py discrepant_events.json discrepant_events_dates.json
```

#### enrich_ia.py
Genera el fichero final enriquecido que vamos a insertar usando la API. Genera el fichero **events_to_add.json**

```bash
python3 enrich_ia.py discrepant_events_dates.json events_to_add.json
```

#### add_events.py
Recorre los eventos generados y hace las invocaciones para ir creando los nuevos eventos.

```bash
python3 add_events.py events_to_add.json
```
