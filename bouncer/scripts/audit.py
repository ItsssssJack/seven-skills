#!/usr/bin/env python3
"""The Bouncer — deterministic gates for auditing an agent skill before install.

Usage: python3 audit.py <path-to-skill-dir> [--skills-home ~/.claude/skills]
Stdlib only. Never executes anything inside the audited skill.
"""

import argparse
import base64
import re
import sys
from pathlib import Path

RED, YEL, GRN, CYN, BOLD, DIM, END = "\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[1m", "\033[2m", "\033[0m"

FOOTPRINT_KB_LIMIT = 15          # a good skill stays under 15KB of always-loadable body
DESC_CHAR_LIMIT = 300            # description sits in the system prompt on EVERY turn
IDLE_TOKEN_ESTIMATE = 4          # chars per token, rough

# Gate 3 patterns: each is (label, compiled regex)
INJECTION_PATTERNS = [
    ("override-instruction", re.compile(r"ignore (all |any )?(previous|prior|above) instructions", re.I)),
    ("concealment", re.compile(r"(do not|don't|never) (tell|mention|reveal|show|inform)( this)?( to)? (the )?(user|human)", re.I)),
    ("silent-action", re.compile(r"\b(silently|secretly|without (telling|asking|notifying))\b", re.I)),
    ("credential-read", re.compile(r"(~\/\.ssh|id_rsa|id_ed25519|\.aws\/credentials|\.env\b|keychain|\.netrc|api[_ ]?keys?\b.{0,40}(read|cat|copy|collect))", re.I)),
    ("exfil-endpoint", re.compile(r"(curl|wget|fetch|post|upload|send).{0,60}https?:\/\/(?!localhost|127\.0\.0\.1)", re.I)),
    ("autonomy-grab", re.compile(r"(every (session|turn|response)|always run|on (start|startup|every prompt)).{0,60}(without|automatic)", re.I)),
]
B64_BLOB = re.compile(r"[A-Za-z0-9+/=]{120,}")


def read_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def gate1_footprint(skill_dir: Path):
    body_files = [p for p in skill_dir.rglob("*") if p.is_file() and p.suffix.lower() in (".md", ".txt")]
    always_loaded = skill_dir / "SKILL.md"
    total_kb = sum(p.stat().st_size for p in body_files) / 1024
    skill_kb = always_loaded.stat().st_size / 1024 if always_loaded.exists() else 0
    tokens = int(always_loaded.stat().st_size / IDLE_TOKEN_ESTIMATE) if always_loaded.exists() else 0
    fm = read_frontmatter(always_loaded.read_text(errors="ignore")) if always_loaded.exists() else {}
    desc = fm.get("description", "")
    flags = []
    if skill_kb > FOOTPRINT_KB_LIMIT:
        flags.append(f"SKILL.md is {skill_kb:.1f}KB (limit {FOOTPRINT_KB_LIMIT}KB) — this loads in full when triggered")
    if len(desc) > DESC_CHAR_LIMIT:
        flags.append(f"description is {len(desc)} chars — it sits in the system prompt on every single turn")
    if not desc:
        flags.append("no description frontmatter — the agent can't know when to trigger it")
    return flags, skill_kb, total_kb, tokens, desc


def gate2_overlap(desc: str, skill_name: str, skills_home: Path):
    if not skills_home.exists():
        return [], []
    words = {w for w in re.findall(r"[a-z]{4,}", desc.lower())
             if w not in {"when", "this", "that", "with", "your", "trigger", "skill", "user", "asks", "wants", "uses", "use", "them", "then", "into", "from", "will", "should"}}
    collisions = []
    for other in sorted(skills_home.glob("*/SKILL.md")):
        oname = other.parent.name
        if oname == skill_name:
            continue
        ofm = read_frontmatter(other.read_text(errors="ignore"))
        odesc = ofm.get("description", "").lower()
        owords = set(re.findall(r"[a-z]{4,}", odesc))
        shared = words & owords
        if len(shared) >= 5:
            collisions.append((oname, sorted(shared)[:6]))
    return collisions, words


def gate3_injection(skill_dir: Path):
    findings = []
    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in (".md", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"):
            continue
        try:
            lines = p.read_text(errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            for label, pat in INJECTION_PATTERNS:
                if pat.search(line):
                    findings.append((label, p.name, i, line.strip()[:110]))
            m = B64_BLOB.search(line)
            if m:
                try:
                    base64.b64decode(m.group(0)[: len(m.group(0)) // 4 * 4])
                    findings.append(("base64-blob", p.name, i, f"{len(m.group(0))}-char encoded blob (decode and read it before trusting)"))
                except Exception:
                    pass
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir", type=Path)
    ap.add_argument("--skills-home", type=Path, default=Path.home() / ".claude" / "skills")
    args = ap.parse_args()

    d = args.skill_dir.resolve()
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    name = d.name

    f1_flags, skill_kb, total_kb, tokens, desc = gate1_footprint(d)
    collisions, _ = gate2_overlap(desc, name, args.skills_home.expanduser())
    findings = gate3_injection(d)

    per_call = int(skill_kb * 1024 / IDLE_TOKEN_ESTIMATE)
    idle = int(len(desc) / IDLE_TOKEN_ESTIMATE)

    print(f"\n{BOLD}🚪 BOUNCER VERDICT: {name}{END}")
    print("━" * 46)

    g1 = f"{GRN}PASS{END}" if not f1_flags else f"{YEL}FLAG{END}"
    print(f"{BOLD}Gate 1 FOOTPRINT{END}   {g1}  {skill_kb:.1f}KB SKILL.md / {total_kb:.1f}KB total, ~{tokens:,} tokens when triggered")
    for fl in f1_flags:
        print(f"   {YEL}⚠ {fl}{END}")

    g2 = f"{GRN}PASS{END}" if not collisions else f"{YEL}FLAG{END}"
    print(f"{BOLD}Gate 2 OVERLAP{END}     {g2}  {len(collisions)} trigger collision(s) with installed skills")
    for oname, shared in collisions:
        print(f"   {YEL}⚠ collides with '{oname}' on: {', '.join(shared)}{END}")

    g3 = f"{GRN}PASS{END}" if not findings else f"{RED}DENY{END}"
    print(f"{BOLD}Gate 3 INJECTION{END}   {g3}  {len(findings)} finding(s)")
    for label, fname, line, snippet in findings:
        print(f"   {RED}✗ [{label}] {fname}:{line} — {snippet}{END}")

    print(f"{BOLD}Gate 4 COST{END}        ~{per_call:,} tokens per invocation, ~{idle} tokens idle tax every turn")
    print("━" * 46)

    if findings:
        tier, color = "DENY & QUARANTINE", RED
    elif f1_flags or collisions:
        tier, color = "ASK FIRST (trial only)", YEL
    else:
        tier, color = "AUTO-ALLOW", GRN
    print(f"{BOLD}TIER: {color}{tier}{END}\n")
    print(f"{DIM}Gate 5 (Daily Driver score) is judgment, not regex — the agent scores it after reading the body.{END}\n")


if __name__ == "__main__":
    main()
