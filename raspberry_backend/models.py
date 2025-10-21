from sqlalchemy import Column, Integer, Float, String
from database import Base

class Sensor(Base):
    """
    Modelo que coincide con el esquema del Excel generado por Servidor.py
    Columnas: Device, IP, LUX, NH3, HS, H, T, time
    """
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Device = Column(String, nullable=True)            # "ESP8266_IOT"
    IP = Column(String, nullable=True)                # "192.168.0.166"
    LUX = Column(Float, nullable=True)                # Luminosidad en lux
    NH3 = Column(Float, nullable=True)                # Amonio (valor analógico)
    HS = Column(Float, nullable=True)                 # Sulfuro H2S (valor analógico)
    H = Column(Float, nullable=True)                  # Humedad (valor analógico)
    T = Column(Float, nullable=True)                  # Temperatura (valor analógico)
    time = Column(String, nullable=True)              # Hora 'HH:MM:SS'