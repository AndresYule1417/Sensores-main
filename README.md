# 🐔 Sistema de Monitoreo Galpón Avícola
**Universidad Cooperativa de Colombia - Campus Neiva**

Sistema de monitoreo ambiental para galpones avícolas utilizando sensores ESP32, Raspberry Pi y dashboard web con autenticación institucional.

---

## 📋 Descripción del Proyecto

Este sistema permite monitorear en tiempo real las condiciones ambientales de galpones avícolas mediante:

- **🌡️ Sensores ESP32** que miden temperatura, humedad, iluminación, NH3 y H2S
- **🍓 Raspberry Pi 4B** como servidor local con PostgreSQL
- **📊 Dashboard web** con Streamlit y autenticación @campusucc.edu.co
- **🌐 Acceso público gratuito** mediante túneles HTTPS

---

## 🏗️ Arquitectura del Sistema

```
ESP32 Sensores  →  Raspberry Pi 4B  →  Dashboard Web Público
    ↓                    ↓                     ↓
Lectura cada        PostgreSQL          Streamlit + Auth
30 segundos         Base Local          @campusucc.edu.co
```

### 📊 Parámetros Monitoreados:
- **LUX:** Iluminación (10-300 lux óptimo)
- **NH3:** Amoniaco (<20 ppm seguro)
- **H2S:** Sulfuro de hidrógeno (<10 ppm buena ventilación)
- **H:** Humedad relativa (50-70% ideal)
- **T:** Temperatura (18-24°C confort animal)

---

## 📁 Estructura del Proyecto

### 🔧 Archivos Principales:
- `streamlit_app.py` - Dashboard original (desarrollo local)
- `main.py` - API FastAPI original (desarrollo local)
- `streamlit_app_raspberry.py` - Dashboard con autenticación UCC
- `main_raspberry.py` - API adaptada para PostgreSQL local
- `min_tabla.py` - Componente de tablas con sparklines
- `styles.css` - Estilos CSS personalizados

### 📚 Documentación:
- `PROMPT_PARA_INNOVASICRASP.md` - **⭐ GUÍA PRINCIPAL DE IMPLEMENTACIÓN**
- `INSTALACION_COMPLETA_RASPBERRY.md` - Manual paso a paso
- `POSTGRESQL_RASPBERRY.md` - Configuración de base de datos
- `ACCESO_PUBLICO_GRATUITO.md` - Opciones de túneles gratuitos
- `ARQUITECTURA_SIMPLIFICADA.md` - Documentación técnica

---

## 🚀 Implementación Rápida

### Para el colaborador **innovasicrasp**:

1. **📖 Lee primero:** `PROMPT_PARA_INNOVASICRASP.md`
2. **⏱️ Tiempo estimado:** 75 minutos
3. **🛠️ Resultado:** Sistema completamente funcional

### Comando de inicio rápido:
```bash
git clone https://github.com/AndresYule1417/Sensores-main.git
cd Sensores-main
# Seguir PROMPT_PARA_INNOVASICRASP.md
```

---

## 🔐 Autenticación y Seguridad

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