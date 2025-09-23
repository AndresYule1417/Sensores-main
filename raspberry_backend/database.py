from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Ruta a la DB SQLite - Compatible con Windows y Linux
if os.name == 'nt':  # Windows
    # Usar la ruta relativa en Windows
    SQLALCHEMY_DATABASE_URL = "sqlite:///../data/galpon_avicultura.db"
else:  # Linux/Raspberry Pi
    SQLALCHEMY_DATABASE_URL = "sqlite:////home/innovasic/galpon/data/galpon.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obtener sesión de base de datos
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()