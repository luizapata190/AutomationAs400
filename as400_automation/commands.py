import jpype
import jpype.imports
from jpype.types import *
import os
import logging
from .exceptions import ConnectionError, AS400Error

class AS400CommandDriver:
    """
    Driver para ejecutar comandos y llamar programas en AS400 usando JT400.
    Más estable que la emulación de pantalla.
    """

    def __init__(self, jar_path: str = None):
        """
        Inicializa el driver de comandos.
        
        Args:
            jar_path (str, optional): Ruta al jt400.jar
        """
        self._as400 = None
        self._connected = False
        
        # Determinar ruta del JAR
        if not jar_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.jar_path = os.path.join(base_dir, "lib", "jt400.jar")
        else:
            self.jar_path = jar_path

        # Iniciar JVM si no está iniciada
        if not jpype.isJVMStarted():
            if not os.path.exists(self.jar_path):
                raise FileNotFoundError(f"No se encontró jt400.jar en: {self.jar_path}")
            
            # Detectar JVM
            jvm_path = None
            try:
                jvm_path = jpype.getDefaultJVMPath()
            except:
                pass

            if not jvm_path or not os.path.exists(jvm_path):
                common_paths = [
                    r"C:\Program Files\Semeru\jdk-17.0.8.101-openj9\bin\server\jvm.dll",
                    r"C:\Program Files\Semeru\jdk-17.0.8.101-openj9\bin\default\jvm.dll",
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        jvm_path = path
                        break
            
            if jvm_path and os.path.exists(jvm_path):
                jpype.startJVM(jvm_path, classpath=[self.jar_path])
            else:
                jpype.startJVM(classpath=[self.jar_path])

    def connect(self, system: str, user: str, password: str) -> None:
        """
        Conecta al sistema AS400.
        
        Args:
            system (str): IP o hostname del AS400
            user (str): Usuario
            password (str): Contraseña
        """
        try:
            from com.ibm.as400.access import AS400
            
            self._as400 = AS400(system, user, password)
            
            # Validar conexión
            if not self._as400.validateSignon():
                raise ConnectionError("Credenciales inválidas.")
            
            self._connected = True
            logging.info(f"Conectado exitosamente a {system}")
            
        except Exception as e:
            raise ConnectionError(f"Error conectando: {e}")

    def disconnect(self) -> None:
        """Desconecta del sistema."""
        if self._as400:
            self._as400.disconnectAllServices()
            self._connected = False
            logging.info("Desconectado del AS400")

    def run_command(self, command: str) -> dict:
        """
        Ejecuta un comando CL en el AS400.
        
        Args:
            command (str): Comando CL (ej: "DSPLIBL")
        
        Returns:
            dict: {"success": bool, "messages": [str]}
        """
        if not self._connected:
            raise ConnectionError("No hay conexión activa.")
        
        try:
            from com.ibm.as400.access import CommandCall
            
            cmd = CommandCall(self._as400)
            success = cmd.run(command)
            
            # Obtener mensajes
            messages = []
            msg_list = cmd.getMessageList()
            for msg in msg_list:
                messages.append(f"{msg.getID()}: {msg.getText()}")
            
            return {
                "success": success,
                "messages": messages
            }
            
        except Exception as e:
            raise AS400Error(f"Error ejecutando comando: {e}")

    def call_program(self, library: str, program: str, parameters: list = None) -> dict:
        """
        Llama a un programa AS400.
        
        Args:
            library (str): Librería del programa
            program (str): Nombre del programa
            parameters (list, optional): Lista de parámetros como strings
        
        Returns:
            dict: {"success": bool, "output_params": [str]}
        """
        if not self._connected:
            raise ConnectionError("No hay conexión activa.")
        
        try:
            from com.ibm.as400.access import ProgramCall, ProgramParameter, AS400Text
            
            pgm_path = f"/QSYS.LIB/{library}.LIB/{program}.PGM"
            pgm = ProgramCall(self._as400)
            
            # Preparar parámetros si existen
            if parameters:
                param_list = []
                for p in parameters:
                    # Convertir string a bytes AS400
                    text_converter = AS400Text(len(p), self._as400)
                    param_list.append(ProgramParameter(text_converter.toBytes(p)))
                
                success = pgm.run(pgm_path, param_list)
            else:
                success = pgm.run(pgm_path)
            
            # Obtener parámetros de salida
            output_params = []
            if parameters and success:
                for i, param in enumerate(pgm.getParameterList()):
                    output_data = param.getOutputData()
                    if output_data:
                        text_converter = AS400Text(len(output_data), self._as400)
                        output_params.append(text_converter.toObject(output_data))
            
            return {
                "success": success,
                "output_params": output_params
            }
            
        except Exception as e:
            raise AS400Error(f"Error llamando programa: {e}")

    def is_connected(self) -> bool:
        """Verifica si hay conexión activa."""
        return self._connected
