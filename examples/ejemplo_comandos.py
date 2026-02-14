"""
Ejemplo: Ejecutar comandos CL en AS400 usando JT400.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.commands import AS400CommandDriver
from as400_automation.settings import settings

def main():
    print("\n--- EJEMPLO: EJECUCIÓN DE COMANDOS (JT400) ---\n")
    
    # Validar configuración
    if not settings.USER or not settings.PASS:
        print("❌ Error: Configura AS400_USER y AS400_PASS en el archivo .env")
        return

    driver = AS400CommandDriver()
    
    try:
        print(f"1. Conectando a {settings.HOST}...")
        driver.connect(settings.HOST, settings.USER, settings.PASS)
        print("   ✅ Conectado exitosamente\n")
        
        # Ejemplo 1: Ver lista de librerías
        print("2. Ejecutando comando DSPLIBL...")
        res = driver.run_command("DSPLIBL")
        if res["success"]:
            print("   ✅ Comando ejecutado. Mensajes:")
            for msg in res["messages"][:5]:
                print(f"      - {msg}")
        
        # Ejemplo 2: Ver estado del sistema
        print("\n3. Ejecutando comando DSPSYSSTS...")
        res = driver.run_command("DSPSYSSTS")
        print(f"   Resultado: {'✅ OK' if res['success'] else '❌ FALLÓ'}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.disconnect()
        print("\nDesconectado.")

if __name__ == "__main__":
    main()
