from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import database
import models

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="🐓 API Galpón Avícola UCC",
    description="API para monitoreo IoT de sensores ESP8266 - Compatible con Servidor.py",
    version="3.0.0"
)

# Configurar CORS para permitir acceso desde otros PCs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar IPs exactas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para respuestas (coincide con esquema de Servidor.py)
class SensorResponse(BaseModel):
    id: int
    Device: Optional[str]       # "ESP8266_IOT"
    IP: Optional[str]           # "192.168.0.166"
    LUX: Optional[float]        # Luminosidad
    NH3: Optional[float]        # Amonio (valor analógico)
    HS: Optional[float]         # Sulfuro H2S (valor analógico)
    H: Optional[float]          # Humedad (valor analógico)
    T: Optional[float]          # Temperatura (valor analógico)
    time: Optional[str]         # Hora 'HH:MM:SS'
    
    class Config:
        from_attributes = True

class SystemStatus(BaseModel):
    status: str
    total_registros: int
    ultima_lectura: Optional[str]
    conexion_esp8266: bool

# Dependency para obtener sesión DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["🏠 Sistema"])
async def root():
    """Endpoint raíz - verificar que la API funciona"""
    return {
        "message": "🐓 API Galpón Avícola UCC - Sistema Activo",
        "version": "3.0.0",
        "esquema": "Compatible con Servidor.py (Device, IP, LUX, NH3, HS, H, T, time)",
        "documentacion": "http://192.168.0.180:8000/docs"
    }

@app.get("/status", response_model=SystemStatus, tags=["🏠 Sistema"])
async def get_system_status(db: Session = Depends(get_db)):
    """Estado general del sistema y conectividad ESP8266"""
    total_registros = db.query(models.Sensor).count()
    
    # Obtener última lectura
    ultima_lectura = db.query(models.Sensor).order_by(models.Sensor.id.desc()).first()
    
    # Determinar si hay conexión reciente (últimos 5 registros)
    lecturas_recientes = db.query(models.Sensor).order_by(models.Sensor.id.desc()).limit(5).all()
    conexion_esp8266 = len(lecturas_recientes) > 0
    
    # Formatear última lectura
    fecha_legible = None
    if ultima_lectura and ultima_lectura.time:
        fecha_legible = ultima_lectura.time
    
    return SystemStatus(
        status="activo",
        total_registros=total_registros,
        ultima_lectura=fecha_legible,
        conexion_esp8266=conexion_esp8266
    )

@app.get("/sensores/ultimos", response_model=List[SensorResponse], tags=["📊 Sensores"])
async def get_last_sensors(limit: int = 10, db: Session = Depends(get_db)):
    """Obtener los últimos N registros de sensores"""
    if limit > 100:
        raise HTTPException(status_code=400, detail="Límite máximo: 100 registros")
    
    sensores = db.query(models.Sensor).order_by(models.Sensor.id.desc()).limit(limit).all()
    return sensores

@app.get("/sensores/tiempo-real", response_model=List[SensorResponse], tags=["📊 Sensores"])
async def get_realtime_sensors(limit: int = 50, db: Session = Depends(get_db)):
    """Obtener sensores más recientes (tiempo real)"""
    if limit > 200:
        raise HTTPException(status_code=400, detail="Máximo 200 registros")
    
    sensores = db.query(models.Sensor).order_by(models.Sensor.id.desc()).limit(limit).all()
    return sensores

@app.get("/sensores/estadisticas", tags=[" Estadísticas"])
async def get_sensor_statistics(db: Session = Depends(get_db)):
    """Estadísticas básicas de los sensores"""
    total = db.query(models.Sensor).count()
    if total == 0:
        return {"message": "No hay datos disponibles"}
    
    # Obtener última lectura
    ultima_lectura = db.query(models.Sensor).order_by(models.Sensor.id.desc()).first()
    
    # Contar registros (últimos 100 como muestra)
    lecturas_recientes = db.query(models.Sensor).order_by(models.Sensor.id.desc()).limit(100).all()
    
    return {
        "total_registros": total,
        "registros_recientes": len(lecturas_recientes),
        "ultima_lectura": {
            "id": ultima_lectura.id,
            "time": ultima_lectura.time,
            "Device": ultima_lectura.Device,
            "IP": ultima_lectura.IP,
            "LUX": ultima_lectura.LUX,
            "NH3": ultima_lectura.NH3,
            "HS": ultima_lectura.HS,
            "H": ultima_lectura.H,
            "T": ultima_lectura.T
        } if ultima_lectura else None
    }

@app.get("/servicios/status", tags=["🔧 Servicios"])  
async def get_services_status():
    """Estado de servicios del sistema"""
    return {
        "servidor_tcp": "active (puerto 8889)",
        "api_rest": "active (puerto 8000)", 
        "sistema": "raspberry_pi",
        "mensaje": "Sistema compatible con Servidor.py de Ivan Camilo Leiton"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)