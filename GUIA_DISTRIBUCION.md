# Guía Maestra de Distribución: AS400 Automation 📦

Esta guía explica las tres formas de compartir tu librería, desde el trabajo en equipo hasta el lanzamiento mundial.

---

## 🏗️ 1. Colaboración en Equipo (Modo Desarrollo)
**Escenario**: Quieres que un compañero de tu mismo equipo trabaje contigo en el código de la librería.

1.  **Compartir**: Envía la carpeta completa del proyecto (asegúrate de incluir `pyproject.toml` y `poetry.lock`).
2.  **Instalar**: Tu compañero debe tener Poetry instalado y ejecutar en la terminal:
    ```bash
    poetry install
    ```
3.  **Resultado**: Poetry creará un entorno virtual idéntico al tuyo, con las mismas versiones de las librerías, garantizando que "si funciona en tu máquina, funciona en la de él".

---

## 🚀 2. Distribución Profesional (Modo "Wheel")
**Escenario**: Quieres que alguien use tu librería en sus propios programas, pero no quieres que vea o toque tu código fuente.

1.  **Generar el Paquete**: Ejecuta en la raíz de tu proyecto:
    ```bash
    poetry build
    ```
2.  **Compartir**: Ve a la carpeta `dist/` y toma el archivo que termina en `.whl` (ej: `as400_automation-2.0.0-py3-none-any.whl`).
3.  **Instalar**: Tu compañero solo necesita ese archivo. Lo instala en su proyecto con:
    ```bash
    pip install as400_automation-2.0.0-py3-none-any.whl
    ```
    *Nota: Como es Versión 2.0.0, los archivos Java (JARs) ya van integrados dentro de ese archivo. ¡Es magia!*

---

## 🌎 3. Lanzamiento a la Comunidad (Modo PyPI)
**Escenario**: Has terminado tus pruebas, la librería es perfecta y quieres que cualquier programador del mundo la instale con un simple `pip install`.

1.  **Preparar**: Regístrate en [PyPI.org](https://pypi.org/) y obtén un Token de API.
2.  **Configurar**:
    ```bash
    poetry config pypi-token.pypi TU_TOKEN_AQUI
    ```
3.  **Publicar**:
    ```bash
    poetry publish --build
    ```
4.  **Resultado**: ¡Listo! Ahora cualquier persona en el planeta podrá usar tu creación ejecutando:
    ```bash
    pip install as400-automation
    ```

---

> [!IMPORTANT]
> **Recomendación Personal**: Como aún estás haciendo pruebas, utiliza la **Opción 2**. Genera el archivo `.whl`, instálalo en un script de prueba y verifica que todo fluya. Cuando sientas que es "imparable", ¡llévala a la Opción 3! 🚀🦁
