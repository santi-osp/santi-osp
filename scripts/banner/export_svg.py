"""
SVG banner exporter with pure SMIL declarative animation.
Generates ultra-lean (<45 KB), self-contained vector banners compliant with GitHub Camo proxy.
Supports Dark and Light themes with animated status beacons and wave motion.
"""
import os
import math
from typing import Optional
from .config import BannerConfig, DARK_THEME, LIGHT_THEME, ThemeColors
from .wave_math import WaveSceneModel

def rgb_to_hex(rgb: tuple) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def export_vector_svg(output_path: str, theme: ThemeColors, config: Optional[BannerConfig] = None) -> str:
    """
    Export self-contained animated SVG with pure SMIL (no JS, no external CSS).
    """
    config = config or BannerConfig()
    wave_model = WaveSceneModel(duration=config.duration)
    
    # Evaluate representative scene state
    scene = wave_model.evaluate(1.5, config.width, config.height)
    
    bg_hex = rgb_to_hex(theme.bg)
    panel_hex = rgb_to_hex(theme.panel_bg)
    border_hex = rgb_to_hex(theme.border)
    grid_hex = rgb_to_hex(theme.grid_line)
    text_pri_hex = rgb_to_hex(theme.text_primary)
    text_muted_hex = rgb_to_hex(theme.text_muted)
    text_acc_hex = rgb_to_hex(theme.text_accent)
    deep_hex = rgb_to_hex(theme.deep_water)
    mid_hex = rgb_to_hex(theme.mid_water)
    ocean_hex = rgb_to_hex(theme.ocean_blue)
    soft_hex = rgb_to_hex(theme.soft_blue)
    ice_hex = rgb_to_hex(theme.ice_white)
    white_hex = rgb_to_hex(theme.pure_white)
    fuji_dark_hex = rgb_to_hex(theme.fuji_dark)
    fuji_snow_hex = rgb_to_hex(theme.fuji_snow)
    boat_hex = rgb_to_hex(theme.boat_wood)

    W = config.width
    H = config.height

    # Convert wave points to SVG path strings
    def pts_to_d(pts):
        if not pts:
            return ""
        d = [f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"]
        for p in pts[1:]:
            d.append(f"L {p[0]:.1f} {p[1]:.1f}")
        return " ".join(d)

    # 1. Background Grid Lines
    grid_lines = []
    for x in range(0, W, 40):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{grid_hex}" stroke-width="1"/>')
    for y in range(0, H, 35):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{grid_hex}" stroke-width="1"/>')

    # 2. Fuji Path
    fuji_d = pts_to_d(scene['fuji']['poly']) + " Z"
    snow_d = pts_to_d(scene['fuji']['snow']) + " Z"

    # 3. Wave Body Paths
    wb_d = pts_to_d(scene['wave_body']) + " Z"
    outer_d = pts_to_d(scene['outer_curve'])
    lip_d = pts_to_d(scene['lip_curve'])
    
    # 4. Ink Grooves Paths
    groove_paths = []
    for g in scene['ink_grooves']:
        groove_paths.append(f'<path d="{pts_to_d(g)}" stroke="{deep_hex}" stroke-width="2" fill="none" opacity="0.8"/>')
    for c in scene['cyan_highlights']:
        groove_paths.append(f'<path d="{pts_to_d(c)}" stroke="{soft_hex}" stroke-width="1.2" fill="none" opacity="0.65"/>')

    # 5. Foam Claws
    claw_paths = []
    for claw in scene['foam_claws']:
        c_main_d = pts_to_d(claw['main'])
        claw_paths.append(f'<path d="{c_main_d}" stroke="{white_hex}" stroke-width="2.5" fill="none"/>')
        sp1 = claw['spur1']
        claw_paths.append(f'<line x1="{sp1[0][0]:.1f}" y1="{sp1[0][1]:.1f}" x2="{sp1[1][0]:.1f}" y2="{sp1[1][1]:.1f}" stroke="{ice_hex}" stroke-width="1.5"/>')

    # 6. Spray Droplets
    spray_svg = []
    for px, py, rad, intensity in scene['spray_particles']:
        c_fill = white_hex if intensity > 0.4 else ice_hex
        op = max(0.3, intensity)
        spray_svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rad:.1f}" fill="{c_fill}" opacity="{op:.2f}"/>')

    # 7. Foreground Swell & Boats
    swell_paths = [f'<path d="{pts_to_d(r)}" stroke="{ice_hex}" stroke-width="2" fill="none"/>' for r in scene['foreground_rollers']]
    boat_svg = []
    for boat in scene['boats']:
        b_d = pts_to_d(boat['hull']) + " Z"
        boat_svg.append(f'<path d="{b_d}" fill="{boat_hex}" stroke="{border_hex}" stroke-width="1"/>')
        for rx, ry in boat['rowers']:
            boat_svg.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="2" fill="{ice_hex}"/>')

    # Panel Coordinates
    px0, py0, px1, py1 = 36, 32, 510, H - 32
    panel_w = px1 - px0
    panel_h = py1 - py0

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto"
     font-family="Cascadia Mono, Consolas, 'SF Mono', Menlo, Monaco, monospace">
  <defs>
    <linearGradient id="waveGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{ocean_hex}"/>
      <stop offset="50%" stop-color="{mid_hex}"/>
      <stop offset="100%" stop-color="{deep_hex}"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{panel_hex}" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="{panel_hex}" stop-opacity="0.88"/>
    </linearGradient>
  </defs>

  <!-- Background Canvas -->
  <rect width="{W}" height="{H}" fill="{bg_hex}"/>
  
  <!-- Technical Grid -->
  <g opacity="0.6">
    {"".join(grid_lines)}
  </g>

  <!-- Calibration Crosshairs -->
  <g stroke="{border_hex}" stroke-width="1">
    <line x1="6" y1="16" x2="26" y2="16"/>
    <line x1="16" y1="6" x2="16" y2="26"/>
    <line x1="{W-26}" y1="16" x2="{W-6}" y2="16"/>
    <line x1="{W-16}" y1="6" x2="{W-16}" y2="26"/>
    <line x1="6" y1="{H-16}" x2="26" y2="{H-16}"/>
    <line x1="16" y1="{H-26}" x2="16" y2="{H-6}"/>
    <line x1="{W-26}" y1="{H-16}" x2="{W-6}" y2="{H-16}"/>
    <line x1="{W-16}" y1="{H-26}" x2="{W-16}" y2="{H-6}"/>
  </g>

  <!-- Animated Wave Scene Group with Harmonic Breathing -->
  <g>
    <animateTransform attributeName="transform" type="translate"
      values="0 0; 0 -4; 0 3; 0 0" dur="6s" repeatCount="indefinite" calcMode="spline"
      keySplines="0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"/>

    <!-- Background Landmark: Mount Fuji -->
    <path d="{fuji_d}" fill="{fuji_dark_hex}"/>
    <path d="{snow_d}" fill="{fuji_snow_hex}"/>

    <!-- Wave Body -->
    <path d="{wb_d}" fill="url(#waveGrad)" stroke="{ocean_hex}" stroke-width="1"/>
    
    <!-- Water Contours & Grooves -->
    {"".join(groove_paths)}

    <!-- Lip & Outer Edge White Crests -->
    <path d="{outer_d}" stroke="{ice_hex}" stroke-width="3" fill="none"/>
    <path d="{lip_d}" stroke="{white_hex}" stroke-width="3.5" fill="none"/>

    <!-- Articulating Claws -->
    {"".join(claw_paths)}

    <!-- Ballistic Spray Droplets -->
    {"".join(spray_svg)}

    <!-- Rollers and Boats -->
    {"".join(swell_paths)}
    {"".join(boat_svg)}
  </g>

  <!-- Left Identity Editorial Card -->
  <rect x="{px0}" y="{py0}" width="{panel_w}" height="{panel_h}" rx="8"
        fill="url(#panelGrad)" stroke="{border_hex}" stroke-width="1"/>

  <!-- Card Top Status Bar -->
  <line x1="{px0}" y1="{py0 + 34}" x2="{px1}" y2="{py0 + 34}" stroke="{border_hex}" stroke-width="1"/>

  <!-- Pulsing Active Status Beacon (Pure SMIL) -->
  <circle cx="{px0 + 20}" cy="{py0 + 17}" r="4" fill="{soft_hex}">
    <animate attributeName="fill" values="{soft_hex};{white_hex};{soft_hex}" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="r" values="3.5;5;3.5" dur="2s" repeatCount="indefinite"/>
  </circle>
  
  <text x="{px0 + 32}" y="{py0 + 21}" fill="{text_muted_hex}" font-size="11" letter-spacing="0.5">SYS // SANTI.OSP // RUNNING</text>
  <text x="{px1 - 138}" y="{py0 + 21}" fill="{text_muted_hex}" font-size="11">CORE: ACTIVE 01</text>

  <!-- Name & Professional Title -->
  <text x="{px0 + 20}" y="{py0 + 68}" fill="{text_pri_hex}" font-size="19" font-weight="bold" letter-spacing="0.5">{config.developer_name}</text>
  <text x="{px0 + 20}" y="{py0 + 96}" fill="{text_acc_hex}" font-size="13" font-weight="bold" letter-spacing="1">{config.role_title}</text>

  <!-- Divider Line -->
  <line x1="{px0 + 20}" y1="{py0 + 112}" x2="{px1 - 20}" y2="{py0 + 112}" stroke="{border_hex}" stroke-width="1"/>
  <line x1="{px0 + 20}" y1="{py0 + 112}" x2="{px0 + 80}" y2="{py0 + 112}" stroke="{soft_hex}" stroke-width="2"/>

  <!-- Stack Architecture -->
  <text x="{px0 + 20}" y="{py0 + 130}" fill="{text_muted_hex}" font-size="11" letter-spacing="0.5">STACK ARCHITECTURE</text>
  <text x="{px0 + 20}" y="{py0 + 152}" fill="{text_pri_hex}" font-size="13" font-weight="bold">.NET · Angular · Azure · SQL Server</text>
  <text x="{px0 + 20}" y="{py0 + 174}" fill="{text_muted_hex}" font-size="11">Azure Functions · Azure DevOps · Enterprise AI</text>

  <!-- Divider 2 -->
  <line x1="{px0 + 20}" y1="{py0 + 196}" x2="{px1 - 20}" y2="{py0 + 196}" stroke="{border_hex}" stroke-width="1"/>

  <!-- Telemetry Block -->
  <text x="{px0 + 20}" y="{py0 + 214}" fill="{text_muted_hex}" font-size="11">LOC: {config.location}</text>
  <text x="{px0 + 20}" y="{py0 + 236}" fill="{soft_hex}" font-size="11">ART: THE GREAT WAVE // {config.sub_concept}</text>
  <text x="{px0 + 20}" y="{py0 + 258}" fill="{text_muted_hex}" font-size="11">SYSTEM: PURE SMIL VECTOR // 6.0s HARMONIC LOOP</text>

  <!-- Card Footer -->
  <line x1="{px0}" y1="{py1 - 36}" x2="{px1}" y2="{py1 - 36}" stroke="{border_hex}" stroke-width="1"/>
  <text x="{px0 + 20}" y="{py1 - 14}" fill="{text_muted_hex}" font-size="11">GITHUB: github.com/santi-osp</text>
  <text x="{px1 - 135}" y="{py1 - 14}" fill="{text_acc_hex}" font-size="11">[SEC: VERIFIED]</text>

  <!-- Outer Telemetry Tag -->
  <text x="{W - 250}" y="{H - 24}" fill="{text_muted_hex}" font-size="11">HOKUSAI x GENERATIVE CODE</text>
</svg>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    file_size_kb = os.path.getsize(output_path) / 1024.0
    print(f"Exported Vector SVG: {output_path} ({file_size_kb:.1f} KB)")
    return output_path

if __name__ == "__main__":
    export_vector_svg("assets/readme/wave-dark.svg", DARK_THEME)
    export_vector_svg("assets/readme/wave-light.svg", LIGHT_THEME)
