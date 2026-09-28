---
name: notion-content-repurposing-pipeline
description: Transform saved social media content (from Notion pipeline) into multi-platform branded content for LinkedIn, Twitter/X, Instagram.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, notion, content, repurposing, marketing]
    related_skills: [social-media-template-engine]
---

# Notion Content Repurposing Pipeline

Transform saved social media content (from Notion pipeline) into multi-platform branded content.

## Trigger
User wants to repurpose Notion content pipeline items into posts for LinkedIn, Twitter/X, Instagram, etc.

## Prerequisites
- Notion database "Content Pipeline" is connected and populated
- Items have AI summaries already generated
- User's brand voice profile is known

## Workflow

1. **Read all items** from Notion database query (up to 100). Extract:
   - Title, URL, Category, Source, AI Summary, AI Tags, Action Items
   - All items should have `Processed = false` and `Status = "New"`

2. **Categorize into content pillars**. Group items by topic:
   - AI Tools & Tech Stack (default for Tech Stack category)
   - Business Strategy & Ops (Business Strategy category + business keywords)
   - Content & Marketing (Marketing + Content Ideas categories)
   - Security & Risk (security/hack/vulnerability keywords)
   - Industry Trends (Meta/Microsoft/open source/AGI keywords)

3. **Generate repurposed content** for each item in the user's voice:
   - **LinkedIn Post**: Hook angle + core insight + founder story CTA + hashtags
   - **Twitter/X Thread**: 5-7 tweet thread with hook, breakdown, proof, CTA
   - **Instagram Carousel Caption**: Cover hook + swipe prompt + body + CTA + hashtags
   - **Image Design Brief**: Visual metaphor, headline text, color palette, composition notes, deliverable sizes

4. **Save output** as JSON with all formats per item, plus a summary text file for quick scanning.

## Voice Rules
- Match the user's established voice profile (direct, no-BS, ADHD founder)
- Angle: "AI is nothing without the people who harness it"
- Always include a CTA
- Use the brand tagline where appropriate

## Output Location
`~/content-factory/content_factory.json`
