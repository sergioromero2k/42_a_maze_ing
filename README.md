*This project has been created as part of the 42 curriculum by serromer and dcasado-.*

## 1. Teoría Fundamental a Estudiar

Antes de tocar el teclado, necesitas comprender los conceptos matemáticos y computacionales detrás de los laberintos:

### Teoría de Grafos
- Entender que un laberinto perfecto es, en esencia, un **Árbol de Expansión Mínimo** (Spanning Tree).

### Algoritmos de Generación
Investiga los más comunes:
- **Recursive Backtracker (DFS)**: Fácil de implementar, genera caminos largos y sinuosos.
- **Prim**: Genera laberintos más "compactos" y ramificados.
- **Kruskal**: Muy eficiente para asegurar que no haya ciclos.

### Búsqueda de Caminos (Pathfinding)
Necesitarás algoritmos como **BFS** (para el camino más corto) o **A*** para resolver el laberinto.

### Representación Binaria/Hexadecimal
- Repasa cómo usar bits para representar paredes (N=1, E=2, S=4, W=8) y cómo convertirlos a hexadecimal.

---

## 2. Pasos para Comenzar (Plan de Trabajo)

### Fase 1: Configuración del Entorno y Estándares
- **Entorno Virtual**: Crea un entorno con `venv` o `conda`.
- **Linter y Tipado**: Configura `flake8` para el estilo de código y `mypy` para las anotaciones de tipo, ya que son obligatorios para aprobar.
- **Makefile**: Escribe las reglas básicas (install, run, lint, clean) para automatizar el flujo desde el día uno.

### Fase 2: El Corazón del Proyecto (Lógica de Generación)
- **Módulo Reutilizable**: Diseña el generador como una clase independiente (`MazeGenerator`) dentro de un paquete instalable con `pip`.
- **Parser de Configuración**: Crea una función que lea el archivo `config.txt` y valide que todos los parámetros (WIDTH, HEIGHT, ENTRY, EXIT, etc.) sean correctos.
- **Algoritmo de Generación**: Implementa la lógica de creación asegurando que se pueda usar una semilla para reproducibilidad.
- **Patrón "42"**: Asegúrate de que el laberinto incluya visualmente el número "42" formado por celdas cerradas.

### Fase 3: Salida y Visualización
- **Exportación a Archivo**: Genera el archivo de salida con el formato hexadecimal, coordenadas de entrada/salida y el camino corto resuelto.
- **Representación Visual**: Implementa una interfaz en ASCII (terminal) o gráfica (MiniLibX) que permita interactuar: regenerar, mostrar solución y cambiar colores.

### Fase 4: Documentación y Entrega
- **README.md**: Debe ser muy detallado, incluyendo roles del equipo, decisiones técnicas y el uso de IA.
- **Empaquetado**: Crea el archivo `.whl` o `.tar.gz` de tu módulo de generación.

---

## 3. Estimación y Dificultad
- **Dificultad**: Media-Alta. No por la complejidad del código en sí, sino por la rigurosidad de los estándares (`flake8`, `mypy`), la gestión de excepciones y los requisitos de empaquetado de Python.
- **Tiempo Estimado**:
  - Estudiantes dedicados: **1 a 2 semanas**.
  - Ritmo pausado: **3 a 4 semanas**.

**Nota**: La lógica del laberinto se resuelve rápido, pero dejar el código "limpio" y profesional según las reglas del Capítulo III suele llevar el 50% del tiempo.

---

### Archivos adicionales

- `test_suite_extra/` → Contiene archivos de teoría y ejercicios extra de datos. No son necesarios para ejecutar el proyecto.


## 4. Un consejo sobre la IA en 42
El documento es muy claro: usa la IA para tareas tediosas (como generar el Makefile o estructuras repetitivas), pero nunca copies código que no entiendas. En la evaluación te pedirán modificar el código en vivo para demostrar que tú tienes el control.


### Arbol estructura

```
a_maze_ing/
├── .gitignore              # Archivo para excluir .pyc, __pycache__ y venv.
├── Makefile                # Automatización: install, run, lint, etc..
├── README.md               # Documentación general y del equipo.
├── config.txt              # Archivo de configuración por defecto.
├── pyproject.toml          # Configuración moderna de empaquetado (reemplaza a setup.py).
├── a_maze_ing.py           # Script principal (punto de entrada obligatorio).
│
├── mazegen/                # El módulo reutilizable.
│   ├── __init__.py         # Expone la clase MazeGenerator.
│   ├── generator.py        # Lógica del algoritmo de generación (clase MazeGenerator).
│   ├── solver.py           # Lógica para encontrar el camino más corto.
│   ├── utils.py            # Manejo de archivos (hexadecimal) y validaciones.
│   └── py.typed            # Indica a mypy que el paquete tiene tipos.
│
├── display/                # Lógica de representación visual.
│   ├── __init__.py
│   ├── terminal.py         # Renderizado ASCII e interacciones de consola.
│   └── graphical.py        # (Opcional) Visualización con MiniLibX.
│
├── tests/                  # Programas de prueba (no se entregan para nota).
│   └── test_logic.py
│
└── dist/                   # Aquí se generará tu .whl o .tar.gz tras el build.
```

Este módulo permite la creación de laberintos perfectos mediante el algoritmo **Recursive Backtracker (DFS)** 
y su resolución óptima usando **Breadth-First Search (BFS)**.

## Instalación

Este módulo permite la creación de laberintos perfectos mediante el algoritmo **Recursive Backtracker (DFS)** 
y su resolución óptima usando **Breadth-First Search (BFS)**.

## Instalación

Desde la carpeta raíz del proyecto, instala el paquete en modo editable:
```bash
pip install -e .
