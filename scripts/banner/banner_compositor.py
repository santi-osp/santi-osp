"""
Banner compositor: combines mathematical wave dynamics with software engineering typography
and renders high-definition Pillow image frames using Cascadia Mono Braille.
"""
import os
import math
from typing import Dict, Any, Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont

from .config import ThemeColors, BannerConfig, DARK_THEME, LIGHT_THEME
from .wave_math import WaveSceneModel
from .rasterizer import SubPixelCanvas

# Palette indices
C_EMPTY = 0
C_DEEP = 1
C_MID = 2
C_OCEAN = 3
C_SOFT = 4
C_ICE = 5
C_PURE = 6
C_FUJI_DARK = 7
C_FUJI_SNOW = 8
C_BOAT = 9

def get_monospace_font(size: int = 14) -> ImageFont.ImageFont:
    """Find the best available developer monospace font supporting Braille."""
    font_candidates = [
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/CascadiaCode.ttf",
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_bold_font(size: int = 16) -> ImageFont.ImageFont:
    bold_candidates = [
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/CascadiaCode.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]
    for path in bold_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return get_monospace_font(size)

class BannerCompositor:
    """Generates complete frames combining Braille wave dynamics with editorial typography."""

    def __init__(self, config: Optional[BannerConfig] = None, theme: Optional[ThemeColors] = None):
        self.config = config or BannerConfig()
        self.theme = theme or DARK_THEME
        self.wave_model = WaveSceneModel(duration=self.config.duration)
        self.sub_canvas = SubPixelCanvas(cols=self.config.cols, rows=self.config.rows)
        
        self.palette = {
            C_EMPTY: self.theme.bg,
            C_DEEP: self.theme.deep_water,
            C_MID: self.theme.mid_water,
            C_OCEAN: self.theme.ocean_blue,
            C_SOFT: self.theme.soft_blue,
            C_ICE: self.theme.ice_white,
            C_PURE: self.theme.pure_white,
            C_FUJI_DARK: self.theme.fuji_dark,
            C_FUJI_SNOW: self.theme.fuji_snow,
            C_BOAT: self.theme.boat_wood
        }

        self.font_braille = get_monospace_font(14)
        self.font_main = get_monospace_font(13)
        self.font_title = get_bold_font(17)
        self.font_subtitle = get_bold_font(12)
        self.font_small = get_monospace_font(11)

    def render_wave_to_subcanvas(self, scene: Dict[str, Any]):
        """Render all wave scene geometry into the sub-pixel dot buffer."""
        self.sub_canvas.clear()
        
        w_px = float(self.config.width)
        h_px = float(self.config.height)
        sx = float(self.sub_canvas.dot_w) / w_px
        sy = float(self.sub_canvas.dot_h) / h_px

        def map_pt(p: Tuple[float, float]) -> Tuple[float, float]:
            return (p[0] * sx, p[1] * sy)

        def map_pts(pts: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
            return [(p[0] * sx, p[1] * sy) for p in pts]

        # 1. Background Swells (z=1)
        for pts in scene['background_swells']:
            self.sub_canvas.draw_curve(map_pts(pts), C_MID, stroke=1.0, z=1)

        # 2. Mount Fuji (z=2, z=3)
        f_poly = map_pts(scene['fuji']['poly'])
        f_snow = map_pts(scene['fuji']['snow'])
        self.sub_canvas.draw_polygon(f_poly, C_FUJI_DARK, z=2)
        self.sub_canvas.draw_polygon(f_snow, C_FUJI_SNOW, z=3)

        # 3. Main Wave Body Polygon with depth gradient (z=4)
        wb_poly = map_pts(scene['wave_body'])
        self.sub_canvas.draw_polygon(wb_poly, C_MID, z=4, is_wave_gradient=True)

        # 4. Secondary Companion Wave (z=4)
        if 'secondary_wave' in scene:
            sec_poly = map_pts(scene['secondary_wave'])
            self.sub_canvas.draw_polygon(sec_poly, C_MID, z=4, is_wave_gradient=True)
            if 'secondary_claws' in scene:
                for sc in scene['secondary_claws']:
                    self.sub_canvas.draw_curve(map_pts(sc['main']), C_ICE, stroke=1.2, z=5)

        # 5. Ink Grooves (z=5) & Cyan highlights (z=6)
        for g_pts in scene['ink_grooves']:
            self.sub_canvas.draw_curve(map_pts(g_pts), C_DEEP, stroke=1.3, z=5)
        for c_pts in scene['cyan_highlights']:
            self.sub_canvas.draw_curve(map_pts(c_pts), C_SOFT, stroke=1.1, z=6)

        # 6. Foam Veins underside barrel (z=7)
        for v_pts in scene['foam_veins']:
            self.sub_canvas.draw_curve(map_pts(v_pts), C_ICE, stroke=1.4, z=7)

        # 7. Outer flank & Lip curves (z=8)
        self.sub_canvas.draw_curve(map_pts(scene['outer_curve']), C_ICE, stroke=1.8, z=8)
        self.sub_canvas.draw_curve(map_pts(scene['lip_curve']), C_PURE, stroke=2.0, z=8)

        # 8. Articulating Foam Claws (z=9)
        for claw in scene['foam_claws']:
            self.sub_canvas.draw_curve(map_pts(claw['main']), C_PURE, stroke=1.6, z=9)
            sp1 = claw['spur1']
            self.sub_canvas.draw_line(sp1[0][0]*sx, sp1[0][1]*sy, sp1[1][0]*sx, sp1[1][1]*sy, C_ICE, stroke=1.2, z=9)
            sp2 = claw['spur2']
            self.sub_canvas.draw_line(sp2[0]*sx, sp2[1]*sy, sp2[2][0]*sx, sp2[2][1]*sy, C_PURE, stroke=1.2, z=9)
            if 'spur3' in claw:
                sp3 = claw['spur3']
                self.sub_canvas.draw_line(sp3[0][0]*sx, sp3[0][1]*sy, sp3[1][0]*sx, sp3[1][1]*sy, C_ICE, stroke=1.0, z=9)

        # 9. Ballistic Spray Particles (z=10)
        for px, py, rad, intensity in scene['spray_particles']:
            cid = C_PURE if intensity > 0.4 else C_ICE
            self.sub_canvas.draw_disc(px * sx, py * sy, rad * sx * 0.9, cid, z=10)

        # 10. Foreground Swells (z=11)
        for r_pts in scene['foreground_rollers']:
            self.sub_canvas.draw_curve(map_pts(r_pts), C_ICE, stroke=1.5, z=11)

        # 11. Fishing Boats (z=12)
        for boat in scene['boats']:
            hull = map_pts(boat['hull'])
            self.sub_canvas.draw_polygon(hull, C_BOAT, z=12)
            for rx, ry in boat['rowers']:
                self.sub_canvas.draw_disc(rx * sx, ry * sy, 1.3, C_ICE, z=12)

    def compose_frame(self, t: float) -> Image.Image:
        """Compose and return a complete rendered frame at time t."""
        W = self.config.width
        H = self.config.height
        
        # 1. Evaluate Wave Scene
        scene = self.wave_model.evaluate(t, W, H)
        self.render_wave_to_subcanvas(scene)
        grid = self.sub_canvas.to_braille_grid(self.palette)

        # 2. Create Base Image Canvas
        img = Image.new("RGB", (W, H), self.theme.bg)
        draw = ImageDraw.Draw(img)

        # 3. Draw Background Coordinate / Technical Grid Lines
        grid_step_x = 40
        grid_step_y = 35
        for gx in range(0, W, grid_step_x):
            draw.line([(gx, 0), (gx, H)], fill=self.theme.grid_line, width=1)
        for gy in range(0, H, grid_step_y):
            draw.line([(0, gy), (W, gy)], fill=self.theme.grid_line, width=1)

        # Corner calibration crosshairs
        ch_len = 10
        corners = [(16, 16), (W - 16, 16), (16, H - 16), (W - 16, H - 16)]
        for cx, cy in corners:
            draw.line([(cx - ch_len, cy), (cx + ch_len, cy)], fill=self.theme.border, width=1)
            draw.line([(cx, cy - ch_len), (cx, cy + ch_len)], fill=self.theme.border, width=1)

        # 4. Render Braille Character Grid
        cell_w = W / float(self.config.cols)
        cell_h = H / float(self.config.rows)
        text_zone_cols = 48
        
        for r_idx in range(self.config.rows):
            y_pos = r_idx * cell_h
            for c_idx in range(self.config.cols):
                cell = grid[r_idx][c_idx]
                if cell['bits'] != 0:
                    x_pos = c_idx * cell_w
                    if c_idx < text_zone_cols:
                        orig_c = cell['color']
                        dimmed = (
                            int(orig_c[0] * 0.18 + self.theme.panel_bg[0] * 0.82),
                            int(orig_c[1] * 0.18 + self.theme.panel_bg[1] * 0.82),
                            int(orig_c[2] * 0.18 + self.theme.panel_bg[2] * 0.82),
                        )
                        draw.text((x_pos, y_pos), cell['char'], font=self.font_braille, fill=dimmed)
                    else:
                        draw.text((x_pos, y_pos), cell['char'], font=self.font_braille, fill=cell['color'])

        # 5. Render Left Identity Editorial Panel
        panel_x0 = 36
        panel_y0 = 32
        panel_x1 = 510
        panel_y1 = H - 32

        panel_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(panel_overlay)
        p_bg_rgba = (*self.theme.panel_bg, 226)  # ~89% opacity
        p_draw.rounded_rectangle([panel_x0, panel_y0, panel_x1, panel_y1], radius=8, fill=p_bg_rgba, outline=(*self.theme.border, 255), width=1)
        img.paste(panel_overlay, (0, 0), mask=panel_overlay)
        draw = ImageDraw.Draw(img)

        # Panel outline
        draw.rounded_rectangle([panel_x0, panel_y0, panel_x1, panel_y1], radius=8, outline=self.theme.border, width=1)

        # Header status divider
        draw.line([(panel_x0, panel_y0 + 34), (panel_x1, panel_y0 + 34)], fill=self.theme.border, width=1)
        
        # Pulsing status beacon
        pulse_phase = math.sin(t * 2.0 * math.pi / 2.0)
        dot_color = self.theme.pure_white if pulse_phase > 0 else self.theme.soft_blue
        draw.ellipse([panel_x0 + 16, panel_y0 + 13, panel_x0 + 24, panel_y0 + 21], fill=dot_color)
        draw.text((panel_x0 + 32, panel_y0 + 10), "SYS // SANTI.OSP // RUNNING", font=self.font_small, fill=self.theme.text_muted)
        draw.text((panel_x1 - 138, panel_y0 + 10), "CORE: ACTIVE 01", font=self.font_small, fill=self.theme.text_muted)

        # Developer Name
        draw.text((panel_x0 + 20, panel_y0 + 52), self.config.developer_name, font=self.font_title, fill=self.theme.text_primary)

        # Professional Role
        draw.text((panel_x0 + 20, panel_y0 + 84), self.config.role_title, font=self.font_subtitle, fill=self.theme.text_accent)

        # Fine Accent Divider
        div_y = panel_y0 + 112
        draw.line([(panel_x0 + 20, div_y), (panel_x1 - 20, div_y)], fill=self.theme.border, width=1)
        draw.line([(panel_x0 + 20, div_y), (panel_x0 + 80, div_y)], fill=self.theme.soft_blue, width=2)

        # Specialties & Core Tech
        draw.text((panel_x0 + 20, panel_y0 + 126), "STACK ARCHITECTURE", font=self.font_small, fill=self.theme.text_muted)
        draw.text((panel_x0 + 20, panel_y0 + 144), ".NET · Angular · Azure · SQL Server", font=self.font_subtitle, fill=self.theme.text_primary)
        draw.text((panel_x0 + 20, panel_y0 + 166), "Azure Functions · Azure DevOps · Enterprise AI", font=self.font_small, fill=self.theme.text_muted)

        # Divider 2
        div_y2 = panel_y0 + 196
        draw.line([(panel_x0 + 20, div_y2), (panel_x1 - 20, div_y2)], fill=self.theme.border, width=1)

        # Telemetry Block
        draw.text((panel_x0 + 20, panel_y0 + 210), f"LOC: {self.config.location}", font=self.font_small, fill=self.theme.text_muted)
        draw.text((panel_x0 + 20, panel_y0 + 232), f"ART: THE GREAT WAVE // {self.config.sub_concept}", font=self.font_small, fill=self.theme.soft_blue)
        draw.text((panel_x0 + 20, panel_y0 + 254), "RES: 256x104 BRAILLE MATRIX // 60 FRAMES (10 FPS)", font=self.font_small, fill=self.theme.text_muted)

        # Card Footer Status Line
        foot_y = panel_y1 - 36
        draw.line([(panel_x0, foot_y), (panel_x1, foot_y)], fill=self.theme.border, width=1)
        draw.text((panel_x0 + 20, foot_y + 11), "GITHUB: github.com/santi-osp", font=self.font_small, fill=self.theme.text_muted)
        draw.text((panel_x1 - 135, foot_y + 11), "[SEC: VERIFIED]", font=self.font_small, fill=self.theme.text_accent)

        # 6. Subtle Outer Wave Watermark / Telemetry Tag on Far Right
        draw.text((W - 250, H - 28), "HOKUSAI x GENERATIVE CODE", font=self.font_small, fill=self.theme.text_muted)

        return img
