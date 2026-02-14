from ..telnet_screen import TelnetScreenDriver

class BasePage:
    """Clase base de la cual heredarán todas las pantallas del AS400."""
    def __init__(self, driver: TelnetScreenDriver):
        self.driver = driver

    def wait_for_ready(self, text: str, timeout: float = 5.0):
        """Espera a que la pantalla sea reconocida por un texto específico."""
        return self.driver.wait_for_text(text, timeout=timeout)
