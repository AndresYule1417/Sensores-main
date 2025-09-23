from sqlalchemy import Column, Integer, Float
from database import Base

class Sensor(Base):
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True)
    tiempo = Column(Integer, nullable=False)          # timestamp UNIX
    temperatura = Column(Float, nullable=True)        # grados Celsius
    humedad = Column(Float, nullable=True)            # porcentaje %
    luminosidad = Column(Integer, nullable=True)      # nivel de luz en lux
    amonio = Column(Float, nullable=True)             # concentración NH3 en ppm
    sulfuro = Column(Float, nullable=True)            # concentración H₂S en ppm