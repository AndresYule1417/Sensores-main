# 🚀 GUÍA COMPLETA - EJECUTAR Y GESTIONAR PROYECTO EN RASPBERRY PI

## 📋 ÍNDICE
1. [Auto-inicio (Recomendado)](#auto-inicio)
2. [Verificación del Sistema](#verificación)
3. [Gestión Manual](#gestión-manual)
4. [Comandos Útiles](#comandos-útiles)
5. [Solución de Problemas](#troubleshooting)

---

## 🎯 1. AUTO-INICIO (RECOMENDADO)

### ✅ Sistema Ya Configurado

El sistema **ya está configurado** para iniciarse automáticamente cuando la Raspberry Pi se enciende.

**Servicios activos:**
- `servidor_tcp.service` → Servidor TCP (puerto 8889)
- `fastapi_backend.service` → API FastAPI (puerto 8000)

### 🔍 Verificar Auto-inicio

```bash
# Ver estado de servicios
sudo systemctl status servidor_tcp.service
sudo systemctl status fastapi_backend.service

# Verificar que están habilitados para auto-inicio
sudo systemctl is-enabled servidor_tcp.service
sudo systemctl is-enabled fastapi_backend.service
```

**Resultado esperado:** `enabled`

---

## 🔍 2. VERIFICACIÓN DEL SISTEMA

### ⚡ Script de Verificación Completa (UN SOLO COMANDO)

```bash
/home/innovasic/galpon/raspberry_backend/verificar_sistema.sh
```

O desde cualquier ubicación:

```bash
~/galpon/raspberry_backend/verificar_sistema.sh
```

Este script verifica automáticamente:
- ✅ Estado de servicios systemd
- ✅ Procesos en ejecución
- ✅ Conectividad de la API
- ✅ Datos en base de datos

---

## 🛠️ 3. GESTIÓN MANUAL DE SERVICIOS

### 📊 Ver Estado

```bash
# Estado del servidor TCP
sudo systemctl status servidor_tcp.service

# Estado de la API
sudo systemctl status fastapi_backend.service

# Estado de AMBOS servicios (compacto)
sudo systemctl status servidor_tcp.service fastapi_backend.service --no-pager
```

### 🚀 Iniciar Servicios

```bash
# Iniciar servidor TCP
sudo systemctl start servidor_tcp.service

# Iniciar API
sudo systemctl start fastapi_backend.service

# Iniciar AMBOS
sudo systemctl start servidor_tcp.service fastapi_backend.service
```

### 🛑 Detener Servicios

```bash
# Detener servidor TCP
sudo systemctl stop servidor_tcp.service

# Detener API
sudo systemctl stop fastapi_backend.service

# Detener AMBOS
sudo systemctl stop servidor_tcp.service fastapi_backend.service
```

### 🔄 Reiniciar Servicios

```bash
# Reiniciar servidor TCP
sudo systemctl restart servidor_tcp.service

# Reiniciar API
sudo systemctl restart fastapi_backend.service

# Reiniciar AMBOS
sudo systemctl restart servidor_tcp.service fastapi_backend.service
```

### 🔓 Habilitar/Deshabilitar Auto-inicio

```bash
# HABILITAR auto-inicio (ya está habilitado)
sudo systemctl enable servidor_tcp.service
sudo systemctl enable fastapi_backend.service

# DESHABILITAR auto-inicio (si no quieres que arranquen al encender)
sudo systemctl disable servidor_tcp.service
sudo systemctl disable fastapi_backend.service
```

---

## 📝 4. COMANDOS ÚTILES

### 📊 Ver Logs en Tiempo Real

```bash
# Logs del servidor TCP (últimas 50 líneas y en vivo)
sudo journalctl -u servidor_tcp.service -f -n 50

# Logs de FastAPI
sudo journalctl -u fastapi_backend.service -f -n 50

# Ver solo errores
sudo journalctl -u servidor_tcp.service -p err -n 50
```

**Presiona `Ctrl+C` para salir del modo "follow" (-f)**

### 📋 Ver Logs Históricos

```bash
# Últimas 100 líneas del servidor TCP
sudo journalctl -u servidor_tcp.service -n 100 --no-pager

# Logs desde hace 1 hora
sudo journalctl -u servidor_tcp.service --since "1 hour ago"

# Logs de hoy
sudo journalctl -u servidor_tcp.service --since today
```

### 🔍 Verificar Procesos Activos

```bash
# Ver procesos del servidor TCP
ps aux | grep Servidor.py | grep -v grep

# Ver procesos de la API
ps aux | grep uvicorn | grep -v grep

# Ver TODOS los procesos relacionados
ps aux | grep -E 'Servidor|uvicorn' | grep -v grep
```

### 🌐 Probar Conectividad API

```bash
# Test rápido de status
curl http://localhost:8000/status

# Ver últimos 5 registros
curl http://localhost:8000/sensores/ultimos?limit=5

# Formato JSON legible
curl -s http://localhost:8000/sensores/ultimos?limit=3 | python3 -m json.tool
```

### 🗄️ Consultar Base de Datos

```bash
# Contar registros totales
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT COUNT(*) FROM sensores"

# Ver últimos 5 registros
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT * FROM sensores ORDER BY id DESC LIMIT 5"

# Ver esquema de la tabla
sqlite3 /home/innovasic/galpon/data/galpon.db ".schema sensores"

# Abrir base de datos interactiva
sqlite3 /home/innovasic/galpon/data/galpon.db
```

**Comandos dentro de SQLite:**
```sql
.tables              -- Ver todas las tablas
.schema sensores     -- Ver estructura de tabla
SELECT * FROM sensores LIMIT 10;
.quit                -- Salir
```

### 📊 Ver Puertos Abiertos

```bash
# Ver puertos en uso
sudo netstat -tlnp | grep -E '8889|8000'

# Ver conexiones activas de ESP8266
sudo netstat -anp | grep 8889 | grep ESTABLISHED
```

---

## 🚨 5. SOLUCIÓN DE PROBLEMAS

### ❌ Problema: Servicio no inicia

```bash
# Ver error exacto
sudo journalctl -u servidor_tcp.service -n 50 --no-pager

# Ver estado detallado
sudo systemctl status servidor_tcp.service -l

# Reiniciar y verificar
sudo systemctl restart servidor_tcp.service
sleep 3
sudo systemctl status servidor_tcp.service
```

### ❌ Problema: Puerto ya en uso

```bash
# Identificar qué está usando el puerto 8889
sudo netstat -tlnp | grep 8889

# Matar proceso manualmente (reemplaza PID)
sudo kill -9 <PID>

# O matar todos los procesos del servidor
sudo pkill -f Servidor.py
```

### ❌ Problema: Base de datos no actualiza

```bash
# Verificar que la tabla existe
sqlite3 /home/innovasic/galpon/data/galpon.db ".tables"

# Ver últimos registros con timestamp
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT id, Device, time FROM sensores ORDER BY id DESC LIMIT 10"

# Verificar permisos del archivo
ls -lh /home/innovasic/galpon/data/galpon.db
```

### ❌ Problema: API no responde

```bash
# Verificar que el servicio está activo
sudo systemctl status fastapi_backend.service

# Ver logs de error
sudo journalctl -u fastapi_backend.service -n 50

# Reiniciar API
sudo systemctl restart fastapi_backend.service

# Probar después de 5 segundos
sleep 5
curl http://localhost:8000/status
```

### 🧹 Limpiar y Reiniciar TODO

```bash
# Detener servicios
sudo systemctl stop servidor_tcp.service fastapi_backend.service

# Matar procesos zombies
sudo pkill -f Servidor.py
sudo pkill -f uvicorn

# Esperar y reiniciar
sleep 3
sudo systemctl start servidor_tcp.service fastapi_backend.service

# Verificar
sleep 5
/home/innovasic/galpon/raspberry_backend/verificar_sistema.sh
```

---

## 📂 6. ESTRUCTURA DE ARCHIVOS IMPORTANTES

```
/home/innovasic/galpon/
│
├── AppIoTEsp8266-UCC-main/Servidor/
│   ├── Servidor.py                    # Servidor TCP (ACTIVO)
│   ├── Servidor_original_backup.py    # Backup del original
│   ├── data_test_14.xlsx             # Archivo Excel con datos
│   └── venv/                         # Entorno virtual Python
│
├── raspberry_backend/
│   ├── main.py                       # FastAPI backend
│   ├── models.py                     # Modelos SQLAlchemy
│   ├── database.py                   # Configuración DB
│   ├── verificar_sistema.sh          # Script de verificación ⭐
│   ├── limpiar_y_reiniciar.sh       # Script de limpieza
│   └── venv/                         # Entorno virtual Python
│
├── data/
│   └── galpon.db                     # Base de datos SQLite ⭐
│
└── /etc/systemd/system/
    ├── servidor_tcp.service          # Servicio TCP
    └── fastapi_backend.service       # Servicio API
```

---

## 🎯 7. WORKFLOWS COMUNES

### 🔄 Después de Reiniciar Raspberry Pi

Los servicios se inician **automáticamente**, pero para verificar:

```bash
# Esperar 30 segundos después del boot
sleep 30

# Verificar sistema completo
~/galpon/raspberry_backend/verificar_sistema.sh
```

### 📊 Monitoreo Diario

```bash
# Ver estado rápido
sudo systemctl status servidor_tcp.service fastapi_backend.service --no-pager

# Ver cuántos datos hay
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT COUNT(*) FROM sensores"

# Probar API
curl http://localhost:8000/status
```

### 🔧 Después de Modificar Código

```bash
# Reiniciar servicios
sudo systemctl restart servidor_tcp.service fastapi_backend.service

# Verificar logs
sudo journalctl -u servidor_tcp.service -f
```

---

## 📞 8. ACCESO DESDE OTROS DISPOSITIVOS

### 🌐 Desde Windows (Dashboard)

```bash
# Abrir PowerShell y ejecutar:
streamlit run frontend_dashboard_v3.py
```

**URL:** `http://localhost:8501`

### 🔗 Desde el Navegador

- **API Docs:** http://192.168.0.180:8000/docs
- **API Status:** http://192.168.0.180:8000/status
- **Dashboard:** http://localhost:8501 (desde Windows)

---

## 📅 Última Actualización

**Fecha:** 21 de octubre de 2025  
**Estado:** ✅ Sistema completamente funcional  
**Auto-inicio:** ✅ Configurado y habilitado

---

## 💡 COMANDOS MÁS USADOS (CHEAT SHEET)

```bash
# ✅ VERIFICAR TODO
~/galpon/raspberry_backend/verificar_sistema.sh

# 🔄 REINICIAR TODO
sudo systemctl restart servidor_tcp.service fastapi_backend.service

# 📊 VER LOGS
sudo journalctl -u servidor_tcp.service -f

# 🗄️ VER DATOS
sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT COUNT(*) FROM sensores"

# 🌐 PROBAR API
curl http://localhost:8000/status

# 🔍 VER PROCESOS
ps aux | grep -E 'Servidor|uvicorn' | grep -v grep
```

---

¡Ya puedes trabajar directamente en la Raspberry Pi sin necesidad de SSH! 🎉
