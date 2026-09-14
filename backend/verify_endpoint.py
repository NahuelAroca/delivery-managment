import os
import shutil
from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
from app.models import driver, record, remito, fuel_record, general_expense, photo
from app.models.driver import Driver

# 1. Configurar una base de datos en memoria (SQLite) para la prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

# 2. Reemplazar la dependencia de la base de datos en FastAPI
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Preparar los datos de prueba
db = TestingSessionLocal()
db.add(Driver(name="Test Driver"))
db.commit()
test_driver = db.query(Driver).first()
db.close()

client = TestClient(app)

def test_create_remito():
    print(f"--- Iniciando prueba de endpoint POST /records ---")
    
    # Simular una foto subida
    file_content = b"fake image bytes"
    files = [
        ("photos", ("test_image.jpg", file_content, "image/jpeg"))
    ]
    
    # Datos del formulario
    data = {
        "driver_id": test_driver.id,
        "category": "remito",
        "date": "2026-09-14",
        "loading_location": "Deposito Central",
        "destination": "Sucursal Norte",
        "company": "Empresa Ficticia S.A.",
        "remito_number": "REM-12345"
    }

    # Hacemos la peticion POST al endpoint
    response = client.post("/records/", data=data, files=files)
    
    if response.status_code == 200:
        print("✅ Endpoint respondio correctamente (HTTP 200)")
        res_json = response.json()
        print("📄 Respuesta del servidor:", res_json)
        
        # Validar el almacenamiento de la foto
        db = TestingSessionLocal()
        from app.models.photo import Photo
        saved_photo = db.query(Photo).filter(Photo.record_id == res_json["id"]).first()
        if saved_photo:
            print(f"✅ Foto registrada en la DB con el path: {saved_photo.file_path}")
            
            # Verificar en disco
            storage_path = os.path.join(os.getcwd(), "storage", "photos", saved_photo.file_path)
            if os.path.exists(storage_path):
                print(f"✅ Archivo fisico encontrado exitosamente en: {storage_path}")
                # cleanup the test file
                os.remove(storage_path)
            else:
                print(f"❌ El archivo fisico no se encontro en {storage_path}")
        else:
            print("❌ La foto no se registro en la DB")
    else:
        print(f"❌ Error en el endpoint (HTTP {response.status_code})")
        print("Detalle:", response.json())
        
    # Cleanup
    if os.path.exists("./test.db"):
        os.remove("./test.db")

if __name__ == "__main__":
    test_create_remito()
