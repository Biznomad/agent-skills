---
name: infra-guardian
description: Infrastructure monitoring and self-healing for Biznomad VPS — check service health, detect failures, and remediate issues
version: 1.0.0
metadata:
  hermes:
    tags: [devops, monitoring, systemd, docker, self-healing, infrastructure]
    related_skills: [devops]
---

# Infra Guardian: Infrastructure Monitoring & Self-Healing

## Overview

You are the infrastructure guardian for the Biznomad VPS. You monitor systemd services, Docker containers, system resources, and application logs. You detect failures and either self-heal or escalate to the user.

## Key Tools

- `hermes-infra-status` — Print human-readable status of all services and containers
- `cat /root/.hermes/logs/infra-status.json` — Read structured status (JSON)
- `cat /root/.hermes/logs/infra-alerts.log` — Read recent alerts (JSON lines)
- `systemctl status <service>` — Check a specific service
- `systemctl restart <service>` — Restart a failed service
- `docker ps` — Check running containers
- `docker restart <container>` — Restart a container
- `journalctl -u <service> --no-pager -n 20` — Read recent logs

## Monitored Services

**Systemd services:**
- `biznomad-telegram-bot` — Main Telegram bot
- `hermes-intel-bot` — Hermes intel callback bot
- `biznomad-bot` — Discord bot
- `cloudflared-tunnel` — Cloudflare tunnel
- `hermes-infra-guardian` — This monitoring daemon

**Docker containers:**
- `n8n` — Workflow automation (required)
- `nocodb` — Database frontend (optional)

## What You Do

### When asked "check my bots" or "server status":
1. Run `hermes-infra-status`
2. If issues found, read `infra-status.json` for details
3. Report clearly: what's healthy, what's broken, what was fixed

### When you detect a failure:
1. **Try self-heal first** (if safe):
   - Restart failed systemd service: `systemctl restart <service>`
   - Restart Docker container: `docker restart <container>`
   - Kill duplicate processes if detected
2. **If restart fails 3 times** or issue is critical (token conflict, auth failure):
   - Alert the user via Telegram/WhatsApp with details
   - Do NOT keep restarting in a loop

### Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Telegram conflict | `Conflict: terminated by other getUpdates request` | Find duplicate bot instance and stop it |
| Discord auth fail | `Authentication failed` or `DISALLOWED_INTENTS` | Check token validity, recreate if needed |
| Service restart loop | `auto-restart` with repeated `exit-code` | See **Restart Loop Debugging Playbook** below |

---

## Restart Loop Debugging Playbook

Use this when systemd services are stuck in `activating auto-restart` or cycling rapidly.

### Step 1: Find ALL failing services
Don't assume the user named the right one. Check broadly:
```bash
systemctl list-units --type=service --state=failed,activating --no-pager
systemctl --failed --no-pager
pm2 list 2>/dev/null
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.RestartCount}}" 2>/dev/null
ps aux | grep -i bot | grep -v grep | head -20
```

### Step 2: Pull error logs per service
```bash
journalctl -u <service> --no-pager -n 30
```
Look for distinct error patterns:
- **DB auth**: `InvalidPasswordError`, `password authentication failed`
- **Missing deps**: `MODULE_NOT_FOUND` (Node), `ImportError` (Python), `No module named`
- **Port conflicts**: `EADDRINUSE`, `address already in use`
- **Token/auth**: `TokenInvalid`, `Authentication failed`

### Step 3: Verify before changing

**DB password issues:**
```bash
# Test the exact password from .env before resetting anything
PGPASSWORD=<from_env> psql -h localhost -U <user> -d <db> -c "SELECT 1"
# If it fails, check pg_hba.conf for auth method
# Reset Postgres password ONLY after confirming no working service depends on it
sudo -u postgres psql -c "ALTER USER <user> WITH PASSWORD '<new_pass>';"
```

**Port conflicts:**
```bash
ss -tlnp | grep <port>
lsof -i :<port> 2>/dev/null
# Check what the conflicting process IS before killing or reassigning
ps -fp <pid>
```
Reassign the non-critical service, never the infrastructure bridge.

**Missing npm modules:**
```bash
cd /opt/<bot> && npm install <module> --save
# ALSO check if package.json is wrong — a root index.js may require a module
# that package.json doesn't list (mismatched codebase)
```

### Step 4: Fix and restart
```bash
systemctl daemon-reload
systemctl restart <service>
sleep 5
```

### Step 5: Verify stability
```bash
# Check restart count since last manual restart
systemctl show <service> --property=NRestarts
systemctl is-active <service>
# For Discord/Node bots: an unhandled rejection (e.g., TokenInvalid) may not
# crash the process if a webhook HTTP server keeps it alive. Rely on NRestarts=0,
# not just "no error in last log line."
```

### More Common Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Guardian false-positive restarts** | Service restarts every ~60 min with "Auto-restarted after failure" alerts. Guardian logs show "Cycle complete. 2 issues found." Platform state is `connected` but `updated_at` is stale. | In `hermes-infra-guardian.py`, bump `platform_connected_grace_minutes` from 60 to 1440 (24h). The `updated_at` timestamp only changes on state transitions, so stable connections look "stuck" after 1 hour. Then `systemctl restart hermes-infra-guardian`. |
| OOM kill | `Out of memory` in logs | Restart service, consider adding swap or upgrading |
| Disk full | `No space left on device` | Run `docker system prune -f`, check logs |
| Docker container down | Container not in `docker ps` | `docker restart <container>` |

## Escalation Rules

- **Auto-fix:** Service down, container stopped, minor crash
- **Alert user:** Token conflicts, auth failures, restart loops, disk full, OOM kills
- **Never auto-fix:** Credential changes, token rotations, network config changes

## Status File Location

`/root/.hermes/logs/infra-status.json` — Updated every 30 seconds by the guardian daemon.
