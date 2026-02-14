from .base_page import BasePage

class LoginPage(BasePage):
    """Abstracción de la pantalla de Sign On del AS400."""
    
    def login(self, user: str, password: str):
        """Realiza el flujo completo de login."""
        self.driver.send_text(user)
        self.driver.send_tab()
        self.driver.send_text(password)
        self.driver.send_enter()
        return self.driver.get_screen_text()

    def is_current(self):
        """Verifica si estamos en la pantalla de Sign On."""
        return "Sign On" in self.driver.get_screen_text()
