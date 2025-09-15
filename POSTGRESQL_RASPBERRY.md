# 🗄️ CONFIGURACIÓN DE POSTGRESQL EN RASPBERRY PI

## 📋 Instalación Rápida

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# 3. Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 4. Verificar instalación
sudo systemctl status postgresql
```

## 🔧 Configuración de Base de Datos

```bash
# 1. Acceder como usuario postgres
sudo -u postgres psql

# 2. Crear base de datos y usuario
CREATE DATABASE galpon_db;
CREATE USER galpon_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE galpon_db TO galpon_user;

# 3. Configurar permisos
ALTER USER galpon_user CREATEDB;
\q

# 4. Probar conexión
psql -h localhost -U galpon_user -d galpon_db
```

## 📊 Crear Tabla de Sensores

```sql
-- Conectar a la base de datos
\c galpon_db

-- Crear tabla sensors3 (igual a tu proyecto actual)
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

-- Crear índices para mejor rendimiento
CREATE INDEX idx_sensors3_device ON sensors3(device);
CREATE INDEX idx_sensors3_time ON sensors3(time);
CREATE INDEX idx_sensors3_device_time ON sensors3(device, time);

-- Verificar tabla creada
\dt
\d sensors3
```

## 🛡️ Configuración de Seguridad

```bash
# 1. Editar configuración PostgreSQL
sudo nano /etc/postgresql/*/main/postgresql.conf

# Buscar y modificar:
listen_addresses = 'localhost'  # Solo conexiones locales
port = 5432

# 2. Configurar autenticación
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Agregar línea:
local   galpon_db   galpon_user   md5

# 3. Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

## 🔌 Variables de Entorno

Crear archivo `.env` en tu proyecto:

```bash
# .env
DB_USER=galpon_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=galpon_db

# Para producción
DATABASE_URL=postgresql://galpon_user:password123@localhost:5432/galpon_db
```

## 📈 Datos de Prueba

```sql
-- Insertar datos de ejemplo
INSERT INTO sensors3 (device, lux, nh3, hs, h, t, ip) VALUES
('ESP32_001', 45.2, 15.1, 5.3, 65.8, 22.4, '192.168.1.100'),
('ESP32_002', 52.7, 18.9, 4.1, 68.2, 23.1, '192.168.1.101'),
('ESP32_003', 38.9, 12.6, 6.8, 62.5, 21.8, '192.168.1.102');

-- Verificar datos insertados
SELECT * FROM sensors3 ORDER BY time DESC LIMIT 10;
```

## 🔄 Backup y Restauración

```bash
# Crear backup
pg_dump -h localhost -U galpon_user galpon_db > backup_galpon.sql

# Restaurar backup
psql -h localhost -U galpon_user galpon_db < backup_galpon.sql

# Backup automático (cron)
echo "0 2 * * * pg_dump -h localhost -U galpon_user galpon_db > /home/pi/backups/galpon_$(date +\%Y\%m\%d).sql" | crontab -
```

## 🚀 Arranque Automático

```bash
# 1. Crear servicio systemd para FastAPI
sudo nano /etc/systemd/system/galpon-api.service

[Unit]
Description=Galpon Avicola API
After=postgresql.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/galpon
Environment=PATH=/home/pi/galpon/venv/bin
ExecStart=/home/pi/galpon/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# 2. Habilitar servicios
sudo systemctl enable galpon-api
sudo systemctl start galpon-api
sudo systemctl status galpon-api
```

## 📊 Monitoreo de Performance

```sql
-- Ver estadísticas de la tabla
SELECT 
    COUNT(*) as total_registros,
    COUNT(DISTINCT device) as dispositivos_unicos,
    MIN(time) as primer_registro,
    MAX(time) as ultimo_registro,
    AVG(t) as temperatura_promedio
FROM sensors3;

-- Registros por dispositivo
SELECT 
    device,
    COUNT(*) as registros,
    MAX(time) as ultima_lectura
FROM sensors3 
GROUP BY device 
ORDER BY registros DESC;
```

## 🔧 Comandos Útiles

```bash
# Ver logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*-main.log

# Verificar conexiones activas
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Ver tamaño de base de datos
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('galpon_db'));"
```

## 📱 Prueba desde ESP32

```cpp
// Código ESP32 para probar conexión
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "TU_WIFI";
const char* password = "TU_PASSWORD";
const char* serverURL = "http://TU_RASPBERRY_IP:8000/api/sensores";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando WiFi...");
  }
  
  Serial.println("WiFi conectado!");
  
  // Enviar datos de prueba
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  String jsonData = "{\"device\":\"ESP32_TEST\",\"lux\":50.0,\"nh3\":15.0,\"hs\":5.0,\"h\":65.0,\"t\":22.0}";
  
  int httpResponseCode = http.POST(jsonData);
  Serial.println("Respuesta: " + String(httpResponseCode));
  
  http.end();
}

void loop() {
  delay(30000); // Enviar cada 30 segundos
}
```

## ✅ Verificación Final

```bash
# 1. PostgreSQL funcionando
sudo systemctl status postgresql

# 2. Base de datos accesible
psql -h localhost -U galpon_user -d galpon_db -c "SELECT COUNT(*) FROM sensors3;"

# 3. API funcionando
curl http://localhost:8000/health

# 4. Probar endpoint
curl -X POST http://localhost:8000/api/sensores \
  -H "Content-Type: application/json" \
  -d '{"device":"TEST","lux":50,"nh3":15,"hs":5,"h":65,"t":22}'
```

¡Con esto tendrás PostgreSQL configurado correctamente en tu Raspberry Pi! 🎉