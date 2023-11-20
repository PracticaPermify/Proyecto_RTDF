from plotly.offline import plot
import plotly.graph_objs as go
from plotly.colors import DEFAULT_PLOTLY_COLORS
from .models import *
from django.db.models import Count
from plotly.subplots import make_subplots

def generar_grafico(informe_id):
    fig = go.Figure()

    pautas = PautaTerapeutica.objects.filter(fk_informe=informe_id)

    for pauta in pautas:
        # Consulta para obtener la cantidad de audios por día
        audios_por_dia = Audio.objects.filter(fk_pauta_terapeutica=pauta) \
            .extra({'fecha_audio': "date(fecha_audio)"}) \
            .values('fecha_audio') \
            .annotate(num_audios=Count('id_audio')) \
            .order_by('fecha_audio')

        # Modificación aquí: Utiliza solo la parte de fecha de la fecha y elimina las horas
        x = [fecha['fecha_audio'].strftime('%Y-%m-%d') for fecha in audios_por_dia]
        y = [int(fecha['num_audios']) for fecha in audios_por_dia]  # Convertir a números enteros

        pauta_id = pauta.id_pauta_terapeutica  
        pauta_nombre = f"Pauta ID: {pauta_id}" 
        tipo_pauta = pauta.fk_tp_terapia.tipo_terapia
        fecha_inicio = pauta.fecha_inicio.strftime('%d-%m-%Y')
        fecha_fin = pauta.fecha_fin.strftime('%d-%m-%Y')

        # Asigna un color específico para cada tipo de pauta
        color = None
        if tipo_pauta == 'Vocalizacion':
            color = 'blue'
        elif tipo_pauta == 'Intensidad':
            color = 'red'

        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=f"{pauta_nombre} - {tipo_pauta} ({fecha_inicio} - {fecha_fin})", marker=dict(size=8, color=color)))

    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.18, xanchor='left', x=0),
        title='Línea de Tiempo de Audios Realizados por Día',
        xaxis=dict(title='Fecha'),
        yaxis=dict(title='Número de Audios', tickmode='linear', tick0=0, dtick=1),  # Configuración para mostrar números enteros en el eje Y
        margin=dict(b=80, t=100, l=50, r=50),  # Ajusta estos valores según tu preferencia
        autosize=True,  # Hace que el gráfico sea responsivo
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generar_grafico_horas(informe_id):
    fig = go.Figure()

    pautas = PautaTerapeutica.objects.filter(fk_informe=informe_id)

    for pauta in pautas:
        # Consulta para obtener la cantidad de audios por hora
        audios_por_hora = Audio.objects.filter(fk_pauta_terapeutica=pauta) \
            .extra({'hora_audio': "hour(fecha_audio)"}) \
            .values('hora_audio') \
            .annotate(num_audios=Count('id_audio')) \
            .order_by('hora_audio')

        x = [hora['hora_audio'] for hora in audios_por_hora]
        y = [int(hora['num_audios']) for hora in audios_por_hora]

        pauta_id = pauta.id_pauta_terapeutica
        pauta_nombre = f"Pauta ID: {pauta_id}"
        tipo_pauta = pauta.fk_tp_terapia.tipo_terapia
        fecha_inicio = pauta.fecha_inicio.strftime('%d-%m-%Y')
        fecha_fin = pauta.fecha_fin.strftime('%d-%m-%Y')

        # Asigna un color específico para cada tipo de pauta
        color = None
        if tipo_pauta == 'Vocalizacion':
            color = 'blue'
        elif tipo_pauta == 'Intensidad':
            color = 'red'

        fig.add_trace(go.Bar(x=x, y=y, name=f"{pauta_nombre} - {tipo_pauta} ({fecha_inicio} - {fecha_fin})", marker=dict(color=color)))

    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.18, xanchor='left', x=0),
        title='Cantidad de Audios por Hora',
        xaxis=dict(title='Hora del día', tickmode='array', tickvals=x, ticktext=[f'{hora}:00' for hora in x]),
        yaxis=dict(title='Número de Audios', tickmode='linear', tick0=0, dtick=1),
        margin=dict(b=80, t=100, l=50, r=50),
        autosize=True,
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def convertir_a_numeros(coeficientes):
    return [float(getattr(coeficientes, f'f{i}')) for i in range(5)] + [
        float(coeficientes.intensidad),
        float(coeficientes.hnr),
        float(coeficientes.local_jitter),
        float(coeficientes.local_absolute_jitter),
        float(coeficientes.rap_jitter),
        float(coeficientes.ppq5_jitter),
        float(coeficientes.ddp_jitter),
        float(coeficientes.local_shimmer),
        float(coeficientes.local_db_shimmer),
        float(coeficientes.apq3_shimmer),
        float(coeficientes.aqpq5_shimmer),
        float(coeficientes.apq11_shimmer),
    ]


