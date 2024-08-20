# Generación de Gráficas
Este proceso se encarga de generar los datos necesarios a partir del fichero **events.json** y almacenarlos en el fichero **events_by_year.json**, para ser graficados.

Los datos:
- **events_by_year.json** --> JSON con la estructura de datos necesaria para la representación de las gráficas.

Los scripts:
- **generate_graf_totals_top.py** --> Genera gráficas con valores totales.
    - **evolucion_eventos_comunidad.html** --> Gráfica con valores por comunidad de tipo Evento
    - **evolucion_eventos_provincia.html** --> Gráfica con valores por provincia de tipo Evento
    - **evolucion_eventos_totales_comunidad.html** --> Gráfica con valores totales por comunidad
    - **evolucion_eventos_totales_provincia.html** --> Gráfica con valores totales por provincia
    - **evolucion_firmas_comunidad.html** --> Gráfica con valores por comunidad de tipo Firma
    - **evolucion_firmas_provincia.html** --> Gráfica con valores por comunidad de tipo Firma

- **generate_graf_year.py** --> Genera gráficas con valores por año.

# Uso
0.- Como requisito tenemos el uso de plotly, que debemos instalar para poder generar las gráficas.
```bash
pip install plotly
```

1.- Generar datos.
```bash
python3 generate_data.py 
    Datos guardados en 'events_by_year.json'
```

2.- Generar gráficas totales.
```bash
python3 generate_graf_totals_top.py 
Archivo /home/.../comicCalendar/generate_graphs/../app/static/graphs/evolucion_eventos_totales_comunidad.html creado con éxito.
Archivo /home/.../comicCalendar/generate_graphs/../app/static/graphs/evolucion_eventos_totales_provincia.html creado con éxito.
...
```

3.- Generar gráficas anuales.
```bash
python3 generate_graf_year.py 
Archivo /home/.../comicCalendar/generate_graphs/../app/static/graphs/graficas_eventos_2006.html creado con éxito.
Archivo /home/.../comicCalendar/generate_graphs/../app/static/graphs/graficas_eventos_2007.html creado con éxito.
...
```