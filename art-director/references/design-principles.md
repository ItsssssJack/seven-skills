# Design Principles — the distilled taste system

Synthesized from Jack's chapter deliverables + Jack's taste-design skill (the power-design ruleset) + the strongest public design skills (ui-ux-pro-max 112K★, taste-skill 70K★, hallmark 20K★, make-interfaces-feel-better 2.6K★). One opinion per topic; Jack's system wins every tie.

## The power-design rules (from Jack's taste-design skill, always enforced)

- **Max 1 accent color, saturation below 80%.** The "AI purple/blue neon" aesthetic is BANNED: no purple button glows, no neon gradients.
- Absolute neutral bases (zinc/slate), never pure `#000000`, one palette per output with no warm/cool gray drift.
- Hierarchy through weight and color, not screaming size. Body max 65 chars per line, relaxed leading.
- For premium/creative work prefer distinctive faces (Geist, Outfit, Satoshi; editorial serifs like Fraunces or Instrument Serif). Serif never appears in dashboards. Numbers go monospace when density is high.
- Motion is spring-physics micro-interaction, perpetual but subtle; nothing blocking, nothing looping loudly.
- The atmosphere dials: density (airy → cockpit), variance (symmetric → artsy), motion (static → cinematic). Pick the dials before designing, then obey them.

## Color

- Base: `#07090f` background, `#0d1119` panels, `#1d2537` borders. Blue-tinted darkness, never gray, never pure black.
- Text: `#e8ecf4` primary, `#8b95ab` muted, `#5b6478` dim. Three levels only.
- Accents: blue `#4d8dff`, teal `#2dd4bf`, violet `#a78bfa` as the traveling gradient; amber `#fbbf24` for money/highlight; red `#f87171` danger; green `#4ade80` success.
- Rule of one: each screen has ONE dominant accent moment. The gradient is seasoning, not sauce.
- Radial glow behind heroes: `radial-gradient(1200px 400px at 50% -10%, rgba(77,141,255,.12), transparent)`.

## Typography

- Display: heavy sans (Inter 800 / Archivo) with ONE italic serif accent word in a contrasting accent color. "The engine and the *window*."
- Numbers: Space Grotesk, always, at every size. Tabular where values update.
- Kickers/labels: mono or letterspaced caps, 11-13px, `.18em` tracking, accent color.
- Body: 14-16px, 1.55 line height, max 800px measure.
- Serif italic for subtitles and metaphor lines. It is the "human voice" register.

## Layout

- One-column narrative scroll for chapters/reports; grid only for comparable items (stats, cards, options).
- Section rhythm: kicker chip → headline → serif subtitle → content blocks → action strip. Repeat. The reader always knows where they are.
- Vertical connector dots/lines between major sections (the journey line).
- Whitespace is the luxury signal: 48px+ between sections, 20px+ card padding.
- Asymmetry beats centering for content blocks; center only heroes and section heads.

## Components

- Stat tile: huge Space Grotesk value, tiny caps label, optional source line.
- Metaphor card ("THINK OF IT LIKE"): icon left, italic serif analogy title, 2-line body, accent border.
- Action strip ("SO WHAT →"): mono, dark panel, key phrase highlighted in accent.
- Verdict/tier cards: colored left border + tier chip (AUTO-ALLOW green / ASK FIRST amber / DENY red).
- Incident card ("NIGHTMARE FILE #"): red border, big stat right, root-cause strip bottom, VERIFIED chip.
- Quote/receipt card: panel background, verbatim text, attribution line with ▲likes.
- Table: caps 11px headers, hairline row borders, generous cell padding, wrapped in a rounded panel.

## Motion (when interactive)

- 150-250ms transitions, ease-out. Interruptible, never blocking.
- Hover: lift 2px + border brighten. No scale jumps.
- Numbers count up once on first view. Nothing loops forever except subtle hero glow.

## Anti-slop checklist (from the public skills, kept because they are right)

- No orphaned single words on headline last lines (balance text wrapping).
- Concentric border radii: inner radius = outer radius minus padding.
- No default purple-blue gradient on white. No emoji as content. No three-column feature grids with icon-title-text repeated six times.
- Icons react on hover (opacity/scale), decorative icons are line-art not emoji.
- Every screen answers: what is the ONE thing this screen wants me to know?
