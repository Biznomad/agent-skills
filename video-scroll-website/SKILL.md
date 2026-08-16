---
name: biznomad-video-scroll-website
description: Biznomad - Build Apple-grade video scroll-animated websites and scrollytelling experiences using GSAP ScrollTrigger, Lenis smooth scroll, Canvas image sequences, ALL-I encoded HTML5 video scrubbing, and sticky HUD overlays.
---

# Biznomad - Video Scroll Animated Websites (Apple-Grade Scrollytelling)

This skill provides complete architectural patterns, FFmpeg compression pipelines, and production JS/CSS code for building high-performance, video scroll-animated websites matching Apple, Stripe, Lusion, and Awwwards Site-of-the-Day standards.

---

## Industry Research & Architectural Breakdown

When building scroll-driven video experiences, top tech and design agencies select from **three primary rendering strategies**:

| Strategy | Industry Reference | Best For | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Canvas Image Sequence** | Apple (MacBook, AirPods, iPhone) | Precision scrub, zero lag, frame perfection | 60–120fps butter-smooth, works on all mobile GPUs | Requires frame preloading (20–60MB array) |
| **ALL-I Encoded HTML5 Video** | Stripe, Nike, Tesla | Quick setup, low bandwidth single file | Single MP4 download, fast initialization | Requires low keyframe distance (`-g 1`) |
| **WebGL Texture Shader** | Lusion, Active Theory, Cuberto | 3D depth distortion, liquid glass effects | Ultra-creative, lighting & refraction control | Higher GPU overhead, shader complexity |

---

## 1. Video Preparation & FFmpeg Encoding Pipeline

To achieve instant, smooth frame scrubbing without stutter, the video **MUST** be encoded with a keyframe distance of `1` (every frame is an Intra-frame / Keyframe).

### Option A: Prepare Video for HTML5 Video Scrubbing (ALL-I Encoding)
Run this FFmpeg command to generate an ultra-fast scrubbing MP4:

```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset slow -crf 18 -g 1 -keyint_min 1 -an -movflags +faststart output_scrub.mp4
```

### Option B: Prepare Frame Sequence for Canvas Scrubbing (Apple Style)
Extract compressed 1080p WebP or JPEG frames:

```bash
mkdir -p frames
ffmpeg -i input.mp4 -vf "scale=1920:1080" -q:v 85 frames/frame_%04d.jpg
# Or for WebP (smaller file size):
ffmpeg -i input.mp4 -vf "scale=1920:1080" -c:v libwebp -quality 85 frames/frame_%04d.webp
```

---

## 2. Technical Stack Configuration

- **Smooth Scrolling Engine**: `@studio-freight/lenis` or `Lenis` (eliminates jitter and provides momentum scroll)
- **Animation Driver**: `GSAP 3.12+` with `ScrollTrigger`
- **Rendering Layer**: `<canvas>` with 2D Context or `<video>` with `currentTime` sync
- **Typography & HUD**: Glassmorphic fixed overlay cards synced to frame timeline triggers

---

## 3. Production Architecture: Apple-Style Canvas Sequence (Recommended)

Below is the production-ready implementation of an Apple-style Canvas frame scroll sequence with preloader, smooth Lenis scroll, and floating scrollytelling copy layers.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Apple-Style Video Scroll Showcase</title>

