import os
import time
from as400_automation.core import AS400Client
from as400_automation.settings import settings
from as400_automation.pages.login_page import LoginPage
from as400_automation.reporting import AS400Reporter

def run_v2_demo():
    print("🚀 Iniciando Demo Versión 2.0 (Enterprise Ready)")
    
    # 1. Configurar Reporte
    reporter = AS400Reporter(evidence_dir="evidence_v2")
    
    # 2. Iniciar Cliente (Ya usa TelnetScreenDriver por defecto)
    client = AS400Client()
    
    try:
        # 3. Conectar usando settings (.env)
        print(f"📡 Conectando a {settings.HOST}...")
        client.connect_screen(settings.HOST)
        
        # 4. Usar Patrón Page Object
        login_page = LoginPage(client.screen)
        
        if login_page.is_current():
            print("✅ Pantalla de Sign On detectada.")
            
            # Realizar login (Los TABs y ENTER son dinámicos ahora)
            print("🔐 Realizando login automático...")
            # Usamos credenciales de settings o hardcodeadas para la demo si no hay .env
            user = settings.USER or "DEBUG_USER"
            passw = settings.PASS or "DEBUG_PASS"
            
            login_page.login(user, passw)
            
            # Guardar evidencia
            client.screen.save_screenshot("evidence_v2", "01_after_login.png")
            reporter.add_result("Login Enterprise", "PASS", ["01_after_login.png"])
            
            print("✨ Demo completada exitosamente.")
        else:
            print("❌ No se detectó la pantalla de Sign On.")
            reporter.add_result("Login Enterprise", "FAIL")

    except Exception as e:
        print(f"💥 Error en la demo: {e}")
        reporter.add_result("Demo V2", "ERROR")
    finally:
        client.disconnect()
        reporter.generate_console_report()

if __name__ == "__main__":
    run_v2_demo()
