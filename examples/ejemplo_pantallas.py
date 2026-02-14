"""
Ejemplo: Automatización de pantallas 5250 vía Telnet.
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver
from as400_automation.settings import settings

def main():
    print("\n--- EJEMPLO: AUTOMATIZACIÓN DE PANTALLAS (TELNET) ---\n")
    
    if not settings.USER or not settings.PASS:
        print("❌ Error: Configura credenciales en el archivo .env")
        return

    driver = TelnetScreenDriver()
    
    try:
        print(f"1. Conectando a {settings.HOST}...")
        driver.connect(settings.HOST)
        
        print(f"2. Iniciando sesión como {settings.USER}...")
        if driver.login(settings.USER, settings.PASS):
            print("   ✅ Login exitoso!\n")
            
            print("3. Capturando pantalla del Menú Principal...")
            time.sleep(1) # Espera técnica para renderizado
            screen_text = driver.get_screen_text()
            
            print("\n--- VISTA PREVIA ---")
            # Mostrar solo primeras 5 líneas
            for line in screen_text.split('\n')[:5]:
                print(f"   {line}")
            print("   ...")
            print("--------------------\n")
            
            # Ejemplo de navegación
            print("4. Enviando comando 'SIGNOFF' para salir...")
            driver.exec_command("SIGNOFF")
            print("   ✅ Comando enviado.")
        else:
            print("   ❌ Error en el proceso de Login.")

    except Exception as e:
        print(f"❌ Error de pantalla: {e}")
    finally:
        driver.disconnect()
        print("\nDesconectado.")

if __name__ == "__main__":
    main()
