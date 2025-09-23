#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con datos de prueba
"""

import sys
import os

# Agregar el directorio del backend al path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raspberry_backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy.orm import Session
import database
import models
import random
import time
from datetime import datetime, timedelta

def create_test_data():
    """Crear datos de prueba para el galpón avícola"""
    
    # Crear tablas si no existen
    models.Base.metadata.create_all(bind=database.engine)
    
    # Obtener sesión de base de datos
    db = database.SessionLocal()
    
    try:
        # Limpiar datos existentes
        db.query(models.Sensor).delete()
        db.commit()
        print("🗑️ Datos anteriores eliminados")
        
        # Generar datos para las últimas 24 horas
        now = int(time.time())
        start_time = now - (24 * 60 * 60)  # 24 horas atrás
        
        print("📊 Generando datos de prueba...")
        
        records_created = 0
        for i in range(288):  # Un registro cada 5 minutos por 24 horas
            timestamp = start_time + (i * 5 * 60)  # Cada 5 minutos
            
            # Simular datos realistas de galpón avícola
            base_temp = 22.0
            base_humidity = 65.0
            
            # Variaciones circadianas (día/noche)
            hour = datetime.fromtimestamp(timestamp).hour
            if 6 <= hour <= 18:  # Día
                temp_variation = random.uniform(3, 8)  # Más calor de día
                light_base = 300
            else:  # Noche
                temp_variation = random.uniform(-2, 2)  # Más fresco de noche
                light_base = 10
            
            sensor_data = models.Sensor(
                tiempo=timestamp,
                temperatura=round(base_temp + temp_variation + random.uniform(-1, 1), 1),
                humedad=round(base_humidity + random.uniform(-10, 10), 1),
                luminosidad=max(0, int(light_base + random.uniform(-50, 150))),
                amonio=round(random.uniform(2.0, 15.0), 1),  # NH3 en ppm
                sulfuro=round(random.uniform(0.5, 8.0), 1)   # H2S en ppm
            )
            
            db.add(sensor_data)
            records_created += 1
            
            # Commit cada 50 registros para eficiencia
            if records_created % 50 == 0:
                db.commit()
                print(f"✅ {records_created} registros creados...")
        
        # Commit final
        db.commit()
        print(f"🎉 ¡Completado! {records_created} registros de prueba creados")
        
        # Mostrar últimos registros
        latest = db.query(models.Sensor).order_by(models.Sensor.id.desc()).limit(3).all()
        print("\n📊 Últimos 3 registros:")
        for record in latest:
            dt = datetime.fromtimestamp(record.tiempo)
            print(f"ID {record.id}: {dt.strftime('%Y-%m-%d %H:%M')} - "
                  f"T:{record.temperatura}°C, H:{record.humedad}%, "
                  f"L:{record.luminosidad}lux, NH3:{record.amonio}ppm")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🐓 Iniciando poblado de base de datos para Galpón Avícola")
    print("=" * 50)
    create_test_data()
    print("=" * 50)
    print("✅ Proceso completado. El dashboard ya debería mostrar datos.")