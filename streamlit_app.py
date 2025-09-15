import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import time
from min_tabla import create_table_with_sparklines
import os

# Configuración de la página (DEBE SER LA PRIMERA INSTRUCCIÓN)
st.set_page_config(
    page_title="Monitoreo Galpón Avícola",
    page_icon="🐔",
    layout="wide"
)
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Función para cargar estilos CSS locales
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("No se encontró el archivo de estilos CSS.")

# Cargar estilos CSS
local_css(os.path.join(os.path.dirname(__file__), "styles.css"))

# Configuración de rangos óptimos para sensores de galpón avícola
SENSOR_RANGES = {
    'lux': {
        'optimal_min': 10,
        'optimal_max': 300,
        'unit': 'lux',
        'description': 'Iluminación para bienestar animal. Rango óptimo entre 10-100 lux.'
    },
    'nh3': {
        'optimal_min': 0,
        'optimal_max': 250,
        'unit': 'ppm',
        'description': 'Nivel de amoniaco. Valores menores a 20 ppm son seguros para las aves.'
    },
    'hs': {
        'optimal_min': 0,
        'optimal_max': 100,
        'unit': 'ppm',
        'description': 'Sulfuro de hidrógeno. Niveles bajos (< 10 ppm) indican buena ventilación.'
    },
    'h': {
        'optimal_min': 50,
        'optimal_max': 100,
        'unit': '%',
        'description': 'Humedad relativa ideal para galpones. Entre 50-70% reduce estrés.'
    },
    't': {
        'optimal_min': 18,
        'optimal_max': 40,
        'unit': '°C',
        'description': 'Temperatura óptima para aves. Rango entre 18-24°C para máximo confort.'
    }
}

# |||||||||||||||||||||-----Conexión a la base de datos------||||||||||||||||||||||||||||||

# Usa DATABASE_URL si está definida, si no, arma la cadena manualmente
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Usa la cadena de conexión de Neon directamente si no hay variable de entorno
    DATABASE_URL = "postgresql://neondb_owner:npg_ufBQCJ69ZlqU@ep-weathered-violet-ad9xrjey-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

db_url = DATABASE_URL

# Simula una carga de datos
with st.spinner("Cargando datos..."):
    time.sleep(2)

# Función para obtener la conexión a la base de datos
def get_connection():
    try:
        engine = create_engine(db_url)
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

