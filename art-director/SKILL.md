---
name: art-director
description: Jack's mega design skill. One dispatcher that gives the agent taste — dark premium aesthetic, editorial typography, schematic illustrations — for any visual output: HTML pages, presentations, dashboards, course chapters, reports. Trigger on any design/build request for a page, deck, deliverable or UI, or "/art-director".
---

# The Art Director

One skill, one taste system. The agent never guesses what good looks like again.

This is a **dispatcher**: the file you are reading stays small and loads the right reference module for the job. Never load more than two modules for one task.

## Dispatch table

| Task looks like | Load |
|---|---|
| Course chapter, presentation, long-form deliverable | `references/design-principles.md` + `references/page-patterns.md` |
| Dashboard, report, research doc | `references/design-principles.md` |
| Quick artifact (card, one-pager, verdict screen) | `references/page-patterns.md` |
| Anything with charts/data | `references/design-principles.md` + the dataviz skill if installed |

## Non-negotiables (always on, no module needed)

1. **Dark premium base.** Near-black blue-tinted background (#07090f family), never pure black, never light mode unless asked.
2. **Cool gradient accents.** Blue → teal → violet. Gold/amber reserved for money, warnings, and the single most important thing on the page. Red only for danger.
3. **Editorial type contrast.** Big bold sans headlines with ONE italic serif accent word. Space Grotesk for every number. Mono for kickers, labels, and file paths.
4. **One metaphor card per concept** ("THINK OF IT LIKE" pattern): line-art icon, one-line analogy, two-line explanation.
5. **Section rhythm**: mono kicker chip → headline with accent word → italic serif subtitle → content → "SO WHAT →" action strip.
6. **Numbers are heroes.** Big stat, small label, source underneath. Never bury a number in a sentence.
7. **No em dashes in copy.** Commas, colons, periods.
8. **Render-verify loop**: screenshot the output with headless Chrome, read the image, fix what looks off, THEN deliver. Never ship unrendered HTML.

## Illustration system

Hero illustrations use the inked-blueprint / Da Vinci schematic style: sepia parchment, fine ink linework, annotated arrows, one human figure for scale. Generate via the visuals/infographic pipeline (nano-banana-2) with the style reference in `~/Desktop/image-assets/preferred-styles/`. One hero illustration per major section, never per paragraph.

## Quality bar

Before delivering, score the output: Would this pass as a $10,000 client deliverable? Is there ONE clear hero element per screen? Can you read every word at arm's length? Does anything look like default AI output (generic cards, purple-on-white, emoji soup)? If any answer is wrong, fix before shipping.
