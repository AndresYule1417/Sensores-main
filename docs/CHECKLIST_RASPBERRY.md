# 🎯 CHECKLIST PARA TÉCNICO RASPBERRY PI

## ✅ TAREAS A COMPLETAR:

### 📂 1. PREPARACIÓN INICIAL
- [ ] Conectar SSH a `192.168.20.33`
- [ ] Crear directorio `/home/innovasic/galpon/backend`
- [ ] Verificar que existe `/home/innovasic/galpon/data/galpon.db`

### 📁 2. ARCHIVOS A RECIBIR
- [ ] `main.py` (servidor FastAPI)
- [ ] `database.py` (conexión SQLite)  
- [ ] `models.py` (modelo tabla sensores)
- [ ] `crud.py` (funciones consulta)
- [ ] `requirements_api.txt` (dependencias)

### 🐍 3. INSTALACIÓN PYTHON
- [ ] Actualizar sistema: `sudo apt update && upgrade`
- [ ] Instalar Python3 y pip
- [ ] Crear entorno virtual en `/home/innovasic/galpon/env`
- [ ] Instalar dependencias: `pip install -r requirements_api.txt`

### 🗄️ 4. VERIFICAR BASE DE DATOS
- [ ] Confirmar tabla `sensores` existe
- [ ] Verificar estructura: id, tiempo, temperatura, humedad, luminosidad, amonio, sulfuro
- [ ] Probar consulta: `SELECT * FROM sensores LIMIT 5;`

### 🚀 5. EJECUTAR API
- [ ] Activar entorno virtual
- [ ] Ejecutar: `uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] Verificar que no hay errores

### ✅ 6. TESTING
- [ ] `curl http://localhost:8000/` → Respuesta JSON
- [ ] `curl http://localhost:8000/status` → Estado sistema
- [ ] `curl http://192.168.20.33:8000/` → Acceso remoto funciona
- [ ] Navegador: `http://192.168.20.33:8000/docs` → Documentación

### 🔧 7. CONFIGURACIÓN PRODUCCIÓN
- [ ] Configurar servicio systemd (opcional)
- [ ] Verificar firewall puerto 8000
- [ ] Ejecutar en background permanente

---

## 🚨 PROBLEMAS COMUNES:

| Error | Solución |
|-------|----------|
| No encuentra galpon.db | Verificar ruta y permisos |
| Puerto 8000 ocupado | `sudo netstat -tlnp \| grep :8000` |
| Dependencias fallan | `pip install --upgrade pip` |
| No acepta conexiones remotas | Verificar `--host 0.0.0.0` |

---

## 📞 COMUNICACIÓN:

**AVISAR CUANDO:**
✅ API responde en `http://192.168.20.33:8000/status`  
✅ Endpoints devuelven datos de sensores  
✅ Sistema listo para frontend  

**CONTACTO:** Técnico Frontend Windows