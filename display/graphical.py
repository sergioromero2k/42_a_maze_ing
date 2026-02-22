import sys
from mlx import Mlx


class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.tile = 30
        self.width = len(maze[0]) * self.tile
        self.height = len(maze) * self.tile

        self.m = Mlx()
        self.ptr = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.ptr, self.width, self.height, "MAZE DEBUG"
        )

        self.img = self.m.mlx_new_image(self.ptr, self.width, self.height)
        # IMPORTANTE: En el mlx.py que pasaste, esto devuelve un memoryview
        self.addr, self.bpp, self.line, self.endian = self.m.mlx_get_data_addr(self.img)

    def put_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            # LA CLAVE: Usar self.line para evitar que el 42 salga "doblado"
            offset = (y * self.line) + (x * (self.bpp // 8))
            # Formato BGRA para la MLX de tu carpeta
            self.addr[offset] = color & 0xFF  # Azul
            self.addr[offset + 1] = (color >> 8) & 0xFF  # Verde
            self.addr[offset + 2] = (color >> 16) & 0xFF  # Rojo
            self.addr[offset + 3] = 255  # Opaco

    def render(self, *args):
        # 1. FORZADO: Pintar toda la pantalla de un color (ej. Azul oscuro)
        # Esto nos dirá si la imagen se está enviando a la ventana
        for i in range(0, len(self.addr), 4):
            self.addr[i] = 50  # Azul
            self.addr[i + 1] = 0  # Verde
            self.addr[i + 2] = 0  # Rojo
            self.addr[i + 3] = 255  # Alpha

        # 2. Dibujar el laberinto encima
        for y, row in enumerate(self.maze):
            for x, val in enumerate(row):
                self.draw_tile(x, y, val)

        # 3. Empujar imagen
        self.m.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)

        # 4. SINCRONIZACIÓN (Obligatoria segun tu carpeta mlx)
        self.m.mlx_do_sync(self.ptr)
        return 0

    def draw_tile(self, x, y, val):
        x0, y0 = x * self.tile, y * self.tile

        # 1. Pintamos el FONDO de la celda primero
        if val == 0:
            color_fondo = 0x444444  # Un gris clarito para el "42"
        else:
            color_fondo = 0x000000  # Negro para los pasillos normales

        for i in range(self.tile):
            for j in range(self.tile):
                self.put_pixel(x0 + i, y0 + j, color_fondo)

        # 2. Dibujamos las paredes (Blanco puro)
        # Solo entran aquí si val NO es 0 o si quieres paredes en el 42
        w = 2
        if val & 1:  # N
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + j, 0xFFFFFF)
        if val & 2:  # E
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + self.tile - 1 - i, y0 + j, 0xFFFFFF)
        if val & 4:  # S
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + self.tile - 1 - j, 0xFFFFFF)
        if val & 8:  # W
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + i, y0 + j, 0xFFFFFF)

    def run(self):
        self.m.mlx_key_hook(
            self.win, lambda k, p: sys.exit(0) if k in [65307, 53] else 0, None
        )
        self.m.mlx_loop_hook(self.ptr, self.render, None)
        self.m.mlx_loop(self.ptr)
