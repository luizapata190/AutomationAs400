"""
Ejemplo de automatización de mantenimiento AS400 usando Telnet.

Este ejemplo muestra cómo:
1. Conectarse a AS400 vía Telnet
2. Navegar por menús
3. Llenar campos en pantallas de mantenimiento
4. Validar datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver
import time

def ejemplo_mantenimiento():
    """
    Ejemplo de automatización de un mantenimiento.
    """
    print("\n=== EJEMPLO: AUTOMATIZACIÓN DE MANTENIMIENTO ===\n")
    
    driver = TelnetScreenDriver()
    
    try:
        # 1. CONECTAR
        print("1. Conectando a AS400...")
        driver.connect("TU_HOST", port=23)
        print("   ✅ Conectado\n")
        
        # 2. ESPERAR PANTALLA DE LOGIN
        print("2. Esperando pantalla de login...")
        time.sleep(2)
        
        # Leer pantalla inicial
        screen = driver.get_screen_text()
        print("   Pantalla actual:")
        print("   " + screen[:200].replace('\n', '\n   '))
        print()
        
        # 3. ENVIAR USUARIO
        print("3. Enviando usuario...")
        driver.send_text("USUARIO")
        driver.send_enter()
        time.sleep(1)
        
        # 4. ENVIAR PASSWORD
        print("4. Enviando password...")
        driver.send_text("PASSWORD")
        driver.send_enter()
        time.sleep(2)
        
        # 5. NAVEGAR A MENÚ
        print("5. Navegando a menú de mantenimientos...")
        driver.send_text("CALL MILIB/MIMENU")
        driver.send_enter()
        time.sleep(1)
        
        # 6. SELECCIONAR OPCIÓN
        print("6. Seleccionando opción de mantenimiento...")
        driver.send_text("1")  # Opción 1 del menú
        driver.send_enter()
        time.sleep(1)
        
        # 7. LLENAR CAMPOS
        print("7. Llenando campos del mantenimiento...")
        
        # Campo 1: Código
        driver.send_text("12345")
        driver.send_enter()  # Tab al siguiente campo
        
        # Campo 2: Descripción
        driver.send_text("PRODUCTO DE PRUEBA")
        driver.send_enter()
        
        # Campo 3: Precio
        driver.send_text("100.50")
        driver.send_enter()
        
        # 8. GRABAR (F10 por ejemplo)
        print("8. Grabando registro...")
        driver.send_function_key(10)  # F10 = Grabar
        time.sleep(1)
        
        # 9. VERIFICAR MENSAJE
        print("9. Verificando mensaje de confirmación...")
        screen = driver.get_screen_text()
        
        if "grabado" in screen.lower() or "added" in screen.lower():
            print("   ✅ Registro grabado exitosamente")
        else:
            print("   ⚠️ Verificar resultado manualmente")
        
        # 10. SALIR
        print("10. Saliendo del mantenimiento...")
        driver.send_function_key(3)  # F3 = Salir
        time.sleep(1)
        
        print("\n✅ Automatización completada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.disconnect()
        print("\nDesconectado.")


def ejemplo_consulta_simple():
    """
    Ejemplo más simple: solo conectar y leer pantalla.
    """
    print("\n=== EJEMPLO SIMPLE: CONECTAR Y LEER ===\n")
    
    driver = TelnetScreenDriver()
    
    try:
        # Conectar
        print("Conectando...")
        driver.connect("PUB400.COM", port=23)
        print("✅ Conectado\n")
        
        # Esperar un poco
        time.sleep(2)
        
        # Leer pantalla
        print("--- PANTALLA INICIAL ---")
        screen = driver.get_screen_text()
        print(screen)
        print("--- FIN ---\n")
        
        # Enviar algo simple
        print("Enviando texto de prueba...")
        driver.send_text("USUARIO_PRUEBA")
        driver.send_enter()
        time.sleep(1)
        
        # Leer respuesta
        print("\n--- PANTALLA DESPUÉS DE ENTER ---")
        screen = driver.get_screen_text()
        print(screen)
        print("--- FIN ---")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.disconnect()


if __name__ == "__main__":
    print("Selecciona el ejemplo:")
    print("1. Ejemplo completo de mantenimiento (requiere configurar host/credenciales)")
    print("2. Ejemplo simple de conexión y lectura")
    
    opcion = input("\nOpción (1 o 2): ").strip()
    
    if opcion == "1":
        ejemplo_mantenimiento()
    else:
        ejemplo_consulta_simple()
