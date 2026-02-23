import sys
from mlx_source import Mlx


class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.tile = 20
        self.rows = len(maze)
        self.cols = len(maze[0])

        # Calculamos el ancho real necesario
        self.actual_width = self.cols * self.tile
        self.actual_height = self.rows * self.tile

        # Para evitar el "doblado", la imagen debe crearse con un ancho que MLX acepte bien.
        # Pero la VENTANA debe medir lo que mide el laberinto.
        self.m = Mlx()
        self.ptr = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.ptr, self.actual_width, self.actual_height, "Maze 42"
        )

        # La imagen la creamos del tamaño exacto de la ventana
        self.img = self.m.mlx_new_image(self.ptr, self.actual_width, self.actual_height)

        # Obtenemos el size_line (self.line) que es el que manda
        res = self.m.mlx_get_data_addr(self.img)
        self.addr, self.bpp, self.line, self.endian = res

    def put_pixel(self, x, y, color):
        # IMPORTANTE: Usar los límites reales de la ventana
        if 0 <= x < self.actual_width and 0 <= y < self.actual_height:
            # ESTA FÓRMULA ES LA QUE EVITA QUE SE DOBLE:
            # y * salto_de_línea_real + x * bytes_por_píxel
            pos = (y * self.line) + (x * 4)

            try:
                self.addr[pos] = color & 0xFF  # Blue
                self.addr[pos + 1] = (color >> 8) & 0xFF  # Green
                self.addr[pos + 2] = (color >> 16) & 0xFF  # Red
                self.addr[pos + 3] = 255  # Alpha
            except IndexError:
                pass

    def draw_tile(self, tx, ty, val):
        # tx es la columna (x), ty es la fila (y)
        x0 = tx * self.tile
        y0 = ty * self.tile

        # Fondo del 42 (Gris oscuro) o laberinto (Negro)
        bg = 0x222222 if val == 0 else 0x000000
        for dy in range(self.tile):
            for dx in range(self.tile):
                self.put_pixel(x0 + dx, y0 + dy, bg)

        # Paredes blancas
        w = 2
        if val & 1:  # Norte
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + j, 0xFFFFFF)
        if val & 2:  # Este
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + self.tile - 1 - i, y0 + j, 0xFFFFFF)
        if val & 4:  # Sur
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + self.tile - 1 - j, 0xFFFFFF)
        if val & 8:  # Oeste
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + i, y0 + j, 0xFFFFFF)

    def render(self, *args):
        # Recorremos la matriz: maze[fila][columna]
        for y in range(self.rows):
            for x in range(self.cols):
                # Dibujamos en (x, y) el valor de maze[y][x]
                self.draw_tile(x, y, self.maze[y][x])

        self.m.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)
        self.m.mlx_do_sync(self.ptr)
        return 0

    def run(self):
        self.m.mlx_key_hook(
            self.win, lambda k, p: sys.exit(0) if k in [65307, 53] else 0, None
        )
        self.m.mlx_loop_hook(self.ptr, self.render, None)
        self.m.mlx_loop(self.ptr)
