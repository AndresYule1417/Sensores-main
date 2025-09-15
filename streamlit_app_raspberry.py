# 🐔 streamlit_app.py - VERSIÓN RASPBERRY PI
# Basado en tu código actual + autenticación simple

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import time
from min_tabla import create_table_with_sparklines
import os
import hashlib

# =====================================================================
# SISTEMA DE AUTENTICACIÓN SIMPLE
# =====================================================================

def check_password(password):
    """Verificar contraseña simple"""
    # Hash MD5 simple para demo (en producción usar bcrypt)
    return hashlib.md5(password.encode()).hexdigest() == "5e884898da28047151d0e56f8dc6292d"  # "hello"

def login_form():
    """Formulario de login"""
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); max-width: 400px; width: 100%;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 3rem; margin: 0;">🐔</h1>
                <h2 style="color: #2E7D32; margin: 0.5rem 0;">Sistema Galpón Avícola</h2>
                <p style="color: #666; margin: 0;">Universidad Cooperativa de Colombia</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acceso Administrativo")
        
        email = st.text_input(
            "📧 Email", 
            placeholder="nombre.apellido@campusucc.edu.co",
            help="Solo emails @campusucc.edu.co"
        )
        
        password = st.text_input(
            "🔑 Contraseña", 
            type="password",
            placeholder="Ingresa tu contraseña"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Iniciar Sesión", use_container_width=True):
                if email.endswith("@campusucc.edu.co") and check_password(password):
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success("✅ ¡Bienvenido al sistema!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
                    
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>🔒 Acceso solo para personal autorizado UCC</p>
            <p>📞 Soporte: sistemas@campusucc.edu.co</p>
        </div>
        """, unsafe_allow_html=True)

def check_authentication():
    """Verificar estado de autenticación"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_form()
        st.stop()

# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================

st.set_page_config(
    page_title="Monitoreo Galpón Avícola - UCC",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticación antes de mostrar la app
check_authentication()

# Enlaces CSS y fuentes
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Función para cargar estilos CSS locales
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Archivo CSS {file_name} no encontrado")

# Cargar estilos CSS
local_css("styles.css")

# =====================================================================
# SIDEBAR CON INFO DE USUARIO Y LOGOUT
# =====================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2E7D32, #4CAF50); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <div style="color: white; text-align: center;">
            <h3 style="margin: 0;">👤 Usuario Activo</h3>
            <p style="margin: 0.5rem 0; font-size: 0.9rem;">{st.session_state.user_email}</p>
            <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">Acceso autorizado UCC</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.rerun()
    
    st.markdown("---")

# =====================================================================
# CONFIGURACIÓN DE SENSORES (TU CÓDIGO ORIGINAL)
# =====================================================================

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

# =====================================================================
# CONEXIÓN A BASE DE DATOS (ADAPTADA PARA RASPBERRY PI)
# =====================================================================

# Configuración de base de datos para Raspberry Pi
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    db_url = DATABASE_URL
else:
    # Configuración local PostgreSQL en Raspberry Pi
    db_user = os.getenv("DB_USER", "galpon_user")
    db_password = os.getenv("DB_PASSWORD", "password123")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "galpon_db")
    
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Simula una carga de datos con spinner mejorado
with st.spinner("🔄 Conectando con sensores del galpón..."):
    time.sleep(1)

def get_connection():
    """Obtener conexión a la base de datos"""
    try:
        engine = create_engine(db_url)
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"❌ Error al conectar a la base de datos: {e}")  
        st.info("💡 Verifica que PostgreSQL esté corriendo en la Raspberry Pi")
        return None

# =====================================================================
# FUNCIONES DE DATOS (TU CÓDIGO ORIGINAL)
# =====================================================================

def get_latest_data(): 
    """Obtener los últimos registros de sensores"""
    conn = get_connection()
    if conn:
        try:
            query = """ 
            SELECT * 
            FROM sensors3
            ORDER BY time DESC
            LIMIT 50
            """   
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error al obtener datos: {e}")
            conn.close()
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def filter_data_by_time(df, time_filter):
    """Filtrar datos por tiempo (TU FUNCIÓN ORIGINAL)"""
    if df.empty:
        return df
    
    df['time'] = pd.to_datetime(df['time'])
    now = pd.Timestamp.now()
    
    if time_filter == "5 minutos":
        cutoff = now - pd.Timedelta(minutes=5)
    elif time_filter == "1 hora":
        cutoff = now - pd.Timedelta(hours=1)
    elif time_filter == "24 horas":
        cutoff = now - pd.Timedelta(hours=24)
    elif time_filter == "7 días":
        cutoff = now - pd.Timedelta(days=7)
    elif time_filter == "30 días":
        cutoff = now - pd.Timedelta(days=30)
    else:  # "Todos los datos"
        cutoff = df['time'].min()
    
    return df[df['time'] >= cutoff]

# =====================================================================
# INTERFAZ PRINCIPAL (TU DISEÑO ORIGINAL MEJORADO)
# =====================================================================

# Header mejorado
st.markdown("""
<div style="background: linear-gradient(135deg, #1E88E5, #42A5F5); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; justify-content: center;">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">
            🐔 Sistema de Monitoreo Galpón Avícola
        </h1>
    </div>
    <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
        Universidad Cooperativa de Colombia - Campus Neiva
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar mejorado con filtros
st.sidebar.markdown("### 🎛️ Controles del Sistema")

# Filtros de tiempo (TU CÓDIGO ORIGINAL)
time_filter = st.sidebar.selectbox(
    "⏰ Filtro de Tiempo",
    ["5 minutos", "1 hora", "24 horas", "7 días", "30 días", "Todos los datos"],
    index=2,
    help="Selecciona el rango de tiempo para visualizar los datos"
)

# Obtener datos
df = get_latest_data()

if not df.empty:
    # Aplicar filtro de tiempo
    df_filtered = filter_data_by_time(df, time_filter)
    
    # Filtro de dispositivos
    devices = df_filtered['device'].unique() if not df_filtered.empty else []
    selected_devices = st.sidebar.multiselect(
        "📱 Sensores Activos", 
        devices,
        default=devices,
        help="Selecciona los sensores ESP32 a mostrar"
    )
    
    if selected_devices:
        df_filtered = df_filtered[df_filtered['device'].isin(selected_devices)]
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("🔄 Actualización Automática (30s)", value=True)
    
    if auto_refresh:
        placeholder = st.empty()
        refresh_placeholder = st.sidebar.empty()
        
        for seconds in range(30, 0, -1):
            refresh_placeholder.info(f"🔄 Próxima actualización en {seconds}s")
            time.sleep(1)
        
        refresh_placeholder.empty()
        st.rerun()

    # Mostrar estadísticas rápidas
    if not df_filtered.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total Registros", 
                len(df_filtered),
                help="Número total de lecturas en el período seleccionado"
            )
        
        with col2:
            active_devices = df_filtered['device'].nunique()
            st.metric(
                "📱 Sensores Activos", 
                active_devices,
                help="Número de dispositivos ESP32 enviando datos"
            )
        
        with col3:
            if not df_filtered.empty:
                latest_time = df_filtered['time'].max()
                time_diff = pd.Timestamp.now() - latest_time
                minutes_ago = int(time_diff.total_seconds() / 60)
                st.metric(
                    "⏱️ Última Lectura", 
                    f"Hace {minutes_ago} min",
                    help="Tiempo transcurrido desde la última lectura recibida"
                )
        
        with col4:
            avg_temp = df_filtered['t'].mean() if not df_filtered.empty else 0
            st.metric(
                "🌡️ Temp. Promedio", 
                f"{avg_temp:.1f}°C",
                help="Temperatura promedio del galpón en el período"
            )

    # AQUÍ PUEDES AGREGAR EL RESTO DE TU CÓDIGO ORIGINAL:
    # - Gráficos de Plotly
    # - Tablas con sparklines  
    # - Análisis de rangos óptimos
    # - etc.
    
    st.info("📝 **Nota:** Esta es la versión base con autenticación. El resto de tu código de gráficos y tablas se mantiene igual.")
    
    # Mostrar datos en tabla simple por ahora
    if not df_filtered.empty:
        st.markdown("### 📋 Datos Recientes")
        st.dataframe(df_filtered.head(20), use_container_width=True)
    else:
        st.warning("⚠️ No hay datos disponibles para el filtro seleccionado")
        
else:
    st.error("❌ No se pudieron cargar los datos")
    st.info("""
    **Posibles soluciones:**
    - Verifica que PostgreSQL esté corriendo
    - Confirma que la tabla 'sensors3' existe
    - Revisa la configuración de la base de datos
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🏛️ <strong>Universidad Cooperativa de Colombia</strong> - Sistema de Monitoreo Avícola</p>
    <p>📧 Soporte técnico: sistemas@campusucc.edu.co | 🔧 Versión Raspberry Pi 1.0</p>
</div>
""", unsafe_allow_html=True)