---
name: dispatcher
description: Route every task to the cheapest model that can actually do it. Benchmark-aware routing across frontier APIs, cheap CLIs and local models, with a cost receipt per session. Trigger on "route this", "cheapest model for", "save tokens on this", batch/mechanical jobs, or "/dispatcher".
---

# The Dispatcher

Frontier models for judgment. Cheap models for muscle. Never pay Opus prices for grep work.

Wraps the existing model-router (`/route`) and the Routing Intelligence System. This skill is the POLICY layer the agent applies before starting any substantial task.

## The routing table

| Task class | Route to | Why |
|---|---|---|
| Deep reasoning, architecture, strategy, final copy | Frontier (Fable/Opus tier) | Judgment is the product |
| Code review of own work, verification passes | Frontier, LOW effort | Cheap insurance |
| Bulk mechanical: renames, format conversion, scraping glue | Cheap CLI (Kimi/OpenRouter budget tier) | 10-30x cheaper, quality identical on mechanical work |
| Long-context reading (100K+ tokens of docs/logs) | Large-context cheap model (Gemini tier) | Context window is the requirement, not IQ |
| Overnight/cron jobs (scout runs, digests, dream writes) | Budget tier ALWAYS | Runs 365x/year; cost compounds silently |
| Private/sensitive data | Local (Ollama) when viable | Data never leaves the box |

## Protocol

1. Before any task estimated over ~20K tokens, classify it against the table and state the route in one line: "Routing: bulk transform → Kimi (est. $0.04 vs $1.80 frontier)."
2. Delegate via the available CLI/subagent for that tier; keep frontier context clean.
3. Log actual cost per session to the OS usage panel; the weekly roll-up feeds the Dream review.
4. If the cheap tier fails quality twice, escalate one tier and note it. Never silently retry the same tier 5 times.

## The receipt (say it out loud)

End every routed session with the one-line receipt: tokens spent by tier + what the same work would have cost frontier-only. That delta is the whole point. Target: the full overnight stack (scout + dream + digests) under $1/night.
