from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import database
import models
import crud

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="🐓 API Galpón Avícola UCC",
    description="API para monitoreo IoT de sensores ESP32",
    version="2.0.0"
)

# Configurar CORS para permitir acceso desde otros PCs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar IPs exactas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para respuestas
class SensorResponse(BaseModel):
    id: int
    tiempo: int
    temperatura: Optional[float]
    humedad: Optional[float]
    luminosidad: Optional[int]
    amonio: Optional[float]
    sulfuro: Optional[float]
    
    # Campos calculados para facilitar el frontend
    @property
    def fecha_legible(self) -> str:
        return datetime.fromtimestamp(self.tiempo).strftime("%Y-%m-%d %H:%M:%S")

class SystemStatus(BaseModel):
    status: str
    total_registros: int
    ultima_lectura: Optional[str]
    conexion_esp32: bool

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
        "version": "2.0.0",
        "documentacion": "http://192.168.20.33:8000/docs"
    }

@app.get("/status", response_model=SystemStatus, tags=["🏠 Sistema"])
async def get_system_status(db: Session = Depends(get_db)):
    """Estado general del sistema y conectividad ESP32"""
    total_registros = db.query(models.Sensor).count()
    ultima_lectura = crud.get_latest_reading(db)
    
    # Verificar si ESP32 está conectado (lectura en últimos 5 minutos)
    lecturas_recientes = crud.get_sensors_last_minutes(db, minutes=5)
    conexion_esp32 = len(lecturas_recientes) > 0
    
    # Convertir timestamp a fecha legible si existe
    fecha_legible = None
    if ultima_lectura:
        fecha_legible = datetime.fromtimestamp(ultima_lectura.tiempo).strftime("%Y-%m-%d %H:%M:%S")
    
    return SystemStatus(
        status="activo",
        total_registros=total_registros,
        ultima_lectura=fecha_legible,
        conexion_esp32=conexion_esp32
    )

@app.get("/sensores/ultimos", response_model=List[SensorResponse], tags=["📊 Sensores"])
async def get_last_sensors(limit: int = 10, db: Session = Depends(get_db)):
    """Obtener los últimos N registros de sensores"""
    if limit > 100:
        raise HTTPException(status_code=400, detail="Límite máximo: 100 registros")
    
    sensores = crud.get_last_sensors(db, limit=limit)
    return sensores

@app.get("/sensores/tiempo-real", response_model=List[SensorResponse], tags=["📊 Sensores"])
async def get_realtime_sensors(minutes: int = 5, db: Session = Depends(get_db)):
    """Obtener sensores de los últimos X minutos (tiempo real)"""
    if minutes > 60:
        raise HTTPException(status_code=400, detail="Máximo 60 minutos")
    
    sensores = crud.get_sensors_last_minutes(db, minutes=minutes)
    return sensores

@app.get("/sensores/historico", response_model=List[SensorResponse], tags=["📊 Sensores"])
async def get_historic_sensors(
    inicio: str,  # Formato: YYYY-MM-DD
    fin: str,     # Formato: YYYY-MM-DD
    db: Session = Depends(get_db)
):
    """Obtener histórico de sensores por rango de fechas"""
    try:
        # Convertir fechas a timestamps UNIX
        inicio_date = datetime.strptime(inicio, "%Y-%m-%d")
        fin_date = datetime.strptime(fin + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        
        inicio_timestamp = int(inicio_date.timestamp())
        fin_timestamp = int(fin_date.timestamp())
        
        sensores = crud.get_sensors_by_date_range(db, inicio_timestamp, fin_timestamp)
        return sensores
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

@app.get("/sensores/alertas", response_model=List[SensorResponse], tags=["🚨 Alertas"])
async def get_sensor_alerts(
    temp_max: float = 35.0,
    humidity_max: float = 80.0,
    nh3_max: float = 25.0,
    h2s_max: float = 10.0,
    db: Session = Depends(get_db)
):
    """Obtener registros que superen umbrales de alerta"""
    sensores = crud.get_sensors_with_alerts(db, temp_max, humidity_max, nh3_max, h2s_max)
    return sensores

@app.get("/sensores/estadisticas", tags=["📈 Estadísticas"])
async def get_sensor_statistics(db: Session = Depends(get_db)):
    """Estadísticas básicas de los sensores"""
    total = db.query(models.Sensor).count()
    if total == 0:
        return {"message": "No hay datos disponibles"}
    
    # Obtener estadísticas básicas
    ultima_lectura = crud.get_latest_reading(db)
    lecturas_hoy = crud.get_sensors_last_minutes(db, minutes=1440)  # 24 horas
    
    return {
        "total_registros": total,
        "registros_hoy": len(lecturas_hoy),
        "ultima_lectura": {
            "tiempo": ultima_lectura.tiempo,
            "fecha": datetime.fromtimestamp(ultima_lectura.tiempo).strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": ultima_lectura.temperatura,
            "humedad": ultima_lectura.humedad,
            "luminosidad": ultima_lectura.luminosidad,
            "amonio": ultima_lectura.amonio,
            "sulfuro": ultima_lectura.sulfuro
        } if ultima_lectura else None
    }

@app.get("/servicios/status", tags=["🔧 Servicios"])  
async def get_services_status():
    """Estado de servicios del sistema (simplificado para Windows)"""
    return {
        "galpon.service": "active",
        "galpon-api.service": "active", 
        "_demo_mode": False,
        "sistema": "windows_local",
        "mensaje": "Servicios simulados para entorno de desarrollo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)