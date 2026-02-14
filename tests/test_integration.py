import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Añadir directorio raíz al path para importar la librería
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.core import AS400Client
from as400_automation.exceptions import ConnectionError

def test_screen_connection():
    """Prueba la conexión a la pantalla 5250."""
    print("\n--- INICIANDO PRUEBA DE CONEXIÓN DE PANTALLA ---")
    
    # DATOS DE CONEXIÓN (Modificar estos datos o usar variables de entorno)
    AS400_HOST = "PUB400.COM" # Host público de ejemplo, cambiar por el real
    AS400_USER = "LUINOSZ"     # Cambiar
    AS400_PASS = "V4l3ritO+"     # Cambiar
    
    # Intentar detectar credenciales de entorno si existen
    if "AS400_HOST" in os.environ: AS400_HOST = os.environ["AS400_HOST"]
    if "AS400_USER" in os.environ: AS400_USER = os.environ["AS400_USER"]
    if "AS400_PASS" in os.environ: AS400_PASS = os.environ["AS400_PASS"]

    print(f"Intentando conectar a: {AS400_HOST} con usuario {AS400_USER}")
    
    client = None
    try:
        # Inicializar cliente (busca JARs automáticamente en lib/)
        client = AS400Client()
        
        # Conectar
        try:
            client.connect_screen(AS400_HOST)
            print("✅ Conexión establecida EXITOSAMENTE.")
        except Exception as e:
             print(f"❌ Error al conectar: {e}")
             return

        # Leer pantalla (Prueba de lectura)
        try:
            print("Leyendo contenido de la pantalla...")
            lines = client.get_screen_dump()
            print("\n--- VISTA PREVIA DE PANTALLA ---")
            for line in lines[:10]: # Mostrar solo primeras 10 líneas
                print(line)
            print("--------------------------------")
        except Exception as e:
            print(f"⚠️ Advertencia leyendo pantalla: {e}")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        if client:
            print("Desconectando...")
            client.disconnect()
            print("Desconectado.")

if __name__ == "__main__":
    # Asegúrate de configurar tus variables de entorno o editar el script antes de ejecutar
    # set AS400_HOST=tuhost
    # set AS400_USER=tuusuario
    # set AS400_PASS=tupassword
    test_screen_connection()
