"""
Ejemplo: Consultas SQL a DB2 usando ODBC.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.database import DatabaseDriver
from as400_automation.settings import settings

def main():
    print("\n--- EJEMPLO: CONSULTAS SQL (DB2/ODBC) ---\n")
    
    if not settings.DB_CONN:
        print("❌ Error: Define AS400_DB_CONN en tu archivo .env")
        return

    db = DatabaseDriver()
    
    try:
        print(f"1. Conectando a base de datos en {settings.HOST}...")
        db.connect(settings.DB_CONN)
        print("   ✅ Conexión establecida\n")
        
        # Consulta de ejemplo
        print("2. Consultando tabla de clientes (QIWS.QCUSTCDT)...")
        query = "SELECT CUSNUM, LSTNAM, CITY FROM QIWS.QCUSTCDT FETCH FIRST 5 ROWS ONLY"
        rows = db.execute_query(query)
        
        print(f"   ✅ Se recuperaron {len(rows)} registros:")
        for row in rows:
            print(f"      - ID: {row['CUSNUM']} | Nombre: {row['LSTNAM']} | Ciudad: {row['CITY']}")

    except Exception as e:
        print(f"❌ Error SQL: {e}")
        print("\nNota: Asegúrate de tener instalado el 'IBM i Access ODBC Driver'.")
    finally:
        db.disconnect()
        print("\nDesconectado de la base de datos.")

if __name__ == "__main__":
    main()
