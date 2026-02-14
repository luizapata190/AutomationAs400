import os
import jpype
import logging
from .settings import settings

def get_jvm_path() -> str:
    """
    Resuelve la ruta de la JVM (jvm.dll) siguiendo una jerarquía de prioridades.
    Máxima portabilidad para distribución empresarial.
    """
    # 1. Prioridad: Configuración explícita en .env (AS400_JVM_PATH)
    if settings.JVM_PATH and os.path.exists(settings.JVM_PATH):
        logging.info(f"Usando JVM definida en configuración: {settings.JVM_PATH}")
        return settings.JVM_PATH

    # 2. Prioridad: Variable de entorno estándar JAVA_HOME
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        # Rutas comunes dentro del JDK para jvm.dll
        sub_paths = [
            r"bin\server\jvm.dll",
            r"bin\default\jvm.dll",
            r"bin\client\jvm.dll",
            r"jre\bin\server\jvm.dll"
        ]
        for sub in sub_paths:
            path = os.path.join(java_home, sub)
            if os.path.exists(path):
                logging.info(f"JVM localizada vía JAVA_HOME: {path}")
                return path

    # 3. Prioridad: Detección automática de JPype
    try:
        auto_path = jpype.getDefaultJVMPath()
        if auto_path and os.path.exists(auto_path):
            logging.debug(f"Usando detección automática de JPype: {auto_path}")
            return auto_path
    except Exception:
        pass

    # 4. Último Recurso: Búsqueda proactiva en rutas comunes de Windows
    common_bases = [
        r"C:\Program Files\Semeru",
        r"C:\Program Files\Eclipse Foundation",
        r"C:\Program Files\Java",
        r"C:\Program Files\AdoptOpenJDK",
        r"C:\Program Files (x86)\Java"
    ]
    
    logging.warning("Iniciando búsqueda proactiva de JVM en el sistema...")
    for base in common_bases:
        if os.path.exists(base):
            for root, _, files in os.walk(base):
                if "jvm.dll" in files:
                    jvm_path = os.path.join(root, "jvm.dll")
                    logging.info(f"JVM auto-descubierta en: {jvm_path}")
                    return jvm_path

    return None
