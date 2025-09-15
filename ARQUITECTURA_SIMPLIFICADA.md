# 🚀 ARQUITECTURA SIMPLIFICADA - STREAMLIT + POSTGRESQL

## 📋 REUTILIZANDO TU CÓDIGO ACTUAL

¡Excelente! Tu código de `streamlit_app.py` y `main.py` está muy bien estructurado. Vamos a **reutilizar el 90%** y solo hacer pequeñas adaptaciones para:

1. **PostgreSQL local** en Raspberry Pi (en lugar de Railway)
2. **Autenticación simple** en Streamlit  
3. **Acceso público gratuito** con túneles
4. **Optimizaciones** para Raspberry Pi

---

## 🏗️ NUEVA ARQUITECTURA SIMPLIFICADA

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    ESP32    │    │    ESP32    │    │    ESP32    │    │     ...     │
│   Sensor 1  │    │   Sensor 2  │    │   Sensor 3  │    │   Sensor N  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │                   │
        └───────────────────┼───────────────────┼───────────────────┘
                           │                   │
                        WiFi/HTTP POST        │
                           │                   │
                           ▼                   ▼
                ┌─────────────────────────────────────┐
                │          RASPBERRY PI 4B            │
                │                                     │
                │  ┌─────────────────────────────┐    │
                │  │     TU CÓDIGO ACTUAL        │    │
                │  │                             │    │
                │  │ • main.py (FastAPI)         │    │  ← REUTILIZAR
                │  │ • streamlit_app.py          │    │  ← REUTILIZAR  
                │  │ • min_tabla.py              │    │  ← REUTILIZAR
                │  │ • styles.css                │    │  ← REUTILIZAR
                │  └─────────────────────────────┘    │
                │                                     │
                │  ┌─────────────────────────────┐    │
                │  │    POSTGRESQL LOCAL         │    │
                │  │   (optimizado MicroSD)      │    │
                │  │                             │    │
                │  │ • Misma tabla sensors3      │    │  ← REUTILIZAR
                │  │ • Backup automático         │    │  ← NUEVO
                │  │ • Login simple              │    │  ← NUEVO
                │  └─────────────────────────────┘    │
                └─────────────────────────────────────┘
                                   │
                            Túnel público gratuito
                             (Cloudflare/ngrok)
                                   │
                                   ▼
                ┌─────────────────────────────────────┐
                │      ACCESO PÚBLICO GRATUITO        │
                │   https://galpon-ucc.ngrok.io       │
                │                                     │
                │  🌐 Tu Streamlit Dashboard          │  ← REUTILIZAR
                │  🔐 + Login @campusucc.edu.co       │  ← NUEVO
                │  📱 Accesible desde cualquier lugar │  
                └─────────────────────────────────────┘
```

---

## 🔄 QUÉ REUTILIZAMOS (90% del código)

### ✅ **MANTENER SIN CAMBIOS:**
- 📊 `streamlit_app.py` - Dashboard completo
- 🎨 `styles.css` - Estilos personalizados  
- 📈 `min_tabla.py` - Tablas con sparklines
- ⚙️ `SENSOR_RANGES` - Configuración de sensores
- 📡 Estructura de datos ESP32
- 🎯 Gráficos de Plotly
- 🔧 Filtros de tiempo
- 📋 Tabla de datos

### ✅ **PEQUEÑAS ADAPTACIONES:**
- 🔌 `main.py` - Cambiar DATABASE_URL a PostgreSQL local
- 🔐 `streamlit_app.py` - Agregar login simple
- 💾 Base de datos - Cambiar de Railway a PostgreSQL local
- 🌐 Acceso - Agregar túnel público

---

## 💾 CONFIGURACIÓN POSTGRESQL SIMPLIFICADA

### Schema exactamente igual al tuyo:
```sql
-- Reutilizar tu tabla sensors3 exacta
CREATE TABLE sensors3 (
    id SERIAL PRIMARY KEY,
    device VARCHAR(50),
    lux INTEGER,
    nh3 INTEGER, 
    hs INTEGER,
    h INTEGER,
    t INTEGER,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(15)
);

-- Solo agregar tabla simple para login
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 CÓDIGO ADAPTADO (Mínimos cambios)

