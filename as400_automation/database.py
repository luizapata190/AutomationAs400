import pyodbc
from typing import List, Dict, Any, Optional
from .exceptions import DatabaseError, ConnectionError

class DatabaseDriver:
    """
    Manejador para conexiones de base de datos DB2 usando ODBC.
    Permite ejecutar consultas y comandos SQL.
    """

    def __init__(self):
        """Inicializa el driver de base de datos."""
        self._conn = None
        self._cursor = None

    def connect(self, connection_string: str) -> None:
        """
        Establece conexión con la base de datos usando un string de conexión ODBC.
        
        Args:
            connection_string (str): Cadena de conexión completa ODBC.
                                     Ej: "DRIVER={IBM i Access ODBC Driver};SYSTEM=..."
        
        Raises:
            ConnectionError: Si la conexión falla.
        """
        try:
            self._conn = pyodbc.connect(connection_string)
            self._cursor = self._conn.cursor()
        except pyodbc.Error as e:
            raise ConnectionError(f"Fallo al conectar a la base de datos: {e}")

    def disconnect(self) -> None:
        """Cierra la conexión y libera recursos."""
        if self._cursor:
            try:
                self._cursor.close()
            except Exception:
                pass
            self._cursor = None
            
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def execute_query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SQL de selección (SELECT) y retorna los resultados.
        
        Args:
            sql (str): Sentencia SQL a ejecutar.
            params (tuple, optional): Parámetros para la consulta parametrizada.

        Returns:
            List[Dict[str, Any]]: Lista de filas, donde cada fila es un diccionario {columna: valor}.

        Raises:
            DatabaseError: Si hay un error en la ejecución.
        """
        if not self._conn or not self._cursor:
            raise ConnectionError("No hay conexión activa a la base de datos.")

        try:
            if params:
                self._cursor.execute(sql, params)
            else:
                self._cursor.execute(sql)
            
            # Obtener nombres de columnas
            if self._cursor.description:
                columns = [column[0] for column in self._cursor.description]
                results = []
                for row in self._cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            return []
            
        except pyodbc.Error as e:
            raise DatabaseError(f"Error ejecutando consulta SQL: {e}")

    def execute_update(self, sql: str, params: tuple = None) -> int:
        """
        Ejecuta una sentencia de actualización (INSERT, UPDATE, DELETE).
        
        Args:
            sql (str): Sentencia SQL a ejecutar.
            params (tuple, optional): Parámetros para la sentencia.

        Returns:
            int: Número de filas afectadas.

        Raises:
            DatabaseError: Si hay un error en la ejecución.
        """
        if not self._conn or not self._cursor:
            raise ConnectionError("No hay conexión activa a la base de datos.")

        try:
            if params:
                self._cursor.execute(sql, params)
            else:
                self._cursor.execute(sql)
            
            self._conn.commit()
            return self._cursor.rowcount
        except pyodbc.Error as e:
            try:
                self._conn.rollback()
            except:
                pass
            raise DatabaseError(f"Error ejecutando actualización SQL: {e}")