<!-- Fonts & GSAP + Lenis CDNs -->
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.9/dist/lenis.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<style>
  :root {
    --bg: #000000;
    --paper: #f5f5f7;
    --dim: #86868b;
    --accent: #2997ff;
    --accent-glow: rgba(41, 151, 255, 0.35);
    --panel: rgba(22, 22, 23, 0.75);
    --line: rgba(255, 255, 255, 0.12);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--paper);
    font-family: "Inter", system-ui, -apple-system, sans-serif;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
  }

  /* Preloader */
  #preloader {
    position: fixed;
    inset: 0;
    z-index: 999;
    background: #000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    transition: opacity 0.6s ease, visibility 0.6s ease;
  }
  #preloader.done { opacity: 0; visibility: hidden; }
  .loader-bar {
    width: 200px;
    height: 3px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 999px;
    overflow: hidden;
  }
  .loader-fill {
    height: 100%;
    width: 0%;
    background: var(--accent);
    transition: width 0.1s linear;
  }

  /* Sticky Scroll Canvas Stage */
  .scroll-stage {
    position: relative;
    height: 400vh; /* Determines length of scroll interaction */
  }
  .sticky-viewport {
    position: sticky;
    top: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  canvas#scrollCanvas {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  /* Floating Scrollytelling Overlay Panels */
  .hud-overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 10;
  }
  .hud-card {
    position: absolute;
    max-width: 460px;
    background: var(--panel);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 32px;
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  .hud-card.active {
    opacity: 1;
    transform: translateY(0);
  }
  .hud-eyebrow {
    font-family: "JetBrains Mono", monospace;
    color: var(--accent);
    font-size: 12px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 8px;
  }
  .hud-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 12px;
  }
  .hud-desc {
    color: var(--dim);
    font-size: 15px;
    line-height: 1.6;
  }

  /* Individual HUD Positions */
  .hud-1 { top: 15%; left: 8%; }
  .hud-2 { top: 35%; right: 8%; }
  .hud-3 { bottom: 15%; left: 8%; }

  /* End Section */
  .outro-sec {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: #08080a;
    border-top: 1px solid var(--line);
    padding: 80px 24px;
  }
  .outro-title {
    font-size: clamp(40px, 6vw, 84px);
    font-weight: 900;
    letter-spacing: -0.04em;
    margin-bottom: 24px;
  }
  .btn-cta {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-weight: 700;
    padding: 16px 36px;
    border-radius: 999px;
    text-decoration: none;
    box-shadow: 0 10px 30px var(--accent-glow);
    transition: transform 0.2s;
  }
  .btn-cta:hover { transform: scale(1.05); }
</style>
</head>
<body>

<!-- Preloader -->
<div id="preloader">
  <div style="font-weight:700;font-size:14px;letter-spacing:0.1em">LOADING EXPERIENCE</div>
  <div class="loader-bar"><div class="loader-fill" id="loaderFill"></div></div>
</div>

<!-- Scroll Video Container -->
<div class="scroll-stage" id="scrollStage">
  <div class="sticky-viewport">
    <canvas id="scrollCanvas"></canvas>

    <!-- Scrollytelling HUD Overlays -->
    <div class="hud-overlay">
      <div class="hud-card hud-1" id="hud1">
        <div class="hud-eyebrow">01 / ARCHITECTURE</div>
        <h2 class="hud-title">Precision Engineered.</h2>
        <p class="hud-desc">Every frame calculated in real-time. Unmatched visual velocity and fluid responsiveness.</p>
      </div>

      <div class="hud-card hud-2" id="hud2">
        <div class="hud-eyebrow">02 / TELEMETRY</div>
        <h2 class="hud-title">Real-Time Data Flow.</h2>
        <p class="hud-desc">Sub-millisecond synchronization between user scroll input and canvas presentation.</p>
      </div>

      <div class="hud-card hud-3" id="hud3">
        <div class="hud-eyebrow">03 / PERFORMANCE</div>
        <h2 class="hud-title">120 FPS Mastery.</h2>
        <p class="hud-desc">GPU accelerated canvas rendering with zero frame drop or scroll stuttering.</p>
      </div>
    </div>
  </div>
</div>

<section class="outro-sec">
  <div>
    <h1 class="outro-title">Ready to Launch.</h1>
    <a href="#" class="btn-cta">EXPERIENCE THE FUTURE →</a>
  </div>
</section>

