# 🍓 INSTRUCCIONES EXACTAS PARA CONFIGURAR RASPBERRY PI - BACKEND

## 📋 PARA EL TÉCNICO DE BACKEND/RASPBERRY PI

### 📍 INFORMACIÓN DEL SISTEMA:
- **IP Raspberry Pi:** `192.168.20.33`
- **Base de datos:** `/home/innovasic/galpon/data/galpon.db`
- **Tabla:** `sensores` (con campos: id, tiempo, temperatura, humedad, luminosidad, amonio, sulfuro)
- **Puerto API:** `8000`

---

## 🎯 PASO 1: PREPARAR DIRECTORIO DE TRABAJO

```bash
# Conectarse a la Raspberry Pi via SSH
ssh pi@192.168.20.33

# Crear estructura de directorios
sudo mkdir -p /home/innovasic/galpon/backend
sudo chown -R pi:pi /home/innovasic/galpon/

# Navegar al directorio backend
cd /home/innovasic/galpon/backend
```

---

## 📂 PASO 2: COPIAR ARCHIVOS DESDE WINDOWS

**El técnico de Windows debe enviarte estos 5 archivos:**

1. `main.py` (servidor FastAPI principal)
2. `database.py` (configuración SQLite)
3. `models.py` (modelo de tabla sensores)
4. `crud.py` (funciones de consulta)
5. `requirements_api.txt` (dependencias)

**Copiar archivos via SCP (desde Windows):**
```bash
# Desde Windows (PowerShell):
scp raspberry_backend/main.py pi@192.168.20.33:/home/innovasic/galpon/backend/
scp raspberry_backend/database.py pi@192.168.20.33:/home/innovasic/galpon/backend/
scp raspberry_backend/models.py pi@192.168.20.33:/home/innovasic/galpon/backend/
scp raspberry_backend/crud.py pi@192.168.20.33:/home/innovasic/galpon/backend/
scp raspberry_backend/requirements_api.txt pi@192.168.20.33:/home/innovasic/galpon/backend/
```

**O usar USB/transferencia manual:**
```bash
# Si usas USB, montar y copiar:
sudo mount /dev/sda1 /mnt/usb
cp /mnt/usb/raspberry_backend/* /home/innovasic/galpon/backend/
```

---

## 🐍 PASO 3: INSTALAR DEPENDENCIAS PYTHON

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip (si no están)
sudo apt install python3 python3-pip python3-venv -y

# Crear entorno virtual (recomendado)
python3 -m venv /home/innovasic/galpon/env

# Activar entorno virtual
source /home/innovasic/galpon/env/bin/activate

# Instalar dependencias del proyecto
cd /home/innovasic/galpon/backend
pip install -r requirements_api.txt
```

**Contenido de requirements_api.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
```

---

## 🗄️ PASO 4: VERIFICAR BASE DE DATOS

```bash
# Verificar que existe la base de datos
ls -la /home/innovasic/galpon/data/galpon.db

# Verificar estructura de tabla
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT name FROM sqlite_master WHERE type='table';"

# Verificar estructura de tabla sensores
sqlite3 /home/innovasic/galpon/data/galpon.db ".schema sensores"

# Ver algunos registros de ejemplo
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT * FROM sensores LIMIT 5;"
```

**La tabla debe tener esta estructura:**
```sql
CREATE TABLE sensores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tiempo INTEGER NOT NULL,
    temperatura REAL,
    humedad REAL,
    luminosidad INTEGER,
    amonio REAL,
    sulfuro REAL
);
```

---

## 🚀 PASO 5: EJECUTAR API FASTAPI

### Método 1: Ejecución directa (para testing)
```bash
# Activar entorno virtual
source /home/innovasic/galpon/env/bin/activate

# Navegar al directorio
cd /home/innovasic/galpon/backend

# Ejecutar API
python main.py
```

### Método 2: Con uvicorn (recomendado)
```bash
# Activar entorno virtual
source /home/innovasic/galpon/env/bin/activate

# Ejecutar con uvicorn
cd /home/innovasic/galpon/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Método 3: En background permanente
```bash
# Ejecutar en background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /home/innovasic/galpon/logs/api.log 2>&1 &

