import random
from collections import deque
from typing import List, Tuple, Optional


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

    def get_hex_grid(self) -> List[str]:
        """Convierte la matriz a formato hexadecimal fila por fila."""
        hex_rows = []
        for row in self.grid:
            hex_rows.append("".join(f"{cell:X}" for cell in row))
        return hex_rows
