# 🚀 GUÍA DE DEPLOYMENT PARA STREAMLIT

---

## ⚠️ **ADVERTENCIA IMPORTANTE**

### 🚨 ESTE ES UN PROYECTO PYTHON/STREAMLIT

**❌ NO USAR VERCEL** - Vercel es para proyectos React/Node.js, NO para Streamlit.

**✅ USAR STREAMLIT CLOUD** - Es la plataforma diseñada para este tipo de proyectos.

¿Tienes un error de Vercel con React y `react-day-picker`? 
→ Lee: [docs/NO_USAR_VERCEL.md](docs/NO_USAR_VERCEL.md) y [docs/SOLUCION_ERROR_VERCEL_REACT.md](docs/SOLUCION_ERROR_VERCEL_REACT.md)

---

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

## 🔄 **Opción 2: Vercel (⚠️ NO RECOMENDADO PARA STREAMLIT)**

### ⚠️ **ADVERTENCIA: VERCEL NO ES COMPATIBLE CON STREAMLIT**

**NO intentes deployar este proyecto en Vercel** porque:
- ❌ Vercel usa Node.js runtime, Streamlit requiere Python
- ❌ Vercel es stateless/serverless, Streamlit necesita sesiones persistentes
- ❌ Streamlit usa WebSockets para tiempo real, incompatible con Vercel
- ❌ La arquitectura es fundamentalmente incompatible

**Si tienes un error de Vercel:** Probablemente estás deployando el proyecto equivocado.
→ Lee: [docs/NO_USAR_VERCEL.md](docs/NO_USAR_VERCEL.md)

### 📁 **Por completitud: Estructura teórica (NO USAR)**
```
vercel-app/
├── api/
│   └── index.py          # FastAPI wrapper
├── requirements.txt      # Dependencies
├── vercel.json          # Vercel config
└── main.py              # Entry point
```

**NOTA:** Esta configuración es compleja, propensa a errores, y NO recomendada.
**USAR STREAMLIT CLOUD EN SU LUGAR.**

### ⚙️ **Configuración teórica (SOLO REFERENCIA):**

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
    # NOTA: Esto NO funciona correctamente en Vercel
    # NO USAR - Solo referencia teórica
    pass
```

**⚠️ ESTE CÓDIGO NO FUNCIONA EN PRODUCCIÓN.**

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

### 🎯 **USAR STREAMLIT CLOUD (Opción 1)**

**STREAMLIT CLOUD es la ÚNICA opción recomendada** porque:
- ✅ Diseñado específicamente para Streamlit
- ✅ Deployment automático desde GitHub
- ✅ SSL/HTTPS gratis
- ✅ Variables de entorno fáciles
- ✅ Logs y monitoreo incluidos
- ✅ 100% compatible con tu código actual
- ✅ GRATIS para proyectos públicos

### ❌ **NO USAR VERCEL**

Vercel es excelente para React/Next.js/Node.js, pero **NO es compatible con Streamlit**.

Si intentaste usar Vercel y obtuviste un error de `npm` o `react-day-picker`:
- 🔍 Probablemente estás deployando el proyecto equivocado
- 📖 Lee: [docs/NO_USAR_VERCEL.md](docs/NO_USAR_VERCEL.md)
- 🛠️ Solución: [docs/SOLUCION_ERROR_VERCEL_REACT.md](docs/SOLUCION_ERROR_VERCEL_REACT.md)

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