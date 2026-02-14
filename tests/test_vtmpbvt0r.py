import pytest
import time
import os
import sys

# Añadir el directorio raíz al path para poder importar as400_automation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from as400_automation.telnet_screen import TelnetScreenDriver
from as400_automation.reporting import AS400Reporter

# Configuración de PUB400.COM
HOST = "PUB400.COM"
USER = "LUINOSZ"
PASS = "V4l3ritO+"

class TestVTMPBVT0R:
    @classmethod
    def setup_class(cls):
        """Inicializar reporter una vez para toda la clase"""
        evidence_dir = os.path.join(os.path.dirname(__file__), "evidence")
        cls.reporter = AS400Reporter(evidence_dir=evidence_dir)

    def setup_method(self, method):
        """Configuración antes de cada test"""
        test_name = method.__name__
        print("\n" + "="*60)
        print(f"SETUP: Conectando al AS400 para {test_name}")
        print("="*60)
        
        self.driver = TelnetScreenDriver()
        self.driver.connect(HOST)
        self.curr_evidence = []
        
        if not self.driver.login(USER, PASS, evidence_dir=self.reporter.evidence_dir):
            print("❌ Login falló")
            pytest.fail("No se pudo iniciar sesión")
        
        ev_file = "01_sign_on_screen.png"
        self.curr_evidence.append(ev_file)
        ev_file2 = "02_login_success.png"
        self.driver.save_screenshot(self.reporter.evidence_dir, ev_file2)
        self.curr_evidence.append(ev_file2)

    def teardown_method(self, method):
        """Limpieza después de cada test"""
        print("\nTEARDOWN: Cerrando conexión")
        try:
            self.driver.send_function_key(3) # Salir
        except:
            pass
        self.driver.disconnect()
        print("✅ Desconectado")

    def ir_al_mantenimiento(self, test_name="test"):
        """Navegación robusta al programa con evidencias"""
        print(f"\n→ Navegando al mantenimiento ({test_name})...")
        self.driver.send_text("CALL LUINOSZ1/VTMPBVT0R")
        self.driver.send_enter(wait=2.0)
        
        for intento in range(5):
            pantalla = self.driver.get_screen_text(wait_if_empty=2.0, clear_buffer=False)
            pantalla_upper = pantalla.upper()
            
            if "NO SE ENCONTRARON REGISTROS" in pantalla_upper:
                print(f"   ⚠️ Popup detectado: 'No se encontraron registros'")
                ev_file = f"{test_name}_03_popup_no_regs.png"
                self.driver.save_screenshot(self.reporter.evidence_dir, ev_file)
                self.curr_evidence.append(ev_file)
                self.driver.get_screen_text(clear_buffer=True)
                self.driver.send_enter(wait=2.0)
                continue
                
            if "VTMPBVT0R" in pantalla_upper or "MANTENIMIENTO" in pantalla_upper:
                print(f"✅ Pantalla cargada en intento {intento+1}")
                ev_file = f"{test_name}_04_main_screen.png"
                self.driver.save_screenshot(self.reporter.evidence_dir, ev_file)
                self.curr_evidence.append(ev_file)
                self.driver.get_screen_text(clear_buffer=True)
                return True
            
            time.sleep(1)
            
        print("❌ No se pudo cargar la pantalla")
        ev_file = f"{test_name}_error_load.png"
        self.driver.save_screenshot(self.reporter.evidence_dir, ev_file)
        self.curr_evidence.append(ev_file)
        return False

    def test_1_verificar_sin_registros(self):
        """Caso 1: Verificar el flujo inicial sin registros"""
        name = "Test 1: Sin Registros"
        print(f"\n{name}")
        status = "PASS" if self.ir_al_mantenimiento("test1") else "FAIL"
        self.reporter.add_result(name, status, self.curr_evidence)

    def test_2_crear_registro(self):
        """Caso 2: Simulación de creación (F6)"""
        name = "Test 2: Crear Registro"
        print(f"\n{name}")
        if self.ir_al_mantenimiento("test2"):
            print("→ Presionando F6 (Nuevo)...")
            self.driver.send_function_key(6)
            time.sleep(2)
            ev_file = "test2_05_create_screen.png"
            self.driver.save_screenshot(self.reporter.evidence_dir, ev_file)
            self.curr_evidence.append(ev_file)
            print("✅ Pantalla de creación capturada")
            self.reporter.add_result(name, "PASS", self.curr_evidence)
        else:
            self.reporter.add_result(name, "FAIL", self.curr_evidence)

    def test_3_editar_registro(self):
        """Caso 3: Simulación de edición (Opción 2)"""
        name = "Test 3: Editar Registro"
        print(f"\n{name}")
        if self.ir_al_mantenimiento("test3"):
            print("→ Escribiendo '2' en el primer registro...")
            self.driver.send_text("2")
            self.driver.send_enter(wait=2)
            ev_file = "test3_05_edit_screen.png"
            self.driver.save_screenshot(self.reporter.evidence_dir, ev_file)
            self.curr_evidence.append(ev_file)
            print("✅ Acción de edición capturada")
            self.reporter.add_result(name, "PASS", self.curr_evidence)
        else:
            self.reporter.add_result(name, "FAIL", self.curr_evidence)

    @classmethod
    def teardown_class(cls):
        """Mostrar reporte profesional usando el módulo reutilizable"""
        cls.reporter.generate_console_report()
        cls.reporter.save_summary_file()
        html_path = cls.reporter.generate_html_report("reporte_mantenimiento_v2.html")
        print(f"✨ Reporte visual generado en: {html_path}")
