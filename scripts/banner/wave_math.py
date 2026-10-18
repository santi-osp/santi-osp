"""
Mathematical geometry and procedural motion curves for Katsushika Hokusai's The Great Wave.
Implements cubic Béziers, harmonic oscillators, articulating foam claws, and ballistic spray droplets.
"""
import math
from typing import List, Tuple, Dict, Any

Point = Tuple[float, float]

def cubic_bezier(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
    """Evaluate cubic Bézier curve at parameter t in [0, 1]."""
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    
    x = uuu * p0[0] + 3.0 * uu * t * p1[0] + 3.0 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3.0 * uu * t * p1[1] + 3.0 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)

def sample_bezier_curve(p0: Point, p1: Point, p2: Point, p3: Point, steps: int = 40) -> List[Point]:
    """Sample points along a cubic Bézier curve."""
    return [cubic_bezier(p0, p1, p2, p3, i / float(steps)) for i in range(steps + 1)]

class WaveSceneModel:
    """Computes the full parametric state of the Great Wave at time t."""
    
    def __init__(self, duration: float = 6.0):
        self.duration = duration

    def evaluate(self, t: float, width: int = 1280, height: int = 420) -> Dict[str, Any]:
        """
        Evaluate full scene geometry at time t (seconds).
        Returns dictionary containing polygons, lines, curves, particles, and landmark objects.
        """
        # Periodic phase angle [0, 2*pi]
        phase = (t % self.duration) * 2.0 * math.pi / self.duration
        
        # Harmonic offsets for natural breathing motion
        rise = 16.0 * math.sin(phase)
        curl = 24.0 * math.sin(phase + 0.6)
        breaking = 32.0 * max(0.0, math.sin(phase - 0.7))
        sway = 7.0 * math.cos(phase * 0.5)

        # 1. Mount Fuji Landmark (situated peacefully in the wave's circular barrel opening)
        fuji_cx = width * 0.71       # ~908 px
        fuji_base_y = height * 0.76   # ~319 px
        fuji_peak_y = height * 0.48   # ~201 px
        fuji_half_base = 82.0
        
        fuji_poly = [
            (fuji_cx - fuji_half_base, fuji_base_y),
            (fuji_cx - 16.0, fuji_peak_y),
            (fuji_cx + 16.0, fuji_peak_y),
            (fuji_cx + fuji_half_base, fuji_base_y)
        ]
        fuji_snow = [
            (fuji_cx - 36.0, fuji_peak_y + 32.0),
            (fuji_cx - 16.0, fuji_peak_y),
            (fuji_cx + 16.0, fuji_peak_y),
            (fuji_cx + 36.0, fuji_peak_y + 32.0),
            (fuji_cx + 18.0, fuji_peak_y + 28.0),
            (fuji_cx, fuji_peak_y + 34.0),
            (fuji_cx - 18.0, fuji_peak_y + 28.0)
        ]

        # 2. Background Sea Swells (distant rollers in the bay)
        background_swells = []
        for band in range(7):
            y_base = height * 0.63 + band * 15.0
            p0 = (width * 0.35, y_base + 8.0 * math.sin(phase + band * 0.8))
            p1 = (width * 0.55, y_base - 14.0 + 4.0 * math.sin(phase))
            p2 = (width * 0.78, y_base + 10.0 * math.sin(phase - band * 0.5))
            p3 = (width + 20.0, y_base - 6.0)
            pts = sample_bezier_curve(p0, p1, p2, p3, steps=36)
            background_swells.append(pts)

        # 3. Main Great Wave Geometry
        # Outer flank sweeping up dramatically to the grand crest
        w_p0 = (width * 0.32, height + 10.0)
        w_p1 = (width * 0.39, height * 0.46 + sway)
        w_p2 = (width * 0.50, height * 0.05 + rise)
        w_p3 = (width * 0.65, height * 0.11 + rise)
        outer_curve = sample_bezier_curve(w_p0, w_p1, w_p2, w_p3, steps=50)
        
        # Breaking crest lip curling inward over Mount Fuji
        lip_p0 = (width * 0.65, height * 0.11 + rise)
        lip_p1 = (width * 0.74, height * 0.14 + rise)
        lip_p2 = (width * 0.73 + curl, height * 0.33 + rise + breaking * 0.5)
        lip_p3 = (width * 0.57 + curl, height * 0.47 + rise + breaking)
        lip_curve = sample_bezier_curve(lip_p0, lip_p1, lip_p2, lip_p3, steps=50)
        
        # Hollow barrel / underside curve returning down into the deep sea
        in_p0 = (width * 0.57 + curl, height * 0.47 + rise + breaking)
        in_p1 = (width * 0.49 + curl, height * 0.28 + rise + breaking * 0.8)
        in_p2 = (width * 0.45, height * 0.70)
        in_p3 = (width * 0.76, height + 10.0)
        inner_curve = sample_bezier_curve(in_p0, in_p1, in_p2, in_p3, steps=50)
        
        # Complete wave body polygon for fill
        wave_body_polygon = outer_curve + lip_curve + inner_curve + [(w_p0[0], height + 10.0)]

        # 4. Secondary Companion Wave (rising from lower-mid to center)
        sec_p0 = (width * 0.26, height + 10.0)
        sec_p1 = (width * 0.33, height * 0.72)
        sec_p2 = (width * 0.42, height * 0.54 + rise * 0.6)
        sec_p3 = (width * 0.50, height * 0.59 + rise * 0.6)
        sec_crest = sample_bezier_curve(sec_p0, sec_p1, sec_p2, sec_p3, steps=30)
        
        sec_lip_p0 = sec_p3
        sec_lip_p1 = (width * 0.54, height * 0.64 + rise * 0.6)
        sec_lip_p2 = (width * 0.50 + curl * 0.5, height * 0.75 + rise * 0.6)
        sec_lip_p3 = (width * 0.44 + curl * 0.5, height * 0.82)
        sec_lip = sample_bezier_curve(sec_lip_p0, sec_lip_p1, sec_lip_p2, sec_lip_p3, steps=25)
        sec_body_poly = sec_crest + sec_lip + [(sec_p0[0], height + 10.0)]

        # 5. Ink Grooves (water muscle contour lines along flank)
        ink_grooves = []
        cyan_highlights = []
        for k in range(16):
            u = k / 16.0
            drift = 6.0 * math.sin(phase - u * 6.5)
            g_start = (w_p0[0] + 10.0 + u * (width * 0.25), height + 10.0)
            g_end = (width * 0.34 + u * (width * 0.30), height * 0.15 + rise + u * 48.0)
            g_mid1 = (width * 0.32 + u * (width * 0.14), height * 0.60 + drift)
            g_mid2 = (width * 0.35 + u * (width * 0.16), height * 0.32 + rise + drift)
            groove_pts = sample_bezier_curve(g_start, g_mid1, g_mid2, g_end, steps=32)
            ink_grooves.append(groove_pts)
            if k % 2 == 0:
                cyan_pts = [(x + 3.0, y - 2.0) for x, y in groove_pts]
                cyan_highlights.append(cyan_pts)

        # 6. Articulating Foam Claws along Lip (Hokusai's signature claw spray)
        foam_claws = []
        # Upper outer crest claws (reaching forward over top)
        for k in range(20):
            u = 0.03 + k * 0.048
            root = cubic_bezier(lip_p0, lip_p1, lip_p2, lip_p3, u)
            theta = -1.52 + u * 2.3 + 0.26 * math.sin(phase + k * 0.75)
            length = 26.0 + 14.0 * math.sin(phase + k * 0.65)
            tip = (root[0] + math.cos(theta) * length, root[1] + math.sin(theta) * length)
            
            ctrl = (root[0] + math.cos(theta) * length * 0.5, root[1] - 12.0)
            claw_curve = sample_bezier_curve(root, ctrl, (tip[0] - 7.0, tip[1] - 5.0), tip, steps=12)
            
            # Hooks and sub-spurs
            sub_tip1 = (tip[0] + 10.0 * math.sin(phase + u * 8.0), tip[1] + 9.0)
            sub_tip2 = (tip[0] - 10.0, tip[1] - 6.0)
            sub_tip3 = (tip[0] + 4.0, tip[1] + 12.0)
            foam_claws.append({
                'main': claw_curve,
                'spur1': (tip, sub_tip1),
                'spur2': ((root[0] + tip[0]) * 0.5, (root[1] + tip[1]) * 0.5, sub_tip2),
                'spur3': (tip, sub_tip3)
            })

        # Secondary wave claws
        sec_claws = []
        for k in range(7):
            u = 0.15 + k * 0.11
            root = cubic_bezier(sec_lip_p0, sec_lip_p1, sec_lip_p2, sec_lip_p3, u)
            theta = -1.35 + u * 1.8 + 0.20 * math.sin(phase + k * 0.9)
            length = 14.0 + 7.0 * math.sin(phase + k * 0.8)
            tip = (root[0] + math.cos(theta) * length, root[1] + math.sin(theta) * length)
            claw_curve = sample_bezier_curve(root, (root[0], root[1] - 6.0), tip, tip, steps=8)
            sec_claws.append({'main': claw_curve, 'tip': tip})

        # 7. Underside Foam Veins folding back into the barrel
        foam_veins = []
        for k in range(12):
            u = 0.25 + k * 0.058
            root = cubic_bezier(lip_p0, lip_p1, lip_p2, lip_p3, u)
            p_v1 = (root[0] - 14.0, root[1] + 14.0)
            p_v2 = (root[0] - 36.0, root[1] + 30.0 + breaking * 0.3)
            p_v3 = (root[0] - 28.0, root[1] + 52.0)
            vein_pts = sample_bezier_curve(root, p_v1, p_v2, p_v3, steps=18)
            foam_veins.append(vein_pts)

        # 8. Ballistic Spray Particles (fountaining out of the crest)
        spray_particles = []
        particle_lifetime = 1.5  # 6.0s / 1.5s = exactly 4 cycles for seamless loop
        for k in range(95):
            cycle_offset = (k * 0.068)
            age = (t + cycle_offset) % particle_lifetime
            u = ((k * 37) % 100) / 100.0
            root = cubic_bezier(lip_p0, lip_p1, lip_p2, lip_p3, u)
            
            vx = 28.0 + (k % 11) * 8.0
            vy = 82.0 + (k % 7) * 12.0
            gravity = 148.0
            
            px = root[0] + vx * age
            py = root[1] - vy * age + gravity * (age * age)
            
            life_fraction = age / particle_lifetime
            if py < height and px < width and life_fraction < 0.95:
                rad = max(0.9, (1.0 - life_fraction) * (2.5 + (k % 3) * 0.6))
                intensity = max(0.2, 1.0 - life_fraction)
                spray_particles.append((px, py, rad, intensity))

        # 9. Foreground Rollers with travelling foam
        foreground_rollers = []
        for k in range(2):
            y_base = height * 0.83 + k * 36.0
            r_p0 = (width * 0.30, y_base + 26.0)
            r_p1 = (width * 0.50, y_base - 48.0 + 12.0 * math.sin(phase + k * 1.3))
            r_p2 = (width * 0.72, y_base + 20.0)
            r_p3 = (width + 20.0, y_base - 14.0)
            roller_pts = sample_bezier_curve(r_p0, r_p1, r_p2, r_p3, steps=36)
            foreground_rollers.append(roller_pts)

        # 10. Longboats (Oshiokuri-bune) riding the swells
        boats = []
        for k in range(2):
            b_x = width * 0.54 + k * 210.0
            b_y = height * 0.70 + (k % 2) * 52.0 + 6.0 * math.sin(phase + k * 1.4)
            hull = [
                (b_x - 68.0, b_y),
                (b_x + 64.0, b_y - 8.0),
                (b_x + 46.0, b_y + 10.0),
                (b_x - 48.0, b_y + 16.0)
            ]
            rowers = []
            for r in range(5):
                rx = b_x - 38.0 + r * 19.0
                ry = b_y + 1.0 - r * 1.0
                rowers.append((rx, ry))
            boats.append({'hull': hull, 'rowers': rowers})

        return {
            'phase': phase,
            'fuji': {'poly': fuji_poly, 'snow': fuji_snow},
            'background_swells': background_swells,
            'wave_body': wave_body_polygon,
            'secondary_wave': sec_body_poly,
            'secondary_claws': sec_claws,
            'outer_curve': outer_curve,
            'lip_curve': lip_curve,
            'ink_grooves': ink_grooves,
            'cyan_highlights': cyan_highlights,
            'foam_claws': foam_claws,
            'foam_veins': foam_veins,
            'spray_particles': spray_particles,
            'foreground_rollers': foreground_rollers,
            'boats': boats
        }
