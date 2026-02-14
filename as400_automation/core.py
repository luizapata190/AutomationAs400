from .telnet_screen import TelnetScreenDriver
from .database import DatabaseDriver
import logging

class AS400Client:
    """
    Cliente principal para automatización de AS400.
    Combina capacidades de interacción con pantalla (5250) y base de datos (ODBC).
    Utiliza el motor de Telnet (Pure Python) por defecto para máxima velocidad.
    """

    def __init__(self):
        """ Inicializa el cliente AS400. """
        self.screen = TelnetScreenDriver()
        self.db = DatabaseDriver()
        self._logger = logging.getLogger(__name__)

    def connect_screen(self, host: str, port: int = 23) -> None:
        """
        Conecta a la sesión de pantalla 5250 vía Telnet.
        """
        self._logger.info(f"Conectando a pantalla 5250 en {host}:{port}...")
        self.screen.connect(host, port)
        self._logger.info("Conexión a pantalla establecida.")

    def connect_db(self, connection_string: str) -> None:
        """
        Conecta a la base de datos DB2.
        """
        self._logger.info("Conectando a base de datos...")
        self.db.connect(connection_string)
        self._logger.info("Conexión a base de datos establecida.")

    def disconnect(self) -> None:
        """Desconecta ambos servicios (Pantalla y DB)."""
        self.screen.disconnect()
        self.db.disconnect()
        self._logger.info("Servicios desconectados.")

    # --- Delegación de métodos de Pantalla (Estrategia Proactiva V2) ---

    def read_text(self, row: int, col: int, length: int = None) -> str:
        """Lee texto de la pantalla en la posición dada (1-based)."""
        return self.screen.get_text_at(row, col, length)

    def write_text(self, text: str) -> None:
        """Escribe texto en la pantalla en la posición actual del cursor."""
        self.screen.send_text(text)

    def send_keys(self, key: str) -> None:
        """
        Envía una tecla especial.
        Soporta: ENTER, TAB, F1-F12.
        """
        key = key.upper()
        if key == "ENTER":
            self.screen.send_enter()
        elif key == "TAB":
            self.screen.send_tab()
        elif key.startswith("F") and key[1:].isdigit():
            self.screen.send_function_key(int(key[1:]))
        else:
            self.screen.send_text(key)

    def get_screen_text(self) -> str:
        """Obtiene el texto completo de la pantalla."""
        return self.screen.get_screen_text()

    # --- Delegación de métodos de Base de Datos ---

    def query(self, sql: str, params: tuple = None) -> list:
        """Ejecuta una consulta SQL y retorna filas."""
        return self.db.execute_query(sql, params)

    def execute(self, sql: str, params: tuple = None) -> int:
        """Ejecuta una sentencia SQL (UPDATE/INSERT) y retorna filas afectadas."""
        return self.db.execute_update(sql, params)
