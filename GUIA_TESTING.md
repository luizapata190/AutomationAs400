# Guía de Testing: ¿Por qué usar Pytest con AS400? 🧪

Para automatizar un AS400 de forma profesional, no basta con que el código "funcione"; debe ser **confiable y auditable**. Por eso, aunque tu librería puede usarse en scripts simples, **recomendamos fuertemente usar Pytest**.

---

## 🧐 ¿Qué es Pytest?
Es un "Framework de Testing". Imagínalo como un **Robot Supervisor** que:
1.  Busca tus archivos de prueba automáticamente.
2.  Prepara el entorno (conecta al AS400) antes de empezar.
3.  Limpia todo (desconecta) al terminar, incluso si hubo un error.
4.  Genera reportes técnicos (HTML, XML) para que tu jefe o cliente vea los resultados.

---

## 🚀 Comandos Clave (Los Superpoderes)

Asegúrate de estar en la raíz de la carpeta y usa estos comandos:

### 1. Ejecutar TODO (El escáner total)
```bash
poetry run pytest
```
*Pytest buscará todos los archivos `test_*.py` y ejecutará cada prueba.*

### 2. Ver lo que pasa en vivo
```bash
poetry run pytest -s
```
*`-s`: Muestra los `print()` y mensajes de log en la terminal mientras el test corre.*

### 3. Ejecutar un solo test (Cirugía láser)
```bash
poetry run pytest -k "crear_registro"
```
*`-k`: Solo corre las funciones que contengan esa palabra en el nombre.*

### 4. Generar Reporte Visual
```bash
poetry run pytest --html=resultado.html --self-contained-html
```
*Crea un archivo HTML profesional con tablas y gráficas de éxito/error.*

---
poetry run pytest tests/test_vtmpbvt0r.py -s -v
-v: Te dice QUÉ test está corriendo (el nombre de la función).
-s: Te deja ver LO QUE PASA dentro (tus prints y logs de conexión).

---

## 🎯 ¿Es obligatorio para mi librería?
**No es obligatorio, pero es lo mejor por 3 razones:**

1.  **Aislamiento**: Si tienes 10 pruebas y la #2 falla, Pytest cerrará esa conexión y pasará a la #3 limpiamente. Si usas un script normal, probablemente el error detendrá todo y dejará sesiones "colgadas" en el AS400.
2.  **Reportes de Evidencia**: Nuestra integración con `pytest-html` permite que las fotos de la pantalla aparezcan automáticamente en el reporte técnico.
3.  **Modularidad**: Puedes reutilizar el código de Login (vía *fixtures*) en 100 tests diferentes sin tener que copiar y pegar el código de conexión cada vez.

---

> [!TIP]
> **Tu Configuración Actual**: Ya he configurado tu proyecto con `conftest.py` y `pyproject.toml` para que estos comandos funcionen de inmediato. ¡Pruébalos! 🦁🚀
