from .screen import ScreenDriver
from .database import DatabaseDriver
import logging

class AS400Client:
    """
    Cliente principal para automatización de AS400.
    Combina capacidades de interacción con pantalla (5250) y base de datos (ODBC).
    """

    def __init__(self, jar_lib_dir: str = None):
        """
        Inicializa el cliente AS400.
        
        Args:
            jar_lib_dir (str, optional): Directorio donde se encuentran jt400.jar y tn5250j.jar.
        """
        self.screen = ScreenDriver(lib_dir=jar_lib_dir)
        self.db = DatabaseDriver()
        self._logger = logging.getLogger(__name__)

    def connect_screen(self, host: str, port: int = 23, code_page: str = "37") -> None:
        """
        Conecta a la sesión de pantalla 5250.
        
        Args:
            host (str): Servidor AS400.
            port (int): Puerto (defecto 23).
            code_page (str): Código de página (37=EEUU, 284=ES).
        """
        self._logger.info(f"Conectando a pantalla 5250 en {host}:{port}...")
        self.screen.connect(host, port, code_page)
        self._logger.info("Conexión a pantalla establecida.")

    def connect_db(self, connection_string: str) -> None:
        """
        Conecta a la base de datos DB2.
        
        Args:
            connection_string (str): Cadena de conexión ODBC completa.
        """
        self._logger.info("Conectando a base de datos...")
        self.db.connect(connection_string)
        self._logger.info("Conexión a base de datos establecida.")

    def disconnect(self) -> None:
        """Desconecta ambos servicios (Pantalla y DB)."""
        self.screen.disconnect()
        self.db.disconnect()
        self._logger.info("Servicios desconectados.")

    # --- Delegación de métodos de Pantalla ---

    def read_text(self, row: int, col: int, length: int) -> str:
        """Lee texto de la pantalla en la posición dada."""
        return self.screen.read_text(row, col, length)

    def write_text(self, row: int, col: int, text: str) -> None:
        """Escribe texto en la pantalla."""
        self.screen.write_text(row, col, text)

    def send_keys(self, key_mnemonic: str) -> None:
        """Envía una tecla (ENTER, F1, etc.)."""
        self.screen.send_keys(key_mnemonic)

    def get_screen_dump(self) -> list:
        """Obtiene el contenido completo de la pantalla."""
        return self.screen.get_screen_content()

    # --- Delegación de métodos de Base de Datos ---

    def query(self, sql: str, params: tuple = None) -> list:
        """Ejecuta una consulta SQL y retorna filas."""
        return self.db.execute_query(sql, params)

    def execute(self, sql: str, params: tuple = None) -> int:
        """Ejecuta una sentencia SQL (UPDATE/INSERT) y retorna filas afectadas."""
        return self.db.execute_update(sql, params)
