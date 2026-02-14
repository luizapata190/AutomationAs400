import os
import sys
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver

def test_telnet_screen():
    """Prueba la automatización de pantallas usando Telnet."""
    print("\n=== PRUEBA DE AUTOMATIZACIÓN DE PANTALLAS (TELNET) ===")
    
    # DATOS DE CONEXIÓN
    AS400_HOST = "PUB400.COM"
    AS400_USER = "LUINOSZ"
    AS400_PASS = "V4l3ritO+"
    
    driver = None
    try:
        # Crear driver
        driver = TelnetScreenDriver()
        
        # Conectar
        print(f"Conectando a {AS400_HOST} vía Telnet...")
        driver.connect(AS400_HOST, port=23)
        print("✅ Conexión Telnet establecida")
        
        # Login
        print(f"\nIniciando sesión como {AS400_USER}...")
        if driver.login(AS400_USER, AS400_PASS):
            print("✅ Login exitoso!")
            
            # Esperar un momento
            time.sleep(2)
            
            # Leer pantalla actual
            print("\n--- PANTALLA ACTUAL ---")
            screen = driver.get_screen_text()
            print(screen[:500])  # Mostrar primeros 500 caracteres
            print("--- FIN PANTALLA ---")
            
            # Ejemplo: Navegar a un menú
            print("\nEjemplo: Enviando comando...")
            driver.send_text("CALL QCMD")
            driver.send_enter()
            time.sleep(1)
            
            screen = driver.get_screen_text()
            print("\n--- PANTALLA DESPUÉS DE COMANDO ---")
            print(screen[:500])
            print("--- FIN ---")
            
        else:
            print("❌ Login falló - Credenciales incorrectas")
        
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
    test_telnet_screen()
