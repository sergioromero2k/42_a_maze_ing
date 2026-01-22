# Algoritmia y Teoría de Grafos

Los laberintos son una aplicación práctica de la teoría de grafos y la aleatoriedad.

## 1. Laberintos Perfectos
- Un laberinto perfecto es aquel que tiene un único camino entre cualquier par de puntos.
- Matemáticamente, esto se conoce como un **Árbol de Expansión** (Spanning Tree).

## 2. Algoritmos de Generación
- **Prim**: Basado en expandir desde una celda aleatoria.
- **Kruskal**: Útil para evitar ciclos.
- **Recursive Backtracker (DFS)**: Crea pasillos largos y complejos.

## 3. Resolución de Laberintos (Pathfinding)
- El proyecto exige calcular el "camino más corto".
- Estudia **BFS** (Breadth-First Search), que es el algoritmo estándar para encontrar la ruta mínima en grafos no pesados.

---

# Manipulación de Bits y Hexadecimal

El formato de salida es muy específico y requiere conocimientos de lógica binaria.

## 1. Codificación por Celdas
- Cada celda se representa con un dígito hexadecimal (0-F).

## 2. Flags de Dirección
- Debes entender cómo asignar valores binarios a las paredes:
  - **Norte**: Bit 0 ($2^0 = 1$)
  - **Este**: Bit 1 ($2^1 = 2$)
  - **Sur**: Bit 2 ($2^2 = 4$)
  - **Oeste**: Bit 3 ($2^3 = 8$)

## 3. Operaciones Bitwise
- Aprende a usar operadores para "encender" o "apagar" paredes (bits) según el diseño del laberinto.

---

# Estándares de Python y Calidad de Código

Este proyecto tiene requisitos técnicos estrictos que se evalúan con herramientas automáticas.

## 1. Anotaciones de Tipo (Type Hinting)
- Es obligatorio usar el módulo `typing` para parámetros y retornos.

## 2. Comprobación Estática
- Debes aprender a interpretar los errores de `mypy`.

## 3. Estilo de Código
- El proyecto debe seguir estrictamente el estándar **flake8**.

## 4. Documentación (Docstrings)
- Debes usar el estándar **PEP 257** (estilo Google o NumPy) para todas tus clases y funciones.

---

# Ingeniería de Software y Empaquetado

No basta con que el código funcione; debe ser profesional y reutilizable.

## 1. Programación Orientada a Objetos (POO)
- Se requiere que la lógica de generación esté encapsulada en una clase única (ej. `MazeGenerator`).

## 2. Empaquetado con Pip
- Aprende a crear archivos de distribución `.whl` (Wheel) o `.tar.gz`.
- Esto implica entender archivos de configuración como `pyproject.toml` o `setup.py`.

## 3. Gestión de Recursos
- Estudia los gestores de contexto (`with`) para el manejo de archivos y así evitar fugas de memoria o descriptores abiertos.
