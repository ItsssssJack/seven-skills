---
name: scout
description: Overnight research runs that end in a morning brief. Watches competitors, comment demand, GitHub trends and niche signals while the user sleeps, writes one skimmable brief with receipts. Trigger on "run the scout", "what did the scout find", "/scout", or as the 04:00 cron on the VPS.
---

# The Scout

Initiative is a skill. The Scout goes looking so the user doesn't have to.

## The nightly run (cron 04:00 on the VPS, or on demand)

1. **Own channel pulse** — yesterday's views/subs/comments on recent uploads (YouTube API, keys in `~/.config/jack-keys.env`). Flag any video beating its 3-day median.
2. **Competitor sweep** — new uploads in the warehouse (yt-intel Supabase), outlier scores, retitle events (title changed since last scrape = packaging signal, always flag).
3. **Comment demand** — new comments on own recent uploads; cluster repeated asks (3+ unique commenters = cluster, even at 0 likes).
4. **GitHub trend check** — star velocity on tracked repos + search for new skill/agent repos created in the last 14 days over 500 stars. Verify every count via API before reporting.
5. **X/Reddit signal** (via agent-reach) — only items under 5 days old. Older = already peaked, skip.

## The morning brief (07:00, Telegram + file)

One screen, max. Format:

```
☀️ SCOUT BRIEF — <date>
TOP SIGNAL: <the one thing worth acting on today, with receipt>
CHANNEL: <pulse in one line>
COMPETITORS: <2-3 lines, outliers + retitles only>
DEMAND: <top comment cluster with count>
FRESH: <1-2 new repos/tools with verified stars>
SKIP: <what looked hot but fails recency/verification, one line>
```

Write the full version with links to `~/Desktop/📋 Notes & Markdown/scout-brief-<date>.md`; send the short version to Telegram.

## Rules

- Recency window 2-5 days for trend signals; velocity is not recency.
- Never report a star count, view count or quote without pulling it live first.
- No idea generation: the Scout reports signals and sources, the human does the craft.
- If nothing clears the bar, the brief says "quiet night" in one line. Never pad.
