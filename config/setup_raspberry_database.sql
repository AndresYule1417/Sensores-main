-- 🍓 Script de configuración de base de datos para Raspberry Pi
-- Universidad Cooperativa de Colombia - Campus Ibagué
-- Sistema de Monitoreo Galpón Avícola

-- Crear base de datos principal
-- Ejecutar con: sqlite3 galpon_avicultura.db < setup_raspberry_database.sql

-- 1. Tabla principal de lecturas de sensores ESP32
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    device_id TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    light_lux REAL,
    nh3_ppm REAL,
    h2s_ppm REAL,
    wifi_rssi INTEGER
);

-- 2. Tabla de estado de dispositivos
CREATE TABLE IF NOT EXISTS device_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de configuración de alertas por administrador UCC
CREATE TABLE IF NOT EXISTS alert_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_email TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    threshold_min REAL,
    threshold_max REAL,
    notification_method TEXT DEFAULT 'email',
    email_enabled BOOLEAN DEFAULT 1,
    whatsapp_enabled BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de historial de alertas
CREATE TABLE IF NOT EXISTS alert_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_email TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    threshold_value REAL,
    actual_value REAL,
    message TEXT,
    notification_sent BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Insertar configuración inicial para administradores UCC
INSERT OR IGNORE INTO alert_config (admin_email, sensor_type, threshold_min, threshold_max) VALUES
('admin1.galpon@campusucc.edu.co', 'temperatura', 15.0, 30.0),
('admin1.galpon@campusucc.edu.co', 'humedad', 40.0, 80.0),
('admin1.galpon@campusucc.edu.co', 'nh3', 0.0, 25.0),
('admin1.galpon@campusucc.edu.co', 'h2s', 0.0, 10.0),
('admin2.sensores@campusucc.edu.co', 'temperatura', 15.0, 30.0),
('admin2.sensores@campusucc.edu.co', 'humedad', 40.0, 80.0),
('admin2.sensores@campusucc.edu.co', 'nh3', 0.0, 25.0),
('admin2.sensores@campusucc.edu.co', 'h2s', 0.0, 10.0);

-- 6. Configurar WAL mode para mejor rendimiento
PRAGMA journal_mode=WAL;

-- 7. Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_sensor_device ON sensor_readings(device_id);
CREATE INDEX IF NOT EXISTS idx_alert_admin ON alert_config(admin_email);

-- Mostrar confirmación
SELECT 'Base de datos configurada correctamente para UCC Ibagué' as status;