# Ver el proceso
ps aux | grep uvicorn

# Ver logs
tail -f /home/innovasic/galpon/logs/api.log
```

---

## ✅ PASO 6: VERIFICAR QUE FUNCIONA

### 6.1 Testing local en Raspberry Pi:
```bash
# Probar endpoint raíz
curl http://localhost:8000/

# Probar estado del sistema
curl http://localhost:8000/status

# Probar últimos sensores
curl http://localhost:8000/sensores/ultimos?limit=5

# Probar tiempo real
curl http://localhost:8000/sensores/tiempo-real?minutes=5
```

### 6.2 Testing remoto desde otra computadora:
```bash
# Desde cualquier PC en la red
curl http://192.168.20.33:8000/status
```

### 6.3 Verificar en navegador:
- Abrir navegador en: `http://192.168.20.33:8000`
- Documentación API: `http://192.168.20.33:8000/docs`

---

## 🔧 PASO 7: CONFIGURAR SERVICIO SYSTEMD (OPCIONAL)

**Para que la API se ejecute automáticamente al iniciar:**

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/galpon-api.service
```

**Contenido del archivo:**
```ini
[Unit]
Description=Galpon IoT FastAPI Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/innovasic/galpon/backend
Environment=PATH=/home/innovasic/galpon/env/bin
ExecStart=/home/innovasic/galpon/env/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Activar servicio:**
```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio para auto-inicio
sudo systemctl enable galpon-api.service

# Iniciar servicio
sudo systemctl start galpon-api.service

# Verificar estado
sudo systemctl status galpon-api.service

# Ver logs del servicio
sudo journalctl -u galpon-api.service -f
```

---

## 🌐 PASO 8: CONFIGURAR FIREWALL (SI ESTÁ ACTIVO)

```bash
# Verificar estado del firewall
sudo ufw status

# Si está activo, permitir puerto 8000
sudo ufw allow 8000

# Verificar reglas
sudo ufw status numbered
```

---

## 📊 PASO 9: ENDPOINTS DISPONIBLES

Una vez funcionando, la API tendrá estos endpoints:

- `GET /` - Estado general
- `GET /status` - Estado del sistema y conexión ESP32
- `GET /sensores/ultimos?limit=N` - Últimos N registros
- `GET /sensores/tiempo-real?minutes=N` - Datos de últimos N minutos  
- `GET /sensores/historico?inicio=YYYY-MM-DD&fin=YYYY-MM-DD` - Histórico
- `GET /sensores/alertas` - Registros que superen umbrales
- `GET /sensores/estadisticas` - Estadísticas básicas
- `GET /docs` - Documentación interactiva

---

## 🚨 TROUBLESHOOTING

### Problema: No encuentra la base de datos
```bash
# Verificar permisos
sudo chown pi:pi /home/innovasic/galpon/data/galpon.db
sudo chmod 664 /home/innovasic/galpon/data/galpon.db
```

### Problema: Puerto 8000 ocupado
```bash
# Ver qué usa el puerto
sudo netstat -tlnp | grep :8000

# Matar proceso si es necesario
sudo kill -9 <PID>
```

### Problema: Dependencias no se instalan
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar manualmente
pip install fastapi uvicorn sqlalchemy pydantic
```

### Problema: No se conecta desde otra PC
```bash
# Verificar que escucha en todas las interfaces
netstat -tlnp | grep :8000

# Debe mostrar: 0.0.0.0:8000
```

---

## ✅ CONFIRMACIÓN FINAL

**La API está lista cuando veas:**
1. ✅ `curl http://localhost:8000/` devuelve JSON
2. ✅ `curl http://192.168.20.33:8000/status` funciona desde otra PC
3. ✅ Navegador muestra documentación en `/docs`
4. ✅ Endpoints devuelven datos de la tabla `sensores`

**¡Informar al equipo cuando esté listo para conectar el frontend!** 🚀