# 🍓 PROMPT PARA CONFIGURAR RASPBERRY PI - UCC IBAGUÉ

## CONTEXTO DE LA MISIÓN:
Necesito configurar un Raspberry Pi 4 para un proyecto de monitoreo de galpón avícola en la Universidad Cooperativa de Colombia campus Ibagué. El sistem    a debe funcionar como servidor MQTT local y base de datos para recibir datos de sensores ESP32 en tiempo real.

## ESPECIFICACIONES TÉCNICAS:
- **Hardware**: Raspberry Pi 4 (4GB RAM mínimo)
- **OS**: Raspberry Pi OS Lite (sin interfaz gráfica para mayor rendimiento)
- **Conectividad**: WiFi y Ethernet
- **Servicios**: MQTT Broker (Mosquitto), Python 3.9+, SQLite, SSH
- **Seguridad**: Firewall configurado, SSH con claves, usuarios limitados

## REQUISITOS DEL SISTEMA:

### 🔌 CONECTIVIDAD Y RED:
- Configurar WiFi con credenciales seguras de UCC
- Habilitar SSH para administración remota
- Configurar IP estática en red universitaria
- Abrir puertos específicos: 22 (SSH), 1883 (MQTT), 8501 (Streamlit)

### 📡 SERVICIOS MQTT:
- Instalar y configurar Mosquitto MQTT Broker
- Configurar autenticación MQTT con usuarios y contraseñas
- Configurar topics específicos: `galpon/+/sensor/+`
- Habilitar logs y monitoreo de conexiones

### 💾 BASE DE DATOS:
- Configurar SQLite con WAL mode para concurrencia
- Crear backup automático de datos cada 24 horas
- Configurar rotación de logs
- Optimizar rendimiento para escrituras frecuentes

### 🐍 ENTORNO PYTHON:
- Python 3.9+ con pip actualizado
- Instalar dependencias: paho-mqtt, sqlite3, streamlit, pandas
- Configurar servicios systemd para auto-inicio
- Crear entorno virtual aislado

### 🔒 SEGURIDAD:
- Cambiar contraseña por defecto del usuario pi
- Configurar fail2ban para SSH
- Configurar UFW firewall
- Deshabilitar servicios innecesarios
- Configurar actualizaciones automáticas de seguridad

### 📊 MONITOREO:
- Configurar logs del sistema
- Monitoreo de temperatura CPU/GPU
- Monitoreo de espacio en disco
- Alertas por sobrecalentamiento

## CONFIGURACIÓN ESPECÍFICA UCC:

### 🏫 INTEGRACIÓN UNIVERSITARIA:
- Documentar configuración para equipo técnico UCC
- Crear usuarios administrativos con permisos limitados
- Configurar respaldos en ubicación segura del campus
- Establecer procedimientos de mantenimiento

### 🌐 RED CAMPUS:
- Coordinar con IT de UCC para asignación de IP fija
- Configurar DNS interno si está disponible
- Documentar puertos utilizados para firewall universitario
- Crear reglas de acceso desde laboratorios específicos

## SCRIPTS DE INSTALACIÓN SOLICITADOS:

1. **Script de instalación inicial** (`setup_raspberry_ucc.sh`)
2. **Script de configuración MQTT** (`configure_mqtt.sh`)
3. **Script de configuración Python** (`setup_python_env.sh`)
4. **Script de seguridad** (`security_hardening.sh`)
5. **Script de monitoreo** (`system_monitor.sh`)

## SERVICIOS SYSTEMD NECESARIOS:

1. **mqtt-collector.service** - Recolector MQTT→SQLite
2. **galpon-dashboard.service** - Dashboard Streamlit
3. **backup-database.service** - Backup automático
4. **system-monitor.service** - Monitoreo del sistema

## ESTRUCTURA DE DIRECTORIOS:
```
/home/galpon/
├── scripts/           # Scripts de administración
├── data/             # Base de datos SQLite
├── logs/             # Logs del sistema
├── backups/          # Respaldos automáticos
├── config/           # Archivos de configuración
└── env/              # Entorno virtual Python
```

## TESTING Y VALIDACIÓN:
- Procedimientos para probar conectividad MQTT
- Scripts de validación de datos
- Benchmarks de rendimiento
- Procedimientos de recovery en caso de fallas

## DOCUMENTACIÓN REQUERIDA:
- Manual de administración para personal UCC
- Guía de troubleshooting común
- Procedimientos de backup y restore
- Contactos de soporte técnico

---

## 🎯 ENTREGABLES ESPERADOS:

1. ✅ Raspberry Pi funcional con todos los servicios
2. ✅ Scripts automatizados de instalación y configuración
3. ✅ Documentación completa en español
4. ✅ Procedimientos de mantenimiento
5. ✅ Sistema de monitoreo y alertas
6. ✅ Integration testing con ESP32 existente

**NOTA IMPORTANTE**: El sistema debe ser robusto para funcionamiento 24/7 en ambiente académico, con mínimo mantenimiento y máxima confiabilidad para investigación avícola.

**TIMELINE**: Configuración completa en máximo 2 días laborales, con testing adicional de 1 día.

**SOPORTE**: El sistema debe incluir documentación suficiente para que el equipo técnico de UCC Ibagué pueda administrarlo independientemente.