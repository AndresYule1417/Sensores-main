# 🐓 Sistema de Monitoreo Galpón Avícola IoT# 🐓 Sistema de Monitoreo Galpón Avícola# 🐓 Sistema de Monitoreo Galpón Avícola IoT - UCC Ibagué# � Sistema de Monitoreo Galpón Avícola IoT - UCC Ibagué



![ESP8266](https://img.shields.io/badge/ESP8266-IoT-red) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green) ![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-blue) ![SQLite](https://img.shields.io/badge/SQLite-Database-orange)

---

## ⚠️ IMPORTANTE: DEPLOYMENT

**Este es un proyecto Python/Streamlit**

✅ **DEPLOYAR EN:** [Streamlit Cloud](https://streamlit.io/cloud)  
❌ **NO USAR:** Vercel (incompatible con Streamlit)

¿Error de Vercel con `react-day-picker`? → [Lee esto](docs/NO_USAR_VERCEL.md)

📖 **Guía completa:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Sistema completo de monitoreo en tiempo real para galpones avícolas usando ESP8266, MQTT, FastAPI y Streamlit**## 🚀 Inicio Rápido



Universidad Cooperativa de Colombia - Campus Ibagué



---### ▶️ Ejecutar Dashboard**Sistema completo de monitoreo en tiempo real para galpones avícolas usando ESP32, FastAPI y Streamlit****Sistema completo de monitoreo en tiempo real para galpones avícolas usando ESP32, FastAPI y Streamlit**



## 🚀 Inicio Rápido```bash



### ▶️ Ejecutar Dashboardstreamlit run frontend_dashboard_v3.py --server.port 8503

```bash

streamlit run frontend_dashboard_v3.py --server.port 8521```

```

![ESP32](https://img.shields.io/badge/ESP32-IoT-red)![ESP32](https://img.shields.io/badge/ESP32-IoT-red)

### 🌐 Acceder al Sistema

- **URL**: http://localhost:8521### 🌐 Acceder al Sistema

- **Usuario Administrador**: `supervisor` / `admin123`

- **Usuario Operador**: `operador` / `oper456`- **URL**: http://localhost:8503![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)



---- **Usuario Administrador**: `supervisor` / `admin123`



## 📊 Características Principales- **Usuario Operador**: `operador` / `oper456`![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-blue)![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-blue)



### 🔄 **Dashboard en Tiempo Real**

- Monitoreo continuo de sensores ESP8266

- Auto-actualización inteligente cada 5-30 segundos## 📊 Características![SQLite](https://img.shields.io/badge/SQLite-Database-orange)![SQLite](https://img.shields.io/badge/SQLite-Database-orange)

- Control de pausa/reanudación de actualización

- Métricas en tiempo real sin recargar página



### 📈 **Sensores Monitoreados**- **✅ Modo Demo Automático**: Funciona siempre, con o sin conexión

- 🌡️ **Temperatura**: 15-35°C

- 💧 **Humedad**: 0-100%- **📈 Dashboard en Tiempo Real**: Temperatura, humedad, amoníaco

- 💡 **Luminosidad**: 0-1000 lux

- 🟡 **NH₃ (Amoníaco)**: 0-5 ppm- **📅 Datos Históricos**: Análisis y exportación CSV## 🏗️ Arquitectura del Sistema## 🏗️ Arquitectura del Sistema

- 🟤 **H₂S (Sulfuro de Hidrógeno)**: 0-5 ppm

- **⚠️ Sistema de Alertas**: Configuración de umbrales

### 📱 **Interfaz de Usuario**

- Dashboard principal con gráficos interactivos- **🔧 Diagnóstico**: Estado del sistema completo

- Histórico de datos con filtros

- Sistema de alertas configurable

- Estado del sistema en tiempo real

## 🔧 Backend (Raspberry Pi)``````

---



## 🏗️ Arquitectura del Sistema

- **IP**: 192.168.20.33:8000ESP32 → MQTT → Raspberry Pi (FastAPI + SQLite) → Windows PC (Streamlit)ESP32 → MQTT → Raspberry Pi (FastAPI + SQLite) → Windows PC (Streamlit)

```

ESP8266 → MQTT → Listener Python → SQLite → FastAPI → Streamlit Dashboard- **Servicios**: galpon.service, galpon-api.service, mosquitto

```

- **Base de Datos**: SQLite (`data/galpon_avicultura.db`)``````

### 🔧 **Componentes**

1. **ESP8266**: Recolección de datos de sensores cada 5 segundos

2. **MQTT**: Transmisión de datos en tiempo real

3. **SQLite**: Base de datos local optimizada## 📁 Estructura del Proyecto

4. **FastAPI**: API REST para backend

5. **Streamlit**: Frontend web interactivo



---```### 📊 Monitoreo en Tiempo Real:### 📊 Monitoreo en Tiempo Real:



## 📁 Estructura del Proyecto📂 Sensores-main/



```├── 🐍 frontend_dashboard_v3.py    # Frontend principal (USAR ESTE)- 🌡️ **Temperatura** ambiente- 🌡️ **Temperatura** ambiente

Sensores-main/

├── frontend_dashboard_v3.py       # Dashboard principal Streamlit├── 📊 data/                       # Base de datos SQLite

├── requirements_frontend.txt      # Dependencias frontend

├── raspberry_backend/             # Backend FastAPI├── 🔧 raspberry_backend/          # API FastAPI- 💧 **Humedad** relativa  - 💧 **Humedad** relativa  

│   ├── main.py                   # API principal

│   ├── models.py                 # Modelos de datos├── 📡 esp32/                      # Código del sensor

│   ├── crud.py                   # Operaciones de base de datos

│   └── requirements_api.txt      # Dependencias backend├── 📚 docs/                       # Documentación completa- 💡 **Luminosidad** (lux)- 💡 **Luminosidad** (lux)

├── esp32/                         # Código ESP8266

│   ├── main.ino                  # Código principal Arduino└── 💾 backup_obsoletos/           # Versiones anteriores

│   └── config.h                  # Configuración

├── data/                          # Base de datos SQLite```- ☁️ **Amoniaco (NH₃)** en ppm- ☁️ **Amoniaco (NH₃)** en ppm

├── config/                        # Configuración del sistema

├── docs/                          # Documentación técnica

└── logs/                          # Archivos de registro

```## 🏗️ Arquitectura- 💨 **Sulfuro de Hidrógeno (H₂S)** en ppm- 💨 **Sulfuro de Hidrógeno (H₂S)** en ppm



---



## ⚙️ Instalación y Configuración```



### 1. **Requisitos Previos**ESP32 → MQTT → Raspberry Pi → SQLite → FastAPI → Dashboard

- Python 3.8+

- ESP8266 con sensores conectados```---## 🚀 INICIO RÁPIDO

- Raspberry Pi (opcional para backend)



### 2. **Instalación Frontend**

```bash## 📞 Soporte

pip install -r requirements_frontend.txt

```



### 3. **Instalación Backend**- **Universidad**: Cooperativa de Colombia - Campus Ibagué## 📁 Estructura del Proyecto### **1. Ejecutar Sistema Completo:**

```bash

cd raspberry_backend- **Documentación**: `/docs/FRONTEND_V3_MODO_DEMO.md`

pip install -r requirements_api.txt

```- **Versión**: 3.0 - Septiembre 2025```bash



### 4. **Configuración ESP8266**

- Copiar `esp32/config.h.template` a `esp32/config.h`

- Configurar credenciales WiFi y MQTT---```# Terminal 1: Recolección MQTT→SQLite

- Cargar código en ESP8266



### 5. **Ejecutar Sistema**

```bash**🎯 Todo funciona perfectamente. Si hay problemas de conexión, el modo demo se activa automáticamente.**📂 galpon-iot-ucc/python mqtt2sqlite_esp32.py

# Backend (Raspberry Pi)

cd raspberry_backend├── 🍓 raspberry_backend/          # Backend FastAPI para Raspberry Pi

uvicorn main:app --host 0.0.0.0 --port 8000

│   ├── main.py                    # Servidor FastAPI principal# Terminal 2: Dashboard con autenticación

# Frontend

streamlit run frontend_dashboard_v3.py --server.port 8521│   ├── database.py                # Configuración SQLitestreamlit run dashboard_ucc_completo.py

```

│   ├── models.py                  # Modelo tabla sensores```

---

│   ├── crud.py                    # Funciones de consulta

## 📊 Endpoints API

│   └── requirements_api.txt       # Dependencias backend### **2. Acceder al Dashboard:**

### Sensores

- `GET /sensores/ultimos` - Últimas lecturas│- URL: `http://localhost:8501`

- `GET /sensores/historico` - Datos históricos

- `GET /status` - Estado del sistema├── 🎨 frontend_dashboard.py       # Dashboard Streamlit (Windows)- Registrarse con email UCC autorizado



### Sistema├── 📦 requirements_frontend.txt   # Dependencias frontend- Configurar alertas personalizadas

- `GET /services/status` - Estado de servicios

- `GET /health` - Salud del sistema│



---├── 📡 esp32/                      # Código para ESP32### **3. Probar Conexión ESP32:**



## 🔧 Configuración│   ├── main.ino                   # Programa principal ESP32```bash



### Variables de Entorno│   ├── config.h                   # Configuración WiFi/MQTTpython mqtt_test_client.py

```bash

API_BASE_URL=http://192.168.20.33:8000│   └── README.md                  # Documentación ESP32```

DEMO_MODE=False

```│



### Configuración de Sensores├── ⚙️ config/                     # Configuraciones---

Los rangos de sensores están optimizados para galpones avícolas:

- Temperatura ideal: 20-25°C│   ├── auth_users.json            # Credenciales usuarios

- Humedad ideal: 50-70%

- Luminosidad: Automática según horario│   ├── mqtt_test_client.py        # Cliente pruebas MQTT## 📁 ESTRUCTURA OPTIMIZADA

- NH₃: < 25 ppm (límite crítico)

- H₂S: < 10 ppm (límite crítico)│   └── setup_raspberry_database.sql # Script BD Raspberry Pi



---│```



## 📈 Funcionalidades Avanzadas├── 💾 data/                       # Base de datos📦 Sensores-main/



### Auto-actualización Inteligente│   └── galpon_avicultura.db       # SQLite principal├── 📡 esp32/                     # Hardware IoT

- Solo actualiza gráficos y datos, no la página completa

- Control de pausa para inspección detallada││   ├── main.ino                  # ✅ Código ESP32 funcional

- Intervalos configurables (5-30 segundos)

- Indicador de cuenta regresiva├── 📚 docs/                       # Documentación│   ├── config.h                  # ✅ Configuración WiFi/MQTT  



### Gestión de Usuarios│   ├── DEPLOYMENT_COMPLETO.md     # Guía de instalación│   └── README.md                 # ✅ Documentación ESP32

- Roles diferenciados (Administrador/Operador)

- Autenticación segura│   ├── INSTRUCCIONES_RASPBERRY_PI.md # Setup Raspberry Pi│

- Permisos específicos por rol

│   ├── CHECKLIST_RASPBERRY.md     # Lista verificación├── 🐍 Backend Python/

### Alertas y Notificaciones

- Umbrales configurables por sensor│   └── PROMPT_RASPBERRY_PI_UCC.md # Configuración avanzada│   ├── mqtt2sqlite_esp32.py      # ✅ MQTT→SQLite principal

- Alertas críticas automáticas

- Historial de eventos││   ├── auth_ucc_sistema.py       # ✅ Autenticación UCC



---├── 📋 logs/                       # Logs del sistema│   ├── alertas_ucc_sistema.py    # ✅ Sistema de alertas



## 🐛 Resolución de Problemas└── 🗂️ backup_obsoletos/          # Archivos históricos│   ├── dashboard_ucc_completo.py # ✅ Dashboard integrado



### Problemas Comunes```│   ├── streamlit_app_galpon.py   # ✅ Dashboard básico



1. **Dashboard no carga datos**│   └── mqtt_test_client.py       # ✅ Cliente de pruebas

   - Verificar que el backend esté ejecutándose

   - Comprobar URL de la API en configuración---│



2. **ESP8266 no envía datos**├── 💾 data/                      # Base de datos SQLite

   - Verificar conexión WiFi

   - Comprobar configuración MQTT## 🚀 Inicio Rápido│   ├── galpon_avicultura.db      # ✅ Datos principales

   - Revisar sensores conectados

│   ├── galpon_avicultura.db-shm  # ✅ Shared memory

3. **Auto-actualización muy lenta**

   - Ajustar intervalo en configuración### 1️⃣ **Configurar Raspberry Pi (Backend)**│   └── galpon_avicultura.db-wal  # ✅ Write-ahead log

   - Verificar rendimiento del sistema

│

---

```bash├── 📚 Documentación/

## 📚 Documentación Adicional

# Copiar archivos backend│   ├── INSTALACION_UCC_COMPLETA.md # ✅ Manual completo

- `docs/INSTRUCCIONES_RASPBERRY_PI.md` - Configuración Raspberry Pi

- `docs/DEPLOYMENT_COMPLETO.md` - Despliegue completoscp -r raspberry_backend/* pi@192.168.20.33:/home/innovasic/galpon/backend/│   ├── PROMPT_RASPBERRY_PI_UCC.md  # ✅ Guía Raspberry Pi

- `docs/CHECKLIST_RASPBERRY.md` - Lista de verificación

- `ADAPTACION_ESP8266_COMPLETA.md` - Detalles de adaptación ESP8266│   └── ESTRUCTURA_OPTIMIZADA.md    # ✅ Documentación limpieza



---# SSH a Raspberry Pi│



## 👥 Equipo de Desarrollossh pi@192.168.20.33└── ⚙️ Configuración/



Universidad Cooperativa de Colombia - Campus Ibagué      ├── requirements_galpon.txt   # ✅ Dependencias Python

Facultad de Ingeniería  

Proyecto IoT Galpón Avícola# Instalar dependencias    ├── logs/mqtt2sqlite.log      # ✅ Logs del sistema



---cd /home/innovasic/galpon/backend    └── .gitignore               # ✅ Configuración Git



## 📄 Licenciapip install -r requirements_api.txt```



Este proyecto está desarrollado para fines académicos y de investigación en la Universidad Cooperativa de Colombia.



---# Ejecutar API---



## 🔄 Última Actualizaciónuvicorn main:app --host 0.0.0.0 --port 8000



- **Versión**: 3.0 Optimizada```## 🔐 ADMINISTRADORES UCC AUTORIZADOS

- **Fecha**: Septiembre 2025

- **Cambios**: Sistema ESP8266 completamente funcional, auto-actualización mejorada, proyecto optimizado

### 2️⃣ **Ejecutar Frontend (Windows)**### **Email Institucional @campusucc.edu.co:**

1. **admin1.galpon@campusucc.edu.co**

```powershell   - Administrador Galpón Principal

# Instalar dependencias   - Facultad de Medicina Veterinaria

pip install -r requirements_frontend.txt

2. **admin2.sensores@campusucc.edu.co** 

# Ejecutar dashboard   - Administrador Sensores IoT

streamlit run frontend_dashboard.py   - Ingeniería de Sistemas

```

---

### 3️⃣ **Acceder al Sistema**

## 🚨 SISTEMA DE ALERTAS CONFIGURABLES

- **Dashboard:** `http://localhost:8501`

- **API Docs:** `http://192.168.20.33:8000/docs`### **Métodos de Notificación:**

- 📧 **Email Outlook** - Correo institucional UCC

**Credenciales:**- 📱 **WhatsApp** - Alertas móviles inmediatas

- **Supervisor:** `supervisor` / `admin123` (acceso completo)

- **Operador:** `operador` / `oper456` (solo visualización)### **Tipos de Alertas:**

- 🌡️ Temperatura crítica (< 15°C o > 30°C)

---- 💧 Humedad extrema (< 40% o > 80%) 

- 🔥 NH3 elevado (> 20ppm advertencia, > 25ppm crítico)

## 🛠️ Funcionalidades- ☣️ H2S tóxico (> 10ppm advertencia, > 15ppm crítico)

- 📡 Pérdida de conexión ESP32

### 🎛️ **Dashboard en Tiempo Real**

- ✅ Gauges interactivos para cada sensor---

- ✅ Gráficos de tendencias en vivo

- ✅ Estado de conexión ESP32## 📊 CARACTERÍSTICAS DEL DASHBOARD

- ✅ Indicadores de alerta visual

### **Métricas en Tiempo Real:**

### 📊 **Análisis Histórico**- 🌡️ Temperatura con estados (Óptima/Alta/Baja)

- ✅ Filtros por rango de fechas- 💧 Humedad con evaluación automática

- ✅ Estadísticas del período- 🔥 NH3 con alertas visuales

- ✅ Descarga de datos CSV/Excel- ☣️ H2S con indicadores de peligro

- ✅ Gráficos comparativos- 💡 Iluminación en lux

- 📶 Calidad señal WiFi

### 🚨 **Sistema de Alertas**

- ✅ Umbrales configurables### **Gráficos Históricos:**

- ✅ Notificaciones visuales- 📈 Evolución temperatura con límites

- ✅ Registro de eventos críticos- 📈 Tendencias de humedad  

- ✅ Dashboard de alertas- 📈 Monitoreo gases tóxicos

- 📊 Datos últimas 24 horas

### 🔐 **Autenticación**

- ✅ Login con roles diferenciados### **Panel Administrativo:**

- ✅ Permisos por usuario- 🚨 Configuración alertas personalizables

- ✅ Sesiones seguras- 📊 Exportación datos CSV

- 📋 Historial alertas enviadas

---- ⚙️ Gestión del sistema



## 🔌 API Endpoints---



| Endpoint | Método | Descripción |## 🛠️ INSTALACIÓN

|----------|--------|-------------|

| `/status` | GET | Estado sistema y ESP32 |### **Dependencias:**

| `/sensores/ultimos` | GET | Últimos N registros |```bash

| `/sensores/tiempo-real` | GET | Datos últimos X minutos |pip install -r requirements_galpon.txt

| `/sensores/historico` | GET | Datos por rango fechas |```

| `/sensores/alertas` | GET | Registros críticos |

| `/sensores/estadisticas` | GET | Estadísticas generales |### **Configuración ESP32:**

1. Abrir `esp32/main.ino` en Arduino IDE

---2. Configurar WiFi en `esp32/config.h`

3. Compilar y subir al ESP32

## 🏫 Configuración UCC

### **Base de Datos:**

### **Red Universitaria**La base de datos SQLite se crea automáticamente al ejecutar el sistema.

- **IP Raspberry Pi:** `192.168.20.33`

- **Puerto API:** `8000`---

- **Puerto Dashboard:** `8501`

## 🧹 OPTIMIZACIÓN REALIZADA

### **Base de Datos**

- **Ubicación:** `/home/innovasic/galpon/data/galpon.db`### **Archivos Eliminados (17):**

- **Tabla:** `sensores`- ❌ Scripts Python obsoletos (mqtt2sqlite.py, main.py, etc.)

- **Campos:** `id, tiempo, temperatura, humedad, luminosidad, amonio, sulfuro`- ❌ Documentación desactualizada

- ❌ Archivos de configuración no usados

### **MQTT Broker**- ❌ Scripts de instalación obsoletos

- **Servidor:** `broker.emqx.io`

- **Puerto:** `1883`### **Archivos Mantenidos (19):**

- **Topics:** `galpon/+/sensor/+`- ✅ Solo código funcional y documentación actualizada

- ✅ Estructura clara y mantenible

---- ✅ Reducción ~40% del tamaño del proyecto



## 📋 Requisitos del Sistema---



### **Raspberry Pi**## 🎯 PRÓXIMOS PASOS

- Raspberry Pi 4 (4GB RAM mínimo)

- Raspberry Pi OS Lite- [ ] **Raspberry Pi** - Usar guía `PROMPT_RASPBERRY_PI_UCC.md`

- Python 3.9+- [ ] **Streamlit Cloud** - Deploy público

- SQLite 3- [ ] **SMTP Real** - Configuración servidor UCC

- [ ] **WhatsApp API** - Integración Business

### **Windows PC**

- Windows 10/11---

- Python 3.8+

- Conexión de red local## 📞 SOPORTE UCC IBAGUÉ



### **ESP32**- **Campus**: sistemas.ibague@ucc.edu.co

- ESP32 DevKit v1- **Mesa de Ayuda**: +57 (8) 276 0010

- Sensores DHT22, BH1750, MQ-135, MQ-136- **Documentación**: Ver archivos .md del proyecto

- WiFi 2.4GHz

---

---

## 🏆 LOGROS

## 👥 Roles de Usuario

✅ **Sistema IoT Completo** - ESP32 + MQTT + SQLite + Dashboard  

### 🔧 **Supervisor** (`supervisor` / `admin123`)✅ **Autenticación UCC** - Integrado con dominio institucional  

- ✅ Ver todos los datos✅ **Alertas Multicanal** - Email + WhatsApp configurables  

- ✅ Configurar alertas✅ **Dashboard Profesional** - Tiempo real + Gráficos históricos  

- ✅ Administrar usuarios✅ **Proyecto Optimizado** - Código limpio y mantenible  

- ✅ Descargar reportes

- ✅ Acceso completo al sistema**🎉 SISTEMA 100% FUNCIONAL PARA UCC IBAGUÉ**



### 👀 **Operador** (`operador` / `oper456`)---

- ✅ Ver datos en tiempo real

- ✅ Ver análisis histórico## 📋 Descripción del Proyecto

- ✅ Generar reportes básicos

- ❌ Sin permisos administrativosEste sistema permite monitorear en tiempo real las condiciones ambientales de galpones avícolas mediante:



---- **🌡️ Sensores ESP32** que miden temperatura, humedad, iluminación, NH3 y H2S

- **🍓 Raspberry Pi 4B** como servidor local con PostgreSQL

## 🔧 Mantenimiento- **📊 Dashboard web** con Streamlit y autenticación @campusucc.edu.co

- **🌐 Acceso público gratuito** mediante túneles HTTPS

### **Logs del Sistema**

```bash---

# Ver logs API

tail -f /home/innovasic/galpon/logs/api.log## 🏗️ Arquitectura del Sistema



# Ver logs MQTT```

tail -f /home/innovasic/galpon/logs/mqtt.logESP32 Sensores  →  Raspberry Pi 4B  →  Dashboard Web Público

```    ↓                    ↓                     ↓

Lectura cada        PostgreSQL          Streamlit + Auth

### **Backup Base de Datos**30 segundos         Base Local          @campusucc.edu.co

```bash```

# Backup manual

sqlite3 galpon.db ".backup backup_$(date +%Y%m%d).db"### 📊 Parámetros Monitoreados:

- **LUX:** Iluminación (10-300 lux óptimo)

# Backup programado (crontab)- **NH3:** Amoniaco (<20 ppm seguro)

0 2 * * * sqlite3 /home/innovasic/galpon/data/galpon.db ".backup /home/innovasic/galpon/backups/backup_$(date +\%Y\%m\%d).db"- **H2S:** Sulfuro de hidrógeno (<10 ppm buena ventilación)

```- **H:** Humedad relativa (50-70% ideal)

- **T:** Temperatura (18-24°C confort animal)

---

---

## 🐛 Troubleshooting

## 📁 Estructura del Proyecto

| Problema | Solución |

|----------|----------|### 🔧 Archivos Principales:

| No conecta a API | Verificar IP `192.168.20.33:8000` |- `streamlit_app.py` - Dashboard original (desarrollo local)

| ESP32 desconectado | Verificar WiFi y broker MQTT |- `main.py` - API FastAPI original (desarrollo local)

| Login falla | Usar credenciales correctas |- `streamlit_app_raspberry.py` - Dashboard con autenticación UCC

| Sin datos | Verificar base de datos SQLite |- `main_raspberry.py` - API adaptada para PostgreSQL local

- `min_tabla.py` - Componente de tablas con sparklines

---- `styles.css` - Estilos CSS personalizados



## 🤝 Contribución### 📚 Documentación:

- `PROMPT_PARA_INNOVASICRASP.md` - **⭐ GUÍA PRINCIPAL DE IMPLEMENTACIÓN**

Este proyecto fue desarrollado para la **Universidad Cooperativa de Colombia - Campus Ibagué** como sistema de monitoreo para galpones avícolas.- `INSTALACION_COMPLETA_RASPBERRY.md` - Manual paso a paso

- `POSTGRESQL_RASPBERRY.md` - Configuración de base de datos

### **Equipo de Desarrollo**- `ACCESO_PUBLICO_GRATUITO.md` - Opciones de túneles gratuitos

- 🏫 **Institución:** UCC Ibagué- `ARQUITECTURA_SIMPLIFICADA.md` - Documentación técnica

- 📧 **Contacto:** admin1.galpon@campusucc.edu.co

- 📧 **Soporte:** admin2.sensores@campusucc.edu.co---



---## 🚀 Implementación Rápida



## 📄 Licencia### Para el colaborador **innovasicrasp**:



Proyecto académico - Universidad Cooperativa de Colombia1. **📖 Lee primero:** `PROMPT_PARA_INNOVASICRASP.md`

2. **⏱️ Tiempo estimado:** 75 minutos

---3. **🛠️ Resultado:** Sistema completamente funcional



## 🎯 Estado del Proyecto### Comando de inicio rápido:

```bash

✅ **ESP32 IoT** - Funcionando  git clone https://github.com/AndresYule1417/Sensores-main.git

✅ **Backend FastAPI** - Implementado  cd Sensores-main

✅ **Frontend Streamlit** - Completado  # Seguir PROMPT_PARA_INNOVASICRASP.md

✅ **Base de Datos** - Configurada  ```

✅ **Autenticación** - Activa  

✅ **Dashboard** - Operativo  ---

✅ **Documentación** - Completa  

## 🔐 Autenticación y Seguridad

**🚀 Sistema listo para producción en UCC Ibagué**
- **✅ Solo emails @campusucc.edu.co**
- **🔒 Contraseña temporal:** `hello` (cambiar en producción)
- **🛡️ Firewall configurado**
- **🌐 HTTPS obligatorio en producción**

---

## 🛠️ Tecnologías Utilizadas

### Backend:
- **Python 3.11+**
- **FastAPI** - API REST para ESP32
- **PostgreSQL** - Base de datos local
- **SQLAlchemy** - ORM para base de datos

### Frontend:
- **Streamlit** - Dashboard interactivo
- **Plotly** - Gráficos y visualizaciones
- **Pandas** - Procesamiento de datos

### Infraestructura:
- **Raspberry Pi 4B** - Servidor local
- **Cloudflare Tunnel** - Acceso público gratuito
- **systemd** - Servicios auto-iniciables

---

## 📊 Esquema de Base de Datos

### Tabla `sensors3`:
```sql
CREATE TABLE sensors3 (
    id SERIAL PRIMARY KEY,
    device VARCHAR(50) NOT NULL,    -- ID del ESP32
    lux FLOAT NOT NULL,             -- Iluminación
    nh3 FLOAT NOT NULL,             -- Amoniaco
    hs FLOAT NOT NULL,              -- Sulfuro de hidrógeno  
    h FLOAT NOT NULL,               -- Humedad
    t FLOAT NOT NULL,               -- Temperatura
    time TIMESTAMP DEFAULT NOW(),   -- Timestamp automático
    ip VARCHAR(45)                  -- IP del dispositivo
);
```

---

## 🔌 API Endpoints

### FastAPI (Puerto 8000):
- `GET /` - Información del sistema
- `GET /health` - Estado de salud
- `POST /api/sensores` - Recibir datos de ESP32
- `GET /api/stats` - Estadísticas del sistema
- `GET /api/latest/{device_id}` - Última lectura por dispositivo

### Dashboard (Puerto 8501):
- **Login:** Autenticación @campusucc.edu.co
- **Dashboard:** Visualización en tiempo real
- **Filtros:** Por tiempo y dispositivo
- **Auto-refresh:** Cada 30 segundos

---

## 🌐 URLs de Acceso

### Desarrollo Local:
- **Dashboard:** http://localhost:8501
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/api/docs

### Producción (Raspberry Pi):
- **Dashboard:** https://galpon-ucc.tudominio.com
- **API:** https://api-galpon-ucc.tudominio.com
- **Documentación:** https://api-galpon-ucc.tudominio.com/api/docs

---

## 👥 Colaboradores

- **📧 AndresYule1417** - Desarrollador principal
- **🍓 innovasicrasp** - Implementador Raspberry Pi
- **🏛️ Universidad Cooperativa de Colombia** - Campus Neiva

---

## 📞 Soporte

- **🐙 Repositorio:** https://github.com/AndresYule1417/Sensores-main
- **📧 Email institucional:** sistemas@campusucc.edu.co
- **🎓 Universidad:** Universidad Cooperativa de Colombia
- **🏢 Campus:** Neiva, Huila

---

## 📋 Checklist de Implementación

- [ ] ✅ Raspberry Pi 4B configurada
- [ ] 🗄️ PostgreSQL instalado y funcionando
- [ ] 🐍 Entorno Python con dependencias
- [ ] 🚀 Servicios systemd creados y activos
- [ ] 🔐 Autenticación @campusucc.edu.co funcionando
- [ ] 🌐 Túnel público configurado y accesible
- [ ] 📱 ESP32 enviando datos correctamente
- [ ] 📊 Dashboard mostrando datos en tiempo real
- [ ] 🔄 Sistema auto-iniciable configurado
- [ ] ✅ Pruebas de conectividad exitosas

---

## 🎯 Estado del Proyecto

**✅ LISTO PARA IMPLEMENTACIÓN**

El código está probado y documentado. Solo falta seguir el `PROMPT_PARA_INNOVASICRASP.md` para desplegar en Raspberry Pi.

**⏱️ Tiempo total de implementación: ~75 minutos**

---

**🐔 Universidad Cooperativa de Colombia - Campus Neiva**  
*Sistema de Monitoreo Galpón Avícola 2024*