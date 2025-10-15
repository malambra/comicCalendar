import json
import os
import plotly.graph_objects as go

# Cargar los datos procesados desde el archivo JSON
with open('events_by_year.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Función para obtener las 10 principales regiones
def obtener_top_10(data):
    top_10 = {}
    for region, años in data.items():
        total = sum(años.values())  # Sumar los valores de todos los años para obtener un total
        top_10[region] = total
    top_10 = dict(sorted(top_10.items(), key=lambda item: item[1], reverse=True)[:10])
    return {region: data[region] for region in top_10.keys()}

# Función para crear la gráfica con menú desplegable para seleccionar regiones
def crear_grafica_con_dropdown(data, title, filename):
    fig = go.Figure()
    
    # Separar las 10 principales y las demás
    top_10 = obtener_top_10(data)
    otras = {k: v for k, v in data.items() if k not in top_10}
    
    # Agregar las trazas para las 10 principales regiones
    for region, años in top_10.items():
        años_ordenados = sorted(años.keys())
        valores = [años[año] for año in años_ordenados]
        fig.add_trace(go.Scatter(
            x=años_ordenados, 
            y=valores, 
            mode='lines+markers', 
            name=region
        ))

    # Agregar las trazas para las demás regiones en gris y desactivadas por defecto
    for region, años in otras.items():
        años_ordenados = sorted(años.keys())
        valores = [años[año] for año in años_ordenados]
        fig.add_trace(go.Scatter(
            x=años_ordenados, 
            y=valores, 
            mode='lines+markers', 
            name=region,
            line=dict(color='gray', width=2, dash='dash'),
            marker=dict(size=6, color='gray'),
            visible='legendonly'  # Inicialmente desactivado
        ))

    # Crear el dropdown de selección para las regiones
    dropdown_buttons = [
        {'label': 'Mostrar todas', 'method': 'update', 'args': [{'visible': [True] * len(data)}, {'title': title}]}
    ]
    
    for region in data.keys():
        visibility = [trace.name == region for trace in fig.data]
        dropdown_buttons.append({
            'label': region,
            'method': 'update',
            'args': [{'visible': visibility + [False] * (len(data) - len(visibility))}, {'title': f'{title} - {region}'}]
        })

    fig.update_layout(
        title=title,
        xaxis_title='Año',
        yaxis_title='Número de Eventos',
        plot_bgcolor='white',
        paper_bgcolor='#ffffff',
        height=600,
        updatemenus=[
            {
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 1.1,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top'
            }
        ]
    )

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    # Construir la ruta de salida
    output_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'graphs', filename)
    fig.write_html(output_path)
    print(f'Archivo {output_path} creado con éxito.')

# Generar y guardar las gráficas solicitadas

# 1. Evolución por años en eventos totales de cada comunidad
crear_grafica_con_dropdown(
    datos["eventos_totales_por_comunidad_y_año"],
    'Evolución de Eventos Totales por Comunidad',
    'evolucion_eventos_totales_comunidad.html'
)

# 2. Evolución por años en eventos totales de cada provincia
crear_grafica_con_dropdown(
    datos["eventos_totales_por_provincia_y_año"],
    'Evolución de Eventos Totales por Provincia',
    'evolucion_eventos_totales_provincia.html'
)

# 3. Evolución por años en Firmas de cada comunidad
crear_grafica_con_dropdown(
    {k: v['Firma'] for k, v in datos["eventos_por_comunidad_tipo_y_año"].items() if 'Firma' in v},
    'Evolución de Firmas por Comunidad',
    'evolucion_firmas_comunidad.html'
)

# 4. Evolución por años en Firmas de cada provincia
crear_grafica_con_dropdown(
    {k: v['Firma'] for k, v in datos["eventos_por_provincia_tipo_y_año"].items() if 'Firma' in v},
    'Evolución de Firmas por Provincia',
    'evolucion_firmas_provincia.html'
)

# 5. Evolución por años en Eventos de cada comunidad
crear_grafica_con_dropdown(
    {k: v['Evento'] for k, v in datos["eventos_por_comunidad_tipo_y_año"].items() if 'Evento' in v},
    'Evolución de Eventos por Comunidad',
    'evolucion_eventos_comunidad.html'
)

# 6. Evolución por años en Eventos de cada provincia
crear_grafica_con_dropdown(
    {k: v['Evento'] for k, v in datos["eventos_por_provincia_tipo_y_año"].items() if 'Evento' in v},
    'Evolución de Eventos por Provincia',
    'evolucion_eventos_provincia.html'
)