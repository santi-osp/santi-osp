"""
Sub-pixel dot-matrix rasterizer for Braille and ASCII rendering.
Converts vector curves, polygons, and particle physics into 2x4 Braille dot matrices.
"""
import math
from typing import List, Tuple, Dict, Optional, Any
from .config import ThemeColors, BannerConfig

Point = Tuple[float, float]

BRAILLE_DOT_MAP = [
    (0, 0, 0x01),
    (0, 1, 0x02),
    (0, 2, 0x04),
    (1, 0, 0x08),
    (1, 1, 0x10),
    (1, 2, 0x20),
    (0, 3, 0x40),
    (1, 3, 0x80)
]

class SubPixelCanvas:
    """A virtual 2D sub-pixel raster buffer."""
    
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.dot_w = cols * 2
        self.dot_h = rows * 4
        self.buffer = [0] * (self.dot_w * self.dot_h)
        self.z_buffer = [0] * (self.dot_w * self.dot_h)

    def clear(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
            self.z_buffer[i] = 0

    def set_dot(self, x: int, y: int, color_id: int, z: int = 1):
        """Set a single sub-dot if within bounds and z >= current z."""
        if 0 <= x < self.dot_w and 0 <= y < self.dot_h:
            idx = y * self.dot_w + x
            if z >= self.z_buffer[idx] or self.buffer[idx] == 0:
                self.buffer[idx] = color_id
                self.z_buffer[idx] = z

    def draw_line(self, x0: float, y0: float, x1: float, y1: float, color_id: int, stroke: float = 1.0, z: int = 1):
        """Draw anti-aliased or thick line on sub-pixel grid using DDA."""
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        steps = max(1, int(dist * 2.0))
        
        nx, ny = 0.0, 0.0
        if dist > 0.001:
            nx = -dy / dist
            ny = dx / dist

        half_s = max(0.0, (stroke - 1.0) * 0.5)
        
        for i in range(steps + 1):
            t = i / steps
            cx = x0 + t * dx
            cy = y0 + t * dy
            
            if half_s <= 0.1:
                self.set_dot(int(round(cx)), int(round(cy)), color_id, z)
            else:
                for off in range(-int(round(half_s)), int(round(half_s)) + 1):
                    self.set_dot(int(round(cx + off * nx)), int(round(cy + off * ny)), color_id, z)

    def draw_curve(self, points: List[Point], color_id: int, stroke: float = 1.0, z: int = 1):
        """Draw piecewise linear polyline."""
        if len(points) < 2:
            return
        for i in range(len(points) - 1):
            self.draw_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], color_id, stroke, z)

    def draw_polygon(self, points: List[Point], color_id: int, z: int = 1, is_wave_gradient: bool = False):
        """Scanline rasterization for convex/concave polygon with optional depth gradient."""
        if len(points) < 3:
            return
        
        min_y = max(0, int(min(p[1] for p in points)))
        max_y = min(self.dot_h - 1, int(max(p[1] for p in points)))
        y_range = max(1.0, float(max_y - min_y))
        
        n = len(points)
        for y in range(min_y, max_y + 1):
            nodes = []
            j = n - 1
            for i in range(n):
                p_i = points[i]
                p_j = points[j]
                if (p_i[1] < y and p_j[1] >= y) or (p_j[1] < y and p_i[1] >= y):
                    x_node = p_i[0] + (y - p_i[1]) / (p_j[1] - p_i[1]) * (p_j[0] - p_i[0])
                    nodes.append(x_node)
                j = i
            
            nodes.sort()
            
            # Determine scanline color if gradient enabled
            cur_color = color_id
            if is_wave_gradient:
                rel_y = (y - min_y) / y_range  # 0 at crest, 1 at bottom
                if rel_y > 0.72:
                    cur_color = 1  # C_DEEP (obsidian/deep ocean)
                elif rel_y > 0.38:
                    cur_color = 2  # C_MID (prussian blue)
                elif rel_y > 0.16:
                    cur_color = 3  # C_OCEAN (ocean blue)
                else:
                    cur_color = 4  # C_SOFT (soft cyan highlight near lip)

            for k in range(0, len(nodes) - 1, 2):
                x_start = max(0, int(math.ceil(nodes[k])))
                x_end = min(self.dot_w - 1, int(math.floor(nodes[k+1])))
                for x in range(x_start, x_end + 1):
                    self.set_dot(x, y, cur_color, z)

    def draw_disc(self, cx: float, cy: float, radius: float, color_id: int, z: int = 1):
        """Draw filled disc."""
        r_int = max(1, int(math.ceil(radius)))
        r_sq = radius * radius
        for dy in range(-r_int, r_int + 1):
            y = int(round(cy + dy))
            if 0 <= y < self.dot_h:
                for dx in range(-r_int, r_int + 1):
                    x = int(round(cx + dx))
                    if 0 <= x < self.dot_w and (dx*dx + dy*dy) <= r_sq:
                        self.set_dot(x, y, color_id, z)

    def to_braille_grid(self, color_palette: Dict[int, Tuple[int, int, int]]) -> List[List[Dict[str, Any]]]:
        """Convert sub-pixel buffer into a 2D matrix of character cells."""
        grid = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                bits = 0
                color_counts = {}
                
                for dx, dy, bit in BRAILLE_DOT_MAP:
                    sub_x = col * 2 + dx
                    sub_y = row * 4 + dy
                    c_id = self.buffer[sub_y * self.dot_w + sub_x]
                    if c_id > 0:
                        bits |= bit
                        color_counts[c_id] = color_counts.get(c_id, 0) + 1
                
                if bits == 0:
                    char = ' '
                    color = color_palette.get(0, (0, 0, 0))
                else:
                    char = chr(0x2800 + bits)
                    best_cid = max(color_counts, key=color_counts.get)
                    color = color_palette.get(best_cid, (255, 255, 255))

                row_cells.append({
                    'char': char,
                    'color': color,
                    'bits': bits
                })
            grid.append(row_cells)
        return grid
