# 🐔 INSTALACIÓN COMPLETA - RASPBERRY PI 4B
**Sistema de Monitoreo Galpón Avícola - Universidad Cooperativa de Colombia**

---

## 📋 Requisitos Previos

### 🛠️ Hardware Necesario
- ✅ Raspberry Pi 4B (4GB RAM mínimo recomendado)
- ✅ MicroSD 32GB Clase 10 o superior
- ✅ Fuente de alimentación oficial Raspberry Pi
- ✅ Cable Ethernet o WiFi configurado
- ✅ Sensores ESP32 configurados

### 💻 Software Base
- ✅ Raspberry Pi OS Lite (64-bit) - Versión más reciente
- ✅ SSH habilitado para acceso remoto
- ✅ Internet estable para descarga de dependencias

---

## 🚀 PASO 1: Preparación del Sistema

### 1.1 Actualizar Sistema
```bash
# Conectar por SSH o terminal local
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 1.2 Instalar Dependencias Base
```bash
# Herramientas esenciales
sudo apt install -y git curl wget vim nano htop tree

# Python 3 y pip
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Dependencias de compilación
sudo apt install -y build-essential libssl-dev libffi-dev
```

---

## 🗄️ PASO 2: Configuración PostgreSQL

### 2.1 Instalación PostgreSQL
```bash
# Instalar PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Iniciar y habilitar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar instalación
sudo systemctl status postgresql
```

### 2.2 Configurar Base de Datos
```bash
# Cambiar a usuario postgres
sudo -u postgres psql

# Ejecutar en psql:
CREATE DATABASE galpon_db;
CREATE USER galpon_user WITH PASSWORD 'UCC2024_Galpon!';
GRANT ALL PRIVILEGES ON DATABASE galpon_db TO galpon_user;
ALTER USER galpon_user CREATEDB;
\q

# Probar conexión
psql -h localhost -U galpon_user -d galpon_db
```

### 2.3 Crear Tabla de Sensores
```sql
-- Conectar a la base de datos
\c galpon_db

-- Crear tabla principal
CREATE TABLE sensors3 (
    id SERIAL PRIMARY KEY,
    device VARCHAR(50) NOT NULL,
    lux FLOAT NOT NULL,
    nh3 FLOAT NOT NULL,
    hs FLOAT NOT NULL,
    h FLOAT NOT NULL,
    t FLOAT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(45)
);

-- Crear índices para optimización
CREATE INDEX idx_sensors3_device ON sensors3(device);
CREATE INDEX idx_sensors3_time ON sensors3(time DESC);
CREATE INDEX idx_sensors3_device_time ON sensors3(device, time DESC);

-- Insertar datos de ejemplo
INSERT INTO sensors3 (device, lux, nh3, hs, h, t, ip) VALUES
('ESP32_001', 45.2, 15.1, 5.3, 65.8, 22.4, '192.168.1.100'),
('ESP32_002', 52.7, 18.9, 4.1, 68.2, 23.1, '192.168.1.101'),
('ESP32_003', 38.9, 12.6, 6.8, 62.5, 21.8, '192.168.1.102');

-- Verificar datos
SELECT * FROM sensors3 ORDER BY time DESC;
\q
```

---

## 📂 PASO 3: Configuración del Proyecto

### 3.1 Crear Estructura de Directorios
```bash
# Crear directorio principal
mkdir -p /home/pi/galpon
cd /home/pi/galpon

# Crear subdirectorios
mkdir -p logs backups config
```

### 3.2 Crear Entorno Virtual Python
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip
```

### 3.3 Instalar Dependencias Python
```bash
# Crear requirements.txt
cat > requirements.txt << 'EOF'
streamlit==1.31.0
fastapi==0.104.1
uvicorn[standard]==0.24.0
pandas==2.1.4
plotly==5.17.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-multipart==0.0.6
pydantic==2.5.2
python-dotenv==1.0.0
EOF

# Instalar dependencias
pip install -r requirements.txt
```

---

## 📁 PASO 4: Archivos del Proyecto

### 4.1 Crear Archivo .env
```bash
cat > .env << 'EOF'
# Configuración Base de Datos
DB_USER=galpon_user
DB_PASSWORD=UCC2024_Galpon!
DB_HOST=localhost
DB_PORT=5432
DB_NAME=galpon_db

# URL completa de conexión
DATABASE_URL=postgresql://galpon_user:UCC2024_Galpon!@localhost:5432/galpon_db

# Configuración de la aplicación
ENVIRONMENT=production
SECRET_KEY=UCC_Galpon_Avicola_2024_Secreto_Muy_Seguro
EOF
```

