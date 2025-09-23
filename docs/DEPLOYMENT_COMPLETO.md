# 🚀 DEPLOYMENT COMPLETO - Sistema Galpón IoT UCC

## 📍 ARQUITECTURA DEL SISTEMA

```
ESP32 → MQTT → Raspberry Pi (192.168.20.33)
                    ↓
               [SQLite Database]
                    ↓
               [FastAPI Backend:8000]
                    ↓
Windows PC ← HTTP Requests ← [Streamlit Frontend]
```

## 🍓 PASO 1: CONFIGURAR RASPBERRY PI (Backend)

### 1.1 Copiar archivos backend a Raspberry Pi
```bash
# En tu PC Windows, copiar archivos via SCP o USB:
scp -r raspberry_backend/* pi@192.168.20.33:/home/innovasic/galpon/backend/
```

### 1.2 Instalar dependencias en Raspberry Pi
```bash
# SSH a la Raspberry Pi
ssh pi@192.168.20.33

# Navegar al directorio backend
cd /home/innovasic/galpon/backend

# Instalar dependencias
pip install -r requirements_api.txt
```

### 1.3 Ejecutar FastAPI Backend
```bash
# Ejecutar en background
python main.py

# O con uvicorn directamente:
uvicorn main:app --host 0.0.0.0 --port 8000

# Para ejecutar en background permanente:
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### 1.4 Verificar que la API funciona
```bash
# Probar endpoints desde la Raspberry Pi:
curl http://localhost:8000/
curl http://localhost:8000/status
curl http://localhost:8000/sensores/ultimos?limit=5
```

## 💻 PASO 2: CONFIGURAR WINDOWS PC (Frontend)

### 2.1 Instalar dependencias
```powershell
# En tu directorio del proyecto
pip install -r requirements_frontend.txt
```

### 2.2 Ejecutar Dashboard Streamlit
```powershell
streamlit run frontend_dashboard.py
```

### 2.3 Acceder al Dashboard
- Abre tu navegador en: `http://localhost:8501`
- **Usuario Supervisor:** `supervisor` / `admin123`
- **Usuario Operador:** `operador` / `oper456`

## 🌐 PASO 3: TESTING DE CONECTIVIDAD

### 3.1 Verificar API desde Windows
```python
import requests

# Probar conexión con Raspberry Pi
response = requests.get("http://192.168.20.33:8000/status")
print(response.json())
```

### 3.2 Endpoints disponibles:
- `GET /` - Estado general
- `GET /status` - Estado del sistema y ESP32
- `GET /sensores/ultimos?limit=N` - Últimos N registros
- `GET /sensores/tiempo-real?minutes=N` - Datos de últimos N minutos
- `GET /sensores/historico?inicio=YYYY-MM-DD&fin=YYYY-MM-DD` - Datos históricos
- `GET /sensores/alertas` - Registros que superen umbrales
- `GET /sensores/estadisticas` - Estadísticas básicas

## 🔧 CONFIGURACIÓN ADICIONAL

### Configurar servicio systemd en Raspberry Pi (Opcional)
```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/galpon-api.service

# Contenido del archivo:
[Unit]
Description=Galpon IoT API
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/innovasic/galpon/backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target

# Habilitar y iniciar servicio
sudo systemctl enable galpon-api.service
sudo systemctl start galpon-api.service
sudo systemctl status galpon-api.service
```

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### ✅ Backend FastAPI:
- ✅ Conexión a SQLite en `/home/innovasic/galpon/data/galpon.db`
- ✅ 6 endpoints REST completos
- ✅ CORS habilitado para acceso remoto
- ✅ Manejo de errores y validaciones
- ✅ Documentación automática en `/docs`

### ✅ Frontend Streamlit:
- ✅ Sistema de login con 2 roles (Supervisor/Operador)
- ✅ Dashboard en tiempo real con gauges y gráficos
- ✅ Página de análisis histórico con filtros
- ✅ Sistema de alertas con umbrales configurables
- ✅ Descarga de datos CSV (solo supervisores)
- ✅ Indicadores de estado ESP32 y API

### ✅ Características Técnicas:
- ✅ Comunicación HTTP entre Windows y Raspberry Pi
- ✅ Gráficos interactivos con Plotly
- ✅ Autenticación basada en roles
- ✅ Responsive design y UX moderna
- ✅ Manejo de errores de conectividad

## 🚨 TROUBLESHOOTING

### Problema: No se conecta a la API
**Solución:**
1. Verificar que Raspberry Pi está en IP `192.168.20.33`
2. Verificar que FastAPI está ejecutándose: `curl http://192.168.20.33:8000`
3. Verificar firewall en Raspberry Pi: `sudo ufw status`

### Problema: Base de datos no encontrada
**Solución:**
1. Verificar que existe `/home/innovasic/galpon/data/galpon.db`
2. Verificar permisos de lectura en el archivo
3. Verificar estructura de tabla `sensores`

### Problema: Credenciales de login
**Usuarios por defecto:**
- **Supervisor:** `supervisor` / `admin123`
- **Operador:** `operador` / `oper456`

## 📊 PRÓXIMOS PASOS

1. **Configurar servicio systemd** para auto-inicio de FastAPI
2. **Implementar WebSockets** para actualizaciones en tiempo real
3. **Añadir notificaciones email** para alertas críticas
4. **Configurar HTTPS** con certificados SSL
5. **Implementar backup automático** de base de datos

## 🎉 ¡SISTEMA LISTO!

El sistema ahora está configurado con:
- ✅ Backend robusto en Raspberry Pi
- ✅ Frontend moderno en Windows
- ✅ Comunicación remota HTTP
- ✅ Autenticación y roles de usuario
- ✅ Visualización en tiempo real
- ✅ Análisis histórico completo