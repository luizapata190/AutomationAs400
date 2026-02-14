class AS400Error(Exception):
    """Excepción base para la librería de automatización AS400."""
    pass

class ConnectionError(AS400Error):
    """Se lanza cuando falla la conexión al AS400."""
    pass

class ScreenError(AS400Error):
    """Se lanza cuando ocurre un error durante la interacción con la pantalla."""
    pass

class DatabaseError(AS400Error):
    """Se lanza cuando falla una operación de base de datos."""
    pass

class ElementNotFoundError(ScreenError):
    """Se lanza cuando no se encuentra un elemento (texto o campo) en la pantalla."""
    pass
