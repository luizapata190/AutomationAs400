"""
Ejemplo: Login y ejecutar STRPDM para demostrar que el login funciona
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver
import time

def demo_strpdm():
    print("\n=== DEMO: LOGIN Y STRPDM ===\n")
    
    driver = TelnetScreenDriver()
    
    try:
        # 1. CONECTAR
        print("1. Conectando a PUB400.COM...")
        driver.connect("PUB400.COM", port=23)
        print("   ✅ Conectado\n")
        
        # 2. LOGIN
        print("2. Haciendo login como LUINOSZ...")
        if driver.login("LUINOSZ", "V4l3ritO+", wait_initial=2.0):
            print("   ✅ Login exitoso!\n")
            
            # 3. LEER MENÚ PRINCIPAL
            print("3. Leyendo menú principal de IBM i...")
            time.sleep(1)
            pantalla = driver.get_screen_text()
            
            print("--- MENÚ PRINCIPAL ---")
            print(pantalla)
            print("--- FIN MENÚ ---\n")
            
            # 4. EJECUTAR STRPDM
            print("4. Ejecutando comando STRPDM...")
            driver.send_text("STRPDM")
            driver.send_enter()
            time.sleep(2)
            
            # 5. LEER PANTALLA DE PDM
            print("\n5. Leyendo pantalla de PDM...")
            pantalla_pdm = driver.get_screen_text()
            
            print("--- PANTALLA PDM ---")
            print(pantalla_pdm)
            print("--- FIN PDM ---\n")
            
            if "PDM" in pantalla_pdm or "Programming Development Manager" in pantalla_pdm:
                print("✅ ¡STRPDM ejecutado exitosamente!")
            else:
                print("⚠️ Verificar si PDM está disponible en PUB400")
            
            # 6. SALIR (F3)
            print("\n6. Saliendo con F3...")
            driver.send_function_key(3)
            time.sleep(1)
            
        else:
            print("   ❌ Login falló\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.disconnect()
        print("\nDesconectado.")

if __name__ == "__main__":
    demo_strpdm()
