# 🚀 GUÍA RÁPIDA DE EJECUCIÓN - Sistema Galpón IoT

## ⚡ EJECUTAR EL PROYECTO (Opción Simple)

### 🎯 **Opción 1: Solo Frontend (Modo Demo)**
Si quieres ver el dashboard sin conectar al backend real:

```powershell
# 1. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 2. Ejecutar dashboard
streamlit run frontend_dashboard_v3.py --server.port 8521

# 3. Abrir en navegador
# http://localhost:8521
```

**Credenciales:**
- **Supervisor**: `supervisor` / `admin123`
- **Operador**: `operador` / `oper456`

---

## 🏗️ **Opción 2: Sistema Completo (Frontend + Backend)**

### **PASO 1: Configurar Backend (Raspberry Pi)**

#### En la Raspberry Pi:
```bash
# 1. Ir a carpeta backend
cd raspberry_backend

# 2. Instalar dependencias
pip install -r requirements_api.txt

# 3. Ejecutar API
uvicorn main:app --host 0.0.0.0 --port 8000

# URL: http://192.168.20.33:8000
```

### **PASO 2: Ejecutar Frontend (Windows)**

#### En tu PC Windows:
```powershell
# 1. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 2. Ejecutar dashboard
streamlit run frontend_dashboard_v3.py --server.port 8521

# 3. Abrir navegador
# http://localhost:8521
```

---

## 🔧 **Configuración de Variables de Entorno (Opcional)**

Si quieres cambiar la URL del backend:

```powershell
# Windows PowerShell
$env:API_BASE_URL = "http://192.168.20.33:8000"
$env:DEMO_MODE = "false"

# Luego ejecutar
streamlit run frontend_dashboard_v3.py --server.port 8521
```

---

## 📊 **Verificar que Todo Funcione**

### ✅ **Verificar Backend (Raspberry Pi):**
```bash
# Probar endpoints
curl http://localhost:8000/
curl http://localhost:8000/status
curl http://localhost:8000/sensores/ultimos?limit=5
```

### ✅ **Verificar Frontend (Windows):**
1. Abrir: streamlit run frontend_dashboard_v3.py --server.port 8521
2. Login con credenciales
3. Ver dashboard con datos en tiempo real

---

## 🐛 **Solución de Problemas Comunes**

### ❌ **Error: ModuleNotFoundError**
```powershell
# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### ❌ **Error: No conecta al backend**
```powershell
# Verificar que backend esté corriendo
# Verificar IP: http://192.168.20.33:8000
# Si no funciona, usar modo demo (automático si backend no responde)
```

### ❌ **Puerto ocupado**
```powershell
# Usar otro puerto
streamlit run frontend_dashboard_v3.py --server.port 8522
```

---

## 📱 **URLs del Sistema**

### **Desarrollo Local:**
- **Dashboard**: http://localhost:8521
- **API Backend**: http://192.168.20.33:8000
- **API Docs**: http://192.168.20.33:8000/docs

### **Producción (Streamlit Cloud):**
- **Dashboard**: https://tu-app.streamlit.app

---

## 🎓 **Arquitectura del Sistema**

```
┌─────────────┐
│  ESP8266    │  ← Sensores físicos
│  Sensores   │
└──────┬──────┘
       │ MQTT (cada 5s)
       ↓
┌─────────────────┐
│  Raspberry Pi   │
│  • MQTT Broker  │
│  • SQLite DB    │
│  • FastAPI:8000 │
└──────┬──────────┘
       │ HTTP Requests
       ↓
┌─────────────────┐
│  Windows PC     │
│  Streamlit:8521 │
│  Dashboard Web  │
└─────────────────┘
```

---

## 🎯 **Inicio Rápido (1 Minuto)**

```powershell
# Clonar o ya tienes el proyecto
cd Sensores-main

# Instalar todo
pip install -r requirements.txt

# Ejecutar
streamlit run frontend_dashboard_v3.py --server.port 8521

# Abrir: http://localhost:8521
# Usuario: supervisor / admin123
```

¡Listo! 🎉

---

## 📚 **Documentación Adicional**

- `README.md` - Documentación completa
- `DEPLOYMENT_GUIDE.md` - Deployment en la nube
- `BACKEND_CLOUD_SOLUTIONS.md` - Soluciones de backend público
- `docs/DEPLOYMENT_COMPLETO.md` - Deployment paso a paso

---

## 👥 **Universidad Cooperativa de Colombia**
Campus Ibagué - Proyecto IoT Galpón Avícola