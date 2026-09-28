# Agent Skills

A curated library of agent skills for [Claude Code](https://claude.com/claude-code) and compatible agent harnesses — covering paid ads auditing, SEO/GEO/AEO, Shopify development, web design, video/image generation, marketing automation, DevOps, and more.

Shared by [Biznomad](https://github.com/Biznomad). Client-specific data, credentials, and infrastructure references have been scrubbed; example names like "Example Brand" and `203.0.113.x` IPs are placeholders — swap in your own.

## Install

Each top-level folder is one skill (a `SKILL.md` plus optional `references/`, `scripts/`, `assets/`).

**Claude Code (all skills):**

```bash
git clone https://github.com/Biznomad/agent-skills.git
cp -R agent-skills/* ~/.claude/skills/
```

**Single skill:**

```bash
cp -R agent-skills/<skill-name> ~/.claude/skills/
```

Skills load automatically; invoke by name (`/skill-name`) or let the agent pick them up from their trigger descriptions.

## Biznomad Shopify CRO audit

[`Biznomad-shopify-cro-audit`](Biznomad-shopify-cro-audit/SKILL.md) provides a full-store CRO, UX, messaging, and functionality audit, optional PostHog analysis, approved fixes with rollback, and NotebookLM media generation. Includes five Python helpers; see the skill for setup and project-specific dependencies.

## Layout

- `SKILL.md` — the skill definition: frontmatter (name, description/triggers) + instructions.
- `references/` — deep-dive docs the skill loads on demand.
- `scripts/` — helper scripts the skill can run.
- `assets/` — templates and static files.

## License

MIT — use freely, attribution appreciated. No warranty; review any skill before running its scripts.
