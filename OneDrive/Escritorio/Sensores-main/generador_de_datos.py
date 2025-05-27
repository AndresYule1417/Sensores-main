import pandas as pd
from sqlalchemy import create_engine, text
import time
import datetime
import os

# Configuración de conexión a la base de datos existente
engine = create_engine('postgresql+psycopg2://postgres:12345@localhost:5432/backup')
# Set para almacenar los IDs que ya hemos mostrado
shown_ids = set()

print("Monitoreando datos de la tabla sensors3...")
try:
    while True:
        # Consulta para obtener los últimos 10 registros
        query = """
        SELECT * FROM sensors3
        ORDER BY id DESC 
        LIMIT 10;
        """
        
        # Ejecuta la consulta
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            
        # Verifica si hay nuevos datos que no hemos mostrado antes
        new_data = False
        for row in rows:
            if row.id not in shown_ids:
                new_data = True
                data = {
                    "id": row.id,
                    "device": row.device,
                    "ip": row.ip,
                    "lux": row.lux,
                    "nh3": row.nh3,
                    "hs": row.hs,
                    "h": row.h,
                    "t": row.t,
                    "time": row.time
                }
                print(f"Nuevo dato recibido para {row.device}: {data}")
                shown_ids.add(row.id)
        
        # Si no hay nuevos datos, muestra un mensaje de espera
        if not new_data:
            print("Esperando nuevos datos...", end="\r")
        
        # Espera antes de la siguiente consulta
        time.sleep(2)  # Consulta cada 2 segundos
except KeyboardInterrupt:
    print("\nMonitoreo detenido por el usuario")