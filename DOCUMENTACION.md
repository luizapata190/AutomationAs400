# Manual Técnico: AS400 Automation Library 🚀 (v2.0.0)

Esta librería profesional de Python automatiza procesos en IBM i (AS400). La **Versión 2.0** introduce una arquitectura de nivel empresarial enfocada en velocidad, seguridad y mantenibilidad.

## 🏗️ Novedades de la Versión 2.0
- **Empaquetado Profesional**: Migración completa a **Poetry**.
- **Driver Unificado**: El `AS400Client` ahora utiliza `TelnetScreenDriver` (Pure Python) por defecto, eliminando la dependencia de Java para la pantalla.
- **Esperas Dinámicas**: Implementación de `wait_for_silence()` que elimina los `time.sleep()` fijos, haciendo la automatización 3x más rápida.
- **Seguridad**: Soporte nativo para variables de entorno mediante `.env` y `settings.py`.
- **Mantenibilidad**: Introducción del patrón **Page Object**.

## 🛠️ Instalación y Requisitos

### Con Poetry (Recomendado V2)
Si tienes Poetry instalado, simplemente corre:
```bash
poetry install
```

### Con Pip tradicional
```bash
pip install .
```

- **Requisitos**: Python 3.11+, Java (solo para el módulo `commands`), Driver ODBC (para `database`).

## 🔐 Configuración de Seguridad
No guardes contraseñas en el código. Crea un archivo `.env` basado en el `.env.example`:
```ini
AS400_HOST=PUB400.COM
AS400_USER=MI_USUARIO
AS400_PASS=MI_PASSWORD
```

## 🚀 Guía de Implementación Enterprise (Page Object)

Para un proyecto profesional, utiliza la estructura de **Pages**:

```python
from as400_automation.core import AS400Client
from as400_automation.pages.login_page import LoginPage
from as400_automation.settings import settings

client = AS400Client()
client.connect_screen(settings.HOST)

# Usar Page Object para abstraer la pantalla
login = LoginPage(client.screen)
login.login(settings.USER, settings.PASS)
```

## � Patrones de Automatización Comunes

Aquí te mostramos cómo resolver las tareas más frecuentes al automatizar programas:

### 1. Enviar Teclas de Función (F6, F12, etc.)
Para presionar teclas especiales, usa el método `send_function_key`:
```python
# Presionar F6 para 'Crear Nuevo'
driver.send_function_key(6)

# Presionar F12 para 'Cancelar/Regresar'
driver.send_function_key(12)
```

### 2. Ingreso de Datos y Navegación
Para escribir datos y moverte entre campos de entrada:
```python
# Escribir código de cliente
driver.send_text("12345")

# Moverse al siguiente campo (TAB)
driver.send_text("\t")

# Escribir nombre
driver.send_text("JUAN PEREZ")

# Confirmar acción (ENTER)
driver.send_enter(wait=2.0)
```

### 3. Validaciones de Pantalla
Es vital verificar que el programa está donde esperas antes de actuar:
```python
# Obtener el texto de la pantalla para validar
pantalla = driver.get_screen_text().upper()

# Validación simple
if "MANTENIMIENTO DE CLIENTES" in pantalla:
    print("✅ Ubicación correcta")
else:
    print("❌ Pantalla inesperada")

# Espera inteligente (Wait for Text)
if driver.wait_for_text("Registro Guardado", timeout=5):
    print("✅ Operación exitosa")
```

### 4. Llenado de Campos Específicos
Si no sabes cómo llegar a un campo, la estrategia más robusta en AS400 es usar el **Tabulador**.

**Técnica Home + TABs:**
1. Al cargar una pantalla, el cursor suele estar en el primer campo.
2. Usa `driver.send_tab(n)` para saltar `n` campos hasta el que necesitas.

```python
# Si quieres llenar el tercer campo de la pantalla:
driver.send_tab(2)  # Salta los primeros 2 campos
driver.send_text("VALOR_CAMPO_3")
driver.send_enter()
```

### 5. Navegación por Nombre (Etiquetas)
En AS400, los campos no tienen "ID" o "Nombre" interno como en la web. La forma profesional de hacerlo es **buscar el texto de la etiqueta** que está al lado del campo:

```python
pantalla = driver.get_screen_text()

# Si buscamos el campo al lado de "Usuario . . . :"
if "Usuario . . . . . :" in pantalla:
    # Sabemos que es el primer campo de entrada
    driver.send_tab(1)
    driver.send_text("MI_USUARIO")
```

