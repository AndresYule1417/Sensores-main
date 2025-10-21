# 🚀 GUÍA DE VERIFICACIÓN RÁPIDA - SISTEMA IoT GALPÓN

## ✅ Verificar TODO el Sistema con UN SOLO COMANDO

### 📍 Desde Windows (Opción 1 - Más Fácil)

```bash
VERIFICAR_RASPBERRY.bat
```

Simplemente **haz doble clic** en el archivo `VERIFICAR_RASPBERRY.bat` en la raíz del proyecto.

---

### 📍 Desde Windows (Opción 2 - PowerShell)

```powershell
ssh innovasic@192.168.0.180 "/home/innovasic/galpon/raspberry_backend/verificar_sistema.sh"
```

---

### 📍 Desde la Raspberry Pi (SSH)

```bash
/home/innovasic/galpon/raspberry_backend/verificar_sistema.sh
```

O más corto:

```bash
cd ~/galpon/raspberry_backend
./verificar_sistema.sh
```

---

## 🔍 ¿Qué hace el script de verificación?

El script `verificar_sistema.sh` realiza automáticamente las siguientes tareas:

1. **🛑 Detiene** todos los servicios existentes
2. **🧹 Limpia** procesos duplicados (Servidor.py y uvicorn)
3. **🚀 Reinicia** los servicios correctos:
   - `servidor_tcp.service` (Puerto 8889 TCP → Excel)
   - `fastapi_backend.service` (Puerto 8000 HTTP → SQLite)
4. **📊 Verifica** el estado de los servicios systemd
5. **🔍 Cuenta** procesos en ejecución (debe haber 1 de cada)
6. **🌐 Prueba** la conectividad de la API (3 intentos)

---

## ✅ Resultado Esperado (Sistema OK)

```
🔍 ===== VERIFICACIÓN DEL SISTEMA IoT GALPÓN =====

🛑 [1/6] Deteniendo servicios systemd...
✅ Servicios detenidos

🧹 [2/6] Limpiando procesos duplicados...
✅ Procesos limpiados

🚀 [3/6] Reiniciando servicios...
✅ Servicios reiniciados

📊 [4/6] Verificando estado de servicios systemd...
   ✅ servidor_tcp.service: active
   ✅ fastapi_backend.service: active

🔍 [5/6] Verificando procesos en ejecución...
   📌 Procesos Servidor.py encontrados: 1
   📌 Procesos uvicorn encontrados: 1
   ✅ Servidor TCP corriendo (1 instancia)
   ✅ FastAPI corriendo (1 instancia)

   Detalles de procesos:
   - /home/innovasic/galpon/.../Servidor.py (PID: XXXX)
   - /home/innovasic/galpon/.../uvicorn main:app (PID: XXXX)

🌐 [6/6] Probando conectividad de la API...
✅ API respondiendo correctamente
   Respuesta: {"status":"activo","total_registros":XXX,"ultima_lectura":"HH:MM:SS","conexion_esp8266":true}

📋 ===== RESUMEN DE VERIFICACIÓN =====

✅✅✅ SISTEMA COMPLETAMENTE FUNCIONAL ✅✅✅

🌐 Dashboard puede conectarse a: http://192.168.0.180:8000
📊 Datos almacenados en: /home/innovasic/galpon/raspberry_backend/galpon.db
📁 Archivo Excel: /home/innovasic/galpon/AppIoTEsp8266-UCC-main/Servidor/data_test_14.xlsx
```

---

## ⚠️ Si hay problemas

El script incluye diagnóstico automático:

- **❌ Servicio no activo**: Muestra el estado exacto
- **⚠️ Múltiples procesos**: Indica cuántas instancias duplicadas hay
- **❌ API no responde**: Verifica qué está usando el puerto 8000

### Comandos de diagnóstico manual:

```bash
# Ver logs del servidor TCP
sudo journalctl -u servidor_tcp.service -n 50

# Ver logs de FastAPI
sudo journalctl -u fastapi_backend.service -n 50

# Ver procesos manualmente
ps aux | grep -E 'Servidor|uvicorn'
```

---

## 🔄 Otros Scripts Disponibles

### 1. **verificar_sistema.sh** (Este script - Verificación completa)
```bash
./verificar_sistema.sh
```

### 2. **limpiar_y_reiniciar.sh** (Limpieza rápida)
```bash
./limpiar_y_reiniciar.sh
```

### 3. **setup_autostart.sh** (Configurar auto-inicio)
```bash
./setup_autostart.sh
```

---

## 📦 Archivos del Sistema

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `verificar_sistema.sh` | `/home/innovasic/galpon/raspberry_backend/` | Verificación completa del sistema |
| `limpiar_y_reiniciar.sh` | `/home/innovasic/galpon/raspberry_backend/` | Limpia duplicados y reinicia |
| `servidor_tcp.service` | `/etc/systemd/system/` | Servicio TCP (puerto 8889) |
| `fastapi_backend.service` | `/etc/systemd/system/` | Servicio FastAPI (puerto 8000) |
| `galpon.db` | `/home/innovasic/galpon/raspberry_backend/` | Base de datos SQLite |
| `data_test_14.xlsx` | `/home/innovasic/galpon/AppIoTEsp8266-UCC-main/Servidor/` | Archivo Excel histórico |

---

## 🎯 Flujo de Trabajo Recomendado

### Después de cambios o reinicio de Raspberry Pi:

1. **Ejecutar verificación**:
   ```bash
   ./verificar_sistema.sh
   ```

2. **Si todo está ✅**, abrir dashboard en Windows:
   ```powershell
   streamlit run frontend_dashboard_v3.py
   ```

3. **Verificar conexión** en dashboard:
   - 🟢 Conectado = OK
   - 🔴 Sin conexión = Ejecutar `verificar_sistema.sh` nuevamente

---

## 📊 Arquitectura del Sistema

```
ESP8266 (192.168.0.166)
    │
    ├─ TCP:8889 ──► Servidor.py ──► data_test_14.xlsx
    │                   │
    └─ TCP:8889 ──► FastAPI:8000 ──► galpon.db
                        │
                        └─ HTTP ──► Dashboard (Windows)
```

---

## 💡 Tips Importantes

1. **Auto-inicio configurado**: No necesitas iniciar servicios manualmente después de un reinicio
2. **Un solo proceso de cada**: Verifica que solo haya 1 Servidor.py y 1 uvicorn
3. **Prueba desde Windows**: Abre `http://192.168.0.180:8000/status` en el navegador
4. **Logs en tiempo real**: `sudo journalctl -u fastapi_backend.service -f`

---

## 📅 Última Actualización

**Fecha**: 21 de octubre de 2025  
**Estado**: ✅ Sistema completamente funcional  
**Versión**: 2.0 (Con verificación automática)
