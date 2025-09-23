# 🔧 SOLUCIÓN PARA ERROR ModuleNotFoundError en Streamlit Cloud

## 🐛 Error Encontrado:
```
ModuleNotFoundError: This app has encountered an error.
File "/mount/src/sensores-main/frontend_dashboard_v3.py", line 12, in <module>
    import plotly.graph_objects as go
```

## ✅ SOLUCIONES APLICADAS:

### 1. **Archivo requirements.txt estándar creado**
- Streamlit Cloud busca `requirements.txt` (no `requirements_frontend.txt`)
- Versiones actualizadas y compatibles con >=

### 2. **Dependencias optimizadas:**
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
requests>=2.31.0
altair>=5.0.0
bcrypt>=4.0.0
```

### 3. **Archivo packages.txt creado**
- Para dependencias del sistema si son necesarias

## 🚀 PASOS PARA ACTUALIZAR EN STREAMLIT CLOUD:

### **Opción A: Trigger nuevo deployment**
1. Hacer cualquier cambio pequeño en el código (ej: agregar comentario)
2. Commit y push a GitHub
3. Streamlit Cloud detectará el cambio y redployará automáticamente

### **Opción B: Redeploy manual**
1. Ir a tu app en Streamlit Cloud
2. Click en "Reboot app" o "Rerun"
3. El deployment usará el nuevo requirements.txt

### **Opción C: Verificar configuración**
En Streamlit Cloud, verificar:
- Python version: 3.9, 3.10, o 3.11
- Requirements file: debe detectar requirements.txt automáticamente

## 🔍 VERIFICACIÓN LOCAL:
✅ Dependencias probadas localmente sin errores

## 📋 SIGUIENTES PASOS:
1. Commit estos cambios
2. Push a GitHub  
3. Streamlit Cloud redeployará automáticamente
4. Verificar que el error se resuelva

Si persiste el error, revisar logs completos en "Manage app" → "Logs" en Streamlit Cloud.