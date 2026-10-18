"""
Configuration parameters for The Great Wave banner generator.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_str = hex_str.lstrip('#')
    return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

@dataclass
class ThemeColors:
    bg: Tuple[int, int, int]
    panel_bg: Tuple[int, int, int]
    deep_water: Tuple[int, int, int]
    mid_water: Tuple[int, int, int]
    ocean_blue: Tuple[int, int, int]
    soft_blue: Tuple[int, int, int]
    ice_white: Tuple[int, int, int]
    pure_white: Tuple[int, int, int]
    fuji_dark: Tuple[int, int, int]
    fuji_snow: Tuple[int, int, int]
    boat_wood: Tuple[int, int, int]
    text_primary: Tuple[int, int, int]
    text_muted: Tuple[int, int, int]
    text_accent: Tuple[int, int, int]
    grid_line: Tuple[int, int, int]
    border: Tuple[int, int, int]

DARK_THEME = ThemeColors(
    bg=hex_to_rgb("#080D16"),           # Obsidian base
    panel_bg=hex_to_rgb("#0B1626"),     # Midnight Navy
    deep_water=hex_to_rgb("#102A46"),   # Deep Ocean
    mid_water=hex_to_rgb("#153C65"),    # Prussian Blue
    ocean_blue=hex_to_rgb("#2563A6"),   # Ocean Blue
    soft_blue=hex_to_rgb("#5FA8E8"),    # Soft Blue accent
    ice_white=hex_to_rgb("#D6ECFF"),    # Ice White foam
    pure_white=hex_to_rgb("#FFFFFF"),   # Pure White crests & spray
    fuji_dark=hex_to_rgb("#1B263B"),    # Fuji silhouette
    fuji_snow=hex_to_rgb("#E0E1DD"),    # Fuji snowcap
    boat_wood=hex_to_rgb("#4A5568"),    # Fishing boat hull
    text_primary=hex_to_rgb("#FFFFFF"),
    text_muted=hex_to_rgb("#5FA8E8"),
    text_accent=hex_to_rgb("#2563A6"),
    grid_line=hex_to_rgb("#102238"),
    border=hex_to_rgb("#1B3A60")
)

LIGHT_THEME = ThemeColors(
    bg=hex_to_rgb("#F5F9FD"),           # Soft Paper White
    panel_bg=hex_to_rgb("#EBF3FA"),     # Mist Blue
    deep_water=hex_to_rgb("#0B2545"),   # Deep Navy
    mid_water=hex_to_rgb("#153C65"),    # Prussian Blue
    ocean_blue=hex_to_rgb("#185B93"),   # Ocean Blue
    soft_blue=hex_to_rgb("#2563A6"),    # Vibrant blue accent
    ice_white=hex_to_rgb("#4A7BA8"),    # Visible foam line
    pure_white=hex_to_rgb("#081A30"),   # High-contrast foam dots
    fuji_dark=hex_to_rgb("#8DA9C4"),    # Fuji silhouette
    fuji_snow=hex_to_rgb("#EEF4F8"),    # Fuji snowcap
    boat_wood=hex_to_rgb("#627D98"),    # Fishing boat hull
    text_primary=hex_to_rgb("#0B2545"),
    text_muted=hex_to_rgb("#185B93"),
    text_accent=hex_to_rgb("#2563A6"),
    grid_line=hex_to_rgb("#D2E3F3"),
    border=hex_to_rgb("#B8D5ED")
)

@dataclass
class BannerConfig:
    width: int = 1280
    height: int = 420
    cols: int = 128
    rows: int = 26
    fps: int = 10
    duration: float = 6.0  # 60 frames = 6s loop
    seed: int = 42
    developer_name: str = "SANTIAGO OSPINA ARANGO"
    role_title: str = "SOFTWARE DEVELOPER"
    specialties: str = ".NET / ANGULAR / AZURE / AUTOMATION"
    sub_concept: str = "ENGINEERING IN MOTION"
    location: str = "MEDELLIN, CO [06°14'N 75°34'W]"
    status_tag: str = "SYSTEM STATUS: NOMINAL // CORE: READY"
    
    # Ramps
    ascii_ramp: str = " .`^:;irsXA253hMHGS#9B&@"
    edge_chars: Tuple[str, str, str, str] = ("|", "\\", "-", "/")