### 4.2 Transferir Archivos del Proyecto
```bash
# Opción A: Transferir desde tu computadora (usar scp o sftp)
# scp streamlit_app_raspberry.py pi@IP_RASPBERRY:/home/pi/galpon/
# scp main_raspberry.py pi@IP_RASPBERRY:/home/pi/galpon/
# scp min_tabla.py pi@IP_RASPBERRY:/home/pi/galpon/
# scp styles.css pi@IP_RASPBERRY:/home/pi/galpon/

# Opción B: Crear archivos directamente (copiar contenido)
nano streamlit_app_raspberry.py  # Pegar contenido del archivo
nano main_raspberry.py           # Pegar contenido del archivo  
nano min_tabla.py               # Pegar contenido original
nano styles.css                 # Pegar contenido original
```

### 4.3 Hacer Archivos Ejecutables
```bash
chmod +x streamlit_app_raspberry.py
chmod +x main_raspberry.py
```

---

## 🚀 PASO 5: Configuración de Servicios

### 5.1 Crear Servicio FastAPI
```bash
sudo nano /etc/systemd/system/galpon-api.service

# Contenido del archivo:
[Unit]
Description=Galpon Avicola FastAPI
After=postgresql.service network.target
Requires=postgresql.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/galpon
Environment=PATH=/home/pi/galpon/venv/bin
ExecStart=/home/pi/galpon/venv/bin/python -m uvicorn main_raspberry:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5.2 Crear Servicio Streamlit
```bash
sudo nano /etc/systemd/system/galpon-dashboard.service

# Contenido del archivo:
[Unit]
Description=Galpon Avicola Dashboard
After=galpon-api.service
Requires=galpon-api.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/galpon
Environment=PATH=/home/pi/galpon/venv/bin
ExecStart=/home/pi/galpon/venv/bin/python -m streamlit run streamlit_app_raspberry.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5.3 Habilitar y Iniciar Servicios
```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicios
sudo systemctl enable galpon-api
sudo systemctl enable galpon-dashboard

# Iniciar servicios
sudo systemctl start galpon-api
sudo systemctl start galpon-dashboard

# Verificar estado
sudo systemctl status galpon-api
sudo systemctl status galpon-dashboard
```

---

## 🌐 PASO 6: Configuración de Acceso Público

### 6.1 Instalar Cloudflare Tunnel (Recomendado)
```bash
# Descargar cloudflared para ARM64
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb

# Instalar
sudo dpkg -i cloudflared-linux-arm64.deb

# Autenticar (seguir instrucciones en pantalla)
cloudflared tunnel login

# Crear túnel
cloudflared tunnel create galpon-ucc

# Anotar el ID del túnel que aparece
```

### 6.2 Configurar Túnel
```bash
# Crear directorio de configuración
mkdir -p ~/.cloudflared

# Crear archivo de configuración
nano ~/.cloudflared/config.yml

# Contenido (reemplazar TU-TUNNEL-ID):
tunnel: TU-TUNNEL-ID
credentials-file: /home/pi/.cloudflared/TU-TUNNEL-ID.json

ingress:
  # Dashboard principal
  - hostname: galpon-ucc.tudominio.com
    service: http://localhost:8501
  
  # API Backend
  - hostname: api-galpon-ucc.tudominio.com
    service: http://localhost:8000
    
  # Catch-all
  - service: http_status:404
```

### 6.3 Crear Servicio Cloudflare
```bash
sudo nano /etc/systemd/system/cloudflared.service

# Contenido:
[Unit]
Description=Cloudflare Tunnel
After=network.target galpon-dashboard.service
Requires=galpon-dashboard.service

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cloudflared tunnel run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Habilitar servicio
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

---

## 🔒 PASO 7: Configuración de Seguridad

### 7.1 Configurar Firewall
```bash
# Instalar y configurar UFW
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow from 192.168.0.0/16  # Red local
```

### 7.2 Instalar Fail2Ban
```bash
# Instalar fail2ban
sudo apt install fail2ban -y

# Configurar
sudo nano /etc/fail2ban/jail.local

# Contenido:
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
ignoreip = 127.0.0.1/8 192.168.0.0/16

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

# Iniciar servicio
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 📊 PASO 8: Configuración de Monitoreo

### 8.1 Script de Monitoreo
```bash
nano /home/pi/galpon/monitor.sh

#!/bin/bash
# Script de monitoreo del sistema

echo "🐔 Estado del Sistema Galpón Avícola UCC"
echo "========================================"
echo "📅 Fecha: $(date)"
echo "🏛️ Universidad Cooperativa de Colombia"
echo ""

# PostgreSQL
echo "🗄️ PostgreSQL:"
sudo systemctl is-active postgresql && echo "   ✅ Activo" || echo "   ❌ Inactivo"

# API FastAPI
echo "🚀 API FastAPI:"
sudo systemctl is-active galpon-api && echo "   ✅ Activo" || echo "   ❌ Inactivo"

# Dashboard Streamlit
echo "📊 Dashboard:"
sudo systemctl is-active galpon-dashboard && echo "   ✅ Activo" || echo "   ❌ Inactivo"

# Cloudflare Tunnel
echo "🌐 Túnel Público:"
sudo systemctl is-active cloudflared && echo "   ✅ Activo" || echo "   ❌ Inactivo"

# Recursos del sistema
echo ""
echo "💻 Recursos del Sistema:"
echo "   CPU: $(cat /proc/loadavg | awk '{print $1}')"
echo "   RAM: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "   Disco: $(df -h / | awk 'NR==2{print $3 "/" $2}')"

# Base de datos
echo ""
echo "📊 Base de Datos:"
SENSOR_COUNT=$(psql -h localhost -U galpon_user -d galpon_db -t -c "SELECT COUNT(*) FROM sensors3;" 2>/dev/null | xargs)
echo "   Registros totales: ${SENSOR_COUNT:-'Error conectando'}"

# Hacer ejecutable
chmod +x /home/pi/galpon/monitor.sh
```

