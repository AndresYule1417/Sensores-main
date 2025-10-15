# 🚀 GUÍA DE DEPLOYMENT PARA STREAMLIT

## 🌐 **Opción 1: Streamlit Cloud (RECOMENDADA)**

### ✅ **Paso 1: Preparar el repositorio**
1. Tu código ya está en GitHub: `https://github.com/AndresYule1417/Sensores-main`
2. Asegúrate de que `requirements_frontend.txt` esté actualizado
3. Archivo principal: `frontend_dashboard_v3.py`

### ✅ **Paso 2: Desplegar en Streamlit Cloud**
1. Ir a: https://streamlit.io/cloud
2. Conectar con tu cuenta de GitHub
3. Seleccionar repositorio: `AndresYule1417/Sensores-main`
4. Archivo principal: `frontend_dashboard_v3.py`
5. Python version: 3.11
6. Click "Deploy"

### 🔧 **Configuración de Variables de Entorno**
En Streamlit Cloud, agregar:
```
API_BASE_URL = "http://192.168.20.33:8000"
DEMO_MODE = "false"
```

---

## 🔄 **Opción 2: Vercel con FastAPI Wrapper**

### 📁 **Estructura para Vercel:**
```
vercel-app/
├── api/
│   └── index.py          # FastAPI wrapper
├── requirements.txt      # Dependencies
├── vercel.json          # Vercel config
└── main.py              # Entry point
```

### ⚙️ **Configuración necesaria:**

1. **vercel.json:**
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

2. **api/index.py:**
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess
import os

app = FastAPI()

@app.get("/")
def run_streamlit():
    # Ejecutar Streamlit como subprocess
    # NOTA: Esto es complejo y no recomendado
    pass
```

---

## 🎯 **Opción 3: Railway/Render (ALTERNATIVA)**

### 🚂 **Railway.app:**
1. Conectar GitHub repo
2. Configurar: `streamlit run frontend_dashboard_v3.py --server.port $PORT`
3. Variables de entorno automáticas

### 🎨 **Render.com:**
1. New Web Service
2. Connect GitHub
3. Build: `pip install -r requirements_frontend.txt`
4. Start: `streamlit run frontend_dashboard_v3.py --server.headless true --server.port $PORT`

---

## ⚡ **RECOMENDACIÓN FINAL**

**USAR STREAMLIT CLOUD** porque:
- ✅ Diseñado específicamente para Streamlit
- ✅ Deployment automático desde GitHub
- ✅ SSL/HTTPS gratis
- ✅ Variables de entorno fáciles
- ✅ Logs y monitoreo incluidos
- ✅ 100% compatible con tu código actual

**URL final será algo como:**
`https://galpon-avicola-ucc.streamlit.app`

---

## 🔧 **Configuración de Backend**

⚠️ **IMPORTANTE:** Tu backend está en IP local `192.168.20.33:8000`

**Para producción necesitas:**
1. **Exponer backend públicamente** (Ngrok, Cloudflare Tunnel)
2. **O migrar backend también a la nube** (Heroku, Railway)

**Ejemplo con Ngrok:**
```bash
# En Raspberry Pi
ngrok http 8000
# Obtienes: https://abc123.ngrok.io
```

Luego cambiar en el código:
```python
API_BASE_URL = "https://abc123.ngrok.io"
```