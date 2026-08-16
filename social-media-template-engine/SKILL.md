---
name: social-media-template-engine
description: Build HTML-based social media carousel/post templates by iterating from a reference profile's aesthetic. Used when the user wants custom visual templates for Instagram/LinkedIn/Twitter content.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, templates, design, carousel, instagram]
    related_skills: [notion-content-repurposing-pipeline]
---

# Social Media Template Engine

Build HTML-based social media carousel/post templates by iterating from a reference profile's aesthetic.

## Trigger
User wants carousel templates, post designs, or visual content assets for social media.

## Workflow

1. **Get the reference**. Ask the user what Instagram account or visual style they want to emulate. If they provide a profile URL, attempt to access it (browser, image search, content analyzer). If blocked by login walls, ask the user to describe the style or proceed from known aesthetics.

2. **Build v1 HTML template**. Create a single self-contained HTML file (1080x1080px canvas) with:
   - Pure black or very dark background (#0a0a0a / #080808)
   - Reference-matching typography (Space Grotesk, JetBrains Mono, Inter)
   - One accent color per template/pillar
   - Topic-specific background graphics (CSS/SVG based)
   - Massive headline text (120px+)
   - Corner brackets, scanlines, or other reference-matching chrome
   - All text content centered, uppercase, bold

3. **Screenshot and review**. Navigate to the HTML file in browser, use browser_vision to screenshot. Show the user.

4. **Iterate based on feedback**. Common feedback patterns:
   - "Text too small" → Increase headline from ~60px to 120-140px
   - "Backgrounds blank" → Increase background element opacity (0.2 → 0.5), reduce dark overlay intensity
   - "Too busy / not like reference" → Strip back to the reference's core aesthetic (simplifyinai = pure black, massive text, one accent, negative space)
   - "Need actual graphics" → Replace abstract shapes with topic-specific visuals (circuit boards for tech, candlesticks for finance, camera viewfinder for content, radar for security, satellite for trends)

5. **Build all pillars**. Once the base template is approved, duplicate for each content pillar (Tech Stack, Business Strategy, Content & Marketing, Security & Risk, Industry Trends) with:
   - Unique accent color per pillar
   - Topic-specific background graphics
   - Consistent typography and layout structure

6. **Save deliverables**. Store all HTML files in `/root/biznomad-content-factory/templates/` with version folders (v1, v2, v3, v4).

## The Simplifyinai Formula (Naeem's Preferred Style)

When the user sends a reference image of simplifyinai-style posts, the formula is:

1. **White top section** — Tool name (56px bold), subtitle (20px gray), colored badge pills
2. **Dark screenshot area** — Actual tool/product screenshot (not decorative graphics), with overlay elements (price tags, alert boxes, metric strips, announcement badges)
3. **Dark bottom section** — Profile pic + massive headline (52px uppercase) with accent-colored keywords + "SWIPE FOR MORE" pill CTA

Key characteristics:
- Clean, minimal, professional
- The background IS the actual content screenshot
- One accent color per post (purple, green, cyan, red)
- Lots of negative space
- No abstract decorative backgrounds

## Key Pitfalls
- **WAIT for a reference image before building.** Do not assume cyberpunk/hacker aesthetic. Naeem's preference is simplifyinai-style: clean, minimal, screenshot-based. The initial v1-v4 builds were all rejected because I assumed wrong.
- **Background opacity must be tested** — CSS opacity at 0.2 is invisible in screenshots. Use 0.4-0.6 for visible art.
- **Dark overlay kills backgrounds** — use `radial-gradient(ellipse at center, rgba(8,8,8,0.2) 0%, rgba(8,8,8,0.6) 100%)` not 0.8+ opacity.
- **Animated elements (code rain, blinking) don't render in static screenshots** — use static positioned elements instead.
- **User's design reference overrides everything**: If they send a simplifyinai reference, abandon the dark briefing style immediately and rebuild clean.

## Output Format
- One HTML file per pillar
- Screenshot PNGs for visual reference
- Design specs markdown for handoff to designers