# Obtener los últimos 12 registros de cada dispositivo
def get_latest_data():
    conn = get_connection()
    if conn:
        try:
            query = """
            SELECT *
            FROM sensors3
            ORDER BY time DESC
            LIMIT 30
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error al consultar datos: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Aplicar estilos condicionales a la tabla
def style_table(df):
    def highlight_status(value, sensor):
        opt_range = SENSOR_RANGES[sensor]
        if value < opt_range['optimal_min']:
            return 'background-color: rgba(255, 0, 0, 0.2); color: red;'
        elif value > opt_range['optimal_max']:
            return 'background-color: rgba(255,165,0,0.2); color: orange;'
        return 'background-color: rgba(0, 255, 0, 0.2); color: green;'

    styled_df = df.style.applymap(
        lambda x, sensor: highlight_status(x, sensor), 
        subset=list(SENSOR_RANGES.keys())
    )
    return styled_df

# Calcular el estado general del galpón
def calculate_overall_status(df):
    critical_count = 0
    warning_count = 0

    for sensor, details in SENSOR_RANGES.items():
        if not df.empty:
            last_values = df[sensor]
            critical_count += sum(last_values > details['optimal_max'] * 1.5)  # Valores críticos
            critical_count += sum(last_values < details['optimal_min'] * 0.5)
            warning_count += sum((last_values > details['optimal_max']) & (last_values <= details['optimal_max'] * 1.5))
            warning_count += sum((last_values < details['optimal_min']) & (last_values >= details['optimal_min'] * 0.5))

    if critical_count > 0:
        return "Crítico"
    elif warning_count > 0:
        return "Advertencia"
    else:
        return "Óptimo"

# Función para crear gráficas con los nuevos parámetros
def create_trading_view_plot(df, sensor, title, max_val, min_val):
    # Configuración de sensores con los nuevos límites del eje Y
    sensors_config = [
        ('lux', 'Luminosidad', 300, 0),  # Máximo ajustado a 300
        ('nh3', 'Amoniaco', 250, 0),    # Máximo ajustado a 250
        ('hs', 'Sulfuro de Hidrógeno', 100, 0),  # Máximo ajustado a 100
        ('h', 'Humedad', 100, 0),       # Máximo ya está bien en 100
        ('t', 'Temperatura', 40, 0)     # Máximo ajustado a 40
    ]

    # Crear un rango de tiempo en intervalos de 30 minutos
    time_range = pd.date_range(start="00:00", end="24:00", freq="30T").strftime("%H:%M").tolist()

    # Crear subplots
    fig = make_subplots(
        rows=1,
        cols=len(sensors_config),
        subplot_titles=[cfg[1] for cfg in sensors_config],
        horizontal_spacing=0.05
    )

    for i, (sensor, title, max_val, min_val) in enumerate(sensors_config, start=1):
        opt_range = SENSOR_RANGES[sensor]

        # Evaluar estado del sensor
        last_value = df[sensor].iloc[-1]
        if last_value < opt_range['optimal_min']:
            status = "Bajo"
            color = "rgba(255, 0, 0, 0.2)"  # Rojo
        elif last_value > opt_range['optimal_max']:
            status = "Alto"
            color = "rgba(255, 165, 0, 0.2)"  # Naranja
        else:
            status = "Óptimo"
            color = "rgba(0, 255, 0, 0.2)"  # Verde

        # Crear traza principal
        trace = go.Scatter(
            x=time_range,  # Usar el rango de tiempo generado
            y=df[sensor],  # Valores del sensor
            mode='lines+markers',
            name=title,
            line=dict(color='rgb(0, 123, 255)', width=2),
            fill='tozeroy',
            fillcolor=color
        )

        # Añadir área de rango óptimo
        optimal_area = go.Scatter(
            x=time_range + time_range[::-1],  # Reflejar el rango de tiempo
            y=[opt_range['optimal_max']] * len(time_range) + [opt_range['optimal_min']] * len(time_range)[::-1],
            fill='toself',
            fillcolor='rgba(0, 255, 0, 0.1)',
            line=dict(color='rgba(0,0,0,0)'),
            name='Rango Óptimo',
            showlegend=False
        )

        # Añadir trazas al subplot
        fig.add_trace(trace, row=1, col=i)
        fig.add_trace(optimal_area, row=1, col=i)

        # Configurar rango del eje Y
        fig.update_yaxes(range=[min_val, max_val], row=1, col=i, title_text=f'{title} ({opt_range["unit"]})')

        # Añadir comentario de estado
        fig.add_annotation(
            x=time_range[-1],
            y=last_value,
            text=f"⚠️ {status}: {last_value} {opt_range['unit']}",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40
        )

    # Configurar diseño general
    fig.update_layout(
        template='plotly_dark',
        autosize=True,  # Hacer la gráfica responsiva
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgb(20, 20, 30)',
        paper_bgcolor='rgb(10, 10, 20)'
    )

    return fig

# ||||||||||||||||||||||||||||-----Configuración del dashboard-----||||||||||||||||||||||||||||||

st.title("📈Monitoreo de Galpón Avícola UCC🐔")

# Sidebar con información adicional
st.sidebar.markdown('<h2 style="font-weight: bold; font-size: 1.5rem;">💠 Panel de Control</h2>', unsafe_allow_html=True)

# Título del selectbox con estilo personalizado
st.sidebar.markdown('<h4>⏱️ Rango de tiempo para visualización</h4>', unsafe_allow_html=True)

# Selectbox debajo del título
time_range = st.sidebar.selectbox(
    "",
    ["Últimos 5 minutos", "Últimos 15 minutos", "Últimos 30 minutos", "Última hora", "Últimas 6 horas", "Últimas 12 horas", "Últimas 24 horas", "Últimos 7 días", "Últimos 30 días", "Todos los datos"],
    index=3
)
# Filtrar los datos según la selección de tiempo
def filter_data_by_time(df, time_range):
    if df.empty or 'time' not in df.columns:
        st.warning("No hay datos o falta la columna 'time'.")
        return pd.DataFrame()
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
 
    # Obtener el tiempo actual
    now = pd.Timestamp.now()

    # Calcular el rango de tiempo según la selección
    if time_range == "Últimos 5 minutos":
        start_time = now - pd.Timedelta(minutes=5)
    elif time_range == "Últimos 15 minutos":
        start_time = now - pd.Timedelta(minutes=15)
    elif time_range == "Últimos 30 minutos":
        start_time = now - pd.Timedelta(minutes=30)
    elif time_range == "Última hora":
        start_time = now - pd.Timedelta(hours=1)
    elif time_range == "Últimas 6 horas":
        start_time = now - pd.Timedelta(hours=6)
    elif time_range == "Últimas 12 horas":
        start_time = now - pd.Timedelta(hours=12)
    elif time_range == "Últimas 24 horas":
        start_time = now - pd.Timedelta(hours=24)
    elif time_range == "Últimos 7 días":
        start_time = now - pd.Timedelta(days=7)
    elif time_range == "Últimos 30 días":
        start_time = now - pd.Timedelta(days=30)
    elif time_range == "Todos los datos":
        start_time = None
    else:
        start_time = None

    # Filtrar los datos si se especificó un rango de tiempo
    if start_time:
        df = df[df['time'] >= start_time]

    return df

# Obtener datos iniciales
df = get_latest_data()

# Filtrar los datos según la selección del tiempo
df = filter_data_by_time(df, time_range)

# Renombrar columnas para mostrar encabezados personalizados
columnas_personalizadas = {
    "device": "Dispositivo",
    "lux": "Luminosidad",
    "nh3": "Amoniaco",
    "hs": "Sulfuro de hidrógeno",
    "h": "Humedad",
    "t": "Temperatura",
    "time": "Fecha y hora",
    "row_num": "N° Lectura"
}
df_mostrar = df.rename(columns=columnas_personalizadas)

# Indicador de estado general
overall_status = calculate_overall_status(df)
st.sidebar.markdown("### Estado General del Galpón🛖")
if overall_status == "Óptimo":
    st.sidebar.success(f"Estado: {overall_status}")
elif overall_status == "Advertencia":
    st.sidebar.warning(f"Estado: {overall_status}")
else:
    st.sidebar.error(f"Estado: {overall_status}")

# Título del multiselect con estilo personalizado
st.sidebar.markdown('<h2>🔻 Seleccionar dispositivos</h2>', unsafe_allow_html=True)

# Multiselect debajo del título
selected_devices = st.sidebar.multiselect(
    "",
    options=["ESP1", "ESP2", "ESP3", "ESP4", "ESP5", "ESP6"],
    default=["ESP1", "ESP2", "ESP3", "ESP4", "ESP5", "ESP6"]
)
# Recomendaciones dinámicas por módulo
with st.sidebar.expander("### Recomendaciones por Módulo 🛠️"):
    if df.empty or 'device' not in df.columns:
        st.warning("No hay datos disponibles para mostrar recomendaciones.")
    else:
        for device in selected_devices:
            device_df = df[df['device'] == device]
            if not device_df.empty:
                recommendations = []
                for sensor, details in SENSOR_RANGES.items():
                    last_value = device_df[sensor].iloc[-1]
                    if last_value < details['optimal_min']:
                        deviation = details['optimal_min'] - last_value
                        recommendations.append(f"⚠️ {sensor.upper()}: Aumentar {details['description'].split(' ')[0]} en al menos {deviation:.2f} {details['unit']}.")
                    elif last_value > details['optimal_max']:
                        deviation = last_value - details['optimal_max']
                        recommendations.append(f"⚠️ {sensor.upper()}: Reducir {details['description'].split(' ')[0]} en al menos {deviation:.2f} {details['unit']}.")
                
                if recommendations:
                    st.markdown(f"**{device}:**")
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                else:
                    st.markdown(f"**{device}:** ✅ Todo en orden.")

# Botón de actualización manual
if st.sidebar.button("Actualizar datos 🔄"):
    st.rerun()

# Contenedor para actualización
update_container = st.container()

# ||||||||||||||||||||||||||||||||||||-----Función principal-----||||||||||||||||||||||||||||||
def main():
    while True:
        df = get_latest_data()
        if df.empty:
            st.warning("No se encontraron datos. Verifica la conexión o la tabla.")
            st.stop()

        with update_container:
            # Sección de Tabla de Datos
            st.markdown("## Registro de Últimas Lecturas📝")
            st.markdown("""
            🔶Esta tabla muestra los 12 registros más recientes de todos los sensores. 
            Cada fila representa una lectura de un módulo en un momento específico.
            """)
            # Renombrar columnas para mostrar encabezados personalizados
            columnas_personalizadas = {
                "device": "Dispositivo",
                "lux": "Luminosidad",
                "nh3": "Amoniaco",
                "hs": "Sulfuro de hidrógeno",
                "h": "Humedad",
                "t": "Temperatura",
                "time": "Fecha y hora",
                "row_num": "N° Lectura"
            }
            df_mostrar = df.rename(columns=columnas_personalizadas)

            # Mostrar la tabla con los nuevos encabezados
            st.dataframe(
                df_mostrar,
                use_container_width=True,
                hide_index=True
            )

            # Resumen del Galpón en tarjetas horizontales
            st.markdown("### Resumen del Galpón 📊")
            
            # Verificar que los datos existen antes de calcular promedios
            if not df.empty and all(col in df.columns for col in ['t', 'h', 'nh3']):
                cols = st.columns(3)  # Crear tres columnas para las tarjetas

                # Tarjeta de Temperatura Promedio
                with cols[0]:
                    temp_mean = df['t'].mean()
                    temp_trend = "↑" if temp_mean > SENSOR_RANGES['t']['optimal_max'] else "↓" if temp_mean < SENSOR_RANGES['t']['optimal_min'] else "→"
                    st.markdown(f"""
                    <div class="summary-card" style="
                        border: 1px solid #4CAF50;
                        border-radius: 10px;
                        padding: 15px;
                        background-color: rgba(240, 240, 240, 0.8);
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                    ">
                        <h4 style="margin-bottom: 5px;">🌡️ <strong>Temperatura Promedio</strong></h4>
                        <p style="margin: 0; font-size: 16px;">{temp_mean:.2f} °C</p>
                        <p style="margin: 0; font-size: 14px; color: gray;">Tendencia: {temp_trend}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Tarjeta de Humedad Promedio
                with cols[1]:
                    humidity_mean = df['h'].mean()
                    humidity_trend = "↑" if humidity_mean > SENSOR_RANGES['h']['optimal_max'] else "↓" if humidity_mean < SENSOR_RANGES['h']['optimal_min'] else "→"
                    st.markdown(f"""
                    <div class="summary-card" style="
                        border: 1px solid #2196F3;
                        border-radius: 10px;
                        padding: 15px;
                        background-color: rgba(240, 240, 240, 0.8);
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                    ">
                        <h4 style="margin-bottom: 5px;">💧 <strong>Humedad Promedio</strong></h4>
                        <p style="margin: 0; font-size: 16px;">{humidity_mean:.2f} %</p>
                        <p style="margin: 0; font-size: 14px; color: gray;">Tendencia: {humidity_trend}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Tarjeta de Amoniaco Promedio
                with cols[2]:
                    nh3_mean = df['nh3'].mean()
                    nh3_trend = "↑" if nh3_mean > SENSOR_RANGES['nh3']['optimal_max'] else "↓" if nh3_mean < SENSOR_RANGES['nh3']['optimal_min'] else "→"
                    st.markdown(f"""
                    <div class="summary-card" style="
                        border: 1px solid #FF5722;
                        border-radius: 10px;
                        padding: 15px;
                        background-color: rgba(240, 240, 240, 0.8);
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                    ">
                        <h4 style="margin-bottom: 5px;">⚠️ <strong>Amoniaco Promedio</strong></h4>
                        <p style="margin: 0; font-size: 16px;">{nh3_mean:.2f} ppm</p>
                        <p style="margin: 0; font-size: 14px; color: gray;">Tendencia: {nh3_trend}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No hay suficientes datos para mostrar el resumen del galpón.")

            # Lista de dispositivos
            devices = selected_devices
            
#|||||||||||||||||||||----- Mostrar gráficas y tabla para cada dispositivo-----|||||||||||||||||
        if df.empty or 'device' not in df.columns:
            st.error("No se pueden mostrar los datos de los dispositivos. Verifica la conexión a la base de datos.")
        else:
            for device in devices:
                device_df = df[df['device'] == device]
                if not device_df.empty:
                    # Título del módulo
                    st.markdown(f"""
                    <h2 style='color: #43a047; font-size: 24px; font-weight: bold;'>
                        <i class="fas fa-microchip"></i> Módulo: {device}
                    </h2>
                    """, unsafe_allow_html=True)

                    # Llamar a la función para crear la tabla con Sparklines
                    sensors_config = [
                        ('lux', 'Luminosidad', 140, 60),
                        ('nh3', 'Amoniaco', 25, 5),
                        ('hs', 'Sulfuro de Hidrógeno', 400, 0),
                        ('h', 'Humedad', 100, 70),
                        ('t', 'Temperatura', 24, 18)
                    ]
                    create_table_with_sparklines(device_df, sensors_config, SENSOR_RANGES)

                    # Botón para desplegar/replegar la sección de pestañas
                    if f"{device}_tabs_expanded" not in st.session_state:
                        st.session_state[f"{device}_tabs_expanded"] = False
                    toggle_button_label = "Ocultar Detalles" if st.session_state[f"{device}_tabs_expanded"] else "Ver Detalles"
                    toggle_button_color = "red" if st.session_state[f"{device}_tabs_expanded"] else "green"
                    if st.button(f"{toggle_button_label}", key=f"toggle_tabs_{device}"):
                        st.session_state[f"{device}_tabs_expanded"] = not st.session_state[f"{device}_tabs_expanded"]

                # Mostrar la sección de pestañas si está expandida
                if st.session_state[f"{device}_tabs_expanded"]:
                    tabs = st.tabs(["📊 Gráficas Detalladas", "📝 Explicación y Sugerencias"])
                    # Pestaña de gráficas detalladas
                    with tabs[0]:
                        st.markdown(f"### Gráficas Detalladas del Módulo {device}")
                        for sensor, title, max_val, min_val in sensors_config:
                            st.markdown(f"<h4 style='color: #1E88E5;'>{title}</h4>", unsafe_allow_html=True)
                            opt_range = SENSOR_RANGES[sensor]
                            time_list = device_df['time'].tolist()
                            optimal_max = [opt_range['optimal_max']] * len(time_list)
                            optimal_min = [opt_range['optimal_min']] * len(time_list)

                            optimal_area = go.Scatter(
                                x=time_list + time_list[::-1],
                                y=optimal_max + optimal_min[::-1],
                                fill='toself',
                                fillcolor='rgba(0, 255, 0, 0.1)',
                                line=dict(color='rgba(0,0,0,0)'),
                                name='Rango Óptimo',
                                showlegend=False
                            )
                            # Crear figura individual
                            fig = go.Figure()
                            # Definir la traza para el sensor actual
                            trace = go.Scatter(
                                x=device_df['time'],
                                y=device_df[sensor],
                                mode='lines+markers',
                                name=title,
                                line=dict(color='rgb(0, 123, 255)', width=2)
                            )
                            fig.add_trace(trace)
                            fig.add_trace(optimal_area)
                            # Configurar diseño
                            fig.update_layout(
                                template='plotly_dark',
                                height=300,
                                showlegend=False,
                                margin=dict(l=20, r=20, t=40, b=20),
                                plot_bgcolor='rgb(20, 20, 30)',
                                paper_bgcolor='rgb(10, 10, 20)',
                                title=f"{title} ({opt_range['unit']})"
                            )
                            # Mostrar gráfica
                            st.plotly_chart(fig, use_container_width=True)
                    # Pestaña de explicación y sugerencias
                    with tabs[1]:
                        st.markdown(f"### Explicación y Sugerencias para el Módulo {device}")
                        sensors_config = [
                            ('lux', 'Luminosidad'),
                            ('nh3', 'Amoniaco'),
                            ('hs', 'Sulfuro de Hidrógeno'),
                            ('h', 'Humedad'),
                            ('t', 'Temperatura')
                        ]
                        # Crear columnas para las tarjetas
                        cols = st.columns(len(sensors_config))
                        for i, (sensor, title) in enumerate(sensors_config):
                            details = SENSOR_RANGES[sensor]
                            last_value = device_df[sensor].iloc[-1]
                            # Determinar el estado, color y el ícono de la tarjeta
                            if last_value < details['optimal_min']:
                                status = "Bajo"
                                color = "rgba(255, 0, 0, 0.2)"  # Rojo
                                icon = '<i class="fas fa-exclamation-circle" style="color: red;"></i>'
                                suggestion = f"Aumentar {details['description'].split(' ')[0]} para alcanzar el rango óptimo."
                            elif last_value > details['optimal_max']:
                                status = "Alto"
                                color = "rgba(255, 165, 0, 0.2)"  # Amarillo
                                icon = '<i class="fas fa-exclamation-triangle" style="color: orange;"></i>'
                                suggestion = f"Reducir {details['description'].split(' ')[0]} para alcanzar el rango óptimo."
                            else:
                                status = "Óptimo"
                                color = "rgba(0, 255, 0, 0.2)"  # Verde
                                icon = '<i class="fas fa-check-circle" style="color: green;"></i>'
                                suggestion = "Todo está funcionando correctamente."
                            # Mostrar tarjeta en la columna correspondiente
                            with cols[i]:
                                st.markdown(f"""
                                <div style="
                                    border: 1px solid #ddd;
                                    border-radius: 10px;
                                    padding: 15px;
                                    margin-bottom: 10px;
                                    background-color: {color};
                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                                " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='4px 4px 15px rgba(0, 0, 0, 0.3)';" 
                                    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='2px 2px 5px rgba(0, 0, 0, 0.1)';">
                                    <h4 style="margin-bottom: 5px; color: #1E88E5;">
                                        {icon} {title}
                                    </h4>
                                    <p style="margin: 0; font-size: 14px;">{details['description']}</p>
                                    <p style="margin: 0; font-size: 14px; color: black;">
                                        <strong>Valor Actual:</strong> {last_value} {details['unit']}
                                    </p>
                                    <p style="margin: 0; font-size: 14px; color: #000; font-weight: bold;">
                                        <strong>Estado:</strong> <span style="color: {icon.split('style="color: ')[1].split(';')[0]};">{status}</span>
                                    </p>
                                    <p style="margin: 0; font-size: 14px; color: #000; font-weight: bold;">
                                        <strong>Sugerencia:</strong> <span style="color: #333;">{suggestion}</span>
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.warning(f"No hay datos para {device}.")

        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()