# Banner Generation Guide: The Great Wave
**Target Repository:** `santi-osp/santi-osp` | **Platform:** Windows 11 / Linux / macOS  
**Document Code:** `OPS-GW-003` | **Runtime:** Python 3.10+ (Tested on Python 3.14.0)

---

## 1. Prerequisites

The banner pipeline is completely self-contained. It requires:
- **Python 3.10+** (standard CPython distribution)
- **Pillow** ($\ge 10.0.0$)
- **NumPy** ($\ge 1.24.0$)
- **Cascadia Mono / Cascadia Code font** (standard on Windows 11; fallback included)

---

## 2. Setup on Windows 11

### Step 1: Open PowerShell in Repository Root
```powershell
cd "C:\Users\santi\Documents\0 REPOSITORIOS\santi-osp"
```

### Step 2: (Optional) Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r scripts\banner\requirements.txt
```

---

## 3. Regenerating Assets

### Standard Generation (All Assets)
To regenerate all assets (Dark & Light animated GIFs, SMIL vector SVGs, fallback snapshots, and dividers):
```powershell
python -m scripts.banner.generate
```

### CLI Configuration Flags

| Flag | Default | Description |
|---|---|---|
| `--format` | `all` | Choose `all`, `gif`, or `svg` |
| `--theme` | `all` | Choose `all`, `dark`, or `light` |
| `--fps` | `10` | Frame rate for animated GIF (10 fps recommended) |
| `--duration` | `6.0` | Cycle duration in seconds (must divide particle lifetime evenly for seamless loop) |
| `--colors` | `128` | Number of quantized palette colors (64–128 ensures <1MB size) |
| `--output-dir` | `assets/readme` | Directory where assets will be written |

### Examples

**Generate only dark theme GIF:**
```powershell
python -m scripts.banner.generate --format gif --theme dark
```

**Generate ultra-high fidelity 12 fps GIF:**
```powershell
python -m scripts.banner.generate --format gif --fps 12 --duration 6.0 --colors 128
```

**Generate only vector SVGs:**
```powershell
python -m scripts.banner.generate --format svg
```

---

## 4. Customizing Parameters

### Modifying Colors & Themes
Open `scripts/banner/config.py` to edit hex codes in `DARK_THEME` or `LIGHT_THEME`:
```python
DARK_THEME = ThemeColors(
    bg=hex_to_rgb("#080D16"),         # Background
    ocean_blue=hex_to_rgb("#2563A6"), # Wave crests
    soft_blue=hex_to_rgb("#5FA8E8"),  # Accents & telemetry
    ...
)
```

### Modifying Identity Text
In `scripts/banner/config.py`, modify fields in `BannerConfig`:
```python
@dataclass
class BannerConfig:
    developer_name: str = "SANTIAGO OSPINA ARANGO"
    role_title: str = "SOFTWARE DEVELOPER"
    specialties: str = ".NET / ANGULAR / AZURE / AUTOMATION"
    sub_concept: str = "ENGINEERING IN MOTION"
    location: str = "MEDELLIN, CO [06°14'N 75°34'W]"
```

---

## 5. Running Automated Tests

Run the full verification test suite:
```powershell
python -m unittest tests/test_banner.py
```
This runs 7 automated unit tests checking:
- Mathematical determinism
- Exact loop continuity ($\Delta = 0$ difference between frame 0 and frame 60)
- Braille sub-pixel mapping
- SVG XML schema and absence of scripts
- GIF dimensions, frame rate, and file size limits
- Fallback PNG integrity
- Security scan for accidental token leaks

---

## 6. Troubleshooting

### Issue: Characters appear as square tofu boxes `[?]`
- **Cause:** Selected font lacks the Unicode Braille Patterns block (`U+2800..U+28FF`).
- **Fix:** On Windows, ensure Cascadia Mono is installed (`C:\Windows\Fonts\CascadiaMono.ttf`). The script automatically selects Cascadia Mono, Cascadia Code, MS Gothic, or Segoe UI.

### Issue: GIF loop exhibits a visual jump at frame 60
- **Cause:** Particle lifetime doesn't divide cycle duration evenly.
- **Fix:** In `scripts/banner/wave_math.py`, ensure `particle_lifetime` divides `duration` evenly (e.g. `6.0 / 1.5 = 4` exact cycles).
