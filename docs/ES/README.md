*Creado como parte del currículo de 42 por **serromer** y **dcasado-**.*

# 42_A_MAZE_ING — El Generador de Laberintos Perfectos

---

## ¿Qué es esto?

**A-Maze-ing** es una suite en Python para generar y resolver **laberintos perfectos** — laberintos donde cualquier par de puntos está conectado por exactamente un camino, sin bucles y sin zonas inaccesibles (un árbol de expansión, en términos de teoría de grafos).

Más allá del algoritmo, el proyecto incrusta un **patrón visual "42"** obligatorio en cada laberinto, incluye un visualizador gráfico en tiempo real y exporta los resultados en un formato hexadecimal compacto de codificación de paredes.

---

## Características

- **Garantía de laberinto perfecto** — conectividad de camino único mediante lógica de árbol de expansión.
- **Easter egg "42"** — el logo de 42 se talla en las paredes del laberinto antes de que comience la generación.
- **Semillas deterministas** — reproduce cualquier laberinto exactamente con una semilla dada.
- **Visualizador interactivo** — ventana con MiniLibX y controles en tiempo real.
- **Exportación hex** — codificación de 4 bits por pared escrita en un archivo de salida configurable.

---

## Requisitos previos

- Python 3.10 o superior
- `pip`
- Librerías `X11` (necesarias para la visualización gráfica con MiniLibX)

---

## Instalación

Desde la raíz del proyecto, instala en modo editable:

```bash
make install
pip install -e .
```

---

## Uso

Ejecutar con el archivo de configuración por defecto:

```bash
make run
```

O apuntando a un config personalizado:

```bash
python3 a_maze_ing.py config.txt
```

### Controles del visualizador

| Tecla | Acción |
|-------|--------|
| `R` | Regenerar laberinto con una nueva semilla aleatoria |
| `S` | Mostrar/ocultar la solución más corta (BFS) |
| `C` | Cambiar paleta de colores |
| `ESC` / Cerrar ventana | Salir limpiamente |

---

## Archivo de configuración

Formato clave-valor. Las líneas que empiezan con `#` son comentarios y se ignoran.

| Clave | Descripción |
|-------|-------------|
| `WIDTH` / `HEIGHT` | Deben ser **enteros impares** (ej. `31`) para mantener la simetría celda-pared |
| `ENTRY` / `EXIT` | Coordenadas indexadas desde cero como `x,y` |
| `SEED` | Entero para generación reproducible |
| `OUTPUT_FILE` | Destino del laberinto codificado en hex |
| `PERFECT` | `True` para generación con DFS |

### Ejemplo

```ini
# Configuración del proyecto
WIDTH=31
HEIGHT=31
ENTRY=1,1
EXIT=29,29
SEED=4242
OUTPUT_FILE=output_maze.txt
PERFECT=True
```

---

## Cómo funciona

### Codificación de paredes — Lógica bitwise de 4 bits

Cada celda se representa con 4 bits, uno por dirección:

| Dirección | Bit | Valor |
|-----------|-----|-------|
| Norte | 0 | 1 |
| Este  | 1 | 2 |
| Sur   | 2 | 4 |
| Oeste | 3 | 8 |

Una celda con valor `0x9` (`1001` en binario) tiene paredes abiertas hacia el **Norte** y el **Oeste**.

### Generación — Backtracker Recursivo (DFS)

Se eligió DFS por su resultado estético: alta tortuosidad y largos callejones sin salida — visualmente mucho más interesante que el algoritmo de Prim, que tiende a generar muchas ramas cortas.

El **patrón "42"** se talla *antes* de que comience la generación. Esas celdas se marcan como visitadas de antemano, de modo que el DFS fluye a su alrededor preservando la forma.

### Resolución — Búsqueda en anchura (BFS)

En un laberinto perfecto no hay ciclos, por lo que la primera vez que BFS alcanza la salida, el camino encontrado está garantizado como el **único** (y por tanto el más corto).

---

## Estructura del proyecto

El proyecto está dividido en dos paquetes independientes:

- **`mazegen`** — lógica de generación pura, sin dependencias de UI. Utilizable en herramientas CLI o notebooks.
- **`display`** — capa de visualización. Se puede reemplazar por Pygame o Matplotlib sin tocar la lógica de generación.

```
42_a_maze_ing
├── a_maze_ing.py          # Punto de entrada principal (el "cerebro")
├── config.txt             # Archivo de configuración de ejemplo
├── Makefile               # Herramienta de automatización (all, run, clean, lint, re)
├── pyproject.toml         # Metadatos y configuración del proyecto Python
├── README.md              # Documentación del proyecto
├── display/               # Módulo gráfico
│   ├── __init__.py
│   └── graphical.py       # Lógica de visualización con MLX
├── docs/                  # Guías y documentación del proyecto
│   ├── ES/                # Traducción a español
│   ├── activate_venv.md
│   ├── differentes_cases_config.txt
│   ├── es.subject_a_maze_py.pdf
│   ├── execution_whl.md
│   ├── mlx_setup.md
│   ├── output_validator.py
│   └── project_division.md
├── libs/                  # Dependencias offline (archivos WHL)
│   ├── mlx-2.2-py3-fedora-any.whl
│   └── mlx-2.2-py3-ubuntu-any.whl
├── mazegen/               # Paquete de lógica principal
│   ├── __init__.py
│   ├── generator.py       # Generación del laberinto (DFS + patrón 42)
│   ├── py.typed           # Soporte para tipado con Mypy
│   ├── solver.py          # Algoritmo de resolución (BFS)
│   └── utils.py           # Parser de configuración y utilidades
├── mlx_source/            # Bindings Python de MLX
│   ├── __init__.py
│   ├── mlx.py
│   └── docs/              # Man pages y cabeceras
│       ├── mlx.3
│       ├── mlx.h
│       └── ... (otros archivos .3)
├── tests/                 # Tests unitarios de lógica y ventana
│   ├── test_logic.py
│   └── test_window.py
└── .gitignore             # Evita el seguimiento de cachés y archivos temporales
```

---

## Equipo

| Miembro | Rol |
|---------|-----|
| **serromer** | Arquitecto principal — motor MazeGenerator, lógica DFS, packaging Python, Makefile |
| **dcasado-** | Desarrollador principal — Solver BFS, parser de configuración, interfaz gráfica con MiniLibX |

### Planificación vs. Realidad

La inyección del patrón "42" llevó más tiempo del esperado, retrasando el generador del Día 2 al Día 3. Recuperamos el tiempo definiendo una interfaz compartida (Clases Base Abstractas) desde el principio, lo que permitió integrar la UI y la lógica en menos de 2 horas.

Usar `mypy --strict` desde el primer día evitó decenas de errores de `NoneType` durante la integración — muy recomendable.

---

## Declaración de uso de IA

Las herramientas de IA se usaron exclusivamente para tareas no algorítmicas:

- Generación de plantillas de `Makefile` y `pyproject.toml`
- Código base para el manejo de señales (`SIGINT`)
- Redacción y traducción de esta documentación

Todos los algoritmos principales (DFS / BFS) fueron diseñados e implementados por el equipo para garantizar la integridad académica.

---

## Recursos

- [Algoritmos de generación de laberintos](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — base teórica
- [Guía de packaging de Python](https://packaging.python.org/) — estándares de `pyproject.toml`