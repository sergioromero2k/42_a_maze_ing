#!/usr/bin/env python3
import sys
import os
from typing import List, Tuple, Any
from mlx import Mlx


class MazeVisualizer:
    """Graphical visualizer that renders the '42' as solid obstacles."""

    def __init__(
        self, maze: List[List[int]], path: str = "", entry: Tuple[int, int] = (0, 0)
    ) -> None:
        """Init MLX and calculate dimensions."""
        self.maze = maze
        self.path = path
        self.entry = entry
        self.tile = 20
        self.rows = len(maze)
        self.cols = len(maze[0])

        # Identify 42 cells for solid rendering
        self.mold_positions = self._get_mold_coords()

        self.w_win = self.cols * self.tile
        self.h_win = self.rows * self.tile
        self.m = Mlx()
        self.ptr: Any = self.m.mlx_init()
        self.win: Any = self.m.mlx_new_window(
            self.ptr, self.w_win, self.h_win, "Maze 42"
        )
        self.img: Any = self.m.mlx_new_image(self.ptr, self.w_win, self.h_win)

        res = self.m.mlx_get_data_addr(self.img)
        self.addr, self.line = res[0], res[2]

    def _get_mold_coords(self) -> List[Tuple[int, int]]:
        """Recalculate stencil positions for rendering."""
        mold = {
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (0, 4),
            (0, 5),
            (0, 6),
            (1, 6),
            (2, 6),
            (2, 5),
            (2, 4),
            (3, 4),
            (4, 4),
            (4, 5),
            (4, 6),
        }
        off_r, off_c = self.rows // 2 - 2, self.cols // 2 - 3
        return [(off_r + dy, off_c + dx) for dy, dx in mold]

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Draw pixel in buffer."""
        if 0 <= x < self.w_win and 0 <= y < self.h_win:
            pos = (y * self.line) + (x * 4)
            self.addr[pos] = color & 0xFF
            self.addr[pos + 1] = (color >> 8) & 0xFF
            self.addr[pos + 2] = (color >> 16) & 0xFF
            self.addr[pos + 3] = 255

    def draw_tile(self, tx: int, ty: int, val: int) -> None:
        """Draw tile. If part of 42, draw as solid block."""
        x0, y0 = tx * self.tile, ty * self.tile

        if (ty, tx) in self.mold_positions:
            for i in range(self.tile):
                for j in range(self.tile):
                    self.put_pixel(x0 + i, y0 + j, 0x333333)  # Solid Gray
            return

        # Regular background and walls
        for i in range(self.tile):
            for j in range(self.tile):
                self.put_pixel(x0 + i, y0 + j, 0x000000)

        w, color = 2, 0xFFFFFF
        if val & 1:  # N
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + j, color)
        if val & 2:  # E
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + self.tile - 1 - i, y0 + j, color)
        if val & 4:  # S
            for i in range(self.tile):
                for j in range(w):
                    self.put_pixel(x0 + i, y0 + self.tile - 1 - j, color)
        if val & 8:  # W
            for i in range(w):
                for j in range(self.tile):
                    self.put_pixel(x0 + i, y0 + j, color)

    def draw_path(self) -> None:
        """Trace solution path."""
        cr, cc = self.entry
        self.fill_rect(cc, cr, 0xFF0000)
        for move in self.path:
            if move == "N":
                cr -= 1
            elif move == "S":
                cr += 1
            elif move == "E":
                cc += 1
            elif move == "W":
                cc -= 1
            self.fill_rect(cc, cr, 0xFF0000)

    def fill_rect(self, col: int, row: int, color: int) -> None:
        """Helper for path squares."""
        m = self.tile // 4
        x0, y0 = col * self.tile + m, row * self.tile + m
        s = self.tile - (m * 2)
        for i in range(s):
            for j in range(s):
                self.put_pixel(x0 + i, y0 + j, color)

    def render(self, *args: Any) -> int:
        """Render frame."""
        try:
            for y in range(self.rows):
                for x in range(self.cols):
                    self.draw_tile(x, y, self.maze[y][x])
            if self.path:
                self.draw_path()
            self.m.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)
        except Exception:
            os._exit(0)
        return 0

    def run(self) -> None:
        """Start MLX loop."""
        self.m.mlx_key_hook(
            self.win, lambda k, p: os._exit(0) if k in [65307, 53] else 0, None
        )
        self.m.mlx_loop_hook(self.ptr, self.render, None)
        self.m.mlx_loop(self.ptr)