def generar_grafico_audio(x, y_auto, y_manual):
    # Dividir las categorías de variables
    frecuencias = x[:5]
    intensidad_hnr = x[5:7]
    jitter = x[7:13]
    shimmer = x[13:]

    # Crear subgráficos
    fig = make_subplots(rows=2, cols=2, subplot_titles=['Frecuencias', 'Intensidad y HNR', 'Jitter', 'Shimmer'])

    # Gráfico 1: Frecuencias
    fig.add_trace(go.Scatter(x=frecuencias, y=y_auto[:5], mode='lines+markers', name='Frecuencia Automático'), row=1, col=1)
    fig.add_trace(go.Scatter(x=frecuencias, y=y_manual[:5], mode='lines+markers', name='Frecuencia Manual'), row=1, col=1)

    # Gráfico 2: Intensidad y HNR
    fig.add_trace(go.Scatter(x=intensidad_hnr, y=y_auto[5:7], mode='lines+markers', name='HNR Automático'), row=1, col=2)
    fig.add_trace(go.Scatter(x=intensidad_hnr, y=y_manual[5:7], mode='lines+markers', name='HNR Manual'), row=1, col=2)

    # Gráfico 3: Jitter
    fig.add_trace(go.Scatter(x=jitter, y=y_auto[7:13], mode='lines+markers', name='Jitter Automático'), row=2, col=1)
    fig.add_trace(go.Scatter(x=jitter, y=y_manual[7:13], mode='lines+markers', name='Jitter Manual'), row=2, col=1)

    # Gráfico 4: Shimmer
    fig.add_trace(go.Scatter(x=shimmer, y=y_auto[13:], mode='lines+markers', name='Shimmer Automático'), row=2, col=2)
    fig.add_trace(go.Scatter(x=shimmer, y=y_manual[13:], mode='lines+markers', name='Shimmer Manual'), row=2, col=2)

    # Configuración del diseño general
    fig.update_layout(title='Comparación de Coeficientes',legend_title_text='Legend Group')

    # Renderizar el gráfico y obtener el código HTML
    graph_html = plot(fig, output_type='div', include_plotlyjs=False)

    return graph_html

def grafico_frecuencias(x, y_auto, y_manual):

    # Dividir las categorías de variables
    frecuencias = x[:5]

    # Crear el gráfico
    fig = go.Figure()

    # Gráfico: Frecuencias
    fig.add_trace(go.Scatter(x=frecuencias, y=y_auto[:5], mode='lines+markers', name='Frecuencia Automático'))
    fig.add_trace(go.Scatter(x=frecuencias, y=y_manual[:5], mode='lines+markers', name='Frecuencia Manual'))

    # Configuración del diseño general
    fig.update_layout(title='Comparación de Frecuencias',
                    legend=dict(orientation='h', yanchor='top', y=1.15, xanchor='left', x=0)
                    ,autosize=True)

    # Renderizar el gráfico y obtener el código HTML
    graph_frecuencias = plot(fig, output_type='div', include_plotlyjs=False)

    return graph_frecuencias

def grafico_intensidad(x, y_auto, y_manual):

    # Dividir las categorías de variables
    intensidad_hnr = x[5:7]

    # Crear el gráfico
    fig = go.Figure()

    # Gráfico: Frecuencias
    fig.add_trace(go.Scatter(x=intensidad_hnr, y=y_auto[:5], mode='lines+markers', name='Frecuencia Automático'))
    fig.add_trace(go.Scatter(x=intensidad_hnr, y=y_manual[:5], mode='lines+markers', name='Frecuencia Manual'))

    # Configuración del diseño general
    fig.update_layout(title='Comparación de Intensidad y HNR',legend=dict(orientation='h', yanchor='top', y=1.15, xanchor='left', x=0))

    # Renderizar el gráfico y obtener el código HTML
    graph_intensidad = plot(fig, output_type='div', include_plotlyjs=False)

    return graph_intensidad


def grafico_jitter(x, y_auto, y_manual):

    # Dividir las categorías de variables
    jitter = x[7:13]

    # Crear el gráfico
    fig = go.Figure()

    # Gráfico: Frecuencias
    fig.add_trace(go.Scatter(x=jitter, y=y_auto[:5], mode='lines+markers', name='Frecuencia Automático'))
    fig.add_trace(go.Scatter(x=jitter, y=y_manual[:5], mode='lines+markers', name='Frecuencia Manual'))

    # Configuración del diseño general
    fig.update_layout(title='Comparación de Jitter',legend=dict(orientation='h', yanchor='top', y=1.15, xanchor='left', x=0))

    # Renderizar el gráfico y obtener el código HTML
    graph_jitter = plot(fig, output_type='div', include_plotlyjs=False)

    return graph_jitter

def grafico_shimmer(x, y_auto, y_manual):

    # Dividir las categorías de variables
    shimmer = x[13:]

    # Crear el gráfico
    fig = go.Figure()

    # Gráfico: Frecuencias
    fig.add_trace(go.Scatter(x=shimmer, y=y_auto[:5], mode='lines+markers', name='Frecuencia Automático'))
    fig.add_trace(go.Scatter(x=shimmer, y=y_manual[:5], mode='lines+markers', name='Frecuencia Manual'))

    # Configuración del diseño general
    fig.update_layout(title='Comparación de Shimmer',legend=dict(orientation='h', yanchor='top', y=1.15, xanchor='left', x=0))

    # Renderizar el gráfico y obtener el código HTML
    graph_shimmer = plot(fig, output_type='div', include_plotlyjs=False)

    return graph_shimmer