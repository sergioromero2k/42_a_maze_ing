import sys
from typing import Dict, Any
from mazegen.generator import MazeGenerator

def parse_config(file_path: str) -> Dict[str, Any]:
    """Lee el archivo de configuración y extrae los parámetros."""
    config: Dict[str, Any] = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=')
                key = key.strip().upper()
                value = value.strip()
                
                # Conversión de tipos
                if key in ['WIDTH', 'HEIGHT']:
                    config[key] = int(value)
                elif key in ['ENTRY', 'EXIT']:
                    config[key] = tuple(map(int, value.split(',')))
                elif key == 'PERFECT':
                    config[key] = value.lower() == 'true'
                else:
                    config[key] = value
        return config
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer configuración: {e}")
        sys.exit(1)

def main():
    # 1. Verificación de argumentos:
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    # 2. Cargar la configuración desde el archivo config.txt:
    config = parse_config(sys.argv[1])
    
    width = config['WIDTH']
    height = config['HEIGHT']
    seed = config.get('SEED')
    entry = config.get('ENTRY', (0, 0))
    exit_cell = config.get('EXIT', (width-1, height-1))
    output_file = config.get('OUTPUT_FILE', 'resultado2.txt')
    
    maze = MazeGenerator(width, height, seed)
    
    # 3. Generar el laberinto:
    print(f"\nGenerando laberinto de {width}x{height}...")
    maze.generate()
    
    # 4. Comprobar si el laberinto generado es perfecto o no:
    if maze.is_perfect():
        print("✅ Verificación lógica: El laberinto es perfecto.")
    else:
        print("❌ Error lógico: El laberinto no cumple las condiciones de perfección.")
    
    # 5. Resolver el laberinto (BFS) para demostrar el camino más corto:
    print("\nBuscando solución óptima...")
    solution_path = maze.solve(entry, exit_cell)
    print(solution_path)
    
    # 6. Guardar los resultados en el archivo resultados.txt:
    maze.save_output(
        output_file, 
        entry, 
        exit_cell, 
        solution_path
    )
    print(f"✅ Laberinto y solución guardados con éxito en {output_file}")
    
    # 7. Visualización 1 del laberinto + camino solución (en la terminal):
    #print("\n--- Visualización en la terminal ---")
    # Mostramos el dibujo con el camino de asteriscos
    #maze.display_ascii_with_solution(entry, solution_path)
    
    # 8. Visualización 3 del laberinto + camino solución (con Pygame):
    print("\nAbriendo visualización gráfica con Pygame...")
    maze.display_pygame(entry, solution_path)
    

if __name__ == "__main__":
    main()
