# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Usa la misma cadena de conexión que tu Streamlit
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:QkqdVQHACSXWDqpWydkHgQhvccLnXGgb@trolley.proxy.rlwy.net:32029/railway")
engine = create_engine(DATABASE_URL)

# Modelo de datos esperado
class SensorData(BaseModel):
    device: str
    lux: int
    nh3: int
    hs: int
    h: int
    t: int
    time: str = None  # Opcional, puedes dejarlo vacío

@app.post("/api/sensores")
async def recibir_datos(data: SensorData):
    # Si no viene 'time', usa la hora actual del servidor
    from datetime import datetime
    time_value = data.time or datetime.utcnow().isoformat()

    query = text("""
        INSERT INTO sensors3 (device, lux, nh3, hs, h, t, time)
        VALUES (:device, :lux, :nh3, :hs, :h, :t, :time)
    """)
    with engine.connect() as conn:
        conn.execute(query, {
            "device": data.device,
            "lux": data.lux,
            "nh3": data.nh3,
            "hs": data.hs,
            "h": data.h,
            "t": data.t,
            "time": time_value
        })
        conn.commit()
    return {"status": "ok", "msg": "Dato guardado correctamente"}

# Endpoint de prueba
@app.get("/")
def root():
    return {"msg": "API de sensores activa"}