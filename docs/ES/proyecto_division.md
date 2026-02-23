# Generador de Laberintos Perfectos

## De qué trata el proyecto
El objetivo es crear un generador de laberintos perfectos (un solo camino entre entrada y salida) utilizando Python 3.10+. No es solo dibujar líneas; el proyecto exige aplicar Teoría de Grafos (árboles de expansión), gestionar archivos de configuración, asegurar la reusabilidad del código mediante un paquete instalable y cumplir con estándares estrictos de calidad como flake8 y mypy.

## Cómo empezar (Lo recomendable)
Antes de tocar el código, lo ideal es:

- **Acordar la interfaz:** Persona A define cómo se llamarán los métodos de la clase `MazeGenerator` (ej: `.generate()`, `.get_solution()`) para que la Persona B pueda programar la visualización sin esperar a que el algoritmo esté terminado.
- **Entorno virtual:** Ambos deben usar `venv` o `conda` para que las dependencias sean idénticas.
- **Git Flow:** Trabajen en ramas separadas (ej: `feat/generator` y `feat/ui`) para evitar conflictos de código.

## Planificación Detallada (1 Semana)

### Día 1: Arquitectura y Parsing (4.5h)
**Persona A (Tú):** Configuración del entorno, Makefile y esqueleto de la Clase.

- **Teoría:** Estructura de paquetes en Python y automatización con Make.
- **Tareas:** Crear el repo, `.gitignore`, y la estructura de la clase `MazeGenerator` con sus type hints.

**Persona B:** Parser de configuración.

- **Teoría:** Manejo de archivos y validación de datos en Python.
- **Tareas:** Leer `config.txt`, ignorar comentarios (`#`), y validar que `WIDTH` y `HEIGHT` sean números positivos.

### Día 2: Algoritmos de Generación (5h)
**Persona A:** El "Motor" del Laberinto.

- **Teoría:** Recursive Backtracker (DFS) o Algoritmo de Prim. Los laberintos perfectos son árboles de expansión.
- **Tareas:** Programar la generación usando una semilla (`seed`) para que sea reproducible.

**Persona B:** Lógica de Celdas y el Patrón "42".

- **Teoría:** Manipulación de matrices y representación de celdas cerradas.
- **Tareas:** Crear la lógica para "dibujar" el número 42 con celdas cerradas dentro del laberinto.

### Día 3: Resolución y Exportación (5h)
**Persona A:** Algoritmo de Búsqueda.

- **Teoría:** BFS (Breadth-First Search) para encontrar el camino más corto.
- **Tareas:** Implementar el método que devuelve la solución como una cadena de caracteres (N, E, S, W).

**Persona B:** Formateo Hexadecimal.

- **Teoría:** Operaciones a nivel de bits (Bitwise). Cada pared es un bit (N=1, E=2, S=4, W=8).
- **Tareas:** Generar el archivo de salida donde cada celda es un dígito hexadecimal coherente con sus vecinas.

### Día 4: UI e Instalación (5h)
**Persona A:** Empaquetado de Software.

- **Teoría:** Distribución de Python con setuptools o poetry.
- **Tareas:** Crear el archivo `.whl` o `.tar.gz` llamado `mazegen-*` y redactar la documentación de uso del módulo.

**Persona B:** Representación Visual.

- **Teoría:** Renderizado ASCII o uso de librerías gráficas (MLX).
- **Tareas:** Crear la interfaz que permita regenerar el laberinto, mostrar la solución y cambiar colores con teclas/comandos.

### Día 5: Calidad de Código (4h)
**Persona A:** Refactorización y Tipado.

- **Teoría:** Programación defensiva y tipado estático.
- **Tareas:** Asegurar que todo el código pase `mypy --strict` y gestionar excepciones para que el programa nunca "crashee".

**Persona B:** Estilo y Documentación.

- **Teoría:** Estándar PEP 8 y PEP 257.
- **Tareas:** Limpiar el código con `flake8` y redactar los Docstrings (estilo Google o NumPy).

### Día 6: README y Pruebas Finales (4h)
**Persona A:** Pruebas de Integración.

- **Tareas:** Instalar el paquete generado en un entorno limpio y verificar que el script principal `a_maze_ing.py` funcione correctamente.

**Persona B:** Documentación Final.

- **Tareas:** Completar el `README.md` con los roles, la planificación real y la justificación del algoritmo elegido.
