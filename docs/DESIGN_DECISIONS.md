# Design Decisions: The Great Wave — Engineering in Motion
**Developer:** Santiago Ospina Arango ([@santi-osp](https://github.com/santi-osp))  
**Document Code:** `DEC-GW-002` | **Status:** Approved & Implemented

---

## 1. Visual Concept & Art Direction

### 1.1. Core Identity: "Engineering in Motion"
The visual identity fuses two distant yet philosophically resonant traditions:
1. **Classical Japanese Ukiyo-e Woodblock Art:** Katsushika Hokusai's *The Great Wave off Kanagawa* (ca. 1831) — representing fluid dynamics, monumental natural forces, and structured rhythmic lines.
2. **Modern Systems & Software Engineering:** Monospace telemetry, dot-matrix rendering, Unicode Braille, terminal control planes, and clean editorial hierarchy.

Rather than pasting a generic JPEG or vectorizing a wave as flat SVG shapes, **the illustration itself is synthesized out of code**: 26,624 addressable Braille dot positions (`U+2800..U+28FF`) computed mathematically from Bézier splines and fluid particle trajectories.

### 1.2. Editorial Tone
- **Technical & Rigorous:** No rainbow gradients, no "code ninja" cliches, no neon cyberpunk excess.
- **Minimalist & Structured:** Strict grid geometry, subtle crosshairs, and monochromatic/bichromatic discipline.
- **Accurate & Honest:** Reflects Santiago's true profile as a Junior Software Developer specializing in .NET, Angular, Azure, SQL Server, and enterprise AI integrations.

---

## 2. Color Palette & Chromatic Strategy

The palette adheres to Hokusai's authentic Prussian blue (*berorin-ai*) legacy adapted for digital displays in both GitHub Dark and GitHub Light themes.

### Dark Theme Palette
- **Obsidian Background (`#080D16`):** Deep terminal black providing maximum contrast for glowing dots.
- **Midnight Navy Card (`#0B1626`):** Translucent backing panel (89% opacity) separating typography from wave currents.
- **Deep Ocean (`#102A46`) & Prussian Blue (`#153C65`):** Base ocean muscle and woodblock ink grooves.
- **Ocean Blue (`#2563A6`) & Soft Blue (`#5FA8E8`):** Wave crest contours, telemetry tags, and active status indicators.
- **Ice White (`#D6ECFF`) & Pure White (`#FFFFFF`):** High-energy foam claws, spray droplets, and primary typographic headers.
- **Grid Accent (`#102238`) & Border (`#1B3A60`):** Fine engineering coordinate lines.

### Light Theme Palette
- **Soft Paper White (`#F5F9FD`):** Emulates Japanese mulberry paper (*washi*).
- **Deep Navy (`#0B2545`) & Ocean Blue (`#185B93`):** High-contrast ink characters and primary headers.
- **Mist Blue Card (`#EBF3FA`):** Clean editorial card backing.
- **Grid Axis (`#D2E3F3`) & Border (`#B8D5ED`):** Subtle technical registration lines.

---

## 3. Typography & Monospace Grid

### Font Family
- **Cascadia Mono / Cascadia Code:** Microsoft's open-source developer monospace font designed for Windows Terminal and VS Code. It provides complete Unicode 15.0 Braille Pattern support (`U+2800..U+28FF`) with circular, anti-aliased sub-pixel matrix dots.
- **Fallback Stack:** `Cascadia Mono, Consolas, "SF Mono", Menlo, Monaco, monospace`.

### Layout Proportions
- **Aspect Ratio:** $3.05 : 1$ ($1280 \times 420\text{ px}$ canvas). Fits GitHub's standard desktop container ($\sim 890 - 1020\text{ px}$ viewport width) without horizontal scrollbar.
- **Asymmetric Composition:**
  - **Left Quadrant ($x: 36\text{ to }510\text{ px}$):** Editorial Identity Card containing Santiago Ospina's name, role, verified tech stack (.NET, Angular, Azure, SQL Server), telemetry coordinates, and status beacon.
  - **Right Quadrant ($x: 420\text{ to }1260\text{ px}$):** The Great Wave rising majestically, curling over Mount Fuji, and discharging ballistic spray into the upper atmosphere.

---

## 4. Generative Art & Motion Engineering

### 4.1. Parametric Bézier Curves
The wave geometry is authored via cubic Bézier curves:
$$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$$
- Outer flank: rises from $x \approx 410$ to crest at $x \approx 832$, $y \approx 46$.
- Breaking lip: curls over toward $x \approx 730$, $y \approx 197$.
- Underside barrel: hollow interior curve framing Mount Fuji.

### 4.2. Harmonic Motion
Motion is computed with periodic trigonometric harmonics over a cycle duration $T = 6.0\text{ s}$:
$$\text{phase} = t \cdot \frac{2\pi}{T}$$
- Crest rise: $16.0 \cdot \sin(\text{phase})$
- Barrel curl: $24.0 \cdot \sin(\text{phase} + 0.6)$
- Breaking descent: $32.0 \cdot \max(0.0, \sin(\text{phase} - 0.7))$
- Lateral flank sway: $7.0 \cdot \cos(\text{phase} \cdot 0.5)$

### 4.3. Articulating Foam Claws & Ballistic Spray
- **20 Claw Finger Clusters:** Branch off the crest lip at varying parameter intervals $u$. Each finger oscillates with independent harmonic angles $\theta = -1.52 + 2.3u + 0.26 \cdot \sin(\text{phase} + 0.75k)$ and divides into sub-hooks.
- **95 Ballistic Spray Droplets:** Spawns along the crest with initial velocities $v_x, v_y$ and parabolic gravity $y(t) = y_0 - v_y \cdot \text{age} + 148 \cdot \text{age}^2$.
- **Seamless Loop Proof:** The particle lifetime is set to exactly $1.5\text{ s}$. Because $6.0\text{ s} / 1.5\text{ s} = 4$ integer cycles, the particle field at $t = 6.0\text{ s}$ is mathematically identical to $t = 0.0\text{ s}$ ($\Delta = 0$ pixels).

---

## 5. Technology Selection & GitHub Compatibility

| Technology | Role | Justification |
|---|---|---|
| **Animated GIF (Dual-Theme)** | Primary Hero Media | 100% universal playback across all mobile apps, desktop browsers, and GitHub proxy caching. Bypasses Camo proxy vector-flattening bug. 553 KB file size is lightweight. |
| **Vector SMIL SVG** | Secondary Vector Banner | Pure declarative SMIL `<animate>` without scripts. Camo compliant (<40 KB). Scalable to 4K displays. |
| **Fallback PNG** | Offline / Reduced-Motion Snapshot | Captured at $t = 3.5\text{ s}$ (peak claw extension). |
| **`<picture>` Markdown Architecture** | Theme Routing | Directs GitHub Dark users to `wave-dark.gif` and Light users to `wave-light.gif` with static fallback. |

---

## 6. Discarded Alternatives

1. **Client-Side WebGL / Canvas:**
   - *Discarded:* GitHub's markdown sanitizer completely strips `<canvas>`, WebGL contexts, and `<script>` tags.
2. **Brute-Force SMIL SVG ($>10,000$ animated text nodes):**
   - *Discarded:* Produces files between $1.5\text{ MB}$ and $3\text{ MB}$. GitHub's Camo caching proxy converts SVGs over $\sim 200\text{ KB}$ into static PNG thumbnails, causing complete animation failure on the profile.
3. **External Server Dynamic Generators:**
   - *Discarded:* Third-party badge servers fail when APIs rate-limit or go down. Self-contained Git assets guarantee 100% uptime with zero maintenance.
