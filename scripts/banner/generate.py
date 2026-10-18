"""
Master generator script for The Great Wave GitHub Profile identity assets.
Produces animated GIFs (dark & light), vector SMIL SVGs, fallback snapshots,
and technical wave section dividers.
"""
import os
import sys
import shutil
import argparse
import time

from .config import BannerConfig, DARK_THEME, LIGHT_THEME
from .export_gif import export_animated_gif
from .export_svg import export_vector_svg

def generate_section_divider(output_path: str, is_dark: bool = True) -> str:
    """Generate subtle wave / dot-matrix technical section divider."""
    bg_hex = "#080D16" if is_dark else "#F5F9FD"
    line_hex = "#153C65" if is_dark else "#B8D5ED"
    dot_hex = "#5FA8E8" if is_dark else "#185B93"
    white_hex = "#FFFFFF" if is_dark else "#0B2545"
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 24" width="100%" height="24">
  <defs>
    <linearGradient id="divGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{line_hex}" stop-opacity="0.1"/>
      <stop offset="25%" stop-color="{line_hex}" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="{dot_hex}" stop-opacity="1.0"/>
      <stop offset="75%" stop-color="{line_hex}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{line_hex}" stop-opacity="0.1"/>
    </linearGradient>
  </defs>
  <!-- Fine base axis -->
  <line x1="40" y1="12" x2="860" y2="12" stroke="url(#divGrad)" stroke-width="1"/>
  <!-- Center wave crest points -->
  <path d="M 410 12 Q 430 4, 450 12 T 490 12" fill="none" stroke="{dot_hex}" stroke-width="1.5"/>
  <circle cx="450" cy="12" r="3" fill="{white_hex}"/>
  <circle cx="430" cy="8" r="1.5" fill="{dot_hex}"/>
  <circle cx="470" cy="16" r="1.5" fill="{dot_hex}"/>
  <!-- Crosshairs -->
  <line x1="38" y1="7" x2="38" y2="17" stroke="{dot_hex}" stroke-width="1"/>
  <line x1="862" y1="7" x2="862" y2="17" stroke="{dot_hex}" stroke-width="1"/>
</svg>"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate Great Wave animated assets for santi-osp profile.")
    parser.add_argument("--format", choices=["all", "gif", "svg"], default="all", help="Output format(s)")
    parser.add_argument("--theme", choices=["all", "dark", "light"], default="all", help="Theme(s) to render")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second for GIF")
    parser.add_argument("--duration", type=float, default=6.0, help="Cycle duration in seconds")
    parser.add_argument("--colors", type=int, default=128, help="Number of quantized colors for GIF")
    parser.add_argument("--output-dir", default="assets/readme", help="Target output directory")
    args = parser.parse_args()

    config = BannerConfig(fps=args.fps, duration=args.duration)
    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 65)
    print("  SANTI.OSP — THE GREAT WAVE // ENGINEERING IN MOTION")
    print("  Generative Braille & Vector Asset Pipeline")
    print(f"  Target: {out_dir}")
    print("=" * 65)
    
    t_start = time.time()
    
    # 1. SVGs
    if args.format in ["all", "svg"]:
        if args.theme in ["all", "dark"]:
            export_vector_svg(os.path.join(out_dir, "wave-dark.svg"), DARK_THEME, config)
        if args.theme in ["all", "light"]:
            export_vector_svg(os.path.join(out_dir, "wave-light.svg"), LIGHT_THEME, config)

    # 2. GIFs
    if args.format in ["all", "gif"]:
        if args.theme in ["all", "dark"]:
            dark_gif = os.path.join(out_dir, "wave-dark.gif")
            fallback_png = os.path.join(out_dir, "wave-fallback.png")
            export_animated_gif(dark_gif, DARK_THEME, config, colors=args.colors, save_fallback_png=fallback_png)
            # Create wave-animated.gif copy for direct standard embeds
            shutil.copyfile(dark_gif, os.path.join(out_dir, "wave-animated.gif"))
            print(f"Copied {dark_gif} -> {os.path.join(out_dir, 'wave-animated.gif')}")

        if args.theme in ["all", "light"]:
            light_gif = os.path.join(out_dir, "wave-light.gif")
            export_animated_gif(light_gif, LIGHT_THEME, config, colors=args.colors)

    # 3. Section Dividers
    sep_dir = os.path.join(out_dir, "separators")
    generate_section_divider(os.path.join(sep_dir, "wave-divider-dark.svg"), is_dark=True)
    generate_section_divider(os.path.join(sep_dir, "wave-divider-light.svg"), is_dark=False)
    print("Generated section dividers in separators/")

    elapsed = time.time() - t_start
    print("=" * 65)
    print(f"Pipeline completed successfully in {elapsed:.2f}s!")
    print("=" * 65)

if __name__ == "__main__":
    main()
