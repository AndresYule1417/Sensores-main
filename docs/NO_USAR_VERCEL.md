# ⚠️ IMPORTANTE: NO USAR VERCEL PARA ESTE PROYECTO

## 🚨 AVISO CRÍTICO

**ESTE REPOSITORIO (Sensores-main) ES UN PROYECTO PYTHON/STREAMLIT.**

**❌ NO DEBES DEPLOYAR ESTE PROYECTO EN VERCEL.**

---

## 🔍 ¿Tienes un error de Vercel?

Si ves un error como este:

```
npm error ERESOLVE could not resolve
npm error While resolving: react-day-picker@8.10.1
npm error Found: react@19.1.1
```

**Probablemente estás intentando deployar el PROYECTO EQUIVOCADO.**

---

## 📊 DIFERENCIA ENTRE TUS PROYECTOS

| Característica | Sensores-main | Mujer-Rural |
|---------------|---------------|-------------|
| **Tipo** | Python/Streamlit | React/Node.js |
| **Lenguaje** | Python | JavaScript |
| **Framework** | Streamlit | React + Create React App |
| **Archivo Principal** | `frontend_dashboard_v3.py` | `package.json` |
| **Plataforma Correcta** | Streamlit Cloud ✅ | Vercel ✅ |
| **¿Tiene package.json?** | ❌ NO | ✅ SÍ |
| **¿Tiene requirements.txt?** | ✅ SÍ | ❌ NO |

---

## ✅ GUÍA RÁPIDA: ¿QUÉ PROYECTO ESTÁS DEPLOYANDO?

### 🔎 Paso 1: Identifica tu proyecto

Ejecuta este comando en tu repositorio:

```bash
ls -la | grep -E "package.json|requirements.txt"
```

**Resultado:**
- Si ves `package.json` → Es un proyecto React/Node.js → Usa Vercel
- Si ves `requirements.txt` → Es un proyecto Python → Usa Streamlit Cloud

### 🔎 Paso 2: Verifica la URL del repositorio

En el error de Vercel, busca la línea:

```
Cloning github.com/AndresYule1417/XXXXXXX
```

- Si dice **`Mujer-Rural`** → Error de React, ver solución abajo
- Si dice **`Sensores-main`** → ¡Proyecto equivocado! Usa Streamlit Cloud

---

## 🛠️ SOLUCIÓN AL ERROR DE VERCEL (Para Mujer-Rural)

### El problema:

Tu proyecto **Mujer-Rural** usa React 19, pero `react-day-picker@8.10.1` solo soporta React 16-18.

### La solución:

**1. Actualizar react-day-picker:**

```bash
# En el proyecto Mujer-Rural (NO Sensores-main):
cd /ruta/a/Mujer-Rural
npm install react-day-picker@latest
```

**2. Commit y push:**

```bash
git add package.json package-lock.json
git commit -m "Fix: Update react-day-picker for React 19 compatibility"
git push origin main
```

**3. Vercel redesplegará automáticamente** y el error desaparecerá.

### Solución alternativa:

Si react-day-picker v9 tiene cambios de API incompatibles:

```bash
npm install react@^18.3.1 react-dom@^18.3.1
```

---

## 🚀 CÓMO DEPLOYAR ESTE PROYECTO (Sensores-main)

### ✅ Opción 1: Streamlit Cloud (RECOMENDADO)

1. **Ir a:** https://streamlit.io/cloud
2. **Conectar con GitHub**
3. **Seleccionar repositorio:** `AndresYule1417/Sensores-main`
4. **Archivo principal:** `frontend_dashboard_v3.py`
5. **Python version:** 3.11
6. **Click "Deploy"**

### 📝 Variables de entorno en Streamlit Cloud:

```
API_BASE_URL = http://192.168.20.33:8000
DEMO_MODE = false
```

---

## ❌ POR QUÉ VERCEL NO FUNCIONA PARA STREAMLIT

| Motivo | Explicación |
|--------|-------------|
| **Runtime** | Vercel usa Node.js; Streamlit requiere Python |
| **Serverless** | Vercel es stateless; Streamlit necesita sesiones persistentes |
| **WebSockets** | Streamlit usa WebSockets para actualización en tiempo real |
| **Arquitectura** | Diseños fundamentalmente incompatibles |

**Conclusión:** Vercel está diseñado para aplicaciones JavaScript/React, NO para Streamlit.

---

## 📚 DOCUMENTACIÓN RELEVANTE

- **Para Sensores-main (este repo):** [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)
- **Para error Vercel/React:** [SOLUCION_ERROR_VERCEL_REACT.md](./SOLUCION_ERROR_VERCEL_REACT.md)
- **Para Streamlit Cloud:** [STREAMLIT_CLOUD_FIX.md](../STREAMLIT_CLOUD_FIX.md)

---

## 🆘 ¿TODAVÍA CONFUNDIDO?

### Pregúntate:

1. **¿Qué repositorio estoy deployando?**
   - URL en el error de Vercel

2. **¿Qué tipo de proyecto es?**
   - `package.json` = React/Node.js
   - `requirements.txt` = Python

3. **¿Qué plataforma debo usar?**
   - React/Node.js → Vercel
   - Python/Streamlit → Streamlit Cloud

---

## 📞 AYUDA ADICIONAL

Si necesitas ayuda específica:

1. **Identifica claramente tu proyecto:**
   - ¿Sensores-main o Mujer-Rural?
   
2. **Comparte el error completo**
   - No solo las últimas líneas

3. **Indica qué intentas lograr:**
   - ¿Deployar dashboard de sensores?
   - ¿Deployar aplicación web React?

---

**🎯 RESUMEN:**
- **Sensores-main** → Streamlit Cloud
- **Mujer-Rural** → Vercel (actualizar react-day-picker)