### 6. Navegación por Posición (Coordenadas)
Aunque recomendamos usar TABs, a veces necesitas validar que un texto exacto esté en una posición exacta de la pantalla. Para esto hemos creado el método `get_text_at()`.

**Ejemplo:** Si quieres validar si en la **Fila 5, Columna 10** aparece la palabra "Nombre":

```python
# get_text_at(fila, columna, largo)
# Si sabes el largo:
texto = driver.get_text_at(5, 10, 6) 

# SI NO SABES EL LARGO (Lee hasta el final de la fila):
texto_completo = driver.get_text_at(5, 10) 
```

> [!TIP]
> **Mejora sugerida**: Si no envías el parámetro de largo (o envías 0), la librería leerá automáticamente desde la columna que le indiques hasta el final de la fila (columna 80). Esto es ideal para leer mensajes de error o etiquetas cuando no quieres contar letras.

> [!IMPORTANT]
> **Coordenadas Naturales**: Este método usa coordenadas del 1 al 24 y del 1 al 80, tal como las ves en tu emulador AS400. No tienes que preocuparte por restar 1 ni por índices raros de programación.

## 📖 Referencia de Métodos Principales

### TelnetScreenDriver
- `connect(host, port=23)`: Establece conexión.
- `login(user, password, evidence_dir)`: Realiza login automático.
- `send_text(text)`: Escribe texto.
- `send_enter(wait)`: Presiona Enter.
- `send_tab(count, wait)`: Envía uno o varios Tabuladores.
- `send_function_key(number)`: Envía F1 a F12.
- `get_screen_text()`: Retorna el contenido de la pantalla 24x80.
- `save_screenshot(folder, filename)`: Genera imagen PNG.

### AS400Reporter
- `add_result(test_name, status, evidence_list)`: Registra un resultado.
- `generate_console_report()`: Muestra estadísticas en consola.
- `save_summary_file()`: Guarda un archivo de texto con el resumen.

### 7. 🤝 Cómo compartir con tus compañeros y la Comunidad

¡Grandes noticias! En la **Versión 2.0.0**, hemos logrado que la librería sea **totalmente autocontenida**. Esto significa que los archivos Java (JARs) ya viajan dentro del paquete.

#### Opción A: Colaboración en Equipo (Poetry)
Si quieres que otro compañero trabaje en el código contigo:
1. Envía el proyecto completo.
2. Tu compañero solo debe ejecutar: `poetry install`.
3. ¡No tiene que mover carpetas manualmente! Todo se configura solo.

#### Opción B: Uso como Librería (Distribución Pro)
Si quieres que alguien use tu librería en sus propios scripts:
1. **Empaquetar**: Ejecuta `poetry build`.
2. **Entregar**: Solo tienes que pasarle el archivo `.whl` que está en la carpeta `dist/`.
3. **Instalar**: Tu compañero lo instala así:
   ```bash
   pip install as400_automation-2.0.0-py3-none-any.whl
   ```
   *¡Y listo! Ya puede usar `from as400_automation...` y los JARs funcionarán automáticamente porque están integrados.*

#### Opción C: Compartir con la Comunidad (PyPI)
Al ser autocontenida, tu librería está lista para brillar en PyPI. Al subirla, cualquier persona en el mundo podrá descargarla y usarla con un solo `pip install`.

> [!TIP]
> **Experiencia Zero-Setup**: Al integrar los JARs, hemos eliminado el error más común (el "File Not Found" de los binarios Java). ¡Ahora es conectar y listo!

### 📚 Recursos de Aprendizaje e Inicio Rápido

He dejado dos carpetas clave para que tú y tus compañeros empiecen con el pie derecho:

-   **📁 `examples/`**: Contiene plantillas listas para ejecutar. Son el mejor punto de partida para copiar, pegar y adaptar a nuevos programas.
-   **📁 `tests/`**: No solo sirven para verificar que todo funciona, sino que muestran ejemplos de flujos complejos y validaciones avanzadas que puedes imitar.

> [!IMPORTANT]
> **Mi recomendación**: No borres estas carpetas. Al compartirlas con tus compañeros, les das un "manual vivo" de cómo automatizar. Es mucho más fácil aprender viendo un ejemplo real que leyendo solo la teoría.

> [!WARNING]
> **No olvides los archivos JAR**: Asegúrate siempre de que la carpeta `lib/` esté presente y tenga los archivos `jt400.jar` y `tn5250j.jar`. Sin ellos, el motor de pantalla no arrancará.

---
*Librería diseñada para escala y mantenibilidad. ¡Lista para compartir!*
