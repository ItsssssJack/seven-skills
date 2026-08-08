# The Seven Skills

**Stop installing skills. Start hiring them.**

Skills are hires. Most people install 100 interns and wonder why the office is chaos. These are the employees for your agent (Claude Code or Hermes Agent), each one earning its seat: judgment → taste → understanding → its own computer → economics → initiative → self-creation.

![Seven Skills](assets/00-hero.jpg)

## The team

| # | Hire | Folder | What it does |
|---|------|--------|--------------|
| 1 | **The Bouncer** | [`bouncer/`](bouncer/) | Audits any skill before it installs: searches for better alternatives first, then gates footprint, overlap, hidden instructions and cost. |
| 2 | **The Art Director** | [`art-director/`](art-director/) | Locks your taste into everything the agent ships. One dispatcher + reference modules loaded on demand. |
| 3 | **The Cartographer** | [`graphify/`](graphify/) | Anything → knowledge graph. The agent queries the map instead of re-reading files. |
| 4 | **Moving Day** | [`moving-day/`](moving-day/) | One command moves the agent to a Linux VPS that never sleeps: harden, install, systemd, watchdog, Telegram. |
| 5 | **The Dispatcher** | [`route/`](route/) | Routes every job to the cheapest model that can actually do it. Frontier for thinking, budget for grunt work. |
| 6 | **The Dreamer** | [Notion page](https://app.notion.com/p/3afe8d6bd13781e5b9f9fd84e52f3e3d) | Thinks about your day (email, calendar, notes, activity) while you sleep. Morning prescriptions. Skill file lives on the page. |
| 7 | **The Professor** | [mattpocock/skills](https://github.com/mattpocock/skills) | The final hire teaches the boss: Matt Pocock's 198k★ pack (Grill Me · Caveat · Teach Me). Not ours — that's the point. |
| + | **Bonus: Agent Reach** | [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | Eyes on the whole internet, 63k★. |

## Install a skill

```bash
git clone https://github.com/ItsssssJack/seven-skills
cp -r seven-skills/art-director ~/.claude/skills/
```

## The Daily Driver Test

A skill earns its seat by scoring on five checks:

1. **Fires daily** — if it didn't run this week, it's shelf-ware
2. **Earns its tokens** — value out > tokens in, under ~15KB
3. **Runs without you** — no babysitting
4. **Compounds** — today's output improves tomorrow's run
5. **Survives an audit** — you know what it reads, where it sends, what it costs

5/5 daily driver · 4 keep · 3 one-week trial · ≤2 delete.

---

Built for the video by [AI Automations with Jack](https://www.youtube.com/@AIAutomationswithJack). Moving Day builds on the community VPS-mode work for Claude OS, and the Art Director distills principles from the giants: ui-ux-pro-max-skill, taste-skill, hallmark, make-interfaces-feel-better.
