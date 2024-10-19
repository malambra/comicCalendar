import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Función para crear y guardar las gráficas en un archivo HTML
def crear_graficas_html(año, datos):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[
        f'Eventos Totales por Comunidad en {año}', 
        f'Eventos Totales por Provincia en {año}', 
        f'Eventos por Comunidad y Tipo en {año}', 
        f'Eventos por Provincia y Tipo en {año}'
    ])
    
    # Gráfico 1: Eventos totales por comunidad y año
    comunidades = []
    total_eventos_comunidad = []
    for comunidad, años in datos["eventos_totales_por_comunidad_y_año"].items():
        if str(año) in años:
            comunidades.append(comunidad)
            total_eventos_comunidad.append(años[str(año)])
    fig.add_trace(go.Bar(x=comunidades, y=total_eventos_comunidad, name='Total por Comunidad'), row=1, col=1)

    # Gráfico 2: Eventos totales por provincia y año
    provincias = []
    total_eventos_provincia = []
    for provincia, años in datos["eventos_totales_por_provincia_y_año"].items():
        if str(año) in años:
            provincias.append(provincia)
            total_eventos_provincia.append(años[str(año)])
    fig.add_trace(go.Bar(x=provincias, y=total_eventos_provincia, name='Total por Provincia'), row=1, col=2)
    
    # Gráfico 3: Eventos por comunidad y tipo y año
    for comunidad, tipos in datos["eventos_por_comunidad_tipo_y_año"].items():
        tipos_eventos = []
        total_eventos_tipo_comunidad = []
        for tipo, años in tipos.items():
            if str(año) in años:
                tipos_eventos.append(tipo)
                total_eventos_tipo_comunidad.append(años[str(año)])
        if tipos_eventos:  # Si hay datos para ese año
            fig.add_trace(go.Bar(x=tipos_eventos, y=total_eventos_tipo_comunidad, name=f'{comunidad}'), row=2, col=1)
    
    # Gráfico 4: Eventos por provincia y tipo y año
    for provincia, tipos in datos["eventos_por_provincia_tipo_y_año"].items():
        tipos_eventos = []
        total_eventos_tipo_provincia = []
        for tipo, años in tipos.items():
            if str(año) in años:
                tipos_eventos.append(tipo)
                total_eventos_tipo_provincia.append(años[str(año)])
        if tipos_eventos:  # Si hay datos para ese año
            fig.add_trace(go.Bar(x=tipos_eventos, y=total_eventos_tipo_provincia, name=f'{provincia}'), row=2, col=2)

    # Layout de la figura
    fig.update_layout(
        title_text=f'Análisis de Eventos en {año}',
        #title_font_color='blue',  # Cambiar el color de la letra del título
        #title_font=dict(size=24, color='blue'),  # Cambiar el tamaño y color de la letra del título
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa',
        showlegend=False,
        height=800,
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
    output_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'graphs', f'graficas_eventos_{año}.html')
    fig.write_html(output_path)
    print(f'Archivo {output_path} creado con éxito.')

# Función principal para leer los datos y generar gráficos para cada año
def main():
    with open('events_by_year.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Obtener todos los años presentes en los datos
    años = set()
    for años_comunidad in datos["eventos_totales_por_comunidad_y_año"].values():
        años.update(años_comunidad.keys())
    for años_provincia in datos["eventos_totales_por_provincia_y_año"].values():
        años.update(años_provincia.keys())
    for tipos_comunidad in datos["eventos_por_comunidad_tipo_y_año"].values():
        for años_tipo in tipos_comunidad.values():
            años.update(años_tipo.keys())
    for tipos_provincia in datos["eventos_por_provincia_tipo_y_año"].values():
        for años_tipo in tipos_provincia.values():
            años.update(años_tipo.keys())
    
    # Generar gráficos para cada año
    for año in sorted(años):
        crear_graficas_html(año, datos)

if __name__ == "__main__":
    main()