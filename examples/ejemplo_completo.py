"""
EJEMPLO COMPLETO DE USO DE LA LIBRERÍA AS400 AUTOMATION

Este script demuestra cómo usar los 3 módulos principales:
1. Comandos (JT400)
2. Base de Datos (ODBC)
3. Pantallas (Telnet)

INSTRUCCIONES:
1. Cambia las variables de configuración abajo
2. Ejecuta: python examples/ejemplo_completo.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.commands import AS400CommandDriver
from as400_automation.database import DatabaseDriver
from as400_automation.telnet_screen import TelnetScreenDriver
from as400_automation.settings import settings
import time

# Las credenciales ahora se cargan automáticamente desde el archivo .env
AS400_HOST = settings.HOST
AS400_USER = settings.USER
AS400_PASS = settings.PASS
AS400_CONN = settings.DB_CONN


def ejemplo_1_comandos():
    """
    Ejemplo 1: Ejecutar comandos CL en AS400
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: EJECUTAR COMANDOS")
    print("="*60)
    
    try:
        # Crear driver
        driver = AS400CommandDriver()
        
        # Conectar
        print(f"\n1. Conectando a {AS400_HOST}...")
        driver.connect(AS400_HOST, AS400_USER, AS400_PASS)
        print("   ✅ Conectado exitosamente")
        
        # Ejecutar comando simple
        print("\n2. Ejecutando comando DSPLIBL...")
        resultado = driver.run_command("DSPLIBL")
        
        if resultado["success"]:
            print("   ✅ Comando ejecutado correctamente")
            if resultado["messages"]:
                print("   Mensajes:")
                for msg in resultado["messages"][:3]:  # Primeros 3
                    print(f"     - {msg}")
        else:
            print("   ❌ Error en comando")
            for msg in resultado["messages"]:
                print(f"     - {msg}")
        
        # Ejecutar otro comando
        print("\n3. Ejecutando comando DSPSYSSTS...")
        resultado = driver.run_command("DSPSYSSTS")
        print(f"   Resultado: {'✅ OK' if resultado['success'] else '❌ ERROR'}")
        
        # Desconectar
        print("\n4. Desconectando...")
        driver.disconnect()
        print("   ✅ Desconectado")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def ejemplo_2_base_datos():
    """
    Ejemplo 2: Consultas SQL a la base de datos
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: CONSULTAS SQL")
    print("="*60)
    
    try:
        # Crear driver
        db = DatabaseDriver()
        
        # String de conexión (Prioriza el del .env si existe)
        conn_str = AS400_CONN if AS400_CONN else (
            "DRIVER={IBM i Access ODBC Driver};"
            f"SYSTEM={AS400_HOST};"
            f"UID={AS400_USER};"
            f"PWD={AS400_PASS};"
        )
        
        # Conectar
        print(f"\n1. Conectando a base de datos en {AS400_HOST}...")
        db.connect(conn_str)
        print("   ✅ Conectado a BD")
        
        # Consultar tabla de ejemplo (existe en todos los AS400)
        print("\n2. Consultando tabla QIWS.QCUSTCDT...")
        rows = db.execute_query(
            "SELECT CUSNUM, LSTNAM, INIT, CDTLMT FROM QIWS.QCUSTCDT",
            params=None
        )
        
        print(f"   ✅ Se encontraron {len(rows)} registros")
        print("\n   Primeros 3 registros:")
        for i, row in enumerate(rows[:3], 1):
            print(f"     {i}. Cliente: {row.get('CUSNUM', 'N/A')} - {row.get('LSTNAM', 'N/A')}")
        
        # Desconectar
        print("\n3. Desconectando...")
        db.disconnect()
        print("   ✅ Desconectado de BD")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n⚠️ NOTA: Este ejemplo requiere el driver ODBC de IBM i instalado")
        import traceback
        traceback.print_exc()


def ejemplo_3_pantallas():
    """
    Ejemplo 3: Automatizar pantallas con Telnet
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: AUTOMATIZAR PANTALLAS")
    print("="*60)
    
    try:
        # Crear driver
        driver = TelnetScreenDriver()
        
        # Conectar
        print(f"\n1. Conectando vía Telnet a {AS400_HOST}...")
        driver.connect(AS400_HOST, port=23)
        print("   ✅ Conexión Telnet establecida")
        
        # Hacer login usando el método que ya funciona
        print(f"\n2. Realizando login como {AS400_USER}...")
        if driver.login(AS400_USER, AS400_PASS, wait_initial=2.0):
            print("   ✅ Login exitoso!")
            
            # Leer pantalla después de login
            print("\n3. Leyendo pantalla del menú principal...")
            time.sleep(1)
            pantalla = driver.get_screen_text()
            
            print(f"   ✅ Pantalla recibida ({len(pantalla)} caracteres)")
            print("\n   --- PRIMEROS 400 CARACTERES DEL MENÚ ---")
            print("   " + pantalla[:400].replace('\n', '\n   '))
            print("   --- FIN ---")
            
        else:
            print("   ❌ Login falló - verificar credenciales")
        
        # Desconectar
        print("\n4. Desconectando...")
        driver.disconnect()
        print("   ✅ Desconectado")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def menu_principal():
    """
    Menú para seleccionar qué ejemplo ejecutar
    """
    print("\n" + "="*60)
    print("EJEMPLOS DE USO - AS400 AUTOMATION LIBRARY")
    print("="*60)
    print(f"\nConfiguración actual:")
    print(f"  Host: {AS400_HOST}")
    print(f"  Usuario: {AS400_USER}")
    print(f"  Password: {'*' * len(AS400_PASS)}")
    
    print("\n⚠️ IMPORTANTE: Cambia las credenciales en la línea 23-25 del script")
    
    print("\nSelecciona el ejemplo a ejecutar:")
    print("  1. Ejecutar Comandos (JT400)")
    print("  2. Consultas SQL (ODBC)")
    print("  3. Automatizar Pantallas (Telnet)")
    print("  4. Ejecutar TODOS los ejemplos")
    print("  0. Salir")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == "1":
        ejemplo_1_comandos()
    elif opcion == "2":
        ejemplo_2_base_datos()
    elif opcion == "3":
        ejemplo_3_pantallas()
    elif opcion == "4":
        ejemplo_1_comandos()
        ejemplo_2_base_datos()
        ejemplo_3_pantallas()
        print("\n" + "="*60)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*60)
    elif opcion == "0":
        print("\n¡Hasta luego!")
    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    menu_principal()
