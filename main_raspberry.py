# 🚀 main.py - VERSIÓN RASPBERRY PI
# FastAPI Backend para ESP32 + PostgreSQL local

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import logging
import os
from datetime import datetime

# =====================================================================
# CONFIGURACIÓN DE LOGGING
# =====================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================================
# CONFIGURACIÓN DE BASE DE DATOS RASPBERRY PI
# =====================================================================

# Configuración de base de datos para Raspberry Pi
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    db_url = DATABASE_URL
else:
    # Configuración local PostgreSQL en Raspberry Pi
    db_user = os.getenv("DB_USER", "galpon_user")
    db_password = os.getenv("DB_PASSWORD", "password123")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "galpon_db")
    
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Crear engine de SQLAlchemy
try:
    engine = create_engine(db_url)
    logger.info("✅ Conexión a PostgreSQL establecida correctamente")
except Exception as e:
    logger.error(f"❌ Error al conectar a PostgreSQL: {e}")
    engine = None

# =====================================================================
# MODELO DE DATOS PARA SENSORES
# =====================================================================

class SensorData(BaseModel):
    """Modelo de datos para sensores ESP32"""
    device: str        # ID del dispositivo ESP32
    lux: float         # Iluminación (lux)
    nh3: float         # Amoniaco (ppm)
    hs: float          # Sulfuro de hidrógeno (ppm) 
    h: float           # Humedad (%)
    t: float           # Temperatura (°C)

# =====================================================================
# APLICACIÓN FASTAPI
# =====================================================================

app = FastAPI(
    title="🐔 API Galpón Avícola - Raspberry Pi",
    description="API para recibir datos de sensores ESP32 en sistema avícola",
    version="2.0.0",
    docs_url="/api/docs",  # Swagger en /api/docs
    redoc_url="/api/redoc"
)

# =====================================================================
# ENDPOINTS DE LA API
# =====================================================================

@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "🐔 API Galpón Avícola - Raspberry Pi",
        "version": "2.0.0",
        "status": "✅ Sistema operativo",
        "database": "PostgreSQL Local",
        "university": "Universidad Cooperativa de Colombia",
        "campus": "Neiva",
        "endpoints": {
            "sensor_data": "/api/sensores",
            "health": "/health",
            "docs": "/api/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar estado del sistema"""
    try:
        # Probar conexión a base de datos
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            db_status = "✅ Conectado"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"
    
    return {
        "status": "✅ Sistema operativo",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "system": "Raspberry Pi",
        "api_version": "2.0.0"
    }

@app.post("/api/sensores")
async def recibir_datos(sensor_data: SensorData, request: Request):
    """
    Recibir datos de sensores ESP32 y almacenar en PostgreSQL
    """
    try:
        # Obtener IP del cliente
        client_ip = request.client.host
        if "x-forwarded-for" in request.headers:
            client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()
        
        logger.info(f"📥 Datos recibidos de ESP32: {sensor_data.device} desde IP: {client_ip}")
        
        # Validar que el engine existe
        if not engine:
            raise HTTPException(status_code=500, detail="Error de conexión a base de datos")
        
        # Insertar datos en PostgreSQL
        with engine.connect() as conn:
            query = text("""
                INSERT INTO sensors3 (device, lux, nh3, hs, h, t, time, ip)
                VALUES (:device, :lux, :nh3, :hs, :h, :t, NOW(), :ip)
            """)
            
            conn.execute(query, {
                "device": sensor_data.device,
                "lux": sensor_data.lux,
                "nh3": sensor_data.nh3,
                "hs": sensor_data.hs,
                "h": sensor_data.h,
                "t": sensor_data.t,
                "ip": client_ip
            })
            
            conn.commit()
        
        logger.info(f"✅ Datos guardados exitosamente para dispositivo: {sensor_data.device}")
        
        return {
            "status": "✅ Datos recibidos correctamente",
            "device": sensor_data.device,
            "timestamp": datetime.now().isoformat(),
            "ip": client_ip,
            "message": "Datos almacenados en PostgreSQL local"
        }
        
    except Exception as e:
        logger.error(f"❌ Error al procesar datos: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )

# =====================================================================
# ENDPOINTS ADICIONALES PARA MONITOREO
# =====================================================================

@app.get("/api/stats")
async def get_statistics():
    """Obtener estadísticas básicas del sistema"""
    try:
        with engine.connect() as conn:
            # Contar total de registros
            total_records = conn.execute(text("SELECT COUNT(*) FROM sensors3")).scalar()
            
            # Dispositivos únicos
            unique_devices = conn.execute(text("SELECT COUNT(DISTINCT device) FROM sensors3")).scalar()
            
            # Último registro
            last_record = conn.execute(text("""
                SELECT device, time 
                FROM sensors3 
                ORDER BY time DESC 
                LIMIT 1
            """)).fetchone()
            
            return {
                "total_records": total_records,
                "unique_devices": unique_devices,
                "last_record": {
                    "device": last_record[0] if last_record else None,
                    "time": last_record[1].isoformat() if last_record else None
                } if last_record else None,
                "status": "✅ Operativo"
            }
            
    except Exception as e:
        logger.error(f"❌ Error al obtener estadísticas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest/{device_id}")
async def get_latest_reading(device_id: str):
    """Obtener la última lectura de un dispositivo específico"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT * FROM sensors3 
                WHERE device = :device_id 
                ORDER BY time DESC 
                LIMIT 1
            """)
            
            result = conn.execute(query, {"device_id": device_id}).fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron datos para el dispositivo: {device_id}")
            
            return {
                "device": result[1],
                "lux": result[2], 
                "nh3": result[3],
                "hs": result[4],
                "h": result[5],
                "t": result[6],
                "time": result[7].isoformat(),
                "ip": result[8]
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al obtener lectura: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# EVENTO DE INICIO
# =====================================================================

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("🚀 Iniciando API Galpón Avícola - Raspberry Pi")
    logger.info("🏛️ Universidad Cooperativa de Colombia - Campus Neiva")
    
    # Verificar conexión a base de datos
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Conexión a PostgreSQL verificada")
    except Exception as e:
        logger.error(f"❌ Error de conexión a PostgreSQL: {e}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    logger.info("🛑 Cerrando API Galpón Avícola")

# =====================================================================
# CONFIGURACIÓN PARA DESARROLLO
# =====================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("🐔 Iniciando servidor FastAPI para Raspberry Pi...")
    print("🌐 API disponible en: http://localhost:8000")
    print("📚 Documentación en: http://localhost:8000/api/docs")
    print("🏛️ Universidad Cooperativa de Colombia - Campus Neiva")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Escuchar en todas las interfaces para acceso remoto
        port=8000,
        reload=True,     # Recarga automática en desarrollo
        log_level="info"
    )