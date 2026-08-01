---
name: route
description: Token-saving model router. Detects which AI providers and CLIs you have (ChatGPT/Codex, Gemini, Grok, OpenRouter, Hermes, local Ollama), then routes each task to the cheapest capable one — delegating grunt work to a cheaper CLI/local model, or switching the whole session's base model. Trigger on /route, "route this", "run this locally", "use the cheapest model", "save tokens", "which model should I use for X", or before any big batch/mechanical/long-context job that doesn't need frontier reasoning.
---

# /route — Token-Saving Model Router

Route each task to the **cheapest model that can actually do it**, instead of burning frontier tokens on work a small/local/subscription model handles fine. Two mechanisms:

- **Delegate** (works live, no restart): keep Claude as the brain, shell out a sub-task to a cheaper CLI or local model, bring the result back.
- **Base-switch** (whole session, needs restart): repoint Claude Code's base model to a cheaper provider for an entire session — same mechanism as `/free-mode`.

## When to use

- `/route` or "route this", "do this on the cheapest model", "run it locally", "save tokens / save $", "which model for X?"
- Before a **batch / mechanical** job (bulk refactors, find-replace-at-scale, boilerplate, test generation)
- Before a **huge-context read** (summarize a giant file / repo) that doesn't need deep reasoning
- When the work is **private** and shouldn't leave the machine

**Don't route** a single genuinely-hard reasoning task — just run it on the frontier model. Routing has overhead; only pay it when the task is cheap-able.

## Step 1 — Detect what's available

Run this first and read the result (caches a profile to `~/.claude/skills/route/providers.json`):

```bash
ROUTE_DIR=~/.claude/skills/route
echo "=== Agent CLIs ==="
for c in ollama codex gemini grok hermes claude; do
  p=$(command -v "$c" 2>/dev/null) && echo "  $c: $p" || echo "  $c: MISSING"
done
echo "=== Local Ollama models ==="
ollama list 2>/dev/null | tail -n +2 | awk 'NF{print "  "$1}' || echo "  (ollama not running)"
[ -z "$(ollama list 2>/dev/null | tail -n +2)" ] && echo "  ⚠ NO MODELS PULLED — run: ollama pull qwen2.5-coder:7b"
echo "=== Provider keys ==="
for k in OPENAI_API_KEY OPENROUTER_API_KEY XAI_API_KEY GEMINI_API_KEY ANTHROPIC_API_KEY; do
  [ -n "$(printenv $k)" ] && echo "  $k: set" || echo "  $k: —"
done
[ -f ~/.config/jack-keys.env ] && echo "  (also source ~/.config/jack-keys.env for stored keys)"
```

## Step 2 — First run: confirm the stack

If `providers.json` is missing (or the user says "re-detect" / "I added a provider"), ask which of these they have **and want to use**, then save the answers:

1. **ChatGPT / OpenAI** — Codex CLI (`codex`) or `OPENAI_API_KEY`
2. **Google Gemini** — `gemini` CLI or `GEMINI_API_KEY`
3. **Grok / xAI** — `XAI_API_KEY`
4. **OpenRouter** — `OPENROUTER_API_KEY` (gives free + cheap models; see `/free-mode`)
5. **Hermes (Nous)** — `hermes` CLI
6. **Local (Ollama)** — and which models are pulled

Persist to `~/.claude/skills/route/providers.json` so later runs skip the questions.

## The routing table

| Task class | Route to | Why |
|---|---|---|
| Private / sensitive data | **Local Ollama only** | Never leaves the machine |
| Bulk / mechanical / boilerplate | Local Ollama → else cheapest API | Volume work, low reasoning |
| Huge-context read / summarize | **Gemini CLI** | Big context window, cheap per token |
| Agentic code grunt (refactor, scaffold) | **Codex CLI** (in a git repo) | Purpose-built, runs on your ChatGPT sub |
| Multi-tool / autonomous run | **Hermes** | Native tool-calling + routing |
| Cheap overflow when local is busy | **OpenRouter** free/cheap model | $0–pennies |
| Hard reasoning / architecture / final synthesis | **Stay on Claude** (or frontier) | Worth the tokens |

## Step 3 — Route the task (delegation, works live)

Pick the target, then shell out via Bash and bring the output back for Claude to review/assemble:

```bash
# Local / private / bulk  (free, offline)
ollama run qwen2.5-coder:7b "<prompt>"

# Huge-context read or summary  (cheap, big window)
gemini -p "<prompt>"                      # or:  cat bigfile | gemini -p "summarize"

# Agentic code grunt work  (must be inside a git repo)
codex exec --full-auto "<prompt>"

# Autonomous / multi-tool run
hermes -z "<prompt>"
```

Then **Claude reviews/finishes** the cheap model's output. The frontier model stays the orchestrator; it just stops doing the cheap parts itself.

## Whole-session cheap mode (base-switch, needs restart)

When the *entire* session is routine work, switch the base model for the whole session instead of delegating task-by-task — identical mechanism to `/free-mode`: set `ANTHROPIC_BASE_URL` + `ANTHROPIC_MODEL` in `~/.claude/settings.json` to a cheaper provider, then restart Claude Code. Use `/free-mode on` for the OpenRouter/Qwen path. Always **confirm with the user** before a base-switch — it forces a restart.

## Cost ladder (try cheapest first, escalate only on failure)

1. **Local Ollama** — $0, private, offline
2. **A subscription you already pay for** (ChatGPT via Codex, Gemini) — sunk cost, no marginal tokens
3. **OpenRouter** free / cheap models
4. **Frontier** (Claude / GPT / Grok premium) — reserve for the hard ~20%

## Principles

- Default to the cheapest plausible model; escalate **only** when it fails or the output is weak.
- Private/sensitive → local only. Never route confidential code or client data off-machine.
- The frontier model is the **brain**; cheap models are the **hands**.
- One model is never strictly best — route by the *specific* task in front of you.
- Confirm before any base-switch (restart required).

## Setup gaps (the detector flags these)

- **No Ollama models** → `ollama pull qwen2.5-coder:7b` (great small coder; use `:32b` if you have ~24GB+ RAM). This is the #1 thing to fix — without it there's no local tier.
- **No OpenRouter key** → run `/free-mode` to get the free Qwen3-Coder path.
- **No Grok** → add `XAI_API_KEY` (or wire Grok via OpenRouter).
