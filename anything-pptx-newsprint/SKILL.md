---
name: pptx
description: General-purpose PowerPoint creation, editing, analysis, and HTML-to-PPTX generation. Supports creating decks from scratch, editing existing PPTX files, using templates, converting HTML slides, and consuming structured handoff files from anything-to-ppt: summary.md, slides_plan.md, images_needed.md, speaker_notes.md, review_checklist.md, and asset folders.
---

# PPTX creation, editing, analysis, and handoff-based generation

This is a general-purpose PowerPoint skill.

It can create or edit decks for many topics, including research talks, project updates, product pitches, training decks, proposals, reviews, reports, and stakeholder presentations.

Do **not** assume the topic or structure in advance. When a handoff directory is provided, infer the deck theme, audience, content, and slide order from `slides_plan.md`.

The default visual style is a Kalam / Patrick Hand hand-drawn sketchbook style. User-provided style, brand, or template instructions override this default.

Before generating or editing a deck, check whether the helper docs and scripts are available in the `pptx` skill directory, especially:

```text
html2pptx.md
ooxml.md
scripts/
```

If those files are missing, do not pretend the full workflow is available. State the limitation and generate the most useful intermediate output, such as HTML slides, an asset map, or an implementation plan.

## 1. Preserve the core pptx workflows

### Create a new deck from scratch

1. Read `html2pptx.md` before generating slides.
2. Create one HTML file per slide, usually 16:9.
3. Convert HTML slides to PowerPoint using `html2pptx.js`.
4. Use PptxGenJS for figures, charts, tables, equations, shapes, highlights, and annotations when HTML conversion is insufficient.
5. Generate thumbnails.
6. Inspect thumbnails.
7. Fix layout issues and regenerate if needed.

### Edit an existing deck

1. Read `ooxml.md` before editing XML.
2. Unpack the deck.
3. Edit OOXML carefully.
4. Validate immediately after edits.
5. Repack the deck.

### Create from a template

1. Extract template text.
2. Generate template thumbnails.
3. Build a template inventory.
4. Map required slides to template layouts.
5. Replace content.
6. Validate visually.

### Create from an anything-to-ppt handoff

Read files in this order:

1. `slides_plan.md` — primary source of deck theme, slide order, slide titles, key messages, bullets, visuals, and speaker notes.
2. `images_needed.md` — visual asset requirements and missing/manual/generated asset instructions.
3. `speaker_notes.md` — speaker notes to add or preserve.
4. `summary.md` — factual verification file.
5. `review_checklist.md` — update after PPT generation.

Expected handoff structure:

```text
summary.md
slides_plan.md
images_needed.md
speaker_notes.md
review_checklist.md
assets/extracted/
assets/manual/
assets/generated/
```

If `slides_plan.md` is missing, do not generate the final deck from guesses. Create or request the missing plan depending on the user's instruction.

## 2. Source-of-truth rules

### Treat `slides_plan.md` as authoritative

Map fields as follows:

```yaml
deck_title: overall deck title
deck_theme: research_talk / project_update / product_pitch / training / proposal / review / report / other
audience: target audience
language: slide language preference
slide_number: slide order
title: slide headline
key_message: main claim or takeaway
bullet_points: short supporting bullets
visual_suggestion: layout and visual plan
visual_assets: concrete asset IDs or file paths
speaker_note: notes fallback if speaker_notes.md is incomplete
source_reference: factual verification marker
status: ready / needs_manual_asset / needs_verification
```

Do not add claims that are not supported by `slides_plan.md`, `summary.md`, or source files. Mark uncertain information as:

```text
待核实
```

### Topic-neutral planning

Choose layouts based on `deck_theme` and slide content.

Examples:

```yaml
research_talk:
  typical_visuals: source figures, tables, method diagrams, equations
project_update:
  typical_visuals: timeline, roadmap, architecture, progress board, risk matrix
product_pitch:
  typical_visuals: user journey, feature mockup, comparison table, metric card
training:
  typical_visuals: step cards, examples, before/after, exercises
review_or_report:
  typical_visuals: dashboard, timeline, highlights, issue summary, action list
```

Never force one deck structure onto all topics.

## 3. Default design style: Kalam / Patrick Hand hand-drawn sketch

Use this style unless the user provides another style, brand guide, or template.

Design intent:

