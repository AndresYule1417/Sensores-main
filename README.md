# 🌡️ Sistema de Monitoreo de Sensores IoT - Galpón UCC

Sistema completo de monitoreo de sensores ambientales usando ESP8266, Raspberry Pi y dashboard web en tiempo real.

## 📋 Descripción

Sistema IoT para monitoreo de condiciones ambientales en galpones:
- **Sensores**: Temperatura, Humedad, Luminosidad (LUX), Amonio (NH3), Sulfuro de hidrógeno (H2S)
- **Hardware**: ESP8266 NodeMCU + Raspberry Pi
- **Frecuencia**: Lecturas cada 10 segundos
- **Visualización**: Dashboard web en tiempo real (Streamlit)

## 🏗️ Arquitectura del Sistema

```
ESP8266 (192.168.0.166)
    ↓ TCP cada 10s
Raspberry Pi (192.168.0.180)
    ├─ Puerto 8889: Servidor.py → Excel (data_test_14.xlsx)
    └─ Puerto 8000: FastAPI → SQLite (galpon.db)
         ↓ HTTP REST
Dashboard Windows (localhost:8501)
```

## 🚀 Inicio Rápido

### 1. Iniciar Dashboard (Windows)
```powershell
cd C:\Users\afeli\OneDrive\Escritorio\Sensores-main
streamlit run frontend_dashboard_v3.py
```
O usar: `SCRIPTS\INICIAR_DASHBOARD.bat`

### 2. Verificar Sistema (Raspberry Pi)
```bash
# Verificar FastAPI activo
curl http://192.168.0.180:8000/status

# Reiniciar si es necesario
cd /home/innovasic/galpon/raspberry_backend
./restart_fastapi.sh

# Importar datos nuevos de Excel
python3 import_excel_to_sqlite.py
```

### 3. Acceder al Dashboard
- URL: http://localhost:8501
- Estado esperado: 🟢 Conectado
- Datos: Actualización automática configurable

## 📁 Estructura del Proyecto

```
Sensores-main/
├── frontend_dashboard_v3.py          # Dashboard Streamlit
├── requirements.txt                  # Dependencias Python
├── README.md                         # Este archivo
│
├── AppIoTEsp8266-UCC-main/          # Proyecto original
│   └── Servidor/
│       ├── Servidor.py              # TCP Server (puerto 8889)
│       └── data_test_14.xlsx        # Base de datos Excel
│
├── esp8266/                         # Código del ESP8266
│   ├── config.h                     # Configuración WiFi/sensores
│   └── README.md
│
├── raspberry_backend/               # API FastAPI
│   ├── main.py                      # Endpoints REST
│   ├── models.py                    # Modelo de datos SQLite
│   ├── database.py                  # Configuración DB
│   ├── import_excel_to_sqlite.py    # Importador Excel→SQLite
│   ├── restart_fastapi.sh           # Script de reinicio
│   ├── install_dependencies.sh      # Instalador de paquetes
│   └── requirements_api.txt         # Dependencias backend
│
├── config/                          # Configuraciones
│   ├── auth_users.json              # Usuarios dashboard
│   └── mqtt_test_client.py
│
├── DOCUMENTACION/                   # Guías detalladas
│   ├── INSTALACION_RASPBERRY_PI.md  # ⭐ Instalación completa
│   ├── SISTEMA_FUNCIONANDO.md       # ⭐ Uso del sistema
│   ├── ARQUITECTURA_SISTEMA.md      # Diagrama técnico
│   ├── BACKEND_COMPATIBLE_SERVIDOR.md # Explicación esquema
│   └── TROUBLESHOOTING.md           # Solución de problemas
│
├── logs/                            # Logs del sistema
└── SCRIPTS/                         # Scripts auxiliares
```

## 🔧 Configuración

### Red WiFi
- **SSID**: `wifi_estudiantes_zona_3`
- **Raspberry Pi**: 192.168.0.180 (IP estática)
- **ESP8266**: 192.168.0.166
- **Gateway**: 192.168.0.1

### Puertos
- **8000**: FastAPI (REST API)
- **8889**: Servidor.py (TCP original)
- **8501**: Dashboard Streamlit

### Base de Datos

**Schema (compatible con Servidor.py):**
```python
{
    "Device": "ESP8266_IOT",      # Identificador
    "IP": "192.168.0.166",        # IP del sensor
    "LUX": 450.5,                 # Luminosidad
    "NH3": 123.4,                 # Amonio (valor analógico)
    "HS": 98.7,                   # H2S (valor analógico)
    "H": 65.2,                    # Humedad (%)
    "T": 24.5,                    # Temperatura (°C)
    "time": "14:30:45"            # Hora lectura
}
```

## 📊 Endpoints API

```bash
# Estado del sistema
GET http://192.168.0.180:8000/status

# Últimas lecturas
GET http://192.168.0.180:8000/sensores/ultimos?limit=10

# Datos en tiempo real
GET http://192.168.0.180:8000/sensores/tiempo-real?minutos=60

# Estadísticas
GET http://192.168.0.180:8000/sensores/estadisticas
```

## 🛠️ Mantenimiento

### Importar Datos Nuevos
```bash
# En Raspberry Pi
ssh innovasic@192.168.0.180
cd /home/innovasic/galpon/raspberry_backend
source venv/bin/activate
python3 import_excel_to_sqlite.py
```

### Reiniciar FastAPI
```bash
# Detiene proceso anterior, reinicia DB, inicia nuevo proceso
./restart_fastapi.sh
```

### Ver Logs
```bash
# Raspberry Pi
tail -f /home/innovasic/galpon/logs/fastapi.log

# Dashboard (Windows)
# Ver terminal donde corre Streamlit
```

## 📖 Documentación Completa

- **Instalación**: Ver `DOCUMENTACION/INSTALACION_RASPBERRY_PI.md`
- **Uso diario**: Ver `DOCUMENTACION/SISTEMA_FUNCIONANDO.md`
- **Problemas**: Ver `DOCUMENTACION/TROUBLESHOOTING.md`
- **Arquitectura**: Ver `DOCUMENTACION/ARQUITECTURA_SISTEMA.md`

## 🔒 Credenciales

**Raspberry Pi:**
- Usuario: `innovasic`
- IP: `192.168.0.180`
- Password: (configurado en raspberry)

**Dashboard:**
- Ver: `config/auth_users.json`

## 📝 Estado Actual (21/10/2025)

✅ **Sistema Operativo:**
- ESP8266 enviando datos cada 10s
- Servidor.py guardando en Excel (223+ registros)
- FastAPI sirviendo datos vía REST
- Dashboard conectado y visualizando

✅ **Última verificación:**
```json
{
  "status": "activo",
  "total_registros": 223,
  "ultima_lectura": "12:58:55",
  "conexion_esp8266": true
}
```

## 👥 Créditos

- **Proyecto Original**: Ivan Camilo Leiton (AppIoTEsp8266-UCC-main)
- **Adaptación Backend**: Sistema FastAPI compatible con Servidor.py
- **Universidad**: UCC (Universidad Cooperativa de Colombia)

## 📞 Soporte

Para problemas o preguntas:
1. Revisar `DOCUMENTACION/TROUBLESHOOTING.md`
2. Verificar logs en `/logs/`
3. Comprobar estado: `curl http://192.168.0.180:8000/status`
