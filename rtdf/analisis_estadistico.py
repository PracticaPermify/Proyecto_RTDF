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
        fechas_audios = Audio.objects.filter(fk_pauta_terapeutica=pauta) \
            .values('fecha_audio') \
            .annotate(num_audios=Count('id_audio'))

        x = [fecha['fecha_audio'] for fecha in fechas_audios]
        y = [fecha['num_audios'] for fecha in fechas_audios]

        pauta_id = pauta.id_pauta_terapeutica  
        pauta_nombre = f"Pauta ID: {pauta_id}" 

        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=pauta_nombre, marker=dict(size=8)))

    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.15, xanchor='left', x=0),
        title='Línea de Tiempo de Pautas Terapéuticas',
        xaxis=dict(title='Fecha'),
        yaxis=dict(title='Número de Audios')
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