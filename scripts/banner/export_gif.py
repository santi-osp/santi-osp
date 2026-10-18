"""
GIF animation exporter for The Great Wave banner.
Renders 60 deterministic frames at 10 fps, applies adaptive palette quantization,
and saves optimized, seamlessly looping animated GIFs for Dark and Light themes.
"""
import os
import time
from typing import Optional, List
from PIL import Image

from .config import BannerConfig, DARK_THEME, LIGHT_THEME, ThemeColors
from .banner_compositor import BannerCompositor

def export_animated_gif(
    output_path: str,
    theme: ThemeColors,
    config: Optional[BannerConfig] = None,
    colors: int = 128,
    save_fallback_png: Optional[str] = None
) -> str:
    """
    Render and export seamless looping animated GIF.
    Returns the absolute path to the generated GIF.
    """
    config = config or BannerConfig()
    compositor = BannerCompositor(config=config, theme=theme)
    
    total_frames = int(config.fps * config.duration)
    dt = config.duration / float(total_frames)
    frame_duration_ms = int(1000.0 / config.fps)
    
    frames: List[Image.Image] = []
    t_start = time.time()
    print(f"Generating {total_frames} frames ({config.fps} fps, {config.duration}s loop) -> {output_path}...")
    
    fallback_snapshot: Optional[Image.Image] = None
    fallback_frame_idx = int(3.5 * config.fps)  # at t = 3.5s
    
    for i in range(total_frames):
        t = i * dt
        frame = compositor.compose_frame(t)
        if i == fallback_frame_idx and save_fallback_png:
            fallback_snapshot = frame.copy()
        
        # Quantize to adaptive palette with subtle Floyd-Steinberg dithering for smooth gradients
        p_frame = frame.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(p_frame)
        if (i + 1) % 10 == 0 or i == total_frames - 1:
            print(f"  Frame {i+1}/{total_frames} ({((i+1)/total_frames)*100:.0f}%)")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Save optimized GIF with infinite loop
    print("Saving optimized animated GIF...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        optimize=True
    )
    
    elapsed = time.time() - t_start
    file_size_kb = os.path.getsize(output_path) / 1024.0
    print(f"Successfully exported {output_path} ({file_size_kb:.1f} KB) in {elapsed:.2f}s")
    
    if save_fallback_png and fallback_snapshot:
        os.makedirs(os.path.dirname(os.path.abspath(save_fallback_png)), exist_ok=True)
        fallback_snapshot.save(save_fallback_png, optimize=True)
        png_size_kb = os.path.getsize(save_fallback_png) / 1024.0
        print(f"Saved fallback PNG snapshot: {save_fallback_png} ({png_size_kb:.1f} KB)")
        
    return output_path

if __name__ == "__main__":
    export_animated_gif("assets/readme/wave-dark.gif", DARK_THEME, save_fallback_png="assets/readme/wave-fallback.png")
    export_animated_gif("assets/readme/wave-light.gif", LIGHT_THEME)
