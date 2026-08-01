---
name: skill-smith
description: The skill that builds skills. Watches for workflows the user repeats manually, drafts a new skill for the pattern, tests it, and submits it to the Bouncer — nothing installs without passing the gates. Trigger on "make this a skill", "I keep doing this manually", the OS skill-recommender flagging a repeated sequence, or "/skill-smith".
---

# The Skill-Smith

Week one, you teach the agent. Week four, it teaches itself. Safely.

## When to forge

Forge a new skill when ANY of:
- The user says "make this a skill" or repeats the same multi-step ask a third time.
- The Claude OS skill-recommender panel flags a repeated manual sequence.
- An overnight run (scout/dream) hits the same manual workaround twice.

Never forge speculatively. A skill nobody asked for three times is shelf-ware.

## The forge protocol

1. **Name the pattern** in one sentence: trigger → steps → output. If it can't be said in one sentence, it's two skills or zero.
2. **Draft** the skill in a QUARANTINE dir (`~/Desktop/seven-skills/.forge/<name>/`), never directly into `~/.claude/skills/`:
   - Frontmatter: name + description under 300 chars with explicit trigger phrases that DON'T collide with installed skills (check first).
   - Body under 15KB. Steps imperative, verifiable, with one worked example.
   - Reference files only if the body would otherwise exceed the limit.
3. **Dry-run test**: execute the skill's steps once end-to-end on a real example. Fix what breaks. A skill that hasn't run isn't a skill, it's a wish.
4. **Face the Bouncer**: `python3 ~/Desktop/seven-skills/bouncer/scripts/audit.py <quarantine-dir>`.
   - AUTO-ALLOW → install to `~/.claude/skills/`, announce with a one-line changelog.
   - ASK FIRST → show the user the flags, install only on their yes.
   - DENY → never install; report the finding verbatim. No exceptions, including for skills this forge wrote itself.
5. **Log the birth** to the OS: name, date, pattern it automates, estimated minutes saved per week.

## The compounding rule

Once a month, review forged skills against the Daily Driver test: anything that hasn't fired in 30 days gets retired to the archive. The library stays small, sharp, and audited. Growth without pruning is how you end up with 989 skills and a bricked agent.
