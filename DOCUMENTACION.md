# Manual Técnico: AS400 Automation Library 🚀

Esta librería proporciona una suite de herramientas en Python para automatizar procesos en IBM i (AS400), abarcando desde la ejecución de comandos hasta la interacción con pantallas 5250 de alta fidelidad.

## 🏗️ Arquitectura del Paquete

El paquete `as400_automation` se divide en módulos especializados:

1.  **`telnet_screen.py`**: El motor principal. Utiliza `pyte` para emular una terminal 24x80 real, permitiendo navegar por menús y capturar pantallas con fidelidad total.
2.  **`commands.py`**: Interfaz para ejecutar comandos CL y llamar a programas (RPG, COBOL, etc.) utilizando la librería JT400.
3.  **`database.py`**: Driver para ejecución de sentencias SQL (ODBC) directamente sobre DB2.
4.  **`reporting.py`**: Sistema modular para generar reportes profesionales con estadísticas de éxito y gestión de evidencias visuales.
5.  **`renderer.py`**: Motor gráfico que convierte el texto de la pantalla en imágenes PNG de alta calidad.

## 🛠️ Instalación y Requisitos

- **Python 3.8+**
- **Java JRE/JDK** (Necesario para JT400)
- **Librerías Python**: `pip install pyte Pillow jpype1 pyodbc pytest`
- **Driver ODBC**: IBM i Access ODBC Driver (para el módulo `database`).

## 🚀 Guía de Implementación Rápida

Para automatizar un nuevo programa, sigue este patrón:

```python
from as400_automation.telnet_screen import TelnetScreenDriver
from as400_automation.reporting import AS400Reporter

# 1. Configurar Reporte
reporter = AS400Reporter(evidence_dir="evidencias_nuevo_programa")

# 2. Iniciar Driver
driver = TelnetScreenDriver()
driver.connect("PUB400.COM")

# 3. Flujo de Negocio
if driver.login("USUARIO", "PASSWORD", evidence_dir="evidencias_nuevo_programa"):
    driver.send_text("CALL MI_LIB/MI_PROG")
    driver.send_enter(wait=2.0)
    
    # Capturar pantalla del programa
    driver.save_screenshot("evidencias_nuevo_programa", "pantalla_inicial.png")
    
    # Reportar Éxito
    reporter.add_result("Carga de Programa", "PASS", ["01_sign_on_screen.png", "pantalla_inicial.png"])
else:
    reporter.add_result("Login", "FAIL")

# 4. Generar Reporte Final
reporter.generate_console_report()
driver.disconnect()
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

### 7. 🤝 Cómo compartir con tus compañeros

Si quieres que otro compañero pueda usar esta librería en su propia computadora, tienes dos formas oficiales de hacerlo:

#### Opción A: Copia Directa (Recomendada para proyectos rápidos)
1. Comprime y envía toda la carpeta del proyecto (asegúrate de incluir la carpeta `as400_automation` y la carpeta `lib`).
2. Tu compañero debe instalar las librerías necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```
3. ¡Listo! Ya puede importar `as400_automation` en sus scripts.

#### Opción B: Instalación como Paquete Local (Profesional)
Si quieres que tu compañero pueda usar la librería desde **cualquier lugar** de su computadora (como si fuera una librería estándar de Python):
1. Envía el proyecto completo.
2. Tu compañero debe abrir una terminal en la carpeta del proyecto y ejecutar:
   ```bash
   pip install -e .
   ```
3. Ahora puede crear un script en cualquier carpeta y simplemente escribir `from as400_automation...` y funcionará.

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
