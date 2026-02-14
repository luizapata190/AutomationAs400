# AS400 Automation Library 🚀 (v2.0.0)

Librería profesional de Python para la automatización de procesos en IBM i (AS400). Combina la potencia de Java (JT400) para llamadas a programas y SQL, con un motor de pantalla Telnet 5250 puro en Python.

## ✨ Características Principales
- **Todo en uno**: Los drivers Java (JT400) vienen integrados en el paquete.
- **Ultra-Rápida**: Motor Telnet con esperas dinámicas (sin `time.sleep` innecesarios).
- **Enterprise Ready**: Soporte para variables de entorno (`.env`) y patrón Page Object.
- **Teclado Completo**: Soporte desde F1 hasta F24.

## 🛠️ Instalación

### Con Poetry (Recomendado)
```bash
poetry add as400-automation
```

### Con Pip
```bash
pip install as400-automation
```

## 🚀 Inicio Rápido

```python
from as400_automation.core import AS400Client

client = AS400Client()
client.connect_screen("TU_HOST")

# Interactuar con la pantalla
client.screen.send_text("USUARIO")
client.screen.send_tab()
client.screen.send_text("PASSWORD")
client.screen.send_enter()

print(client.screen.get_screen_text())
client.disconnect()
```

## 📚 Documentación y Ejemplos
Para guías detalladas sobre patrones avanzados, base de datos y reportes, consulta la [DOCUMENTACION.md](./DOCUMENTACION.md). Encontrarás ejemplos listos para usar en la carpeta `/examples`.

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
