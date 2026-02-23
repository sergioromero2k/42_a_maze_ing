# Guía Técnica del Proyecto: A-Maze-ing

Desglose completo de cada archivo, clase y función del proyecto — qué hace y por qué existe.

---

## `a_maze_ing.py` — Punto de Entrada

| Función | Descripción |
|---------|-------------|
| `handle_sigint()` | Captura la señal `SIGINT` (Ctrl+C) y cierra el programa de forma elegante, sin imprimir un stack trace en la consola. |
| `main()` | Orquesta el flujo completo: valida argumentos, llama al parser, gestiona la semilla, instancia el generador, ejecuta el solver y lanza la interfaz. |

---

## `mazegen/` — Lógica y Algoritmos

### `generator.py` — Clase `MazeGenerator`

| Función | Descripción |
|---------|-------------|
| `__init__` | Inicializa las dimensiones, la semilla, los puntos de entrada/salida y el flag de "perfección". |
| `setup_matrices()` | Crea la rejilla inicial llena de paredes (celdas cerradas) antes de empezar a tallar cualquier camino. |
| `draw_42()` | Modifica celdas específicas de la matriz para dibujar el número 42. Al marcarlas como visitadas antes de que corra el algoritmo, el generador las trata como obstáculos fijos, preservando el patrón. |
| `generate()` | Implementa el DFS (Recursive Backtracker). Es el motor principal que talla los túneles del laberinto. |
| `_break_extra_walls()` | Si el laberinto no debe ser perfecto, esta función rompe paredes adicionales para introducir ciclos y caminos alternativos. |
| `_get_unvisited_neighbors()` | Escanea las 4 direcciones cardinales para encontrar celdas adyacentes que aún no han sido visitadas. |
| `save_to_file()` | Codifica la matriz en formato hexadecimal (1, 2, 4, 8) y escribe el archivo de salida con la solución. |

### `solver.py`

| Función | Descripción |
|---------|-------------|
| `solve()` | Implementa el algoritmo BFS. Explora el laberinto por niveles para encontrar el camino más corto. Devuelve la solución como una cadena de direcciones (ej. `"SSENW"`). |

### `utils.py` — Procesamiento de Configuración

| Función | Descripción |
|---------|-------------|
| `get_raw_config()` | Lee el archivo línea por línea y extrae los pares clave=valor, ignorando comentarios. |
| `format_value()` | Convierte strings en tipos Python correctos (ej. `"10"` → `10`, `"True"` → `True`). |
| `format_config()` | Aplica el formateo a todo el diccionario de configuración. |
| `validate_logic()` | Verifica que los datos sean coherentes (ej. que las coordenadas de entrada/salida estén dentro de los límites del laberinto). |
| `parse_config()` | La función maestra que coordina todo el pipeline de lectura y validación. |

---

## `display/` — Interfaz Gráfica

### `graphical.py` — Clase `MazeVisualizer`

| Función | Descripción |
|---------|-------------|
| `__init__` | Configura la ventana de MiniLibX y escala el tamaño de los bloques según la resolución de pantalla. |
| `put_pixel()` | Función de bajo nivel para pintar un píxel individual en el buffer de imagen. |
| `draw_tile()` | Dibuja una celda completa (suelo y paredes) leyendo e interpretando sus bits hexadecimales. |
| `terminal_menu()` | Imprime los controles de teclado en la consola para que el usuario sepa cómo interactuar. |
| `handle_keys()` | Gestiona los eventos de teclado (Esc para salir, R para regenerar, S para mostrar/ocultar la solución). |
| `render()` | La función en bucle que redibuja la ventana continuamente para mantener la imagen actualizada. |
| `run()` | Lanza `mlx_loop()`, cediendo el control a la interfaz gráfica. |

---

## Preguntas clave para la defensa

**¿Por qué dividiste `utils.py` en tantas funciones pequeñas?**

> "Para seguir el Principio de Responsabilidad Única. Cada función hace exactamente una cosa — leer, formatear o validar — lo que facilita aislar errores y reutilizar el código en otros contextos."

**¿Por qué DFS para la generación y BFS para la resolución?**

> "DFS produce laberintos con alta tortuosidad y largos callejones sin salida — visualmente complejos e interesantes. BFS es la herramienta correcta para resolver porque en un laberinto perfecto (sin ciclos), la primera vez que alcanza la salida, ese camino está garantizado como el único y, por tanto, el más corto."

**¿Por qué pre-marcar las celdas del "42" antes de la generación?**

> "Si talláramos el patrón después de la generación, el DFS podría haber llenado esas celdas con túneles, destruyendo la forma. Al marcarlas como visitadas primero, el algoritmo las trata como paredes y fluye a su alrededor de forma natural."

---

## `mlx_source/` — El Puente con la MiniLibX

Este directorio contiene el código que permite a Python "hablar" con la librería gráfica original escrita en C. Es fundamental para el rendimiento gráfico del proyecto.

### `mlx.py` — MLX Python Wrapper

Un wrapper que usa la librería `ctypes` para conectar Python con el binario `libmlx.so`. Sus funciones principales:

| Función | Descripción |
|---------|-------------|
| `__init__` | Localiza el archivo `.so` en el sistema y carga las funciones de C en el entorno de Python. |

**Gestión de Ventanas**

| Función | Descripción |
|---------|-------------|
| `mlx_new_window()` | Solicita al sistema operativo la creación de la ventana gráfica. |
| `mlx_clear_window()` / `mlx_destroy_window()` | Funciones de limpieza para evitar fugas de memoria al cerrar el programa. |

**Gestión de Imágenes**

| Función | Descripción |
|---------|-------------|
| `mlx_new_image()` | Crea un buffer de píxeles en memoria para dibujar más rápido que haciéndolo directamente en la ventana. |
| `mlx_get_data_addr()` | **Crítica.** Devuelve la dirección de memoria de la imagen, permitiendo a Python manipular los píxeles directamente como una matriz de datos. |
| `mlx_put_image_to_window()` | Vuelca todo el buffer de imagen en la ventana de un solo golpe, evitando el parpadeo de pantalla. |

**Eventos (Hooks)**

| Función | Descripción |
|---------|-------------|
| `mlx_key_hook()` / `mlx_hook()` | Registran las funciones del código (como movimiento o cierre con ESC) para que se ejecuten cuando el usuario interactúa con el teclado o el ratón. |
| `mlx_loop()` | Mantiene el programa vivo y escuchando eventos constantemente. |

**Utilidades**

| Función | Descripción |
|---------|-------------|
| `mlx_get_screen_size()` | Obtiene la resolución del monitor para escalar el laberinto. |
| `mlx_png_file_to_image()` | Permite cargar texturas o iconos externos si se desea. |

---

## Nota para la evaluación — El "API Break"

**¿Por qué algunas funciones devuelven tuplas (ej. `mlx_get_screen_size` devuelve `(val, w, h)`)?**

> "En C, las funciones devuelven valores a través de punteros pasados como argumentos. En este wrapper de Python, hemos convertido esos punteros en tuplas de retorno para que el código sea más legible e idiomático, siguiendo las convenciones estándar de Python."