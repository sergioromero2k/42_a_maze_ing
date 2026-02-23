#!/usr/bin/env python3
import os
import random
import threading
from typing import Any
from mlx import Mlx
from mazegen.solver import solve


class MazeVisualizer:
    """
    Interactive Graphical Visualizer for 42 Maze.
    Uses a separate thread for the terminal menu to prevent freezing.
    """

    def __init__(self, maze_obj: Any, solution: str) -> None:
        self.maze_obj = maze_obj
        self.path = solution

        # -- State Variables (Ajustados a tus fotos)
        self.pattern_color = 0x333333
        self.show_path = True
        self.wall_color = 0xFFFFFF
        self.player_color = 0xFF00FF  # Lilac/Fuchsia
        self.exit_color = 0xFF0000  # Red
        self.won = False
        self.running = True

        # -- Player Position
        self.player_pos = list(self.maze_obj.entry)

        # -- Display Settings
        self.tile = 25
        self.win_w = self.maze_obj.width * self.tile
        self.win_h = self.maze_obj.height * self.tile

        # -- MLX Initialization
        self.m = Mlx()
        self.ptr = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.ptr, self.win_w, self.win_h, "A-Maze-ing 42"
        )
        self.img = self.m.mlx_new_image(self.ptr, self.win_w, self.win_h)

        res = self.m.mlx_get_data_addr(self.img)
        self.addr, self.line = res[0], res[2]

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Safe pixel drawing."""
        if 0 <= x < self.win_w and 0 <= y < self.win_h:
            pos = (y * self.line) + (x * 4)
            self.addr[pos] = color & 0xFF
            self.addr[pos + 1] = (color >> 8) & 0xFF
            self.addr[pos + 2] = (color >> 16) & 0xFF
            self.addr[pos + 3] = 255

    def draw_tile(self, tx: int, ty: int, val: int) -> None:
        """Draw walls based on hex bits."""
        x0, y0 = tx * self.tile, ty * self.tile
        is_42 = (ty, tx) in self.maze_obj.mold_positions
        bg = self.pattern_color if is_42 else 0x000000
        for i in range(self.tile):
            for j in range(self.tile):
                self.put_pixel(x0 + i, y0 + j, bg)
        if is_42:
            return
        w = 2
        if val & 1:  # North
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + j, self.wall_color)
        if val & 2:  # East
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(
                        x0 + self.tile - 1 - i, y0 + j, self.wall_color)
        if val & 4:  # South
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(
                        x0 + i, y0 + self.tile - 1 - j, self.wall_color)
        if val & 8:  # West
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + i, y0 + j, self.wall_color)

    def terminal_menu(self) -> None:
        """Menu loop running in a separate thread to avoid freezing MLX."""
        while self.running:
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ")

            if choice == "1":
                self.maze_obj.seed = random.randint(0, 9999)
                random.seed(self.maze_obj.seed)
                self.maze_obj.setup_matrices()
                self.maze_obj.generate()
                self.path = solve(
                    self.maze_obj.grid, self.maze_obj.entry, self.maze_obj.exit
                )
                self.player_pos = list(self.maze_obj.entry)
                self.won = False
                print("Maze regenerated!")
            elif choice == "2":
                self.show_path = not self.show_path
            elif choice == "3":
                self.wall_color = random.getrandbits(24)
                self.pattern_color = random.getrandbits(24)  # Add this line
                print("Colors rotated!")
            elif choice == "4":
                self.running = False
                os._exit(0)

    def handle_keys(self, key: int, param: Any) -> int:
        """Movement logic from the window."""
        if key == 65307 or key == 53:
            os._exit(0)
        if not self.won:
            r, c = self.player_pos
            val = self.maze_obj.grid[r][c]
            if key == 65362 and not (val & 1):
                self.player_pos[0] -= 1
            elif key == 65364 and not (val & 4):
                self.player_pos[0] += 1
            elif key == 65361 and not (val & 8):
                self.player_pos[1] -= 1
            elif key == 65363 and not (val & 2):
                self.player_pos[1] += 1
            if tuple(self.player_pos) == self.maze_obj.exit:
                print("\nYOU WON!")
                self.won = True
        return 0

    def render(self, *args: Any) -> int:
        """Main rendering loop."""
        try:
            if self.won:
                for y in range(self.win_h):
                    for x in range(self.win_w):
                        self.put_pixel(x, y, 0x000000)
            else:
                for y in range(self.maze_obj.height):
                    for x in range(self.maze_obj.width):
                        self.draw_tile(x, y, self.maze_obj.grid[y][x])

                if self.show_path and self.path:
                    r, c = self.maze_obj.entry
                    for move in self.path:
                        if move == "N":
                            r -= 1
                        elif move == "S":
                            r += 1
                        elif move == "E":
                            c += 1
                        elif move == "W":
                            c -= 1
                        margin = self.tile // 3
                        for i in range(self.tile - margin * 2):
                            for j in range(self.tile - margin * 2):
                                self.put_pixel(
                                    c * self.tile + margin + i,
                                    r * self.tile + margin + j,
                                    0x440000,
                                )

                # Draw player and exit (Relleno proporcional)
                ex, ey = self.maze_obj.exit
                px, py = self.player_pos

                margin = self.tile // 4  # Margen para que no toque las paredes
                size = self.tile - (margin * 2)

                for i in range(size):
                    for j in range(size):
                        # Dibujar Salida (Roja)
                        self.put_pixel(
                            ey * self.tile + margin + i,
                            ex * self.tile + margin + j,
                            self.exit_color,
                        )
                        # Dibujar Jugador (Lila)
                        self.put_pixel(
                            py * self.tile + margin + i,
                            px * self.tile + margin + j,
                            self.player_color,
                        )

            self.m.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)
            if self.won:
                self.m.mlx_string_put(
                    self.ptr,
                    self.win,
                    self.win_w // 2 - 30,
                    self.win_h // 2,
                    0xFFFF00,
                    "YOU WON!",
                )
        except Exception:
            os._exit(0)
        return 0

    def run(self) -> None:
        """Start thread and MLX."""
        # Start menu thread
        menu_thread = threading.Thread(target=self.terminal_menu, daemon=True)
        menu_thread.start()

        # Start MLX hooks
        self.m.mlx_key_hook(self.win, self.handle_keys, None)
        self.m.mlx_hook(self.win, 17, 0, lambda p: os._exit(0), None)
        self.m.mlx_loop_hook(self.ptr, self.render, None)
        self.m.mlx_loop(self.ptr)
