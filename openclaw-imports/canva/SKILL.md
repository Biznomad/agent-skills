---
name: canva
description: Create, search, edit, and manage Canva designs via the mcporter CLI bridge to Canva MCP. Use when users want to generate designs, search existing designs, export designs, manage folders, or comment on designs.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["mcporter"]}}}
---

# Canva MCP Integration

Access Canva's full design platform through mcporter.

## Quick Reference

### Search & Browse

```bash
mcporter call canva.search-designs query="marketing"
mcporter call canva.list-folder-items folder_id="<id>"
mcporter call canva.search-folders query="brand"
```

### Get Design Details

```bash
mcporter call canva.get-design design_id="<id>"
mcporter call canva.get-design-pages design_id="<id>"
mcporter call canva.get-design-content design_id="<id>" content_types=richtexts
```

### Generate Designs (AI-powered)

```bash
mcporter call canva.generate-design query="professional Instagram post for wellness brand" design_type=instagram_post
mcporter call canva.create-design-from-candidate job_id="<job_id>" candidate_id="<candidate_id>"
```

Available design types: business_card, card, doc, document, facebook_cover, facebook_post, flyer, infographic, instagram_post, invitation, logo, phone_wallpaper, photo_collage, pinterest_pin, postcard, poster, presentation, proposal, report, resume, twitter_post, your_story, youtube_banner, youtube_thumbnail

### Export & Download

```bash
mcporter call canva.get-export-formats design_id="<id>"
mcporter call canva.export-design design_id="<id>" format=png
```

### Upload & Import

```bash
mcporter call canva.upload-asset-from-url url="https://example.com/image.jpg" name="Product Photo"
mcporter call canva.import-design-from-url url="https://example.com/design.pdf" name="Imported Design"
```

### Folders

```bash
mcporter call canva.create-folder name="Client Assets" parent_folder_id="<id>"
mcporter call canva.move-item-to-folder item_id="<id>" to_folder_id="<id>"
```

### Comments & Collaboration

```bash
mcporter call canva.comment-on-design design_id="<id>" message_plaintext="Looks good!"
mcporter call canva.list-comments design_id="<id>"
mcporter call canva.reply-to-comment design_id="<id>" comment_id="<id>" message_plaintext="Thanks!"
```

### Brand Kits

```bash
mcporter call canva.list-brand-kits
```

### Shortlinks

```bash
mcporter call canva.resolve-shortlink shortlink_id="abc123"
```

## Tips

- Always include `user_intent` parameter for better AI-generated results
- Use `--output json` with mcporter for machine-readable output
- Design IDs look like: DAGip_FRf4g
- For pagination, use the `continuation` token from previous responses
- The `generate-design` tool uses AI to create designs from text descriptions

## Auth

OAuth tokens are cached at `/data/.mcp-auth/`. Tokens auto-refresh via refresh_token.
If auth expires, run locally on user's Mac:

```bash
npx mcp-remote https://mcp.canva.com/mcp 3333
```

Then copy `~/.mcp-auth/mcp-remote-0.1.37/` to `/data/.mcp-auth/mcp-remote-0.1.37/` on the VPS.
