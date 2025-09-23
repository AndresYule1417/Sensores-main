#!/usr/bin/env python3
"""
🚀 Script de deployment para Streamlit Cloud
Prepara el repositorio para deployment en múltiples plataformas
"""

import os
import json
import subprocess
import sys

def check_requirements():
    """Verificar que requirements.txt esté actualizado"""
    print("📦 Verificando requirements...")
    
    # Verificar que existe requirements_frontend.txt
    if not os.path.exists("requirements_frontend.txt"):
        print("❌ No se encontró requirements_frontend.txt")
        return False
        
    print("✅ requirements_frontend.txt encontrado")
    return True

def create_streamlit_config():
    """Crear configuración de Streamlit"""
    print("⚙️ Configurando Streamlit...")
    
    os.makedirs(".streamlit", exist_ok=True)
    
    config_content = """[global]
developmentMode = false

[server]
port = 8521
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Configuración de Streamlit creada")

def verify_main_file():
    """Verificar que el archivo principal esté correcto"""
    print("🔍 Verificando archivo principal...")
    
    if not os.path.exists("frontend_dashboard_v3.py"):
        print("❌ No se encontró frontend_dashboard_v3.py")
        return False
        
    # Verificar que use variables de entorno
    with open("frontend_dashboard_v3.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    if "os.getenv" not in content:
        print("⚠️  Archivo no configurado para variables de entorno")
        return False
        
    print("✅ Archivo principal verificado")
    return True

def prepare_for_streamlit_cloud():
    """Preparar para Streamlit Cloud"""
    print("\n🌐 PREPARANDO PARA STREAMLIT CLOUD")
    print("=" * 50)
    
    print("\n📋 PASOS PARA STREAMLIT CLOUD:")
    print("1. 🔗 Ir a: https://streamlit.io/cloud")
    print("2. 🔑 Conectar con GitHub")
    print("3. 📂 Seleccionar repo: AndresYule1417/Sensores-main")
    print("4. 📄 Archivo principal: frontend_dashboard_v3.py")
    print("5. 🐍 Python version: 3.11")
    print("6. ⚙️  Variables de entorno:")
    print("   - API_BASE_URL = http://192.168.20.33:8000")
    print("   - DEMO_MODE = false")
    print("7. 🚀 Click 'Deploy'")
    
    print("\n🎯 URL FINAL será algo como:")
    print("https://galpon-avicola-ucc.streamlit.app")

def prepare_for_vercel():
    """Preparar para Vercel"""
    print("\n🔷 PREPARANDO PARA VERCEL")
    print("=" * 50)
    
    print("\n📋 PASOS PARA VERCEL:")
    print("1. 🔗 Ir a: https://vercel.com")
    print("2. 🔑 Conectar con GitHub")
    print("3. 📂 Importar repo: AndresYule1417/Sensores-main")
    print("4. ⚙️  Variables de entorno en Vercel:")
    print("   - API_BASE_URL = http://192.168.20.33:8000")
    print("   - DEMO_MODE = false")
    print("5. 🚀 Deploy")
    
    print("\n⚠️  NOTA: Vercel es más complejo para Streamlit")
    print("Se recomienda usar Streamlit Cloud")

def check_git_status():
    """Verificar estado de Git"""
    print("\n📊 ESTADO DE GIT:")
    
    try:
        # Verificar si hay cambios sin commitear
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️  Hay cambios sin commitear:")
            print(result.stdout)
            print("\n💡 Ejecutar:")
            print("git add .")
            print('git commit -m "Preparar para deployment"')
            print("git push origin main")
        else:
            print("✅ Repositorio actualizado")
            
    except FileNotFoundError:
        print("❌ Git no está instalado o no es un repositorio Git")

def main():
    """Función principal"""
    print("🚀 PREPARACIÓN PARA DEPLOYMENT")
    print("=" * 50)
    
    # Verificaciones
    if not check_requirements():
        sys.exit(1)
    
    if not verify_main_file():
        sys.exit(1)
    
    # Configuraciones
    create_streamlit_config()
    
    # Mostrar opciones
    prepare_for_streamlit_cloud()
    prepare_for_vercel()
    
    # Estado de Git
    check_git_status()
    
    print("\n🎉 ¡PREPARACIÓN COMPLETADA!")
    print("📖 Lee DEPLOYMENT_GUIDE.md para más detalles")
    print("🔧 Lee BACKEND_CLOUD_SOLUTIONS.md para el backend")

if __name__ == "__main__":
    main()