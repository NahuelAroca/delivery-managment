import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def reset_db():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("Error: DATABASE_URL no encontrado en el .env")
        return
        
    # asyncpg expects postgresql:// not postgresql+psycopg://
    url = url.replace("postgresql+psycopg://", "postgresql://")
        
    print(f"Conectando a la base de datos...")
    try:
        conn = await asyncpg.connect(url)
        
        # Eliminar las tablas problemáticas (CASCADE fuerza el borrado aunque tengan foreign keys)
        queries = [
            "DROP TABLE IF EXISTS alembic_version CASCADE;",
            "DROP TABLE IF EXISTS photos CASCADE;",
            "DROP TABLE IF EXISTS general_expenses CASCADE;",
            "DROP TABLE IF EXISTS fuel_records CASCADE;",
            "DROP TABLE IF EXISTS remitos CASCADE;",
            "DROP TABLE IF EXISTS receipts CASCADE;",
            "DROP TABLE IF EXISTS records CASCADE;",
            "DROP TABLE IF EXISTS loads CASCADE;",
            "DROP TABLE IF EXISTS drivers CASCADE;"
        ]
        
        for q in queries:
            print(f"Ejecutando: {q}")
            await conn.execute(q)
            
        await conn.close()
        print("✅ Base de datos limpiada exitosamente.")
    except Exception as e:
        print(f"❌ Error al conectar o limpiar la DB: {e}")

if __name__ == "__main__":
    asyncio.run(reset_db())
