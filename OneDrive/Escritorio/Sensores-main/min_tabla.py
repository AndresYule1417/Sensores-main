import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Define SENSOR_RANGES with example values
SENSOR_RANGES = {
    "sensor1": {"unit": "°C", "optimal_min": 20, "optimal_max": 30},
    "sensor2": {"unit": "%", "optimal_min": 40, "optimal_max": 60},
    # Add more sensors as needed
}

def create_table_with_sparklines(device_df, sensors_config, sensor_ranges):
    """
    Genera una tabla con Sparklines para cada sensor de un dispositivo.

    Args:
        device_df (pd.DataFrame): Datos del dispositivo.
        sensors_config (list): Lista de configuraciones de sensores.
        sensor_ranges (dict): Rangos óptimos de los sensores.

    Returns:
        None
    """
    # Crear una lista para almacenar las filas de la tabla
    table_rows = []

    for sensor, title, *_ in sensors_config:
        # Obtener los últimos datos del sensor
        sensor_data = device_df[sensor].tolist()
        time_data = device_df['time'].tolist()

        # Crear un Sparkline para el sensor
        sparkline = go.Figure(
            data=[
                go.Scatter(
                    x=time_data,
                    y=sensor_data,
                    mode='lines',
                    line=dict(color='rgb(0, 123, 255)', width=1),
                    fill='tozeroy',
                    fillcolor="rgba(0, 255, 0, 0.2)"
                )
            ],
            layout={
                'template': 'plotly_dark',
                'height': 50,
                'margin': dict(l=5, r=5, t=5, b=5),
                'showlegend': False,
                'xaxis': {'visible': False},
                'yaxis': {'visible': False},
                'plot_bgcolor': 'rgb(20, 20, 30)',
                'paper_bgcolor': 'rgb(10, 10, 20)'
            }
        )

        # Determinar el estado del sensor
        last_value = device_df[sensor].iloc[-1]
        opt_range = sensor_ranges[sensor]
        if last_value < opt_range['optimal_min']:
            status = '<span style="color: red;">Bajo</span>'
        elif last_value > opt_range['optimal_max']:
            status = '<span style="color: orange;">Alto</span>'
        else:
            status = '<span style="color: green;">Óptimo</span>'

        # Agregar fila a la tabla
        table_rows.append({
            "Sensor": title,
            "Último Valor": f"{last_value} {opt_range['unit']}",
            "Estado": status,
            "Sparkline": sparkline
        })

    # Mostrar la tabla con Streamlit
    for row in table_rows:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
        col1.markdown(f"**{row['Sensor']}**")
        col2.markdown(row["Último Valor"])
        col3.markdown(row["Estado"], unsafe_allow_html=True)
        col4.plotly_chart(row["Sparkline"], use_container_width=True)