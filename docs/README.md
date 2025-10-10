# 📚 Documentación del Proyecto Sensores-main

## 📋 Índice de Documentos

### 🚀 Deployment y Configuración

1. **[DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)** ⭐
   - Guía principal para deployar en Streamlit Cloud
   - **IMPORTANTE:** NO usar Vercel para este proyecto

2. **[NO_USAR_VERCEL.md](./NO_USAR_VERCEL.md)** ⚠️
   - Explicación de por qué Vercel NO es compatible
   - Guía para identificar qué proyecto estás deployando

3. **[SOLUCION_ERROR_VERCEL_REACT.md](./SOLUCION_ERROR_VERCEL_REACT.md)** 🔧
   - Solución específica para error de `react-day-picker` en Vercel
   - **NOTA:** Para el proyecto "Mujer-Rural", NO este proyecto

4. **[STREAMLIT_CLOUD_FIX.md](../STREAMLIT_CLOUD_FIX.md)**
   - Solución para errores de ModuleNotFoundError en Streamlit Cloud

---

### 🍓 Raspberry Pi (Backend)

5. **[INSTRUCCIONES_RASPBERRY_PI.md](./INSTRUCCIONES_RASPBERRY_PI.md)**
   - Configuración del backend FastAPI en Raspberry Pi
   - Instalación de dependencias Python

6. **[DEPLOYMENT_COMPLETO.md](./DEPLOYMENT_COMPLETO.md)**
   - Guía completa del deployment del sistema
   - Backend + Frontend integrados

7. **[CHECKLIST_RASPBERRY.md](./CHECKLIST_RASPBERRY.md)**
   - Lista de verificación para configuración Raspberry Pi

8. **[PROMPT_RASPBERRY_PI_UCC.md](./PROMPT_RASPBERRY_PI_UCC.md)**
   - Configuración avanzada para UCC Ibagué

---

### 📡 Hardware IoT

9. **[ADAPTACION_ESP8266_COMPLETA.md](../ADAPTACION_ESP8266_COMPLETA.md)**
   - Detalles técnicos de la adaptación ESP8266/ESP32
   - Configuración de sensores

---

## 🚨 PREGUNTAS FRECUENTES

### ❓ ¿Puedo deployar este proyecto en Vercel?

**❌ NO.** Este es un proyecto Python/Streamlit. Vercel es para React/Node.js.

→ **Usar Streamlit Cloud:** [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)

---

### ❓ Tengo un error de Vercel con `react-day-picker`

**Probablemente estás deployando el proyecto equivocado.**

Este repositorio (Sensores-main) NO tiene código React. Si ves ese error:
1. Verifica qué repositorio estás deployando
2. Lee: [NO_USAR_VERCEL.md](./NO_USAR_VERCEL.md)
3. Si es el proyecto "Mujer-Rural": [SOLUCION_ERROR_VERCEL_REACT.md](./SOLUCION_ERROR_VERCEL_REACT.md)

---

### ❓ ¿Cómo configuro el backend en Raspberry Pi?

**Sigue estos pasos:**
1. [INSTRUCCIONES_RASPBERRY_PI.md](./INSTRUCCIONES_RASPBERRY_PI.md) - Configuración básica
2. [DEPLOYMENT_COMPLETO.md](./DEPLOYMENT_COMPLETO.md) - Deployment completo

---

### ❓ ¿Qué plataforma debo usar para deployment?

| Tipo de Proyecto | Plataforma Correcta |
|------------------|---------------------|
| **Sensores-main** (Python/Streamlit) | ✅ Streamlit Cloud |
| **Mujer-Rural** (React/Node.js) | ✅ Vercel |

---

## 📞 Soporte

- **Universidad:** Cooperativa de Colombia - Campus Ibagué
- **Repositorio:** https://github.com/AndresYule1417/Sensores-main
- **Documentación:** Este directorio `/docs/`

---

## 🎯 Inicio Rápido

### Para deployment del Dashboard:

```bash
# 1. Ir a Streamlit Cloud
https://streamlit.io/cloud

# 2. Conectar con GitHub y seleccionar:
# Repositorio: AndresYule1417/Sensores-main
# Archivo: frontend_dashboard_v3.py
# Python: 3.11

# 3. Variables de entorno:
API_BASE_URL = http://192.168.20.33:8000
DEMO_MODE = false
```

### Para configuración de Raspberry Pi:

```bash
# Seguir guía completa:
docs/INSTRUCCIONES_RASPBERRY_PI.md
```

---

**📖 Toda la documentación está en este directorio `/docs/`**
