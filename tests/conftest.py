import pytest
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar el resultado de los tests y adjuntar capturas de pantalla al reporte HTML.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call':
        # Buscar el driver en el test para tomar captura si falló
        driver = None
        if hasattr(item.funcargs.get('self', None), 'driver'):
            driver = item.funcargs['self'].driver
        
        # Si el test falló y tenemos driver, adjuntamos captura
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            if driver:
                evidence_dir = "evidence_v2"
                os.makedirs(evidence_dir, exist_ok=True)
                file_name = f"fail_{item.name}_{datetime.now().strftime('%H%M%S')}.png"
                img_path = driver.save_screenshot(evidence_dir, file_name)
                
                if img_path:
                    # Enlace relativo para el reporte HTML
                    rel_path = os.path.join("evidence_v2", file_name)
                    extra.append(pytest_html.extras.image(rel_path))
        
        report.extra = extra
