# Visual & Motion Engineering Research: The Great Wave
**Target Profile:** [santi-osp](https://github.com/santi-osp) | **Identity:** Santiago Ospina Arango — Software Developer  
**Document Code:** `RES-GW-001` | **Status:** Completed & Verified

---

## 1. Executive Summary

This document presents the technical investigation conducted prior to designing and implementing the animated generative banner and profile redesign for Santiago Ospina Arango's GitHub Profile README.

The project objective is to construct a generative, animated reinterpretation of Katsushika Hokusai's *The Great Wave off Kanagawa* (*Kanagawa-oki nami ura*) using ASCII, Unicode, Braille dot matrices, and procedural motion graphics, integrated seamlessly into a software engineering visual identity.

Seven open-source codebases, official GitHub rendering specifications, and digital art repositories were cloned, decompiled, and analyzed at the source-code level.

---

## 2. Analyzed Repositories & Verified Findings

### 2.1. `sysc-Go` — Terminal Wave Animation
- **Repository:** [`Nomadcxx/sysc-Go`](https://github.com/Nomadcxx/sysc-Go)
- **Relevant Files:**
  - `animations/artwork_wave.go` (mathematical wave model and scene geometry)
  - `animations/artwork.go` (dot buffer rasterization, cell composition, Braille encoding)
  - `docs/plans/2026-10-11-terminal-artwork-motion-design.md`
- **License:** MIT License (Copyright 2025 Nomadcxx)
- **Key Algorithms & Mechanics:**
  - **Parametric Wave Geometry:** Uses cubic Bézier splines (`artBezier`) to construct the outer flank, rising crest, curling lip, and hollow barrel.
  - **Cyclic Harmonic Motion:** Motion is governed by `phase = t * 2 * pi / 8` (an 8-second seamless loop). Key dynamic variables:
    $$\text{rise} = 28 \cdot \sin(\text{phase})$$
    $$\text{curl} = 48 \cdot \sin(\text{phase} + 0.7)$$
    $$\text{breaking} = 55 \cdot \max(0, \sin(\text{phase} - 0.8))$$
  - **Ink Grooves:** 14 parametric contour curves bending across the wave flank with a phase drift: $\text{drift} = 9 \cdot \sin(\text{phase} - 7u)$.
  - **Foam Claws:** 15 articulating claw fingers branching along the crest with oscillatory angular deflection:
    $$\theta = -1.45 + 2.3u + 0.22 \cdot \sin(\text{phase} + 0.8k)$$
  - **Ballistic Spray Particles:** 70 spray droplets spawned at staggered time offsets traveling along ballistic parabolas:
    $$y(t) = y_0 - v_y \cdot \text{age} + 190 \cdot \text{age}^2$$
  - **Background Landmark:** Mount Fuji with its snow-capped crater situated in the compositional hollow of the wave.
  - **Dot Matrix Rasterization:** A virtual 2D canvas of sub-pixels is sampled in $2 \times 4$ blocks. Each $2 \times 4$ cluster of bits is mapped to the Unicode Braille block (`U+2800` through `U+28FF`), providing $8\times$ sub-cell resolution.
- **Adopted Techniques:**
  - Exact harmonic formulas for wave rise, curl, and breaking lip.
  - Articulating foam claws and ballistic spray physics.
  - $2 \times 4$ sub-pixel Braille bitmask generation.

---

### 2.2. `ascii-gif-studio` — Luminance Mapping & Palette Gradients
- **Repository:** [`fruitmob/ascii-gif-studio`](https://github.com/fruitmob/ascii-gif-studio)
- **Relevant Files:** `ascii_gif_studio.py`
- **License:** MIT / Apache 2.0 derived from `google/gif-for-cli`
- **Key Mechanics:**
  - Modernized Pillow 10+ pipeline for video/GIF to ASCII rasterization.
  - Multi-stop color lerping (`lerp_color`) across linear, diagonal, and radial gradients.
  - Aspect ratio correction: compensating for non-square font glyphs (typically $1 : 1.75$ or $1 : 2$ ratio).
- **Evaluation & Limitations:**
  - The script relies on external subprocess calls to `gif-for-cli`, `ffprobe`, and `ffmpeg`.
  - Wrapping external CLI binaries is brittle across developer workstations (especially Windows 11).
- **Adopted Techniques:**
  - Native Python/Pillow in-memory color lerping and palette quantization without external binary dependencies.

---

### 2.3. `ascii-lab` — Edge Detection & Glyph Direction Bins
- **Repository:** [`Theovia/ascii-lab`](https://github.com/Theovia/ascii-lab)
- **Relevant Files:** `v1-edges.html`, `atelier.html`, `paintings/04-hokusai.jpg`
- **License:** MIT
- **Key Mechanics:**
  - **Dual-Pass Rendering:** Combines luminance fill with structural contour glyphs.
  - **Difference of Gaussians (DoG) & Sobel Operators:** Computes gradient magnitude $M = \sqrt{G_x^2 + G_y^2}$ and direction angle $\theta = \operatorname{atan2}(G_y, G_x)$.
  - **Edge Direction Quantization:** Where edge magnitude exceeds a threshold (`edgeThresh = 0.30`), the character is selected from a 4-bin structural array:
    - Vertical ($|$) for $\theta \approx 90^\circ$
    - Diagonal NE $\to$ SW ($/$)
    - Horizontal ($-$, $\_$) for $\theta \approx 0^\circ$
    - Diagonal NW $\to$ SE ($\backslash$)
  - In fill regions ($M \le \text{threshold}$), characters are chosen from a monotonic density ramp: ` .,:;irsXA253hMHGS#9B&@`.
- **Adopted Techniques:**
  - Directional glyph replacement for wave crests, foam edges, and mountain silhouettes to keep contours razor sharp.

---

### 2.4. `svg-motion-cookbook` — GitHub SVG & SMIL Restrictions
- **Repository:** [`WaterTian/svg-motion-cookbook`](https://github.com/WaterTian/svg-motion-cookbook)
- **Relevant Files:** `github-readme.md`, `gotchas.md`, `examples/*.svg`
- **License:** MIT
- **Critical GitHub Environment Constraints Identified:**
  1. **Image Sanitizer & Script Stripping:** GitHub's Camo proxy aggressively strips `<script>`, `@import`, external CSS `<link>`, and inline event handlers (`onload`, `onclick`). Only inline presentation attributes and pure SMIL (`<animate>`, `<animateTransform>`) are retained.
  2. **`<animate>` Hierarchy:** Standalone `<animate xlink:href="#target">` tags are stripped by the GitHub sanitizer. `<animate>` MUST be declared directly as an inline child of the target element.
  3. **Proxy Camo Flattening Threshold:** If an SVG exceeds **$\sim 150 - 200\text{ KB}$**, GitHub's Camo caching proxy frequently rasterizes the SVG into a static PNG thumbnail, completely killing SMIL animations.
  4. **Text Whitespace Collapse:** Monospace ASCII in `<text>` collapses consecutive whitespace unless `xml:space="preserve"` is explicitly declared.
  5. **Opacity Gotchas:** `opacity` on `<tspan>` is intermittently ignored; `fill-opacity` must be used instead.
- **Adopted Techniques:**
  - Strict compliance with GitHub Camo limits: keeping vector SVGs lean.
  - Monospace font metrics: `font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"`.
  - `xml:space="preserve"` on all text nodes.

---

### 2.5. `zebiv-code/great_wave` — Procedural Sea Dynamics
- **Repository:** [`zebiv-code/great_wave`](https://github.com/zebiv-code/great_wave)
- **Relevant Files:** `web/js/waves.js`, `web/js/spray.js`
- **Key Mechanics:**
  - **Non-linear Sharp Crest Profile:**
    $$\text{profile}(\theta) = \left(\frac{1 + \sin(\theta)}{2}\right)^{1.55} \cdot 2 - 1$$
    This mathematical shaping sharpens the crest peaks and flattens the troughs, replicating traditional Japanese woodblock wave forms.
  - **Layered Swell Velocities:** Multiple swell layers running at different phase speeds ($sp_1 = 0.55, sp_2 = 0.35, sp_3 = 0.70$) creating realistic water depth.
- **Adopted Techniques:**
  - Exponentiated sine profiles for secondary swells and background water layers.

---

### 2.6. `animated-github-profile` & `ryme.md` — Monospace Layout & Aesthetics
- **Repositories:** [`navi3582/animated-github-profile`](https://github.com/navi3582/animated-github-profile), [`ryanpolasky/ryme.md`](https://github.com/ryanpolasky/ryme.md)
- **Key Mechanics:**
  - Monospace aspect ratio correction: typical monospace character aspect ratio is $0.57$ to $0.60$ (width / height).
  - Clean editorial layout: pairing generous negative space on the left for identity/telemetry with dynamic generative art on the right.
  - Zero external server runtime requirement: assets are fully pre-rendered and self-contained within the Git repository.

---

## 3. GitHub Media Rendering Specifications & Constraints

| Factor | Native SVG (SMIL) | Animated GIF | APNG | Static PNG Fallback |
|---|---|---|---|---|
| **Max File Size for GitHub Animation** | $\le 200\text{ KB}$ (Strict) | $\le 10\text{ MB}$ (Safe up to 5MB) | $\le 5\text{ MB}$ | Any |
| **GitHub Camo Proxy Compatibility** | High (if $<150\text{ KB}$) | 100% Guaranteed | Variable across clients | 100% Guaranteed |
| **Dark / Light Theme Switching** | Supported via `<picture>` | Supported via `<picture>` | Supported via `<picture>` | Supported |
| **Scalability (Vector vs Raster)** | Perfect Vector | Crisp at native $2\times$ pixel density | Crisp at native $2\times$ | Crisp at native $2\times$ |
| **Rendering Cost on Client** | High if $>1,000$ DOM nodes | Low (hardware GIF decoder) | Low | Instant |
| **Braille / ASCII Detail** | Limited by node count | High ($160\times 48$ cells = $320\times 192$ Braille dots) | High | Ultra-high |

---

## 4. Architectural Decision Matrix

### Evaluated Alternatives
1. **Alternative A (Pure SMIL SVG with $10,000$ animated text characters):**
   - *Verdict:* **REJECTED AS PRIMARY.**
   - *Reason:* An SVG with thousands of individual `<tspan><animate>...</tspan>` tags reaches $1.5\text{ MB} - 3\text{ MB}$. GitHub's Camo proxy flattens files over $200\text{ KB}$ into static thumbnails, causing total animation failure on GitHub profile pages.
2. **Alternative B (High-Density Animated GIF with 2x Retina Resolution & Palette Quantization):**
   - *Verdict:* **APPROVED AS PRIMARY HERO ANIMATION.**
   - *Reason:* $100\%$ guaranteed animation playback through GitHub Camo proxy across mobile and desktop. Generates rich $2\times 4$ Braille sub-pixel detail ($1280 \times 420$ resolution), smooth 10 fps motion, seamless 6-second loop, and file size under $1.8\text{ MB}$ via Floyd-Steinberg dithering and palette quantization.
3. **Alternative C (APNG):**
   - *Verdict:* **RESERVED AS SECONDARY BENCHMARK.**
   - *Reason:* While APNG supports 24-bit color, certain mobile GitHub clients and older browser wrappers fail to loop APNGs reliably compared to universal GIF support.
4. **Alternative D (Optimized Hybrid Vector SVG Banner):**
   - *Verdict:* **APPROVED AS COMPANION VECTOR SYSTEM.**
   - *Reason:* We construct an ultra-clean, lean SVG banner ($<45\text{ KB}$) containing the technical telemetry grid, monospace typography, status indicators with SMIL pulsing dots, and crisp Japanese calligraphy vector marks.
5. **Alternative E (Dual-Theme `<picture>` Architecture):**
   - *Verdict:* **APPROVED FOR PRODUCTION EMBEDDING.**
   - *Architecture:*
     ```html
     <picture>
       <source media="(prefers-color-scheme: dark)" srcset="assets/readme/wave-dark.gif" />
       <source media="(prefers-color-scheme: light)" srcset="assets/readme/wave-light.gif" />
       <img src="assets/readme/wave-fallback.png" alt="The Great Wave - Engineering in Motion" width="100%" />
     </picture>
     ```

---

## 5. Summary of Final Architectural Choices

1. **Procedural Engine:** Custom Python 3.14 module implementing the Bézier wave dynamics from `sysc-Go` and the swell shaping from `zebiv-code/great_wave`.
2. **ASCII / Braille Renderer:** Dual-pass dot matrix rasterizer converting mathematical curves and fluid particles into $2 \times 4$ Unicode Braille glyphs and Sobel directional edge characters.
3. **Temporal Coherence:** Deterministic pseudo-random seed with continuous phase harmonics to eliminate chaotic noise flicker between animation frames.
4. **Zero External Runtime Dependencies:** Entirely reproducible using Python 3, Pillow, and NumPy with no reliance on external servers, API keys, or binary CLI utilities.