- clear whiteboard explanation
- annotated notebook feel
- human and approachable
- creative but still rigorous and readable

This is not a childish doodle style. Prioritize clarity and hierarchy.

### Colors

```yaml
background: "#fdfbf7"
foreground: "#2d2d2d"
muted: "#e5e0d8"
accent: "#ff4d4d"
border: "#2d2d2d"
secondary_accent: "#2d5da1"
post_it: "#fff9c4"
white: "#ffffff"
```

### Typography

```yaml
english_headings: Kalam
english_body: Patrick Hand
chinese_fallback: FangSong / 仿宋
equations_and_symbols: Cambria Math / Latin Modern Math / STIX Two Math / Times New Roman / serif
```

Rules:

- Use `Kalam` for English titles and large callouts.
- Use `Patrick Hand` for English body text, captions, and annotations.
- Use `FangSong` / `仿宋` for Chinese text.
- Use math/scientific fonts for equations, Greek letters, formulas, variables, and formal notation.
- Do not use handwritten fonts for equations or formal symbols.
- Do not depend on remote web fonts.
- Do not embed, copy, or distribute font files.

### Minimum font size

Never create new text smaller than **14 pt**.

If a caption, source, or table note does not fit:

1. Shorten it on the slide.
2. Put the full reference in notes or `review_checklist.md`.
3. Crop, enlarge, split the slide, or move details to appendix.

Imported screenshots may contain smaller original text, but newly added deck text must not be smaller than 14 pt.

### Visual language

Use selectively:

- wobbly borders
- slight rotations for decorative elements
- hard offset shadows
- warm paper background
- dashed lines and hand-drawn arrows
- sticky-note key messages
- red marker highlights
- blue ballpoint annotations

Avoid:

- dense paragraphs
- heavy gradients
- glassmorphism
- blurred shadows
- unnecessary doodles
- framing every visual by default

## 4. Figure, table, screenshot, and equation policy

Figures, screenshots, diagrams, and tables do **not** need to be placed inside cards by default. Choose the least intrusive treatment.

```yaml
borderless_large:
  use_when: dense or already complete visual
light_annotation:
  use_when: one highlight or arrow is needed
wobbly_frame:
  use_when: placeholder, concept sketch, or small crop
full_bleed_crop:
  use_when: large table, dense screenshot, architecture figure, or dashboard
```

Default choices:

```yaml
figures: borderless_large or light_annotation
tables: full_bleed_crop or borderless_large
screenshots: full_bleed_crop or light_annotation
dashboards: full_bleed_crop
placeholders: wobbly_frame
conceptual_diagrams: wobbly_frame or sticky-note layout
```

Equations and technical symbols:

- Prefer source equation screenshots when fidelity matters.
- If recreating equations, use a math-capable font.
- Keep operators, functions, subscripts, and Greek letters readable.
- If an equation cannot be reliably read, use a placeholder and mark `待核实`.

## 5. HTML slide CSS tokens

When creating HTML slides, define a shared CSS block like this:

```css
:root {
  --paper: #fdfbf7;
  --ink: #2d2d2d;
  --muted: #e5e0d8;
  --red: #ff4d4d;
  --blue: #2d5da1;
  --postit: #fff9c4;
  --white: #ffffff;
  --shadow: 4px 4px 0px 0px #2d2d2d;
  --shadow-sm: 2px 2px 0px 0px #2d2d2d;
  --wobbly: 14pt;
  --wobbly-md: 10pt;
  --font-heading: "Kalam", "Patrick Hand", "FangSong", "仿宋", "Comic Sans MS", Georgia, serif;
  --font-body: "Patrick Hand", "Kalam", "FangSong", "仿宋", "Comic Sans MS", Georgia, serif;
  --font-cn: "FangSong", "仿宋", serif;
  --font-math: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", serif;
}

html, body {
  margin: 0;
  padding: 0;
  width: 720pt;
  height: 405pt;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16pt;
}

.slide {
  position: relative;
  width: 720pt;
  height: 405pt;
  box-sizing: border-box;
  padding: 28pt 34pt;
  overflow: hidden;
}

h1, h2, h3, .slide-title, .big-claim, .step-number {
  margin: 0;
  color: var(--ink);
  line-height: 1.05;
  font-family: var(--font-heading);
  font-weight: 700;
}

h1, .big-claim { font-size: 38pt; }
h2, .slide-title { font-size: 28pt; }
h3 { font-size: 21pt; }
p, li { font-size: 16pt; line-height: 1.35; }
.caption, .source, .annotation, .label, .footer { font-size: 14pt; line-height: 1.2; }
.cn, .zh, .chinese { font-family: var(--font-cn); }
.math, .equation, .symbol, .formula {
  font-family: var(--font-math);
  font-size: 18pt;
  line-height: 1.2;
  font-style: italic;
}
.card {
  background: var(--white);
  border: 2.5pt solid var(--ink);
  border-radius: var(--wobbly-md);
  box-shadow: var(--shadow);
  padding: 14pt 16pt;
}
.postit {
  background: var(--postit);
  border: 2pt solid var(--ink);
  border-radius: var(--wobbly-md);
  box-shadow: var(--shadow-sm);
  padding: 12pt 14pt;
}
.visual-raw, .figure-raw, .table-raw, .screenshot-raw {
  background: transparent;
  border: 0;
  box-shadow: none;
  padding: 0;
}
.visual-frame, .placeholder-frame {
  background: var(--white);
  border: 2pt solid var(--ink);
  border-radius: var(--wobbly-md);
  box-shadow: var(--shadow-sm);
  padding: 8pt;
}
```

