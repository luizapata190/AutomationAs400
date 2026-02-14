"""
Prueba simple de login mejorada
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver
import time

def prueba_login_simple():
    print("\n=== PRUEBA DE LOGIN MEJORADA ===\n")
    
    driver = TelnetScreenDriver()
    
    try:
        # Conectar
        print("1. Conectando a PUB400.COM...")
        driver.connect("PUB400.COM", port=23)
        print("   ✅ Conectado\n")
        
        # Hacer login
        print("2. Intentando login...")
        resultado = driver.login("LUINOSZ", "V4l3ritO+", wait_initial=2.0)
        
        if resultado:
            print("   ✅ LOGIN EXITOSO!\n")
        else:
            print("   ❌ Login falló\n")
        
        # Leer pantalla después de login
        print("3. Leyendo pantalla después de login...")
        time.sleep(1)
        pantalla = driver.get_screen_text()
        
        print("--- PANTALLA COMPLETA ---")
        print(pantalla)
        print("--- FIN ---\n")
        
        # Verificar si estamos en el menú principal
        if "MAIN MENU" in pantalla or "IBM i" in pantalla or "PUB400" in pantalla:
            print("✅ Parece que el login funcionó correctamente")
        else:
            print("⚠️ No se detectó el menú principal")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.disconnect()
        print("\nDesconectado.")

if __name__ == "__main__":
    prueba_login_simple()
