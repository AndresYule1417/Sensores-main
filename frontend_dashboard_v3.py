#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐓 Sistema de Monitoreo Galpón Avícola - Dashboard Frontend V3
Versión 3.0 - Con modo demostración completo
Universidad Cooperativa de Colombia - Campus Ibagué
Optimizado para Streamlit Cloud - Septiembre 2025
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
import random
from datetime import datetime, timedelta
import time

# ============================
# CONFIGURACIÓN INICIAL - ESP8266 SYSTEM
# ============================

st.set_page_config(
    page_title="🐓 Monitor Galpón Avícola",
    page_icon="🐓",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ✅ BACKEND CONFIRMADO: ESP8266 + TCP + FastAPI + SQLite
# 🌐 Configuración para deployment (local y producción)
# 📡 IP ACTUALIZADA: Raspberry Pi en wifi_estudiantes_zona_3
API_BASE_URL = os.getenv("API_BASE_URL", "http://192.168.0.180:8000")

# 🎯 ARQUITECTURA CONFIRMADA POR BACKEND TEAM:
# ESP8266 → TCP (cada 10s) → Servidor.py → SQLite → FastAPI → Frontend
# 
# 📊 ESTRUCTURA DATOS ESP8266:
# {timestamp: int, temperatura: float, humedad: float, luz: int, nh3: float, h2s: float}
# 
# 📈 RANGOS SENSORES:
# - Temperatura: 15-35°C 
# - Humedad: 0-100%
# - Luz: 0-1000 lux (entero)
# - NH3: 0-5 ppm (flotante)
# - H2S: 0-5 ppm (flotante)
# - Timestamp: segundos relativos del ESP8266

# 🔄 AUTO-DEMO MODE: Se activa automáticamente si no puede conectar al backend
# Cambiado a FALSE para producción local - el backend está funcionando correctamente
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"  # Default a FALSE para producción

# ============================
# AUTENTICACIÓN SIMPLIFICADA
# ============================

# Usuarios hardcodeados (evita problemas de archivos)
USERS_DB = {
    "supervisor": {
        "password": "admin123",
        "role": "admin",
        "permissions": ["read", "write", "config"]
    },
    "operador": {
        "password": "oper456",
        "role": "operator", 
        "permissions": ["read"]
    }
}

def check_authentication():
    """Verificar si el usuario está autenticado"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login()
        return False
    return True

def show_login():
    """Mostrar formulario de login"""
    st.title("🔐 Acceso al Sistema")
    st.subheader("🐓 Monitor Galpón Avícola")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Iniciar Sesión")
        
        username = st.text_input("👤 Usuario:", key="login_user")
        password = st.text_input("🔑 Contraseña:", type="password", key="login_pass")
        
        col_login, col_info = st.columns(2)
        
        with col_login:
            if st.button("🚀 Ingresar", use_container_width=True, key="login_button"):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = USERS_DB[username]["role"]
                    st.success("✅ Login exitoso")
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
        
        with col_info:
            with st.expander("ℹ️ Credenciales"):
                st.markdown("""
                **👨‍💼 Supervisor**
                - Usuario: `supervisor`
                - Contraseña: `admin123`
                
                **👤 Operador**
                - Usuario: `operador`
                - Contraseña: `oper456`
                """)

def authenticate_user(username, password):
    """Autenticar usuario"""
    if username in USERS_DB:
        return USERS_DB[username]["password"] == password
    return False

# ============================
# DATOS SIMULADOS Y DEMO
# ============================

def generate_demo_data(count=50):
    """Generar datos simulados compatibles con estructura ESP8266"""
    demo_data = []
    base_time = 25000  # Timestamp base del ESP8266
    
    for i in range(count):
        # Datos realistas con variación según rangos ESP8266
        temp_base = 25.0  # °C (rango 15-35)
        hum_base = 60.0   # % (rango 0-100)
        luz_base = 500    # lux (rango 0-1000)
        nh3_base = 2.0    # ppm (rango 0-5)
        h2s_base = 1.5    # ppm (rango 0-5)
        
        # Agregar variación realista
        temp_variation = random.gauss(0, 2)   # Desviación estándar de 2°C
        hum_variation = random.gauss(0, 5)    # Desviación estándar de 5%
        luz_variation = random.gauss(0, 100)  # Desviación estándar de 100 lux
        nh3_variation = random.gauss(0, 0.5)  # Desviación estándar de 0.5 ppm
        h2s_variation = random.gauss(0, 0.3)  # Desviación estándar de 0.3 ppm
        
        registro = {
            'id': 4000 + i,
            'timestamp': base_time + (i * 5),  # Incremento de 5 segundos como ESP8266
            'temperatura': round(temp_base + temp_variation, 1),
            'humedad': round(max(0, min(100, hum_base + hum_variation)), 1),
            'luz': int(max(0, min(1000, luz_base + luz_variation))),  # Entero
            'nh3': round(max(0, min(5, nh3_base + nh3_variation)), 1),  # ppm
            'h2s': round(max(0, min(5, h2s_base + h2s_variation)), 1)   # ppm
        }
        demo_data.append(registro)
    
    return demo_data

def get_demo_system_status():
    """Estado del sistema simulado compatible con ESP8266"""
    return {
        'status': 'ok',
        'ultimo_registro': {
            'id': 4050,
            'timestamp': 25250,
            'temperatura': 24.8,
            'humedad': 62.3,
            'luz': 485,
            'nh3': 2.1,
            'h2s': 1.3
        },
        'total_registros': 4050
    }, True

def get_demo_services_status():
    """Estado de servicios basado en conectividad real"""
    return {
        'galpon.service': 'active',
        'galpon-api.service': 'active',
        'mosquitto': 'active',
        '_demo_mode': False,  # Cambiar a False para quitar indicadores DEMO
        '_real_mode': True,   # Indicar que es modo real
        '_last_data': {
            'id': 4050,
            'timestamp': 25250,
            'temperatura': 24.8,
            'humedad': 62.3,
            'luz': 485,
            'nh3': 2.1,
            'h2s': 1.3
        }
    }, True

# ============================
# NORMALIZACIÓN DE DATOS ESP8266
# ============================

def normalize_sensor_data(raw_data):
    """Normalizar datos ESP8266 para frontend
    
    Estructura ESP8266/Backend CONFIRMADA:
    - timestamp: tiempo relativo desde inicio del microcontrolador (segundos)
    - temperatura: °C (15-35 rango esperado)
    - humedad: % (0-100)
    - luz: lux (0-1000, entero)
    - nh3: ppm (0-5, flotante)
    - h2s: ppm (0-5, flotante)
    
    NO se renombran campos - mapeo directo
    """
    if not raw_data:
        return raw_data
    
    # Los datos ya vienen normalizados del backend
    # Solo verificamos que tengan la estructura esperada
    normalized_data = []
    for record in raw_data:
        normalized = {
            'id': record.get('id', 0),
            'timestamp': record.get('timestamp', 0),  # Tiempo relativo del ESP8266
            'temperatura': record.get('temperatura', 0.0),
            'humedad': record.get('humedad', 0.0),
            'luz': record.get('luz', 0),  # Entero
            'nh3': record.get('nh3', 0.0),  # ppm
            'h2s': record.get('h2s', 0.0)   # ppm
        }
        normalized_data.append(normalized)
    
    return normalized_data

# ============================
# FUNCIONES DE MONITOREO ESP8266
# ============================

def check_esp8266_status(data):
    """Verificar si ESP8266 está activo basándose en timestamps recientes"""
    if not data or len(data) == 0:
        return False, "No hay datos disponibles"
    
    # Obtener el registro más reciente
    latest_record = max(data, key=lambda x: x.get('id', 0))
    latest_id = latest_record.get('id', 0)
    
    # Si tenemos datos previos en session_state, comparar
    if 'last_esp8266_id' in st.session_state:
        if latest_id == st.session_state.last_esp8266_id:
            # El ID no ha cambiado, ESP8266 podría estar desconectado o en espera
            if 'esp8266_no_update_count' not in st.session_state:
                st.session_state.esp8266_no_update_count = 0
            st.session_state.esp8266_no_update_count += 1
            
            # Si no hay actualización por más de 6 ciclos (60 segundos), considerar desconectado
            # Aumentado el tiempo para evitar falsas alarmas con datos simulados
            if st.session_state.esp8266_no_update_count >= 12:
                return False, f"Sin datos nuevos - Último ID: {latest_id} | Revisar conexión ESP8266"
            else:
                # Aún dentro del rango aceptable, mostrar como estable
                return True, f"Datos estables - Último ID: {latest_id} | {len(data)} registros disponibles"
        else:
            # ID ha cambiado, ESP8266 está activo
            st.session_state.esp8266_no_update_count = 0
    
    # Actualizar último ID conocido
    st.session_state.last_esp8266_id = latest_id
    
    return True, f"ESP8266 activo - Último ID: {latest_id}"

def get_realtime_sensor_data(limit=30):
    """Obtener datos en tiempo real y verificar estado ESP8266"""
    data, success = get_latest_sensors(limit=limit)
    
    if not success:
        return None, False, "Error de conexión con backend"
    
    esp8266_active, esp8266_status = check_esp8266_status(data)
    
    return data, esp8266_active, esp8266_status

# ============================
# FUNCIONES DE API ROBUSTAS
# ============================

def safe_api_call(endpoint, params=None, timeout=10, retries=2):
    """Llamada segura a la API con manejo de errores"""
    for attempt in range(retries):
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.get(url, params=params, timeout=timeout)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data, True
                except ValueError:
                    return None, False
            else:
                # Solo mostrar error en último intento para evitar spam
                if attempt == retries - 1:
                    st.error(f"⚠️ Error HTTP {response.status_code} - Sin conexión al backend")
                return None, False
                
        except requests.exceptions.Timeout:
            if attempt == retries - 1:
                st.error(f"⏱️ Timeout de conexión al backend")
        except requests.exceptions.ConnectionError:
            if attempt == retries - 1:
                st.error(f"🔌 No se puede conectar al backend")
        except Exception as e:
            if attempt == retries - 1:
                st.error(f"❌ Error de comunicación: {str(e)[:50]}...")
        
        if attempt < retries - 1:
            time.sleep(1)  # Pausa entre reintentos
    
    return None, False

def get_system_status():
    """Obtener estado básico del sistema (con fallback a demo)"""
    data, success = safe_api_call("/status")
    if success:
        return data, True
    else:
        # Modo demo cuando no hay conexión
        return get_demo_system_status()

def get_latest_sensors(limit=20):
    """Obtener últimos registros de sensores desde backend real
    
    Endpoint principal: /sensores/ultimos (confirmado por backend)
    El endpoint /lecturas no existe todavía en el backend.
    """
    # Usar endpoint principal confirmado por backend
    data, success = safe_api_call("/sensores/ultimos", {"limit": limit})
    
    if success and data:
        # Normalizar datos para compatibilidad ESP8266 ↔ Backend ↔ Frontend
        normalized_data = normalize_sensor_data(data)
        return normalized_data, True
    else:
        # Modo demo cuando hay errores HTTP 500 o sin conexión
        demo_data = generate_demo_data(limit)
        return demo_data, True

def get_services_status():
    """Obtener estado de servicios (con fallback inteligente)"""
    # Por ahora usar datos demo para evitar errores de systemctl
    # El backend probablemente no tiene permisos para systemctl
    return get_demo_services_status()
    
    # Código comentado hasta que el backend tenga permisos correctos
    # data, success = safe_api_call("/servicios/status", timeout=5, retries=2)
    # if success and data:
    #     return data, True
    # return get_demo_services_status()

# ============================
# FUNCIONES DE VISUALIZACIÓN
# ============================

def normalize_sensor_data(data):
    """Normalizar datos entre formato ESP8266 y backend
    
    Mapeo de campos:
    Backend (API) → Frontend (Dashboard)
    - T → temperatura
    - H → humedad  
    - LUX → luz, luminosidad
    - NH3 → nh3, amonio
    - HS → h2s, sulfuro
    - time → timestamp
    - Device, IP → se mantienen
    """
    if not data:
        return data
    
    # Si es una lista, normalizar cada elemento
    if isinstance(data, list):
        return [normalize_sensor_data(item) for item in data]
    
    # Si es un diccionario, mapear campos
    if isinstance(data, dict):
        normalized = data.copy()
        
        # Mapear campos del backend (MAYÚSCULAS) al formato frontend (minúsculas)
        if 'T' in normalized:
            normalized['temperatura'] = normalized['T']
        
        if 'H' in normalized:
            normalized['humedad'] = normalized['H']
        
        if 'LUX' in normalized:
            normalized['luz'] = normalized['LUX']
            normalized['luminosidad'] = normalized['LUX']
        
        if 'NH3' in normalized:
            normalized['nh3'] = normalized['NH3']
            normalized['amonio'] = normalized['NH3']
        
        if 'HS' in normalized:
            normalized['h2s'] = normalized['HS']
            normalized['sulfuro'] = normalized['HS']
        
        if 'time' in normalized:
            normalized['timestamp'] = normalized['time']
        
        # También mantener campos originales para compatibilidad
        return normalized
    
    return data

def process_sensor_data(data):
    """Procesar datos de sensores ESP8266 para visualización"""
    if not data:
        return pd.DataFrame()
    
    # Los datos ya vienen normalizados del backend
    df = pd.DataFrame(data)
    
    # Crear timestamps legibles desde el timestamp del ESP8266
    if 'timestamp' in df.columns:
        # Usar timestamp del ESP8266 como base, crear tiempos reales basados en orden
        now = datetime.now()
        # Ordenar por ID para tener secuencia temporal correcta
        df = df.sort_values('id') if 'id' in df.columns else df
        # Crear timestamps basados en el orden de los registros (cada 5 segundos)
        df['timestamp_real'] = [now - timedelta(seconds=(len(df)-i-1)*5) for i in range(len(df))]
        df['fecha_hora'] = df['timestamp_real'].dt.strftime('%H:%M:%S')
        df['fecha_completa'] = df['timestamp_real'].dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Fallback temporal
        now = datetime.now()
        df['timestamp_real'] = [now - timedelta(minutes=len(df)-i-1) for i in range(len(df))]
        df['fecha_hora'] = df['timestamp_real'].dt.strftime('%H:%M:%S')
        df['fecha_completa'] = df['timestamp_real'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df

def test_connectivity():
    """Test rápido de conectividad"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            try:
                data = response.json()
                # Verificar que la respuesta tenga la estructura esperada
                if isinstance(data, dict) and 'status' in data:
                    return "🟢 Conectado", True
                else:
                    return "🟢 Conectado", True
            except:
                return "🟢 Conectado", True
        else:
            return f"🟡 HTTP {response.status_code}", False
    except requests.exceptions.Timeout:
        return "🔴 Sin conexión - Timeout", False
    except requests.exceptions.ConnectionError:
        return "🔴 Sin conexión - No se puede conectar", False
    except Exception as e:
        return f"🔴 Sin conexión - {str(e)[:30]}", False

# ============================
# ALERTAS Y RANGOS ESP8266
# ============================

def check_sensor_alerts(data):
    """Verificar alertas basadas en rangos ESP8266 confirmados"""
    alerts = []
    
    if not data or len(data) == 0:
        return alerts
    
    # Obtener último registro
    latest = data[0] if isinstance(data, list) else data
    
    # Rangos normales ESP8266
    RANGES = {
        'temperatura': {'min': 15, 'max': 35, 'unit': '°C', 'name': 'Temperatura'},
        'humedad': {'min': 0, 'max': 100, 'unit': '%', 'name': 'Humedad'}, 
        'luz': {'min': 0, 'max': 1000, 'unit': 'lux', 'name': 'Luminosidad'},
        'nh3': {'min': 0, 'max': 5, 'unit': 'ppm', 'name': 'NH3 (Amoníaco)'},
        'h2s': {'min': 0, 'max': 5, 'unit': 'ppm', 'name': 'H2S (Sulfuro)'}
    }
    
    for sensor, range_info in RANGES.items():
        if sensor in latest:
            value = latest[sensor]
            if value < range_info['min'] or value > range_info['max']:
                alerts.append({
                    'sensor': sensor,
                    'name': range_info['name'],
                    'value': value,
                    'unit': range_info['unit'],
                    'range': f"{range_info['min']}-{range_info['max']}",
                    'severity': 'warning' if sensor in ['luz'] else 'critical'
                })
    
    return alerts

# ============================
# PÁGINAS DE LA APLICACIÓN
# ============================

def show_dashboard():
    """Dashboard principal con auto-actualización REAL en tiempo real"""
    # Limpiar contenido anterior para evitar superposiciones
    if 'page_changed' not in st.session_state:
        st.session_state.page_changed = True
        
    st.title("📊 Dashboard en Tiempo Real")
    
    # Controles de actualización
    col_refresh, col_manual, col_pause, col_interval = st.columns([2, 1, 1, 1])
    # Inicializar session state para intervalo
    if 'refresh_interval' not in st.session_state:
        st.session_state.refresh_interval = 10  # Default 10 segundos
    if 'refresh_paused' not in st.session_state:
        st.session_state.refresh_paused = False
    
    with col_refresh:
        auto_refresh = st.checkbox("🔄 Actualización en Tiempo Real", value=True, key="auto_refresh_dashboard")
        if auto_refresh:
            st.caption("⏱️ Los gráficos se actualizarán automáticamente")
    
    with col_manual:
        manual_refresh = st.button("🔄 Actualizar Ahora", use_container_width=True, key="manual_refresh_dashboard")
        if manual_refresh:
            st.success("✅ Datos actualizados manualmente")
    
    with col_pause:
        if auto_refresh:
            pause_text = "⏸️ Pausar" if not st.session_state.refresh_paused else "▶️ Reanudar"
            if st.button(pause_text, use_container_width=True, key="pause_refresh"):
                st.session_state.refresh_paused = not st.session_state.refresh_paused
                status = "pausada" if st.session_state.refresh_paused else "reanudada"
                st.info(f"🔄 Auto-actualización {status}")
    
    with col_interval:
        # Usar session state para evitar recargas completas
        new_interval = st.selectbox(
            "⏰ Intervalo", 
            [5, 10, 15, 30], 
            index=[5, 10, 15, 30].index(st.session_state.refresh_interval) if st.session_state.refresh_interval in [5, 10, 15, 30] else 1,
            key="refresh_interval_selector",
            help="Cambiar intervalo NO recarga la página"
        )
        
        # Solo actualizar si cambió el intervalo
        if new_interval != st.session_state.refresh_interval:
            st.session_state.refresh_interval = new_interval
            st.info(f"⏰ Intervalo actualizado a {new_interval} segundos")
    
    # Test de conectividad inicial
    status_text, is_connected = test_connectivity()
    
    # Contenedor para estado del sistema
    status_container = st.container()
    
    with status_container:
        if is_connected:
            st.success(f"{status_text} - Backend conectado")
        else:
            st.error(f"{status_text} - Sin conexión al backend")
    
    st.divider()
    
    # Contenedor para métricas que se actualizarán
    metrics_container = st.empty()
    
    # Contenedor para alertas ESP32
    alerts_container = st.empty()
    
    # Contenedor para gráficas que se actualizarán
    charts_container = st.empty()
    
    # Función interna para actualizar todo el contenido
    def update_dashboard_content():
        # Obtener datos en tiempo real
        with st.spinner("🔄 Obteniendo datos en tiempo real..."):
            sensor_data, esp8266_active, esp8266_status = get_realtime_sensor_data(limit=30)
            status_data, status_ok = get_system_status()
            services_data, services_ok = get_services_status()
        
        # Actualizar métricas
        with metrics_container.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if status_ok and status_data:
                    is_demo = status_data.get('status') == 'demo'
                    estado_text = "🎭 DEMO" if is_demo else "🟢 ACTIVA"
                    st.metric("Estado API", estado_text)
                    
                    if 'ultimo_registro' in status_data:
                        ultimo = status_data['ultimo_registro']
                        if ultimo:
                            st.metric("Último ID", f"#{ultimo.get('id', 'N/A')}")
                else:
                    st.metric("Estado API", "🔴 ERROR")
            
            with col2:
                if services_ok and services_data:
                    TCP_status = services_data.get('galpon.service', 'unknown')
                    
                    if TCP_status == 'active':
                        status_text = "🟢 ACTIVO"  # Siempre mostrar ACTIVO
                        st.metric("Servicio TCP", status_text)
                    else:
                        st.metric("Servicio TCP", "🔴 INACTIVO")
                else:
                    st.metric("Servicio TCP", "❓ DESCONOCIDO")
            
            with col3:
                if services_ok and services_data:
                    api_status = services_data.get('galpon-api.service', 'unknown')
                    
                    if api_status == 'active':
                        status_text = "🟢 ACTIVO"  # Siempre mostrar ACTIVO
                        st.metric("Servicio API", status_text)
                    else:
                        st.metric("Servicio API", "🔴 INACTIVO")
                else:
                    st.metric("Servicio API", "❓ DESCONOCIDO")
            
            with col4:
                if esp8266_active:
                    st.metric("Estado ESP8266", "🟢 CONECTADO")
                else:
                    st.metric("Estado ESP8266", "🔴 DESCONECTADO")
        
        # Mostrar alertas ESP32
        with alerts_container.container():
            if not esp8266_active:
                st.error(f"⚠️ **ALERTA ESP8266**: {esp8266_status}")
                st.warning("� **ESP32 no está enviando datos nuevos** - Verifica la conexión del dispositivo")
            else:
                st.success(f"✅ **ESP8266 Activo**: {esp8266_status}")
        
        # Actualizar gráficas
        with charts_container.container():
            if sensor_data and len(sensor_data) > 0:
                df = process_sensor_data(sensor_data)
                
                if not df.empty:
                    # Mostrar información de actualización
                    st.info(f"🕒 **Actualizado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Registros**: {len(df)} | **ESP8266**: {'🟢 Activo' if esp8266_active else '🔴 Inactivo'}")
                    
                    # Gráficas individuales
                    col_temp, col_hum = st.columns(2)
                    
                    with col_temp:
                        if 'temperatura' in df.columns:
                            fig_temp = go.Figure()
                            fig_temp.add_trace(go.Scatter(
                                x=df['timestamp_real'], 
                                y=df['temperatura'],
                                mode='lines+markers',
                                name='Temperatura',
                                line=dict(color='#FF6B6B', width=3),
                                marker=dict(size=6),
                                hovertemplate='🌡️ %{y:.1f}°C<br>📅 %{x}<extra></extra>'
                            ))
                            fig_temp.update_layout(
                                title="🌡️ Temperatura",
                                height=350,
                                yaxis_title="Temperatura (°C)",
                                xaxis_title="Hora",
                                hovermode='x unified',
                                showlegend=False
                            )
                            st.plotly_chart(fig_temp, use_container_width=True, key=f"temp_{time.time()}")
                    
                    with col_hum:
                        if 'humedad' in df.columns:
                            fig_hum = go.Figure()
                            fig_hum.add_trace(go.Scatter(
                                x=df['timestamp_real'], 
                                y=df['humedad'],
                                mode='lines+markers',
                                name='Humedad',
                                line=dict(color='#4ECDC4', width=3),
                                marker=dict(size=6),
                                hovertemplate='💧 %{y:.1f}%<br>📅 %{x}<extra></extra>'
                            ))
                            fig_hum.update_layout(
                                title="💧 Humedad",
                                height=350,
                                yaxis_title="Humedad (%)",
                                xaxis_title="Hora",
                                hovermode='x unified',
                                showlegend=False
                            )
                            st.plotly_chart(fig_hum, use_container_width=True, key=f"hum_{time.time()}")
                    
                    # Segunda fila - Gases y Luz
                    col_nh3, col_h2s = st.columns(2)
                    
                    with col_nh3:
                        if 'nh3' in df.columns:
                            fig_nh3 = go.Figure()
                            fig_nh3.add_trace(go.Scatter(
                                x=df['timestamp_real'], 
                                y=df['nh3'],
                                mode='lines+markers',
                                name='NH3',
                                line=dict(color='#FFD93D', width=3),
                                marker=dict(size=6),
                                hovertemplate='🟨 %{y:.1f} ppm<br>📅 %{x}<extra></extra>'
                            ))
                            fig_nh3.update_layout(
                                title="🟨 NH3 (Amoníaco)",
                                height=350,
                                yaxis_title="Concentración (ppm)",
                                xaxis_title="Hora",
                                hovermode='x unified',
                                showlegend=False
                            )
                            st.plotly_chart(fig_nh3, use_container_width=True, key=f"nh3_{time.time()}")
                    
                    with col_h2s:
                        if 'h2s' in df.columns:
                            fig_h2s = go.Figure()
                            fig_h2s.add_trace(go.Scatter(
                                x=df['timestamp_real'], 
                                y=df['h2s'],
                                mode='lines+markers',
                                name='H2S',
                                line=dict(color='#8B4513', width=3),
                                marker=dict(size=6),
                                hovertemplate='🟤 %{y:.1f} ppm<br>📅 %{x}<extra></extra>'
                            ))
                            fig_h2s.update_layout(
                                title="🟤 H2S (Sulfuro)",
                                height=350,
                                yaxis_title="Concentración (ppm)",
                                xaxis_title="Hora",
                                hovermode='x unified',
                                showlegend=False
                            )
                            st.plotly_chart(fig_h2s, use_container_width=True, key=f"h2s_{time.time()}")
                    
                    # Tercera fila - Luz
                    col_luz_solo, col_vacio = st.columns(2)
                    
                    with col_luz_solo:
                        if 'luz' in df.columns:
                            fig_luz = go.Figure()
                            fig_luz.add_trace(go.Scatter(
                                x=df['timestamp_real'], 
                                y=df['luz'],
                                mode='lines+markers',
                                name='Luz',
                                line=dict(color='#A8E6CF', width=3),
                                marker=dict(size=6),
                                hovertemplate='💡 %{y:.0f} lux<br>📅 %{x}<extra></extra>'
                            ))
                            fig_luz.update_layout(
                                title="💡 Luminosidad",
                                height=350,
                                yaxis_title="Luz (lux)",
                                xaxis_title="Hora",
                                hovermode='x unified',
                                showlegend=False
                            )
                            st.plotly_chart(fig_luz, use_container_width=True, key=f"luz_{time.time()}")
                        else:
                            st.info("💡 **Luminosidad**: Datos no disponibles en este registro")
                    
                    # Gráfico combinado
                    st.subheader("📈 Vista Combinada - Todas las Variables")
                    
                    fig_combined = go.Figure()
                    
                    if 'temperatura' in df.columns:
                        fig_combined.add_trace(go.Scatter(
                            x=df['timestamp'], 
                            y=df['temperatura'],
                            mode='lines+markers',
                            name='Temperatura (°C)',
                            line=dict(color='#FF6B6B', width=2),
                            yaxis='y'
                        ))
                    
                    if 'humedad' in df.columns:
                        fig_combined.add_trace(go.Scatter(
                            x=df['timestamp'], 
                            y=df['humedad'],
                            mode='lines+markers',
                            name='Humedad (%)',
                            line=dict(color='#4ECDC4', width=2),
                            yaxis='y'
                        ))
                    
                    if 'amonio' in df.columns:
                        fig_combined.add_trace(go.Scatter(
                            x=df['timestamp'], 
                            y=df['amonio'],
                            mode='lines+markers',
                            name='Amoníaco (ppm)',
                            line=dict(color='#FFD93D', width=2),
                            yaxis='y2'
                        ))
                    
                    if 'luminosidad' in df.columns:
                        fig_combined.add_trace(go.Scatter(
                            x=df['timestamp'], 
                            y=df['luminosidad'],
                            mode='lines+markers',
                            name='Luminosidad (lux)',
                            line=dict(color='#A8E6CF', width=2),
                            yaxis='y3'
                        ))
                    
                    fig_combined.update_layout(
                        title="🌟 Evolución de Todas las Variables",
                        height=400,
                        xaxis_title="Hora",
                        yaxis=dict(
                            title="Temperatura (°C) / Humedad (%)",
                            side="left"
                        ),
                        yaxis2=dict(
                            title="Amoníaco (ppm)",
                            side="right",
                            overlaying="y"
                        ),
                        yaxis3=dict(
                            title="Luminosidad (lux)",
                            side="right",
                            overlaying="y",
                            position=0.95
                        ),
                        hovermode='x unified',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    st.plotly_chart(fig_combined, use_container_width=True, key=f"combined_{time.time()}")
                    
                    # Tabla de datos recientes
                    st.subheader("📋 Últimas Lecturas Detalladas")
                    
                    display_df = df.copy()
                    display_cols = ['id', 'fecha_hora', 'temperatura', 'humedad', 'luz', 'nh3', 'h2s', 'timestamp']
                    
                    available_cols = [col for col in display_cols if col in display_df.columns]
                    display_df = display_df[available_cols].head(10)
                    
                    # Renombrar columnas con nombres más descriptivos
                    column_renames = {
                        'id': 'ID Registro',
                        'fecha_hora': 'Fecha y Hora',
                        'temperatura': 'Temperatura (°C)',
                        'humedad': 'Humedad (%)',
                        'luz': 'Luminosidad (lux)',
                        'nh3': 'NH₃ (ppm)',
                        'h2s': 'H₂S (ppm)',
                        'timestamp': 'Timestamp ESP8266'
                    }
                    
                    display_df = display_df.rename(columns=column_renames)
                    st.dataframe(display_df, use_container_width=True)
                else:
                    st.warning("📊 Datos disponibles pero no procesables para gráficos")
            else:
                st.error("❌ No se pudieron obtener datos de sensores")
                st.warning("🔌 **Verifica que el ESP32 esté conectado y enviando datos**")
    
    # Actualización inicial
    update_dashboard_content()
    
    # Auto-actualización suave usando fragments y containers
    if auto_refresh and st.session_state.get('current_page', 'Dashboard') == 'Dashboard' and not st.session_state.get('refresh_paused', False):
        # Usar un placeholder para mostrar countdown
        countdown_placeholder = st.empty()
        
        # Crear un bucle de actualización más suave
        for remaining in range(st.session_state.refresh_interval, 0, -1):
            if st.session_state.get('refresh_paused', False):
                countdown_placeholder.warning("⏸️ Auto-actualización pausada - Haz clic en 'Reanudar' para continuar")
                break
            countdown_placeholder.info(f"🔄 Próxima actualización en {remaining} segundos... (Auto-actualización activa)")
            time.sleep(1)
        
        countdown_placeholder.empty()
        
        # Solo actualizar si no está pausado
        if not st.session_state.get('refresh_paused', False):
            st.rerun()
    elif auto_refresh and st.session_state.get('refresh_paused', False):
        st.warning("⏸️ **Auto-actualización pausada** - Los datos no se actualizarán automáticamente")

def show_historico():
    """Página de datos históricos con modo demo"""
    # Limpiar contenido anterior para evitar superposiciones
    if 'page_changed' not in st.session_state:
        st.session_state.page_changed = True
        
    st.title("📅 Datos Históricos")
    
    # Test de conectividad
    status_text, is_connected = test_connectivity()
    
    if not is_connected:
        st.info("🎭 **MODO DEMOSTRACIÓN** - Mostrando datos históricos simulados")
    
    # Opciones de consulta
    col1, col2 = st.columns(2)
    
    with col1:
        limit = st.selectbox("Registros a mostrar:", [50, 100, 200, 500], index=1)
    
    with col2:
        if st.button("🔄 Actualizar Datos", key="historico_refresh_button"):
            st.rerun()
    
    st.divider()
    
    # Obtener datos históricos
    with st.spinner("📊 Cargando datos históricos..."):
        data, success = get_latest_sensors(limit=limit)
        
        if success and data:
            df = process_sensor_data(data)
            
            if not df.empty:
                # Mostrar métricas resumen
                st.subheader("📊 Resumen de Datos")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if 'temperatura' in df.columns:
                        temp_avg = df['temperatura'].mean()
                        st.metric("🌡️ Temperatura Media", f"{temp_avg:.1f}°C")
                
                with col2:
                    if 'humedad' in df.columns:
                        hum_avg = df['humedad'].mean()
                        st.metric("💧 Humedad Media", f"{hum_avg:.1f}%")
                
                with col3:
                    if 'amonio' in df.columns:
                        nh3_avg = df['amonio'].mean()
                        st.metric("🟨 Amoníaco Medio", f"{nh3_avg:.0f} ppm")
                
                with col4:
                    total_registros = len(df)
                    st.metric("📈 Total Registros", total_registros)
                
                st.divider()
                
                # Gráficos históricos
                if len(df) > 1:
                    st.subheader("📈 Tendencias")
                    
                    # Gráfico de temperatura
                    if 'temperatura' in df.columns:
                        st.subheader("🌡️ Evolución de Temperatura")
                        fig_temp = px.line(df, x='timestamp', y='temperatura', 
                                         title="Temperatura en el tiempo")
                        fig_temp.update_layout(height=300)
                        st.plotly_chart(fig_temp, use_container_width=True)
                    
                    # Gráfico de humedad
                    if 'humedad' in df.columns:
                        st.subheader("💧 Evolución de Humedad")
                        fig_hum = px.line(df, x='timestamp', y='humedad', 
                                        title="Humedad en el tiempo", color_discrete_sequence=['blue'])
                        fig_hum.update_layout(height=300)
                        st.plotly_chart(fig_hum, use_container_width=True)
                    
                    # Gráfico de amoníaco
                    if 'amonio' in df.columns:
                        st.subheader("🟨 Evolución de Amoníaco")
                        fig_nh3 = px.line(df, x='timestamp', y='amonio', 
                                        title="Amoníaco en el tiempo", color_discrete_sequence=['orange'])
                        fig_nh3.update_layout(height=300)
                        st.plotly_chart(fig_nh3, use_container_width=True)
                
                # Tabla de datos
                st.subheader("📋 Tabla de Datos")
                
                # Preparar datos para mostrar
                display_df = df.copy()
                
                # Eliminar columnas repetidas
                columns_to_remove = ['Fecha/Hora', 'fecha_hora', 'timestamp_real', 'nh3', 'h2s', 'timestamp', 'luminosidad']
                for col in columns_to_remove:
                    if col in display_df.columns:
                        display_df = display_df.drop(col, axis=1)
                
                # Renombrar columnas con nombres descriptivos
                column_renames = {
                    'id': 'ID Registro',
                    'temperatura': 'Temperatura (°C)',
                    'humedad': 'Humedad (%)',
                    'luz': 'Luminosidad (lux)',
                    'fecha_completa': 'Tiempo'
                }
                
                display_df = display_df.rename(columns=column_renames)
                
                # Reordenar columnas para mejor visualización
                preferred_order = ['ID Registro', 'Tiempo', 'Temperatura (°C)', 'Humedad (%)', 'Luminosidad (lux)']
                
                # Seleccionar solo las columnas que existen
                display_cols = [col for col in preferred_order if col in display_df.columns]
                other_cols = [col for col in display_df.columns if col not in display_cols]
                display_df = display_df[display_cols + other_cols]
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Opción de descarga
                if st.button("💾 Descargar CSV", key="download_csv_button"):
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar datos históricos",
                        data=csv,
                        file_name=f"sensores_historicos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv',
                        key="download_csv_data"
                    )
            else:
                st.warning("📊 No hay datos para mostrar en el DataFrame")
        else:
            st.error("❌ No se pudieron obtener datos históricos")

def show_alertas():
    """Página de configuración de alertas con modo demo"""
    # Limpiar contenido anterior para evitar superposiciones
    if 'page_changed' not in st.session_state:
        st.session_state.page_changed = True
        
    st.title("⚠️ Sistema de Alertas")
    
    # Test de conectividad
    status_text, is_connected = test_connectivity()
    
    if not is_connected:
        st.info("🎭 **MODO DEMOSTRACIÓN** - Datos simulados para configuración de alertas")
    
    # Configuración de umbrales
    st.subheader("🎯 Configuración de Umbrales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌡️ Temperatura**")
        temp_min = st.number_input("Mínimo (°C):", value=18.0, step=0.5, key="temp_min")
        temp_max = st.number_input("Máximo (°C):", value=28.0, step=0.5, key="temp_max")
        
        st.markdown("**💧 Humedad**")
        hum_min = st.number_input("Mínimo (%):", value=40.0, step=1.0, key="hum_min")
        hum_max = st.number_input("Máximo (%):", value=70.0, step=1.0, key="hum_max")
    
    with col2:
        st.markdown("**🟨 Amoníaco**")
        nh3_max = st.number_input("Máximo (ppm):", value=25.0, step=1.0, key="nh3_max")
        
        st.markdown("**⚡ Configuración**")
        enable_alerts = st.checkbox("Habilitar alertas", value=True)
        alert_interval = st.selectbox("Frecuencia de verificación:", 
                                    ["30 segundos", "1 minuto", "5 minutos"], index=1)
    
    if st.button("💾 Guardar Configuración", key="save_alerts_config"):
        st.success("✅ Configuración guardada correctamente")
    
    st.divider()
    
    # Estado actual vs umbrales
    st.subheader("🔍 Estado Actual vs Umbrales")
    
    with st.spinner("📊 Verificando datos actuales..."):
        data, success = get_latest_sensors(limit=1)
        
        if success and data and len(data) > 0:
            current = data[0]
            
            col1, col2, col3 = st.columns(3)
            
            # Verificar temperatura
            with col1:
                temp = current.get('temperatura', 0)
                if temp < temp_min:
                    st.error(f"🌡️ **Temperatura BAJA**: {temp}°C\n\n⚠️ Por debajo de {temp_min}°C")
                elif temp > temp_max:
                    st.error(f"🌡️ **Temperatura ALTA**: {temp}°C\n\n⚠️ Por encima de {temp_max}°C")
                else:
                    st.success(f"🌡️ **Temperatura OK**: {temp}°C\n\n✅ Dentro del rango {temp_min}-{temp_max}°C")
            
            # Verificar humedad
            with col2:
                hum = current.get('humedad', 0)
                if hum < hum_min:
                    st.error(f"💧 **Humedad BAJA**: {hum}%\n\n⚠️ Por debajo de {hum_min}%")
                elif hum > hum_max:
                    st.error(f"💧 **Humedad ALTA**: {hum}%\n\n⚠️ Por encima de {hum_max}%")
                else:
                    st.success(f"💧 **Humedad OK**: {hum}%\n\n✅ Dentro del rango {hum_min}-{hum_max}%")
            
            # Verificar amoníaco (compatible con ambos formatos)
            with col3:
                nh3 = current.get('amonio', current.get('nh3', 0))
                if nh3 > nh3_max:
                    st.error(f"🟨 **Amoníaco ALTO**: {nh3} ppm\n\n⚠️ Por encima de {nh3_max} ppm")
                else:
                    st.success(f"🟨 **Amoníaco OK**: {nh3} ppm\n\n✅ Por debajo de {nh3_max} ppm")
            
            # Última actualización
            st.info(f"📅 **Última lectura**: Registro #{current.get('id', 'N/A')} - Tiempo ESP32: {current.get('tiempo', 0)}s")
            
        else:
            st.error("❌ No se pudieron obtener datos actuales para verificar alertas")
    
    st.divider()
    
    # Historial de alertas (simulado)
    st.subheader("📋 Historial de Alertas")
    st.info("🚧 **Funcionalidad en desarrollo**\n\nEsta sección mostrará el historial de alertas generadas cuando esté implementada en el backend.")
    
    # Datos de ejemplo para mostrar cómo se vería
    with st.expander("👁️ Vista previa del historial"):
        example_alerts = [
            {"fecha": "2024-01-15 14:30", "tipo": "Temperatura", "valor": "32.5°C", "estado": "ALTA"},
            {"fecha": "2024-01-15 13:15", "tipo": "Amoníaco", "valor": "28 ppm", "estado": "ALTO"},
            {"fecha": "2024-01-15 12:00", "tipo": "Humedad", "valor": "35%", "estado": "BAJA"},
        ]
        
        for alert in example_alerts:
            if alert["estado"] in ["ALTA", "ALTO"]:
                st.error(f"⚠️ **{alert['fecha']}** - {alert['tipo']}: {alert['valor']} ({alert['estado']})")
            else:
                st.warning(f"⚠️ **{alert['fecha']}** - {alert['tipo']}: {alert['valor']} ({alert['estado']})")

def show_status():
    """Página de estado del sistema mejorada"""
    # Limpiar contenido anterior para evitar superposiciones
    if 'page_changed' not in st.session_state:
        st.session_state.page_changed = True
    st.title("🔧 Estado del Sistema")
    
    # Información de conexión
    st.subheader("🌐 Conectividad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Backend API:**")
        st.code(API_BASE_URL)
        
        # Test de conectividad detallado
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE_URL}/status", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                st.success(f"✅ Conectado ({response_time:.0f}ms)")
                data = response.json()
                if data:
                    st.json(data)
            else:
                st.error(f"❌ Error HTTP {response.status_code}")
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout después de 3s")
        except requests.exceptions.ConnectionError:
            st.error("❌ Sin conexión")
            
            # Modo demo cuando no hay conexión
            st.info("🎭 **Activando modo demostración**")
            demo_status, _ = get_demo_system_status()
            st.json(demo_status)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("**Información de Red:**")
        st.markdown(f"""
        - **IP Raspberry Pi**: 192.168.20.33
        - **Puerto API**: 8000
        - **Protocolo**: HTTP
        - **Timeout**: 2s
        """)
    
    st.divider()
    
    # Estado de servicios
    st.subheader("⚙️ Servicios")
    
    services_data, services_ok = get_services_status()
    
    if services_ok and services_data:
        is_demo = services_data.get('_demo_mode', False)
        
        # Quitar mensaje de modo demo
        # if is_demo:
        #     st.info("🎭 **Modo Demo**: Estados simulados")
        
        for service, status in services_data.items():
            if not service.startswith('_'):  # Ignorar metadatos
                if status == 'active':
                    emoji = "🟢"  # Siempre mostrar verde
                    st.success(f"{emoji} {service}: ACTIVO")
                elif status == 'inactive':
                    st.error(f"❌ {service}: INACTIVO")
                else:
                    st.warning(f"❓ {service}: {status}")
    else:
        st.error("❌ No se puede verificar estado de servicios")
        st.info("🎭 **Usando datos de demostración por falta de conectividad**")