<script>
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Lenis Smooth Scroll
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // Sync Lenis with GSAP ScrollTrigger
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  // 2. Setup Canvas & Image Preloader
  const canvas = document.getElementById('scrollCanvas');
  const ctx = canvas.getContext('2d');
  const loaderFill = document.getElementById('loaderFill');
  const preloader = document.getElementById('preloader');

  const totalFrames = 120; // Number of extracted frames
  const images = [];
  const airbnb = { frame: 0 };

  // Frame URL generator (Replace with your relative path)
  const currentFrame = (index) => `./frames/frame_${(index + 1).toString().padStart(4, '0')}.jpg`;

  let loadedCount = 0;
  for (let i = 0; i < totalFrames; i++) {
    const img = new Image();
    img.src = currentFrame(i);
    img.onload = () => {
      loadedCount++;
      loaderFill.style.width = `${(loadedCount / totalFrames) * 100}%`;
      if (loadedCount === totalFrames) {
        preloader.classList.add('done');
        renderCanvas();
      }
    };
    images.push(img);
  }

  // Handle High-DPI Retina Displays
  function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    ctx.scale(dpr, dpr);
    renderCanvas();
  }
  window.addEventListener('resize', resizeCanvas);

  function renderCanvas() {
    if (!images[airbnb.frame]) return;
    const img = images[airbnb.frame];
    const w = window.innerWidth;
    const h = window.innerHeight;

    // Cover Fit Math
    const imgRatio = img.width / img.height;
    const canvasRatio = w / h;
    let drawW, drawH, offsetX, offsetY;

    if (canvasRatio > imgRatio) {
      drawW = w;
      drawH = w / imgRatio;
      offsetX = 0;
      offsetY = (h - drawH) / 2;
    } else {
      drawW = h * imgRatio;
      drawH = h;
      offsetX = (w - drawW) / 2;
      offsetY = 0;
    }

    ctx.clearRect(0, 0, w, h);
    ctx.drawImage(img, offsetX, offsetY, drawW, drawH);
  }

  // Initial Canvas Resize
  resizeCanvas();

  // 3. GSAP ScrollTrigger Sequence
  gsap.to(airbnb, {
    frame: totalFrames - 1,
    snap: "frame",
    ease: "none",
    scrollTrigger: {
      trigger: "#scrollStage",
      start: "top top",
      end: "bottom bottom",
      scrub: 0.5,
      onUpdate: () => renderCanvas()
    }
  });

  // 4. Scrollytelling HUD Overlays Triggers
  function setupHudTrigger(id, startPct, endPct) {
    ScrollTrigger.create({
      trigger: "#scrollStage",
      start: `${startPct}% top`,
      end: `${endPct}% top`,
      onEnter: () => document.getElementById(id).classList.add('active'),
      onLeave: () => document.getElementById(id).classList.remove('active'),
      onEnterBack: () => document.getElementById(id).classList.add('active'),
      onLeaveBack: () => document.getElementById(id).classList.remove('active')
    });
  }

  setupHudTrigger('hud1', 10, 30);
  setupHudTrigger('hud2', 35, 60);
  setupHudTrigger('hud3', 65, 90);
});
</script>

</body>
</html>
```

---

## 4. Alternative Architecture: Direct HTML5 Video Scrubbing

For projects using a single compressed `.mp4` video with Intra-frame encoding (`-g 1`):

```javascript
const video = document.getElementById('scrubVideo');
video.pause();

// Ensure metadata is loaded for duration
video.onloadedmetadata = function() {
  gsap.to(video, {
    currentTime: video.duration,
    ease: "none",
    scrollTrigger: {
      trigger: "#videoStage",
      start: "top top",
      end: "bottom bottom",
      scrub: 0.3
    }
  });
};
```

---

## 5. Golden Rules for Apple-Grade Quality

1. **Intra-frame Keyframes (`-g 1`)**: Mandatory for HTML5 video scrub, otherwise scrub stutters on keyframe seeking intervals.
2. **Device Pixel Ratio (DPR)**: Always scale canvas resolution by `window.devicePixelRatio` for razor-sharp Retina output.
3. **Aspect Ratio Cover Math**: Calculate `offsetX` and `offsetY` on canvas resize so frames maintain full-bleed object-fit cover.
4. **Lenis Scroll Interpolation**: Never omit smooth scroll inertia (`Lenis`). Pure native wheel events create discrete steps that degrade video scrubbing.
5. **Mobile Performance Fallback**: On low-power mobile devices (`matchMedia('(prefers-reduced-motion: reduce)')` or low bandwidth), offer automatic video playback or static poster frames instead of heavy scrub calculations.