### 1. `main.py` - Solo cambiar DATABASE_URL
```python
# main.py - IGUAL pero con PostgreSQL local
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# ÚNICO CAMBIO: PostgreSQL local en lugar de Railway
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/galpon_db")
engine = create_engine(DATABASE_URL)

# TODO EL RESTO IGUAL - tu clase SensorData y endpoints
class SensorData(BaseModel):
    device: str
    lux: int
    nh3: int
    hs: int
    h: int
    t: int
    time: str = None

@app.post("/api/sensores")
async def recibir_datos(data: SensorData, request: Request):
    # ... EXACTAMENTE EL MISMO CÓDIGO QUE TIENES
    pass

@app.get("/")
def root():
    return {"msg": "API de sensores activa - Raspberry Pi"}
```

### 2. `streamlit_app.py` - Solo agregar login simple
```python
import streamlit as st
import hashlib

# Función simple de autenticación
def check_login():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🐔 Sistema Galpón Avícola - Login")
        
        email = st.text_input("Email @campusucc.edu.co")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión"):
            if email.endswith("@campusucc.edu.co") and password == "admin123":  # Temporal
                st.session_state.authenticated = True
                st.success("¡Bienvenido!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        
        st.stop()  # No mostrar el resto de la app
    
    # Botón de logout en sidebar
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

# Llamar al inicio de tu app
check_login()

# TODO TU CÓDIGO ACTUAL DE STREAMLIT AQUÍ
# (streamlit_app.py sin cambios)
```

---

## 🔗 ACCESO PÚBLICO GRATUITO

### Opción 1: Ngrok (Más fácil)
```bash
# En Raspberry Pi
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Configurar
ngrok config add-authtoken TU_TOKEN

# Ejecutar (40,000 requests gratuitos/mes)
ngrok http 8501  # Puerto de Streamlit
# Resultado: https://galpon-ucc.ngrok.io
```

### Opción 2: Cloudflare Tunnel (Ilimitado)
```bash
# Instalar cloudflared
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-armhf.deb
sudo dpkg -i cloudflared.deb

# Configurar túnel para Streamlit
cloudflared tunnel --url http://localhost:8501
# Resultado: https://random-name.trycloudflare.com
```

---

## 🚀 INSTALACIÓN SIMPLIFICADA (30 minutos)

### 1. Preparar Raspberry Pi
```bash
# Raspberry Pi OS + actualizaciones
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip postgresql postgresql-contrib
```

### 2. Configurar PostgreSQL
```bash
# Configurar PostgreSQL
sudo -u postgres psql
CREATE DATABASE galpon_db;
CREATE USER galpon_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE galpon_db TO galpon_user;
\q

# Crear tabla (tu schema actual)
psql -U galpon_user -d galpon_db
CREATE TABLE sensors3 (
    id SERIAL PRIMARY KEY,
    device VARCHAR(50),
    lux INTEGER,
    nh3 INTEGER, 
    hs INTEGER,
    h INTEGER,
    t INTEGER,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(15)
);
```

### 3. Subir tu código
```bash
# Copiar tus archivos actuales
scp streamlit_app.py main.py min_tabla.py styles.css pi@IP_RASPBERRY:/home/pi/galpon/

# Instalar dependencias
pip3 install streamlit fastapi uvicorn sqlalchemy psycopg2-binary plotly pandas
```

### 4. Ejecutar
```bash
# Terminal 1: FastAPI (puerto 8000)
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Streamlit (puerto 8501)  
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# Terminal 3: Túnel público
ngrok http 8501
```

---

## 💰 COSTOS FINALES

### Hardware (una vez):
- Raspberry Pi 4B Kit: $80-100
- ESP32 + sensores (6x): $60-80  
- **Total: $140-180**

### Software (gratis para siempre):
- PostgreSQL: $0
- Streamlit: $0
- Ngrok: $0 (40k requests/mes)
- Cloudflare: $0 (ilimitado)
- **Total mensual: $0**

---

## 🎯 BENEFICIOS DE ESTA VERSIÓN

✅ **Reutiliza 90% de tu código actual**  
✅ **Streamlit + PostgreSQL** (tecnologías que ya conoces)  
✅ **Instalación en 30 minutos**  
✅ **Acceso público gratuito**  
✅ **Login @campusucc.edu.co**  
✅ **Sin límites de datos**  
✅ **Control total del sistema**  

**¿Te gusta más esta versión simplificada? ¡Podemos empezar a implementarla ahora mismo!** 🚀