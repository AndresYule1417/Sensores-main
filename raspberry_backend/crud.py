from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timedelta
import models

def get_last_sensors(db: Session, limit: int = 10):
    """Obtener los últimos N registros ordenados por ID descendente"""
    return db.query(models.Sensor).order_by(desc(models.Sensor.id)).limit(limit).all()

def get_sensors_by_date_range(db: Session, inicio_timestamp: int, fin_timestamp: int):
    """Obtener sensores filtrados por rango de fechas (timestamps UNIX)"""
    return db.query(models.Sensor).filter(
        and_(
            models.Sensor.tiempo >= inicio_timestamp,
            models.Sensor.tiempo <= fin_timestamp
        )
    ).order_by(desc(models.Sensor.tiempo)).all()

def get_sensors_with_alerts(db: Session, 
                          temp_max: float = 35.0,
                          humidity_max: float = 80.0,
                          nh3_max: float = 25.0,
                          h2s_max: float = 10.0):
    """Obtener registros que superen los umbrales de alerta"""
    return db.query(models.Sensor).filter(
        (models.Sensor.temperatura > temp_max) |
        (models.Sensor.humedad > humidity_max) |
        (models.Sensor.amonio > nh3_max) |
        (models.Sensor.sulfuro > h2s_max)
    ).order_by(desc(models.Sensor.tiempo)).all()

def get_latest_reading(db: Session):
    """Obtener la lectura más reciente"""
    return db.query(models.Sensor).order_by(desc(models.Sensor.id)).first()

def get_sensors_last_minutes(db: Session, minutes: int = 5):
    """Obtener sensores de los últimos X minutos (para tiempo real)"""
    current_timestamp = int(datetime.now().timestamp())
    threshold_timestamp = current_timestamp - (minutes * 60)
    
    return db.query(models.Sensor).filter(
        models.Sensor.tiempo >= threshold_timestamp
    ).order_by(desc(models.Sensor.tiempo)).all()