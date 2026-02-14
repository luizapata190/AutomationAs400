import os
from dotenv import load_dotenv

# Cargar variables desde .env si existe
load_dotenv()

class Settings:
    """Gestor centralizado de configuración."""
    
    HOST = os.getenv("AS400_HOST", "PUB400.COM")
    USER = os.getenv("AS400_USER")
    PASS = os.getenv("AS400_PASS")
    
    DB_CONN = os.getenv("AS400_DB_CONN")
    LIB_DIR = os.getenv("AS400_LIB_DIR", "./lib")

settings = Settings()
