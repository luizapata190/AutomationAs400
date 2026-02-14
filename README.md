# AS400 Automation Library

Librería profesional de Python para automatizar interacciones con IBM i (AS400).

## 🚀 Instalación Rápida

```bash
pip install -r requirements.txt
```

## 📖 Uso Básico

### Ejecutar Comandos

```python
from as400_automation.commands import AS400CommandDriver

driver = AS400CommandDriver()
driver.connect("MIHOST", "USUARIO", "PASSWORD")

result = driver.run_command("DSPLIBL")
print(result)

driver.disconnect()
```

### Consultas SQL

```python
from as400_automation.database import DatabaseDriver

db = DatabaseDriver()
db.connect("DRIVER={IBM i Access ODBC Driver};SYSTEM=MIHOST;UID=user;PWD=pass;")

rows = db.execute_query("SELECT * FROM MILIB.MITABLA")
for row in rows:
    print(row)

db.disconnect()
```

## 📚 Documentación

Ver [walkthrough.md](C:\\Users\\lzapataa\\.gemini\\antigravity\\brain\\9b663404-41f2-4358-9b66-0ae3e94a499a\\walkthrough.md) para documentación completa.

## ✅ Estado

- ✅ Comandos AS400 (JT400)
- ✅ Base de Datos (ODBC)
- ✅ Pantallas 5250 (Alta fidelidad con pyte)
- ✅ Evidencia Visual (Capturas PNG)

## 🧪 Pruebas

```bash
python -m pytest tests/test_vtmpbvt0r.py -s -v
```

## 📦 Requisitos

- Python 3.8+
- Java (JRE/JDK)
- JPype1
- pyodbc
- pyte
- Pillow