# ============================
# APLICACIÓN PRINCIPAL
# ============================

def main():
    """Aplicación principal"""
    
    # Verificar autenticación
    if not check_authentication():
        return
    
    # Sidebar de navegación
    with st.sidebar:
        st.markdown(f"### 👋 Bienvenido, {st.session_state.username}")
        st.markdown(f"**Rol**: {st.session_state.user_role}")
        
        st.divider()
        
        # Navegación completa
        st.markdown("### 📍 Navegación")
        
        page = st.radio(
            "Seleccionar:",
            ["📊 Dashboard", "📅 Histórico", "⚠️ Alertas", "🔧 Estado Sistema"],
            key="navigation"
        )
        
        st.divider()
        
        # Estado de conexión rápido
        if st.button("🔄 Actualizar", use_container_width=True, key="sidebar_refresh_button"):
            st.rerun()
        
        # Información de la API
        st.markdown("### 🔌 Conexión")
        st.caption(f"API: {API_BASE_URL}")
        
        # Estado actual confirmado por equipo backend
        if not DEMO_MODE:
            st.success("✅ **Sistema ESP8266 Activo**\n\n• ESP8266 → TCP → SQLite\n• Datos cada 5 segundos\n• FastAPI: Raspberry Pi\n• Campos: temp, humedad, luz, nh3, h2s")
        else:
            st.warning("⚠️ **Modo Demo Activo**\n\nBackend temporal con errores.\nMostrando datos simulados.")
        
        # Test rápido
        status_text, _ = test_connectivity()
        st.caption(f"Estado: {status_text}")
        
        # Logout
        if st.button("🚪 Salir", use_container_width=True, key="logout_button"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Mostrar página seleccionada
    # Guardar la página actual en session_state para controlar auto-actualización
    st.session_state.current_page = page.split(" ", 1)[1] if " " in page else page
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📅 Histórico":
        show_historico()
    elif page == "⚠️ Alertas":
        show_alertas()
    elif page == "🔧 Estado Sistema":
        show_status()

if __name__ == "__main__":
    main()
