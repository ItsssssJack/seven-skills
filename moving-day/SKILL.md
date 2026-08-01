---
name: moving-day
description: Move the agent's brain to a server that never sleeps. One command deploys Hermes Agent + Claude OS onto a fresh Linux VPS (hosting.com), hardens it, wires systemd + watchdog + nightly Dream, connects Telegram, and verifies end to end. Trigger on "deploy my agent", "set up the VPS", "moving day", "/moving-day".
---

# Moving Day

Your laptop closes. Your agent shouldn't. This skill moves the brain to a VPS and keeps the window on your machine.

Prereqs the user must provide: VPS IP + root SSH access (hosting.com 12-month XS or S unmanaged Linux plan), and optionally a domain. Ask for these first, then run the phases IN ORDER, verifying each before the next. Announce each phase in one line as you go.

## Phase 1 — Harden the box (5 min)

```bash
ssh root@<IP> "apt update && apt upgrade -y && adduser --disabled-password --gecos '' claudeos && usermod -aG sudo claudeos && mkdir -p /home/claudeos/.ssh && cp ~/.ssh/authorized_keys /home/claudeos/.ssh/ && chown -R claudeos:claudeos /home/claudeos/.ssh"
ssh root@<IP> "ufw allow OpenSSH && ufw allow 80,443/tcp && ufw --force enable && sed -i 's/#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && systemctl restart ssh"
```
Verify: `ssh claudeos@<IP> whoami` returns claudeos; root login refused.

## Phase 2 — Runtime + agents (10 min)

As claudeos: install bun + node + git + tmux, clone the Claude OS repo (VPS-mode branch with `deploy/` units) to `/opt/claude-os/app`, `bun install`, copy `.env.example` → `.env.local` and set: `CLAUDE_OS_TRUSTED_HOSTS=<domain>`, `HERMES_HOME`, `CLAUDE_OS_CLAUDE_DIR`, plan declarations (`CLAUDE_OS_CLAUDE_PLAN`), `CLAUDE_OS_AGENT_DREAM_DIR=/opt/agent-dream`. Install Hermes agent under the same user with its data dir on a mounted volume.

## Phase 3 — Always-on plumbing (10 min)

```bash
sudo cp /opt/claude-os/app/deploy/*.service /opt/claude-os/app/deploy/*.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now claude-os.service claude-os-aggregate.timer claude-os-watchdog.timer
```
Reverse proxy with Caddy (auto-HTTPS): `<domain> { reverse_proxy 127.0.0.1:8081 }`. Verify: dashboard loads at the domain, watchdog restarts the service if you kill it (test once).

## Phase 4 — The Night Shift (10 min)

1. Cron the overnight jobs as claudeos: scout run at 04:00, Dream write at 06:30, morning brief at 07:00 (local user timezone).
2. Agent-fulfilled Dreams: drop the dream SKILL.md contract in `CLAUDE_OS_AGENT_DREAM_DIR`, confirm wizard step 7 shows "agent-fulfilled: ready".
3. Telegram gateway: connect the bot token so the user can message the agent from their phone; send the proof message: "🌙 I'm in. The night shift starts tonight."

## Phase 5 — Verify like you mean it

- Dashboard reachable over HTTPS at the domain, localhost-only otherwise.
- `systemctl status` green on all three units after a reboot (`sudo reboot`, wait, re-check).
- Send a Telegram message, get a reply from the VPS agent.
- Next morning: Dream card populated + morning brief delivered. THEN call it done.

## Rules

- Never store API keys in shell history: write them straight into `.env.local` over SSH stdin.
- Every phase verifies before the next starts. A failed verify halts the move and reports plainly.
- The laptop keeps a full backup of the agent folder BEFORE the move (the folder is the agent).
