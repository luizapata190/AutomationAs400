import pytest
from as400_automation.database import DatabaseDriver
from as400_automation.settings import settings

class TestDatabaseSQL:
    @classmethod
    def setup_class(cls):
        """Conectar a la DB usando el string de conexión del .env"""
        cls.db = DatabaseDriver()
        if not settings.DB_CONN:
            pytest.skip("No se ha configurado AS400_DB_CONN en el archivo .env")
        cls.db.connect(settings.DB_CONN)

    @classmethod
    def teardown_class(cls):
        cls.db.disconnect()

    def test_sql_select_simple(self):
        """Probar una consulta SELECT básica"""
        # Cambiar por una tabla real de tu esquema si es necesario
        sql = "SELECT CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1"
        results = self.db.execute_query(sql)
        assert len(results) > 0
        print(f"\n✅ Resultado SELECT: {results[0]}")

    def test_sql_query_with_params(self):
        """Probar consulta parametrizada (Segura contra Inyección SQL)"""
        sql = "SELECT * FROM SYSIBM.SYSDUMMY1 WHERE IBMREQD = ?"
        results = self.db.execute_query(sql, ('Y',))
        assert len(results) > 0
        print(f"✅ Resultado con parámetros: {results[0]}")

if __name__ == "__main__":
    # Ejecución manual rápida si no se usa pytest
    db = DatabaseDriver()
    try:
        print("Intentando conectar a DB...")
        db.connect(settings.DB_CONN)
        res = db.execute_query("SELECT CURRENT DATE FROM SYSIBM.SYSDUMMY1")
        print(f"Fecha en AS400: {res}")
    finally:
        db.disconnect()
