---
name: scroll-scrub-hero
description: Build a cinematic scroll-scrubbed hero — a sticky canvas that plays a video frame-by-frame as the user scrolls, with real HTML copy on top. Use when asked for a "scroll animation", "scrollytelling hero", "Apple-style scroll video", "video that plays as you scroll", "cinematic hero", or to replicate the exampleclientjunk.com / OFFMARKET hero on another site. Covers sourcing footage (AI-generated or filmed), frame extraction and interpolation, WebP encoding, the sticky-canvas driver, and the QA gate.
version: 1.0.0
---

# Scroll-Scrub Hero

A sticky `<canvas>` that advances through a WebP frame sequence as the page scrolls, with
**real DOM copy** layered over it. Proven on `exampleclientjunk.com` and
`deals.example.com`.

## The one rule that matters

**Never bake copy into the frames.** If the headline lives in the pixels, it is invisible
to search engines and screen readers, untranslatable, unselectable, and — the failure that
actually bites — it is cropped away the moment the viewport aspect changes. A 16:9 frame
cover-cropped to a 0.46-aspect phone loses ~74% of its width, taking the headline with it.

Copy is centred DOM. The frames are the backdrop. Always.

---

## Pipeline

### 1. Source footage

Needs a **single continuous camera move, no cuts**, so scroll position maps to depth.
A cut mid-sequence reads as a glitch when scrubbed.

Generated (Higgsfield Seedance 2.0 via CLI — see the `seedance-*` skills for prompt craft):

    higgsfield generate create seedance_2_0 --prompt "$(cat prompt.txt)" \
      --aspect_ratio 16:9 --duration 8 --resolution 1080p --generate_audio false --json
    higgsfield generate wait <job_id> --json      # -> result_url

Prompt must state: *"a single continuous unbroken shot — no cuts, no scene changes"*,
one named camera move, and a negative list including `no text, no captions, no titles,
no watermarks, no logos`. Text in frames defeats rule one.

### 2. Decide frame count

    ffprobe -v error -count_frames -select_streams v:0 \
      -show_entries stream=nb_read_frames,r_frame_rate -of default=nw=1 in.mp4

Aim for **~8–10px of scroll per frame**: `frames ≈ (runwayVh - 100) × vh / 9`.
A 300vh runway at 900px tall ≈ 1800px of scroll ≈ 200–290 frames.

Beyond the native count you must interpolate:

    ffmpeg -i in.mp4 -vf "minterpolate=fps=36:mi_mode=mci:mc_mode=aobmc:vsbmc=1,\
    scale=1920:1080:flags=lanczos" -start_number 0 -y png/%04d.png

`aobmc` + `vsbmc` are not optional on scenes with thin structures — bare branches,
power lines, railings, fences. Plain `mi_mode=mci` smears them into mush.
**Always open a synthesised in-between frame (an odd index) at full crop and look**
before encoding the set.

### 3. Encode

ffmpeg on macOS usually has **no libwebp encoder** — extract PNG, then `cwebp`:

    for f in png/*.png; do n=$(basename "$f" .png)
      cwebp -quiet -q 56 -m 5 -sharp_yuv "$f" -o "big/$n.webp"; done
    for f in png/*.png; do n=$(basename "$f" .png)
      cwebp -quiet -q 52 -m 5 -resize 960 540 "$f" -o "sm/$n.webp"; done
    cp big/0000.webp big/photo.webp && cp sm/0000.webp sm/photo.webp   # poster

Budget: q56 at 1920 ≈ 55–60KB/frame. 287 frames ≈ 18MB. Photographic footage compresses
far worse than flat CGI — do not assume a previous set's size carries over.

### 4. Cache busting — the trap

Frame filenames are stable (`0000.webp`), so a new sequence **overwrites the old names**.
Behind a CDN with `max-age`, clients keep serving the previous animation and you will
swear the deploy failed. Bump a `?v=N` on *every* reference at once: the driver, the CSS
poster, any preload, any hero background reusing a frame.

### 5. Markup

    <section class="scrub-sec" id="stage">
      <div class="scrub-stick">
        <canvas class="scrub-canvas" id="scrubCanvas"></canvas>
        <div class="scrub-vignette" aria-hidden="true"></div>
        <div class="scrub-copy">
          <div class="beat" id="beat1">…visible at load…</div>
          <div class="beat" id="beat2" style="opacity:0">…</div>
          <div class="beat" id="beat3" style="opacity:0">…ends on the CTA…</div>
        </div>
        <div class="scrub-cue" id="scrubCue">Scroll ▾</div>
      </div>
    </section>

Beat 1 carries the value proposition and is **opacity 1 at load** — the top of the page
must never be a wordless picture.

See `assets/scrub-hero.html` for the complete drop-in implementation.

---

## Non-negotiables

- **Reset section padding.** A generic `section{padding:Xpx 0}` rule pushes the sticky
  child down and leaves a band of background under the nav. `.scrub-sec{padding:0;margin:0}`.
- **Poster background on the sticky element**, set to frame 0, so first paint is the
  scene rather than black.
- **Eager-load ~10 frames, then the rest on `requestIdleCallback`** so the sequence never
  competes with the hero for bandwidth.
- **`nearest(i)` fallback** — draw the closest loaded frame so scrubbing mid-stream never
  shows a hole.
- **DPR capped at 2** in `drawCover`.
- **Mobile runs it too.** Walk the same sequence in larger steps (~120 of 287) rather than
  shipping a second set. Skipping it on phones throws away the majority of traffic.
- **Reduced motion**: collapse the runway to `100vh`, jump to the final frame, show the
  closing beat, hide the cue. Static but complete — never blank.
- Use a plain rAF driver. GSAP ScrollTrigger works but is ~60KB to lerp one number.

## QA gate

- [ ] Beat 1 legible at scroll 0; headline is DOM text, not pixels
- [ ] Sticky element flush under the nav (measure `getBoundingClientRect().top`)
- [ ] Progress advances evenly across 8 sampled scroll positions
- [ ] Mobile at 390w: animation runs, no horizontal overflow, reduced frame count confirmed
- [ ] Reduced-motion emulation: readable, closing CTA present
- [ ] `?v=` bumped on every frame reference; verify a frame URL returns the *new* bytes
- [ ] No console errors after a full scroll-through
- [ ] Interpolated set: a synthesised frame inspected at full crop

## Gotchas paid for in blood

| Symptom | Cause |
|---|---|
| Hero blank for reduced-motion users | Branch set `height:0` and never called `draw()` |
| Copy vanishes on phones | Text baked into a 16:9 frame, cropped out in portrait |
| Canvas renders but nothing shows | `IntersectionObserver` callback tested `es.some()`; it only reports *changed* entries, so a second target leaving cleared the class. Track membership in a `Set` |
| Old animation persists after deploy | `?v=` not bumped; CDN served the previous frames |
| Black band under the nav | Inherited `section` padding on the scrub section |
| `p` is `NaN`, nothing animates | `prog()` divided by `(sectionHeight - innerHeight)` when the runway was collapsed to one screen. Guard the zero |
| Deferral does nothing | `IntersectionObserver` `rootMargin:100%` counts the stage as visible at scroll 0 on a short page. Use ~50% |