### 8.2 Configurar Cron para Monitoreo
```bash
# Editar crontab
crontab -e

# Agregar líneas:
# Backup diario a las 2 AM
0 2 * * * pg_dump -h localhost -U galpon_user galpon_db > /home/pi/galpon/backups/backup_$(date +\%Y\%m\%d).sql

# Log de monitoreo cada hora
0 * * * * /home/pi/galpon/monitor.sh >> /home/pi/galpon/logs/system_$(date +\%Y\%m\%d).log

# Limpiar logs antiguos (más de 30 días)
0 3 * * * find /home/pi/galpon/logs -name "*.log" -mtime +30 -delete
```

---

## ✅ PASO 9: Verificación Final

### 9.1 Probar Servicios Localmente
```bash
# Verificar API
curl http://localhost:8000/health

# Verificar endpoint de sensores
curl -X POST http://localhost:8000/api/sensores \
  -H "Content-Type: application/json" \
  -d '{"device":"TEST_PI","lux":50,"nh3":15,"hs":5,"h":65,"t":22}'

# Verificar dashboard (en navegador)
# http://IP_RASPBERRY:8501
```

### 9.2 Probar Acceso Público
```bash
# Verificar túnel (reemplazar por tu dominio)
curl -I https://galpon-ucc.tudominio.com
curl https://api-galpon-ucc.tudominio.com/health
```

### 9.3 Ver Logs de Sistema
```bash
# Logs de servicios
sudo journalctl -u galpon-api -f
sudo journalctl -u galpon-dashboard -f
sudo journalctl -u cloudflared -f

# Logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*-main.log

# Monitor del sistema
/home/pi/galpon/monitor.sh
```

---

## 🔧 Comandos Útiles de Mantenimiento

```bash
# Reiniciar todos los servicios
sudo systemctl restart galpon-api galpon-dashboard cloudflared

# Ver estado de todos los servicios
sudo systemctl status galpon-api galpon-dashboard cloudflared postgresql

# Actualizar código (después de cambios)
cd /home/pi/galpon
source venv/bin/activate
# (transferir archivos nuevos)
sudo systemctl restart galpon-api galpon-dashboard

# Backup manual
pg_dump -h localhost -U galpon_user galpon_db > backup_manual_$(date +%Y%m%d_%H%M).sql

# Ver conexiones activas a la base de datos
psql -h localhost -U galpon_user -d galpon_db -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

---

## 📱 URLs de Acceso Final

Después de completar la instalación, tendrás acceso a:

- **🏠 Dashboard Principal:** `https://galpon-ucc.tudominio.com`
- **🚀 API Backend:** `https://api-galpon-ucc.tudominio.com`
- **📚 Documentación API:** `https://api-galpon-ucc.tudominio.com/api/docs`
- **📊 Estado del Sistema:** `https://api-galpon-ucc.tudominio.com/health`

---

## 🆘 Solución de Problemas

### Problema: Servicio no inicia
```bash
# Ver logs detallados
sudo journalctl -u nombre-servicio -n 50

# Verificar permisos
sudo chown -R pi:pi /home/pi/galpon
```

### Problema: Error de base de datos
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Probar conexión manual
psql -h localhost -U galpon_user -d galpon_db
```

### Problema: No hay acceso público
```bash
# Verificar túnel
cloudflared tunnel info galpon-ucc

# Ver logs del túnel
sudo journalctl -u cloudflared -f
```

---

## 🎉 ¡Instalación Completada!

Tu sistema de monitoreo galpón avícola está ahora funcionando en:

✅ **Raspberry Pi 4B** con sistema local robusto  
✅ **PostgreSQL** con datos persistentes y backups automáticos  
✅ **FastAPI** recibiendo datos de sensores ESP32  
✅ **Streamlit** con dashboard profesional y autenticación  
✅ **Acceso público gratuito** vía Cloudflare Tunnel  
✅ **Monitoreo automático** y logs del sistema  

**🏛️ Universidad Cooperativa de Colombia - Campus Neiva**  
**📧 Soporte:** sistemas@campusucc.edu.co  

¡Tiempo total de instalación: ~30 minutos! ⏱️