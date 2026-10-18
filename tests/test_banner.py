"""
Automated test suite for The Great Wave banner generator and GitHub Profile assets.
Validates SVG XML integrity, GIF animation parameters, ASCII/Braille matrix determinism,
image sizes, and security compliance.
"""
import os
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

from scripts.banner.config import BannerConfig, DARK_THEME, LIGHT_THEME
from scripts.banner.wave_math import WaveSceneModel
from scripts.banner.rasterizer import SubPixelCanvas
from scripts.banner.banner_compositor import BannerCompositor

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets", "readme")

class TestGreatWaveGenerator(unittest.TestCase):
    
    def setUp(self):
        self.config = BannerConfig()
        self.model = WaveSceneModel(duration=6.0)

    def test_wave_model_determinism(self):
        """Verify wave mathematics produce identical, deterministic results for same t."""
        scene_a = self.model.evaluate(2.0, 1280, 420)
        scene_b = self.model.evaluate(2.0, 1280, 420)
        
        self.assertEqual(len(scene_a['foam_claws']), len(scene_b['foam_claws']))
        self.assertEqual(len(scene_a['spray_particles']), len(scene_b['spray_particles']))
        self.assertAlmostEqual(scene_a['phase'], scene_b['phase'], places=7)
        self.assertAlmostEqual(scene_a['outer_curve'][0][0], scene_b['outer_curve'][0][0], places=7)

    def test_infinite_loop_mathematical_continuity(self):
        """Verify t=0.0s and t=duration (6.0s) produce exactly identical scenes."""
        comp = BannerCompositor(self.config, DARK_THEME)
        im0 = np.array(comp.compose_frame(0.0))
        im_end = np.array(comp.compose_frame(self.config.duration))
        
        diff = np.abs(im0.astype(int) - im_end.astype(int))
        self.assertEqual(diff.max(), 0, "Discontinuity detected between loop start and end!")
        self.assertAlmostEqual(float(diff.mean()), 0.0, places=6)

    def test_subpixel_canvas_braille_mapping(self):
        """Verify subpixel canvas converts dot patterns to valid Unicode Braille."""
        canvas = SubPixelCanvas(cols=10, rows=5)
        # Set all 8 dots in first cell -> 0xFF (U+28FF, '⣿')
        for dx in range(2):
            for dy in range(4):
                canvas.set_dot(dx, dy, color_id=1)
        
        palette = {0: (0, 0, 0), 1: (255, 255, 255)}
        grid = canvas.to_braille_grid(palette)
        
        self.assertEqual(grid[0][0]['char'], '⣿')
        self.assertEqual(grid[0][0]['bits'], 0xFF)
        self.assertEqual(grid[0][1]['char'], ' ')  # Empty adjacent cell
        self.assertEqual(grid[0][1]['bits'], 0x00)

    def test_svg_xml_validity_and_security(self):
        """Verify generated SVGs are well-formed XML and contain no forbidden scripts/external CSS."""
        svg_files = [
            os.path.join(ASSETS_DIR, "wave-dark.svg"),
            os.path.join(ASSETS_DIR, "wave-light.svg"),
            os.path.join(ASSETS_DIR, "separators", "wave-divider-dark.svg"),
            os.path.join(ASSETS_DIR, "separators", "wave-divider-light.svg")
        ]
        
        for path in svg_files:
            self.assertTrue(os.path.exists(path), f"Missing SVG file: {path}")
            size_kb = os.path.getsize(path) / 1024.0
            self.assertLess(size_kb, 150.0, f"SVG {path} exceeds safe GitHub Camo proxy limit of 150KB!")
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Security checks
            self.assertNotIn("<script", content.lower(), f"Forbidden <script> found in {path}")
            self.assertNotIn("javascript:", content.lower(), f"Forbidden javascript: found in {path}")
            self.assertNotIn("<iframe", content.lower(), f"Forbidden <iframe> found in {path}")
            self.assertNotIn("@import", content.lower(), f"Forbidden @import found in {path}")
            
            # XML parsing validation
            try:
                root = ET.fromstring(content)
                self.assertIn("viewBox", root.attrib)
            except ET.ParseError as e:
                self.fail(f"Invalid XML syntax in {path}: {e}")

    def test_gif_animation_parameters(self):
        """Verify animated GIF dimensions, frame count, durations, and file sizes."""
        gif_files = [
            os.path.join(ASSETS_DIR, "wave-dark.gif"),
            os.path.join(ASSETS_DIR, "wave-light.gif"),
            os.path.join(ASSETS_DIR, "wave-animated.gif")
        ]
        
        for path in gif_files:
            self.assertTrue(os.path.exists(path), f"Missing GIF file: {path}")
            size_mb = os.path.getsize(path) / (1024.0 * 1024.0)
            self.assertLess(size_mb, 4.0, f"GIF {path} exceeds 4 MB optimization target!")
            
            with Image.open(path) as im:
                self.assertTrue(im.is_animated, f"{path} is not recognized as an animated GIF!")
                self.assertEqual(im.size, (1280, 420), f"Incorrect dimensions for {path}: {im.size}")
                self.assertEqual(im.n_frames, 60, f"Expected 60 frames for 6s @ 10fps in {path}, got {im.n_frames}")
                
                # Check frame duration
                duration = im.info.get('duration', 0)
                self.assertEqual(duration, 100, f"Expected 100ms frame duration in {path}, got {duration}ms")
                
                # Check motion existence between frames
                im.seek(0)
                f0 = np.array(im.convert("RGB"))
                im.seek(15)  # quarter cycle
                f15 = np.array(im.convert("RGB"))
                diff = np.abs(f0.astype(int) - f15.astype(int)).max()
                self.assertGreater(diff, 30, f"No significant motion detected between frames in {path}!")

    def test_fallback_png_validity(self):
        """Verify fallback snapshot exists, has correct dimensions and reasonable size."""
        png_path = os.path.join(ASSETS_DIR, "wave-fallback.png")
        self.assertTrue(os.path.exists(png_path))
        with Image.open(png_path) as im:
            self.assertEqual(im.size, (1280, 420))
            self.assertEqual(im.format, "PNG")
        size_kb = os.path.getsize(png_path) / 1024.0
        self.assertLess(size_kb, 300.0)

    def test_security_and_confidentiality(self):
        """Verify repository contains no hardcoded tokens, passwords, or internal confidential keys."""
        forbidden_substrings = [
            "password=", "secret=", "bearer ", "eyj", "api_key", "client_secret",
            "postobon_internal", "sap_secret", "prod_connection"
        ]
        files_to_scan = [
            os.path.join(REPO_ROOT, "README.md"),
            os.path.join(REPO_ROOT, "scripts", "banner", "config.py"),
            os.path.join(REPO_ROOT, "scripts", "banner", "generate.py"),
            os.path.join(REPO_ROOT, "scripts", "banner", "banner_compositor.py")
        ]
        for fpath in files_to_scan:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                    for word in forbidden_substrings:
                        self.assertNotIn(word, content, f"Potentially sensitive term '{word}' found in {fpath}")

if __name__ == "__main__":
    unittest.main()