Compatibility notes:

- CSS gradients do not convert reliably; use flat backgrounds or rasterized assets.
- CSS transform may not convert through HTML alone; apply final rotations with PptxGenJS when needed.
- Elliptical `border-radius` slash syntax does not convert reliably; use simple radius values.
- Image opacity should be converted to PptxGenJS `transparency` in `addImage()` when supported by the local script.

## 6. Generating `report.pptx` from a handoff directory

Use these paths:

```text
html_slides/
report.pptx
thumbnails/
review_checklist.md
```

Steps:

1. Parse `slides_plan.md`.
2. Validate each slide has title, key message, bullets, visual suggestion, speaker note, and source reference.
3. Read `deck_theme`, `audience`, `language`, and `tone`.
4. Read `images_needed.md` and map available assets.
5. Read `summary.md` for factual verification.
6. Choose layout recipes based on the actual deck theme.
7. Generate one HTML file per slide under `html_slides/`.
8. Apply the default hand-drawn CSS unless user style/template overrides it.
9. Convert HTML to PPTX through `html2pptx.js`.
10. Add figures, screenshots, charts, tables, highlights, arrows, equations, and labels with PptxGenJS when needed.
11. Save as `report.pptx`.
12. Generate thumbnails.
13. Inspect thumbnails and fix issues.
14. Update `review_checklist.md`.

## 7. Layout recipes

Choose recipes based on `deck_theme` and slide purpose.

- Cover: large title, metadata, optional marker underline.
- Context/background: short bullets plus diagram, screenshot, or visual metaphor.
- Problem/bottleneck: 2-3 cards or one large evidence visual.
- Core idea/proposal: sticky-note key message plus simple before/after or current/proposed flow.
- Method/architecture/workflow: numbered steps or large source figure.
- Result/evidence: large table, chart, screenshot, metric board, or highlighted comparison.
- Timeline/roadmap: 3-5 milestones with risks or dependencies.
- Training/procedure: numbered steps plus example or exercise.
- Multi-visual analysis: 2-panel or 3-4 panel layout only if readable.
- Conclusion: value, limitation/risk, takeaway/next step.

## 8. Quality checklist

Before final delivery, verify:

- `report.pptx` exists.
- deck aspect ratio is correct.
- thumbnails were generated and inspected.
- deck theme matches `slides_plan.md`.
- user style/template/brand overrides were respected.
- default fonts are applied where appropriate.
- equations and symbols use math/scientific fonts.
- no new text is smaller than 14 pt.
- text does not overflow.
- figures, screenshots, and tables remain readable.
- visuals are not unnecessarily constrained by frames.
- each slide has one key message.
- factual slides have source references.
- missing visuals are placeholders, not fabricated replacements.
- `review_checklist.md` is updated.

## 9. User override rules

User instructions override the default hand-drawn style when they request:

- corporate style
- minimal academic style
- product or brand style
- a specific template
- a specific color palette
- no handwritten style
- Chinese-only or English-only slides

Even when the style is overridden, keep the handoff discipline:

- use `slides_plan.md` as source of truth
- do not invent content
- keep source references
- update `review_checklist.md`
