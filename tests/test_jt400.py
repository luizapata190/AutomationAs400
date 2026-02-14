import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.commands import AS400CommandDriver

def test_jt400_connection():
    """Prueba la conexión usando JT400 (sin pantalla, solo comandos)."""
    print("\n=== PRUEBA DE CONEXIÓN JT400 ===")
    
    # DATOS DE CONEXIÓN
    AS400_HOST = "PUB400.COM"
    AS400_USER = "LUINOSZ"
    AS400_PASS = "V4l3ritO+"
    
    # Detectar de entorno si existen
    if "AS400_HOST" in os.environ: AS400_HOST = os.environ["AS400_HOST"]
    if "AS400_USER" in os.environ: AS400_USER = os.environ["AS400_USER"]
    if "AS400_PASS" in os.environ: AS400_PASS = os.environ["AS400_PASS"]

    print(f"Conectando a: {AS400_HOST} como {AS400_USER}")
    
    driver = None
    try:
        # Inicializar driver
        driver = AS400CommandDriver()
        
        # Conectar
        print("Estableciendo conexión...")
        driver.connect(AS400_HOST, AS400_USER, AS400_PASS)
        print("✅ CONEXIÓN EXITOSA!")
        
        # Ejecutar un comando simple
        print("\nEjecutando comando: DSPLIBL")
        result = driver.run_command("DSPLIBL")
        
        if result["success"]:
            print("✅ Comando ejecutado correctamente")
            print("Mensajes:")
            for msg in result["messages"]:
                print(f"  - {msg}")
        else:
            print("⚠️ Comando falló")
            for msg in result["messages"]:
                print(f"  - {msg}")
        
        # Intentar otro comando
        print("\nEjecutando comando: DSPSYSSTS")
        result2 = driver.run_command("DSPSYSSTS")
        print(f"Resultado: {'✅ OK' if result2['success'] else '❌ FALLÓ'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\nDesconectando...")
            driver.disconnect()
            print("Desconectado.")

if __name__ == "__main__":
    test_jt400_connection()
