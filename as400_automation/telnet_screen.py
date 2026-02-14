import socket
import time
import os
import pyte
from .exceptions import ConnectionError, ScreenError
from .renderer import AS400Renderer

class TelnetScreenDriver:
    """
    Driver para interactuar con pantallas AS400 vía Telnet.
    Usa pyte para emulación de terminal 24x80 y reconstrucción de cuadrícula.
    """
    
    def __init__(self, encoding: str = 'latin-1'):
        self._host = None
        self._port = None
        self._socket = None
        self._connected = False
        self._encoding = encoding
        self._buffer = b"" 
        self._renderer = AS400Renderer()
        
        # Emulador de terminal profesional (24 filas x 80 columnas)
        self._screen = pyte.Screen(80, 24)
        self._stream = pyte.Stream(self._screen)

    def connect(self, host: str, port: int = 23, timeout: int = 10) -> None:
        """Establece la conexión Telnet."""
        self._host = host
        self._port = port
        try:
            self._socket = socket.create_connection((host, port), timeout=timeout)
            self._connected = True
            print(f"✅ Conectado a {host}:{port}")
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar a {host}:{port}: {e}")

    def _read_available(self, timeout: float = 0.5) -> bytes:
        """Lee datos del socket y los procesa a través del emulador pyte."""
        if not self._socket: return b""
        self._socket.settimeout(timeout)
        raw_data = b""
        try:
            while True:
                chunk = self._socket.recv(4096)
                if not chunk: break
                raw_data += chunk
                self._socket.settimeout(0.1) 
        except (socket.timeout, ConnectionAbortedError):
            pass
        except Exception:
            pass
        
        if not raw_data:
            return b""

        # 1. Filtrar protocolos Telnet (IAC)
        clean_data = b""
        i = 0
        while i < len(raw_data):
            if raw_data[i] == 255: # IAC
                if i + 1 < len(raw_data):
                    cmd = raw_data[i+1]
                    if cmd == 250: # SB
                        se_idx = raw_data.find(b"\xff\xf0", i)
                        i = (se_idx + 2) if se_idx != -1 else len(raw_data)
                    elif cmd in (251, 252, 253, 254): i += 3
                    else: i += 2
                else: i += 1
            else:
                clean_data += bytes([raw_data[i]])
                i += 1
        
        if clean_data:
            self._buffer += clean_data
            # 2. Alimentar el emulador
            try:
                # pyte espera texto decodificado
                text = clean_data.decode(self._encoding, errors='ignore')
                self._stream.feed(text)
            except Exception as e:
                print(f"   [WARNING] Error alimentando emulador: {e}")
        
        return clean_data

    def login(self, user: str, password: str, wait_initial: float = 2.0, evidence_dir: str = None) -> bool:
        """Realiza login procesando banners iniciales."""
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        
        try:
            # 1. Pasar banner inicial (PUB400 requiere ENTER)
            time.sleep(wait_initial)
            self._read_available(timeout=1.0)
            self.send_enter(wait=2.0)
            
            # 2. Verificar Sign On (usando lo que ya tiene el screen)
            screen = self.get_screen_text(clear_buffer=False)
            if "User" not in screen and "Usuario" not in screen and "Sign On" not in screen:
                self.send_enter(wait=2.0)
                screen = self.get_screen_text(clear_buffer=False)

            if evidence_dir:
                self.save_screenshot(evidence_dir, "01_sign_on_screen.png")

            # 3. Enviar credenciales
            self.send_text(user)
            time.sleep(0.5)
            self.send_text("\t") # TAB
            time.sleep(0.5)
            self.send_text(password)
            time.sleep(0.5)
            self.send_enter(wait=3.0)
            
            # 4. Verificar éxito
            screen = self.get_screen_text(clear_buffer=False)
            if any(term in screen.lower() for term in ["not valid", "not correct", "cpf1296", "incorrecto"]):
                if evidence_dir: self.save_screenshot(evidence_dir, "error_login.png")
                return False
            
            return True
        except Exception as e:
            raise ConnectionError(f"Error en login: {e}")

    def disconnect(self) -> None:
        """Cierra la conexión Telnet."""
        if self._socket:
            try: self._socket.close()
            except: pass
        self._connected = False
        print("✅ Desconectado")

    def send_text(self, text: str) -> None:
        """Envía texto al AS400."""
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        self._socket.sendall(text.encode(self._encoding))

    def wait_for_silence(self, timeout: float = 3.0, silence_threshold: float = 0.3) -> bool:
        """
        Espera dinámicamente a que el socket deje de recibir datos (pantalla estable).
        
        Args:
            timeout (float): Tiempo máximo total de espera.
            silence_threshold (float): Cuánto tiempo de silencio se considera 'estable'.
            
        Returns:
            bool: True si se alcanzó el silencio, False si hubo timeout.
        """
        if not self._connected: return False
        
        end_time = time.time() + timeout
        last_data_time = time.time()
        
        while time.time() < end_time:
            # Intentar leer datos sin bloquear demasiado
            data = self._read_available(timeout=0.05)
            if data:
                last_data_time = time.time()
            elif (time.time() - last_data_time) > silence_threshold:
                # Se alcanzó el tiempo de silencio requerido
                return True
        return False

    def send_enter(self, wait: float = None) -> None:
        """
        Envía ENTER y espera estabilidad.
        Si se pasa 'wait', se usa ese tiempo fijo (retrocompatibilidad).
        """
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        self._socket.sendall(b"\r\n")
        
        if wait:
            time.sleep(wait)
            self._read_available(timeout=0.1)
        else:
            self.wait_for_silence()

    def send_tab(self, count: int = 1, wait: float = None) -> None:
        """
        Envía una o varias teclas TAB.
        Si se pasa 'wait', se usa ese tiempo fijo.
        """
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        self._socket.sendall(b"\t" * count)
        
        if wait:
            time.sleep(wait)
            self._read_available(timeout=0.1)
        else:
            self.wait_for_silence(timeout=1.0, silence_threshold=0.1)

    def get_screen_text(self, wait_if_empty: float = 0.5, clear_buffer: bool = True) -> str:
        """Retorna el contenido de la pantalla desde el emulador pyte (24x80)."""
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        if wait_if_empty > 0:
            self._read_available(timeout=wait_if_empty)
            
        # El emulador mantiene la cuadrícula en self._screen.display
        text = "\n".join(self._screen.display)
        
        if clear_buffer:
            self._buffer = b""
        return text

    def get_text_at(self, row: int, col: int, length: int = None) -> str:
        """
        Obtiene el texto en una posición específica usando coordenadas naturales (1 a 24, 1 a 80).
        Si length no se especifica o es 0, lee hasta el final de la fila.
        
        Args:
            row (int): Fila (1 a 24).
            col (int): Columna (1 a 80).
            length (int): Cantidad de caracteres a leer (opcional).
        """
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        screen = self._screen.display # Lista de 24 filas
        
        # Ajustar de coordenadas humanas (1-based) a índices de Python (0-based)
        r_idx = row - 1
        c_idx = col - 1
        
        if 0 <= r_idx < 24:
            line = screen[r_idx]
            if not length or length <= 0:
                # Leer hasta el final de la fila (80 columnas)
                return line[c_idx:].strip()
            else:
                return line[c_idx : c_idx + length].strip()
        return ""

    def save_screenshot(self, folder: str, filename: str) -> str:
        """Captura y guarda imagen basada en el emulador."""
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        screen_text = self.get_screen_text(clear_buffer=False)
        return self._renderer.render_to_image(screen_text, path)

    def send_function_key(self, key_number: int) -> None:
        """
        Envía una tecla de función (F1-F24).
        """
        if not self._connected: raise ConnectionError("No hay conexión activa.")
        
        # Secuencias de escape estándar para terminales funcionales
        escape_sequences = {
            1: b"\x1b[11~", 2: b"\x1b[12~", 3: b"\x1b[13~", 
            4: b"\x1b[14~", 5: b"\x1b[15~", 6: b"\x1b[17~",
            7: b"\x1b[18~", 8: b"\x1b[19~", 9: b"\x1b[20~",
            10: b"\x1b[21~", 11: b"\x1b[23~", 12: b"\x1b[24~",
            13: b"\x1b[25~", 14: b"\x1b[26~", 15: b"\x1b[28~",
            16: b"\x1b[29~", 17: b"\x1b[31~", 18: b"\x1b[32~",
            19: b"\x1b[33~", 20: b"\x1b[34~", 21: b"\x1b[35~",
            22: b"\x1b[36~", 23: b"\x1b[37~", 24: b"\x1b[38~",
        }
        
        if key_number in escape_sequences:
            self._socket.sendall(escape_sequences[key_number])
            self.wait_for_silence()
        else:
            from .exceptions import ScreenError
            raise ScreenError(f"Tecla F{key_number} no soportada. Rango válido: 1-24.")

    def wait_for_text(self, text: str, timeout: int = 10) -> bool:
        """Espera hasta que aparezca un texto en el emulador."""
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            screen = self.get_screen_text(wait_if_empty=0.5, clear_buffer=False)
            if text in screen:
                return True
            time.sleep(0.5)
        return False
