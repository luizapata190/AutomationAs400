import jpype
import jpype.imports
from jpype.types import *
import time
import os
import logging
from .exceptions import ConnectionError, ScreenError, ElementNotFoundError
from . import keys

# Constantes de dimensiones por defecto
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24

class ScreenDriver:
    """
    Controlador para interactuar con pantallas AS400 5250 usando la librería Tn5250J vía JPype.
    Requiere 'tn5250j.jar' y 'jt400.jar' en la carpeta 'lib'.
    """

    def __init__(self, lib_dir: str = None):
        """
        Inicializa el driver de pantalla.
        
        Args:
            lib_dir (str, optional): Directorio donde están los JARs.
        """
        self._connected = False
        self._session = None
        self._screen = None
        self._start_jvm(lib_dir)

    def _start_jvm(self, lib_dir):
        """Inicia la JVM con los JARS necesarios en el classpath."""
        if jpype.isJVMStarted():
            return

        if not lib_dir:
            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            lib_dir = os.path.join(pkg_dir, "lib")

        # Buscar JAR de tn5250j dinámicamente
        tn5250_jar = None
        if os.path.exists(lib_dir):
            for file in os.listdir(lib_dir):
                if file.startswith("tn5250j") and file.endswith(".jar") and "installer" not in file:
                    tn5250_jar = os.path.join(lib_dir, file)
                    break
        
        if not tn5250_jar:
            tn5250_jar = os.path.join(lib_dir, "tn5250j.jar")

        # Lista de Jars
        jars = [
            os.path.join(lib_dir, "jt400.jar"),
            tn5250_jar
        ]
        
        # Validar existencia
        classpath = []
        for jar in jars:
            if os.path.exists(jar):
                classpath.append(jar)
            else:
                logging.warning(f"No se encontró el JAR: {jar}. Algunas funciones pueden fallar.")

        if not classpath:
            raise FileNotFoundError("No se encontraron los archivos .jar necesarios en la carpeta 'lib'.")

        logging.info(f"Iniciando JVM con Classpath: {classpath}")

        # Intentar detectar jvm.dll si no está en PATH


        # Intentar detectar jvm.dll si no está en PATH
        jvm_path = None
        try:
            jvm_path = jpype.getDefaultJVMPath()
        except:
            pass

        if not jvm_path or not os.path.exists(jvm_path):
            # Rutas comunes encontradas en el sistema del usuario
            common_paths = [
                r"C:\Program Files\Semeru\jdk-17.0.8.101-openj9\bin\server\jvm.dll",
                r"C:\Program Files\Semeru\jdk-17.0.8.101-openj9\bin\default\jvm.dll",
                r"C:\Program Files\Java\jdk-11\bin\server\jvm.dll",
                r"C:\Program Files\Eclipse Adoptium\jdk-17.0.8.101-hotspot\bin\server\jvm.dll"
            ]
            for path in common_paths:
                if os.path.exists(path):
                    jvm_path = path
                    logging.info(f"JVM encontrada en: {jvm_path}")
                    break
        
        if jvm_path and os.path.exists(jvm_path):
            jpype.startJVM(jvm_path, classpath=classpath)
        else:
            # Dejar que JPype intente encontrarla o falle
            jpype.startJVM(classpath=classpath)

    def connect(self, host: str, port: int = 23, code_page: str = "37") -> None:
        """
        Conecta a la sesión 5250.
        
        Args:
            host (str): Hostname o IP.
            port (int): Puerto Telnet (defecto 23).
            code_page (str): Código de página (defecto 37 para US/Estandar, 284 para ES).
        """
        try:
            # Importar clases de Tn5250J dinámicamente
            from org.tn5250j import Session5250, SessionConfig
            from java.util import Properties
            
            props = Properties()
            props.put("host", host)
            props.put("port", str(port))
            props.put("codepage", code_page)
            
            # Crear configuración de sesión (Requerido por beta2)
            # El constructor es SessionConfig(String, String) - Probablemente nombre y archivo
            config = SessionConfig("default", "default")

            # Asegurar que la configuración tenga las propiedades correctas
            # Si no se setean aqui, Session5250 podría ignorar las 'props' pasadas al constructor
            # y usar defaults (localhost)
            config.setProperty("host", host)
            config.setProperty("port", str(port))
            config.setProperty("codepage", code_page)
            
            # Algunos flags adicionales útiles para automatización
            config.setProperty("sslType", "none") 

            # Crear sesión
            # La versión beta2 de tn5250j requiere 4 argumentos: (Properties, String site, String view, SessionConfig config)
            self._session = Session5250(props, None, None, config)
            
            # Conectar
            self._session.connect()
            
            # Esperar a que la conexión se establezca
            timeout = 10
            start_time = time.time()
            while not self._session.isConnected() and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                
            if not self._session.isConnected():
                raise ConnectionError("No se pudo establecer conexión con el host (Timeout).")
                
            self._screen = self._session.getScreen()
            self._connected = True
            
        except Exception as e:
            # Capturar errores de importación si falta el jar
            if "org.tn5250j" in str(e) or "ModuleNotFoundError" in str(type(e).__name__) or "java.lang.NoClassDefFoundError" in str(e):
                logging.error(f"Error detallado de importación: {e}") 
                raise ImportError(f"Error cargando clases de Tn5250J. Verifique dependencias. Detalle: {e}")
            raise ConnectionError(f"Error conectando: {e}")

    def disconnect(self) -> None:
        """Desconecta la sesión."""
        if self._session and self._session.isConnected():
            self._session.disconnect()
        self._connected = False
        self._session = None
        self._screen = None

    def read_text(self, row: int, col: int, length: int) -> str:
        """
        Lee texto de la pantalla.
        
        Args:
            row (int): Fila (1-based).
            col (int): Columna (1-based).
            length (int): Cantidad de caracteres a leer.
        """
        if not self._connected or not self._screen:
            raise ConnectionError("No hay conexión activa.")
            
        # Tn5250J suele usar 0-based internamente, pero verifiquemos.
        # Asumiremos conversion de 1-based (API usuario) a 0-based.
        text_chars = self._screen.getString(row - 1, col - 1, length)
        return str(text_chars)

    def write_text(self, row: int, col: int, text: str) -> None:
        """
        Escribe texto en la pantalla en una posición específica.
        
        Args:
            row (int): Fila.
            col (int): Columna.
            text (str): Texto a escribir.
        """
        if not self._connected or not self._screen:
            raise ConnectionError("No hay conexión activa.")

        # Mover cursor y escribir
        self._screen.setCursor(row - 1, col - 1)
        self._screen.sendKeys(text)

    def send_keys(self, key_mnemonic: str) -> None:
        """
        Envía una tecla de control (Ej: ENTER, PF1).
        
        Args:
            key_mnemonic (str): Constante de teclas (ver keys.py).
        """
        if not self._connected or not self._screen:
            raise ConnectionError("No hay conexión activa.")

        # Mapeo simple a los mnemonicos que entienda tn5250j sendKeys
        # Tn5250J suele aceptar "[enter]", "[pf1]", etc.
        cmd = f"[{key_mnemonic.lower()}]"
        self._screen.sendKeys(cmd)
        
        # Esperar desbloqueo de teclado (AID wait)
        time.sleep(0.5) # Pequeña pausa por defecto

    def is_connected(self) -> bool:
        return self._connected and self._session and self._session.isConnected()

    def get_screen_content(self) -> list:
        """Retorna todo el contenido de la pantalla como lista de strings."""
        if not self._connected or not self._screen:
            return []
            
        lines = []
        for r in range(SCREEN_HEIGHT):
            lines.append(self.read_text(r + 1, 1, SCREEN_WIDTH))
        return lines
