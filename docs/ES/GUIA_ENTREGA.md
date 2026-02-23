# Guía de Entrega: A-Maze-ing

Sigue estos pasos en orden para asegurar que cumples con todos los requisitos del Chapter VI (Reusabilidad) y el Chapter IX (Entrega).

---

## 1. Limpieza Total (Pre-entrega)

Antes de generar nada, elimina todos los binarios y cachés que están prohibidos en el repositorio.

```bash
# Ejecuta tu regla de limpieza
make clean

# Elimina carpetas de construcción anteriores si existen
rm -rf dist/ build/ *.egg-info

# Elimina el binario de MLX (se debe compilar/instalar en el sitio)
rm -f mlx_source/libmlx.so
```

---

## 2. Generación del Paquete Reutilizable (`.whl`)

El subject exige que el módulo `mazegen` sea instalable.

**Paso 1** — Instala la herramienta de empaquetado:

```bash
pip install build
```

**Paso 2** — Construye el paquete:

```bash
python3 -m build
```

**Paso 3** — Mueve el archivo a la raíz (REQUISITO OBLIGATORIO): El evaluador debe encontrar el `.whl` en la raíz, no dentro de una carpeta `dist/`.

```bash
mv dist/mazegen-*.whl .
```

---

## 3. Verificación de Estructura Final

Tu repositorio en GitHub/GitLab debe verse exactamente así:

```
42_a_maze_ing/
├── a_maze_ing.py                        # Script principal
├── config.txt                           # Configuración por defecto
├── Makefile                             # Con reglas install, run, lint, clean, debug
├── pyproject.toml                       # Metadatos para el build
├── README.md                            # Documentación profesional
├── mazegen-1.0.0-py3-none-any.whl       # <-- AQUÍ EN LA RAÍZ
├── mazegen/                             # Carpeta con la lógica
├── display/                             # Carpeta con la UI
├── mlx_source/                          # Carpeta con el wrapper (sin el .so)
└── .gitignore                           # Ignorando __pycache__ y .so
```

---

## 4. El Simulacro de Evaluación

Haz esto para estar 100% seguro de que no fallarás delante del evaluador:

```bash
# 1. Crea un entorno virtual limpio
python3 -m venv test_env
source test_env/bin/activate

# 2. Instala tu propio archivo .whl
pip install mazegen-1.0.0-py3-none-any.whl

# 3. Prueba el linting (debe dar 0 errores)
make lint

# 4. Prueba la ejecución
make run

# 5. Sal del entorno y borra la prueba
deactivate
rm -rf test_env
```

---

## 5. Checklist de Defensa

Prepárate para responder esto:

**¿Por qué el `.whl`?**
> "Para cumplir con el requisito de reusabilidad. Permite que cualquier otro desarrollador instale mi lógica de generación como una librería estándar de Python."

**¿Cómo dibujas el 42?**
> "Lo inyecto en la matriz antes de generar el laberinto y marco esas celdas como visitadas para que el algoritmo las rodee sin romper el camino."

**¿Qué pasa si el `config.txt` tiene un tamaño imposible?**
> "El parser valida las coordenadas contra el ancho y alto. Si son incoherentes, lanza un error controlado en lugar de un crash."
