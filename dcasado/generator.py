import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import random
from collections import deque
from typing import List, Tuple, Optional
import pygame


class MazeGenerator:
    """Clase encargada de la generación lógica y resolución de laberintos perfectos.

    Atributos:
        width (int): Ancho del laberinto en celdas.
        height (int): Alto del laberinto en celdas.
        seed (Optional[int]): Semilla para la generación aleatoria.
        grid (List[List[int]]): Matriz de celdas codificadas en bits (N=1, E=2, S=4, W=8).
    """

    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        """Inicializa el generador con dimensiones y una semilla opcional."""
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.grid: List[List[int]] = [[15 for _ in range(width)] for _ in range(height)]
        
        if self.seed is not None:
            random.seed(self.seed)

    def generate(self) -> None:
        """Genera el laberinto usando el algoritmo Recursive Backtracker (DFS).
        
        El algoritmo asegura que el laberinto sea perfecto (árbol de expansión).
        """
        stack: List[Tuple[int, int]] = []
        start_cell: Tuple[int, int] = (0, 0)
        stack.append(start_cell)
        visited: List[List[bool]] = [[False for _ in range(self.width)] for _ in range(self.height)]
        visited[0][0] = True

        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_unvisited_neighbors(cx, cy, visited)

            if neighbors:
                nx, ny, direction, opp_direction = random.choice(neighbors)
                # Eliminamos las paredes (bitwise) entre la celda actual y la vecina
                self.grid[cy][cx] -= direction
                self.grid[ny][nx] -= opp_direction
                
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: List[List[bool]]
    ) -> List[Tuple[int, int, int, int]]:
        """Busca vecinos no visitados y retorna su posición y bits de pared.

        Retorna:
            List[Tuple[nx, ny, dir, opp_dir]]: Dirección actual y su opuesta.
        """
        neighbors = []
        # Direcciones: (dx, dy, bit_actual, bit_opuesto)
        directions = [
            (0, -1, 1, 4),  # Norte (1) -> Opuesto Sur (4)
            (1, 0, 2, 8),   # Este (2)  -> Opuesto Oeste (8)
            (0, 1, 4, 1),   # Sur (4)   -> Opuesto Norte (1)
            (-1, 0, 8, 2)   # Oeste (8) -> Opuesto Este (2)
        ]

        for dx, dy, bit, opp_bit in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx]:
                neighbors.append((nx, ny, bit, opp_bit))
        
        return neighbors
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """Encuentra el camino más corto usando BFS y retorna la cadena N,E,S,W.
        
        Args:
            start: Coordenadas (x, y) de entrada.
            end: Coordenadas (x, y) de salida.
            
        Returns:
            str: Cadena de direcciones (ej. 'EESNW').
        """
        queue: deque[Tuple[int, int, str]] = deque([(start[0], start[1], "")])
        visited: set[Tuple[int, int]] = {start}
        
        # Mapeo de bits a movimientos y letras
        # Bit 0:N(1), 1:E(2), 2:S(4), 3:W(8)
        directions = [
            (0, -1, 1, 'N'),
            (1, 0, 2, 'E'),
            (0, 1, 4, 'S'),
            (-1, 0, 8, 'W')
        ]

        while queue:
            cx, cy, path = queue.popleft()

            if (cx, cy) == end:
                return path

            for dx, dy, bit, char in directions:
                nx, ny = cx + dx, cy + dy
                
                # Verificar si no hay pared en esa dirección (bit no está en la celda)
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (self.grid[cy][cx] & bit) and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + char))
        
        return ""
    
    def get_solution_as_string(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """Método que obtiene la cadena de solución (N,E,S,W) del camino calculado por BFS."""
        return self.solve(start, end)

    def get_hex_grid(self) -> List[str]:
        """Convierte la matriz a formato hexadecimal fila por fila."""
        hex_rows = []
        for row in self.grid:
            # Convierte cada celda (0-15) a un dígito hexadecimal (0-F)
            hex_rows.append("".join(f"{cell:X}" for cell in row))
        return hex_rows

    def save_output(self, filename: str, entry: Tuple[int, int], exit: Tuple[int, int], solution: str) -> None:
        """Genera el archivo de salida con el formato requerido por el subject."""
        try:
            with open(filename, 'w') as f:
                # 1. Grilla Hexadecimal
                hex_rows = self.get_hex_grid()
                for row in hex_rows:
                    f.write(row + "\n")
                
                # 2. Línea vacía obligatoria
                f.write("\n")
                
                # 3. Coordenadas de entrada y salida
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit[0]},{exit[1]}\n")
                
                # 4. Cadena de la solución (N, E, S, W)
                f.write(solution + "\n")
        except Exception as e:
            print(f"Error crítico al guardar: {e}")
            raise  # Re-lanzamos para que el main sepa que falló
        
    # USANDO LA TERMINAL PARA LA VISUALIZACIÓN (DEL LABERINTO + CAMINO DE SOLUCIÓN):
    def display_ascii_with_solution(self, start: Tuple[int, int], path: str):
        """Dibuja el laberinto en la consola marcando el camino de la solución para pruebas visuales."""
        # Calculamos todas las coordenadas del camino
        solution_cells = {start}
        cx, cy = start
        for move in path:
            if move == 'N': cy -= 1
            elif move == 'E': cx += 1
            elif move == 'S': cy += 1
            elif move == 'W': cx -= 1
            solution_cells.add((cx, cy))

        for y in range(self.height):
            # Dibujar las paredes norte
            line1 = ""
            for x in range(self.width):
                line1 += "+---" if (self.grid[y][x] & 1) else "+   "
            print(line1 + "+")
            
            # Dibujar las paredes oeste y el contenido de la celda (con solución)
            line2 = ""
            for x in range(self.width):
                wall = "|" if (self.grid[y][x] & 8) else " "
                # Si la celda está en el camino, ponemos un '*', si no, espacio
                content = " * " if (x, y) in solution_cells else "   "
                line2 += wall + content
            print(line2 + "|")
            
        # Dibujar la línea final (paredes sur de la última fila)
        last_line = ""
        for x in range(self.width):
            last_line += "+---" if (self.grid[self.height-1][x] & 4) else "+   "
        print(last_line + "+")
        
    # USANDO PYGAME PARA LA VISUALIZACIÓN (DEL LABERINTO + CAMINO DE SOLUCIÓN) EN VENTANA EMERGENTE:
    def display_pygame(self, start: Tuple[int, int], path: str):
        #Muestra el laberinto en una ventana de Pygame.
        pygame.init()
        
        cell_size = 30
        width = self.width * cell_size
        height = self.height * cell_size
        screen = pygame.display.set_mode((width + 40, height + 60))
        pygame.display.set_caption("A_maze_ing visualizer")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255)) # Fondo blanco
            
            # Dibujar Texto de longitud
            font = pygame.font.SysFont("Arial", 18)
            text = font.render(f"Distancia más corta (BFS): {len(path)} pasos", True, (0, 0, 255))
            screen.blit(text, (20, 10))

            # Dibujar el laberinto (desplazado para el texto)
            offset_y = 40
            offset_x = 20

            for y in range(self.height):
                for x in range(self.width):
                    lx, ly = x * cell_size + offset_x, y * cell_size + offset_y
                    bits = self.grid[y][x]
                    
                    # Paredes (Negro)
                    if bits & 1: pygame.draw.line(screen, (0,0,0), (lx, ly), (lx + cell_size, ly), 2)
                    if bits & 2: pygame.draw.line(screen, (0,0,0), (lx + cell_size, ly), (lx + cell_size, ly + cell_size), 2)
                    if bits & 4: pygame.draw.line(screen, (0,0,0), (lx, ly + cell_size), (lx + cell_size, ly + cell_size), 2)
                    if bits & 8: pygame.draw.line(screen, (0,0,0), (lx, ly), (lx, ly + cell_size), 2)

            # Dibujar Camino Solución (Rojo)
            if path:
                cx, cy = start
                for move in path:
                    old_x, old_y = cx, cy
                    if move == 'N': cy -= 1
                    elif move == 'E': cx += 1
                    elif move == 'S': cy += 1
                    elif move == 'W': cx -= 1
                    
                    p1 = (old_x * cell_size + cell_size//2 + offset_x, old_y * cell_size + cell_size//2 + offset_y)
                    p2 = (cx * cell_size + cell_size//2 + offset_x, cy * cell_size + cell_size//2 + offset_y)
                    pygame.draw.line(screen, (255, 0, 0), p1, p2, 3)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        
    def is_perfect(self) -> bool:
        """
        Verifica si el laberinto es perfecto contando celdas y paredes.
        Un laberinto perfecto de N celdas tiene exactamente N-1 pasajes.
        """
        total_cells = self.width * self.height
        walls_broken = 0
        
        for y in range(self.height):
            for x in range(self.width):
                # Contamos paredes rotas al Este y Sur
                if not (self.grid[y][x] & 2): # Bit 1: Este
                    if x < self.width - 1: 
                        walls_broken += 1
                if not (self.grid[y][x] & 4): # Bit 2: Sur
                    if y < self.height - 1: 
                        walls_broken += 1
                        
        return walls_broken == (total_cells - 1)
