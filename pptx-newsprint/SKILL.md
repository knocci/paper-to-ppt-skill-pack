---
name: pptx
description: Presentation creation, editing, analysis, and PowerPoint generation. Customized to default to a Newsprint editorial presentation style and to consume paper-to-ppt handoff files such as slides_plan.md, images_needed.md, speaker_notes.md, paper_summary.md, and review_checklist.md.
---

# PPTX creation, editing, analysis, and paper-to-ppt handoff

This skill extends the base `pptx` workflow with two defaults:

1. **Default visual style**: Newsprint editorial style — high-contrast typography, strict rectangular grids, visible borders, paper texture, and sparse editorial red accents.
2. **Default structured input**: direct support for handoff files such as `slides_plan.md`, `images_needed.md`, `speaker_notes.md`, `paper_summary.md`, and `review_checklist.md`.

This skill is a customization layer over the original low-level PPTX tooling. Before generating or editing a deck, check whether the original helper docs and scripts are available in the `pptx` skill directory, especially:

```text
html2pptx.md
ooxml.md
scripts/
```

If those files are missing, do not pretend the full workflow is available. Tell the user the base PowerPoint tooling is missing, then generate the most useful intermediate files, such as HTML slides, asset mapping, or an implementation plan.

---

## 1. Preserve the original pptx workflows

The original `pptx` skill remains authoritative for low-level PowerPoint operations.

### 1.1 Create a new deck from scratch

When creating a new `.pptx` from scratch:

1. Read the full `html2pptx.md` file before generating slides.
2. Create one HTML file per slide with 16:9 dimensions.
3. Convert HTML slides to PowerPoint using `html2pptx.js`.
4. Use PptxGenJS for precise insertion of figures, charts, tables, equations, shapes, highlights, captions, and annotations when HTML conversion is insufficient.
5. Generate thumbnails.
6. Inspect thumbnails.
7. Fix layout issues and regenerate if needed.

### 1.2 Edit an existing deck

When editing an existing `.pptx`:

1. Read the full `ooxml.md` file before editing XML.
2. Unpack the deck.
3. Edit OOXML carefully.
4. Validate immediately after edits.
5. Repack the deck.

### 1.3 Create from a template

When creating from a template:

1. Extract template text with `markitdown`.
2. Generate template thumbnails.
3. Build a template inventory.
4. Map required slides to template layouts.
5. Replace content.
6. Validate visually.

Do not assume unavailable tools. If required scripts or dependencies are missing, state the limitation and generate the most useful intermediate files instead.

---

## 2. Default design style: Newsprint editorial

Unless the user explicitly requests another style or provides a template that must be followed, use this style.

### 2.1 Design intent

The deck should feel like:

- A serious newspaper feature translated into slides.
- A publication-of-record explanation of a paper.
- Dense but orderly editorial analysis.
- Authoritative, intellectual, urgent, and trustworthy.

For paper presentations, Newsprint is **not** a decorative newspaper cosplay. Prioritize research clarity, figure readability, and source traceability over texture or ornament.

### 2.2 Core visual DNA

Use these principles by default:

- **Sharp geometry**: all containers, panels, callouts, tables, and labels use zero border radius.
- **Visible structure**: grid lines, column dividers, section rules, and borders are explicit.
- **High contrast**: ink-black text on off-white paper.
- **Editorial hierarchy**: very large serif headlines, compact metadata, and short body text.
- **Sparse accent**: editorial red appears only for key labels, highlights, section marks, or one emphasis per slide.
- **Flat design**: no blurred shadows, glassmorphism, gradient backgrounds, or soft rounded cards.
- **Paper texture**: subtle dot or line texture may be used, but it must not reduce readability.

### 2.3 Language policy

Default to **English-first slides**:

```yaml
slide_titles: English by default
main_bullets: English by default
figure_labels: English by default
source_references: English or original paper style
speaker_notes: Chinese is allowed and often preferred
Chinese_on_slides: only when useful, short, and readable
```

For handoff workflows:

- If `slides_plan.md` is already in Chinese, translate slide titles and bullets into concise English unless the user explicitly asks to keep Chinese slides.
- Keep technical terms faithful to the paper.
- Do not translate proper nouns, dataset names, model names, benchmark names, or metric names unless the paper itself does so.
- Speaker notes may remain Chinese.
- If a claim is uncertain, keep `待核实` instead of translating it into a confident English statement.

### 2.4 Color tokens

Use this palette by default:

```yaml
background: "#F9F9F7"       # newsprint off-white
foreground: "#111111"       # ink black
muted: "#E5E5E0"            # divider grey
accent: "#CC0000"           # editorial red, sparse use only
border: "#111111"           # primary grid/border color
neutral_100: "#F5F5F5"
neutral_200: "#E5E5E5"
neutral_400: "#A3A3A3"
neutral_500: "#737373"
neutral_600: "#525252"
neutral_700: "#404040"
white: "#FFFFFF"
```

Rules:

- Use `#111111` for all major text and structural borders.
- Use `#CC0000` sparingly. Never use red as body text on black.
- Use `#F9F9F7` as the default slide background.
- Use black inverted sections only when a slide needs strong contrast or section-break drama.

### 2.5 Typography policy

This customized skill is intentionally strict about the Newsprint type system while protecting equations and scientific notation.

Use this rule by default:

```yaml
display_headlines:
  primary: Playfair Display
  fallback:
    - Times New Roman
    - Georgia
    - serif
body_text:
  primary: Lora
  fallback:
    - Georgia
    - Times New Roman
    - serif
ui_labels_metadata:
  primary: Inter
  fallback:
    - Helvetica Neue
    - Arial
    - sans-serif
data_and_code:
  primary: JetBrains Mono
  fallback:
    - Consolas
    - Courier New
    - monospace
chinese_fallback:
  primary: FangSong
  localized_name: 仿宋
equations_and_symbols:
  primary: Cambria Math
  fallback:
    - Latin Modern Math
    - STIX Two Math
    - Times New Roman
    - serif
```

Mandatory defaults:

- Use `Playfair Display` for slide titles, hero claims, section dividers, and major editorial headings.
- Use `Lora` for paragraph text, explanatory bullets, and longer reading text.
- Use `Inter` for labels, navigation-like markers, badges, small captions, source markers, and metadata.
- Use `JetBrains Mono` for dates, edition numbers, figure numbers, code snippets, metrics, and compact data labels.
- Use `FangSong` / `仿宋` for Chinese text.
- Use math/scientific fonts such as `Cambria Math`, `Latin Modern Math`, `STIX Two Math`, or `Times New Roman` for equations, variables, Greek letters, tensor symbols, loss functions, model notation, and paper-defined symbols.
- Do **not** render equations or paper symbols in `Playfair Display`, `Lora`, `Inter`, or `JetBrains Mono` unless the item is purely a label and not mathematical notation.
- Do **not** depend on remote web fonts for a portable PPTX.
- Do **not** embed, copy, or distribute font files.
- If `Playfair Display`, `Lora`, `Inter`, or `JetBrains Mono` is not installed, still write those font names into the deck and tell the user to install them locally, then regenerate or reopen the deck.

### 2.6 Local font installation reminder

Before generating or opening a final PPTX, remind the user to install these fonts locally:

```text
Required style fonts:
- Playfair Display
- Lora
- Inter
- JetBrains Mono

Recommended already-available / fallback fonts:
- Cambria Math
- FangSong / 仿宋
- Times New Roman
- Georgia
- Consolas
```

Suggested Windows workflow:

```powershell
# Option A: install manually
# 1. Download the font families from Google Fonts or each font's official release page.
# 2. Extract the .zip files.
# 3. Select the .ttf/.otf files, right-click, and choose "Install for all users".

# Option B: if using a package manager such as Chocolatey or Scoop,
# search the exact font package names first because package availability may vary.
```

Never include font files in this skill package or generated deliverables. Only reference font names and tell the user what to install.

### 2.7 Minimum font size policy

Never use text smaller than **14 pt** anywhere in the deck.

This applies to:

- Slide titles.
- Bullets.
- Captions.
- Source references.
- Figure labels.
- Table notes.
- Axis labels in recreated charts.
- Metadata strips.
- Placeholders.
- Footers.
- Appendix notes.

If a source reference, figure number, or caption does not fit at 14 pt:

1. Shorten it on the slide, for example `Source: PDF p.6, Fig. 3`.
2. Put the full reference in speaker notes or `review_checklist.md`.
3. Do not reduce the font below 14 pt.

Imported screenshots may contain smaller text from the original paper, but the deck must not add new text smaller than 14 pt. If a table or figure screenshot becomes unreadable, crop, enlarge, split the slide, or move low-priority visuals to appendix.

### 2.8 Visual language

Use:

- Strict 12-column or newspaper-column grids.
- Black 1 pt to 2 pt rules for section dividers and panel boundaries.
- Heavy 3 pt to 4 pt rules for major slide-section breaks.
- Zero-radius rectangular containers.
- Editorial metadata such as `Vol. 1 | Paper Reading | Fig. 2`.
- Uppercase labels with wide letter spacing.
- Drop-cap style only for optional explanatory paragraph slides.
- Paper dot or line texture only when subtle and compatible with conversion.
- Grayscale treatment only for decorative or non-evidence images.

Avoid:

- Rounded cards.
- Wobbly borders.
- Handwritten fonts.
- Sticky notes.
- Corporate gradients.
- Glassmorphism.
- Heavy blurred shadows.
- Dense paragraphs without hierarchy.
- Random newspaper decorations that distract from research content.
- Framing every figure/table by default.

---

## 3. Figure, table, and equation display policy

### 3.1 Do not frame every figure or table

Figures and tables do **not** need to be placed inside cards by default. A card frame can restrict size and reduce readability.

Choose the least intrusive visual treatment:

```yaml
borderless_large:
  use_when: the figure/table is already visually complete or contains dense text
  treatment: place directly on paper background, maximize size, add only minimal figure number, source marker, or red highlight

light_editorial_rule:
  use_when: the visual needs separation from text but should remain large
  treatment: use one top/bottom black rule or a thin side rule, not a full card

annotated_evidence:
  use_when: the original figure/table needs one takeaway or one highlighted region
  treatment: no outer card; use red box/underline/callout and a short 14 pt+ label

full_bleed_crop:
  use_when: a large table or dense architecture figure must be readable
  treatment: crop to the important region and use most of the slide area

grid_panel:
  use_when: 2-4 related visuals can remain readable
  treatment: newspaper grid with shared borders and panel labels A/B/C/D
```

Default choice for paper figures and tables:

```yaml
figures: borderless_large or annotated_evidence
tables: full_bleed_crop or borderless_large
placeholders: grid_panel or light_editorial_rule
conceptual diagrams: grid_panel with sharp rectangles
```

### 3.2 Large tables

For large tables:

- Do not shrink a full paper table until it becomes unreadable.
- Prefer cropped screenshots of key rows/columns.
- Use editorial red boxes or underlines to highlight the relevant rows/columns.
- Use a short 14 pt or larger takeaway beside or above the table.
- Split into multiple slides if one table still cannot be read.
- Do not redraw exact numbers unless the values are explicitly verified.

### 3.3 Multiple figures or tables

Academic papers often contain many figures and tables. Do not blindly place all of them into one slide.

Use this decision tree:

```yaml
one_visual:
  layout: figure_focus
  rule: make the visual large and add one takeaway

two_visuals:
  layout: two_column_evidence
  rule: side-by-side only if both remain readable at 14 pt added labels

three_or_four_visuals:
  layout: editorial_grid_board
  rule: use A/B/C/D labels, shared borders, one shared takeaway, minimal bullets

more_than_four_visuals:
  layout: split_or_appendix
  rule: split across multiple slides, move low-priority visuals to appendix, or summarize as a visual inventory

large_table:
  layout: full_bleed_crop
  rule: crop to relevant rows/columns or split the table

multiple_tables:
  layout: separate_by_question
  rule: one table per evidence claim; do not combine unrelated metrics into one slide
```

### 3.4 Equations and paper-defined symbols

**Fundamental rule:** an equation is not ordinary text. A math font can improve glyph shape, but it cannot perform TeX/MathML layout such as subscripts, superscripts, fractions, operators, constraints, multi-line alignment, or spacing. Do not rely on plain HTML text plus `font-family: Cambria Math` as the primary equation-rendering method.

For equations:

- Prefer the paper's original equation screenshot when reliability and exact reproduction matter.
- If recreating equations, write the formula as valid LaTeX and render it to an equation asset before placing it on a slide.
- Use SVG as the preferred equation asset because it scales cleanly in HTML preview and modern PowerPoint.
- If SVG insertion is unreliable in the target environment, render a high-resolution transparent PNG fallback at 2x or 3x.
- Insert equation assets into HTML slides with `<img class="equation-img" src="...">`.
- Insert equation assets into PPTX with PptxGenJS `addImage`, not as plain text.
- Use math/scientific fonts only for short inline symbols that do not need full layout.
- Never use Newsprint display/body/UI fonts for equations, Greek letters, loss functions, model notation, or paper-defined symbols.
- If an equation cannot be reliably parsed or rendered, use a visible placeholder and mark `待核实`.

### 3.5 Equation rendering pipeline

Use this pipeline for every recreated formula:

```text
LaTeX source
  -> MathJax / LaTeX renderer
  -> standalone SVG equation asset
  -> HTML preview uses <img>
  -> PPTX final uses PptxGenJS addImage
```

Do **not** write formulas like this in slide HTML:

```html
<div class="equation">min F_task(T,l) + F_control(tau) s.t. C(T)</div>
```

Instead, store the formula as LaTeX:

```latex
\min_{\tau}\; F_{\mathrm{task}}(T,l) + F_{\mathrm{control}}(\tau)
\quad \mathrm{s.t.}\quad C(T)
```

Then render it to an asset such as:

```text
assets/generated/equations/eq_method_objective.svg
```

And use:

```html
<img
  class="equation-img"
  src="../assets/generated/equations/eq_method_objective.svg"
  alt="Optimization objective"
/>
```

Recommended equation authoring format in handoff files:

```yaml
equations:
  - id: eq_method_objective
    latex: |
      \min_{\tau}\; F_{\mathrm{task}}(T,l) + F_{\mathrm{control}}(\tau)
      \quad \mathrm{s.t.}\quad C(T)
    display: true
    source_reference: "PDF p.X, Eq. Y"
```

When creating a deck:

1. Scan `slides_plan.md`, `paper_summary.md`, and `images_needed.md` for formulas and paper-defined symbols.
2. Convert formula-like plain text into LaTeX only when the meaning is clear.
3. Write a formula manifest such as `assets/generated/equations/equations.json`.
4. Render each formula into SVG before generating final slides.
5. Use equation images in both HTML and PPTX.
6. Keep all formula source LaTeX in `review_checklist.md` or a generated formula manifest for review.
7. If conversion is ambiguous, use a placeholder and mark `待核实` instead of guessing.

### 3.6 MathJax helper script

This skill may include or generate a helper script named:

```text
scripts/render-equations-svg.mjs
```

Expected command pattern:

```powershell
cd path\to\output-dir
npm install @mathjax/src@4
node path\to\pptx\scripts\render-equations-svg.mjs `
  --input assets\generated\equations\equations.json `
  --out assets\generated\equations
```

Expected `equations.json` format:

```json
[
  {
    "id": "eq_method_objective",
    "latex": "\\min_{\\tau}\\; F_{\\mathrm{task}}(T,l) + F_{\\mathrm{control}}(\\tau) \\quad \\mathrm{s.t.}\\quad C(T)",
    "display": true
  }
]
```

Each rendered formula should produce:

```text
assets/generated/equations/eq_method_objective.svg
```

---

## 4. HTML slide CSS tokens

When creating HTML slides, define a shared CSS block like this. Keep only CSS that survives the `html2pptx` workflow; approximate unsupported effects with PptxGenJS shapes.

```css
:root {
  --paper: #F9F9F7;
  --ink: #111111;
  --muted: #E5E5E0;
  --red: #CC0000;
  --neutral-100: #F5F5F5;
  --neutral-200: #E5E5E5;
  --neutral-500: #737373;
  --neutral-600: #525252;
  --neutral-700: #404040;
  --white: #FFFFFF;

  --font-display: "Playfair Display", "Times New Roman", Georgia, serif;
  --font-body: "Lora", Georgia, "Times New Roman", serif;
  --font-ui: "Inter", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "JetBrains Mono", Consolas, "Courier New", monospace;
  --font-cn: "FangSong", "仿宋", serif;
  --font-math: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", serif;
}

html, body {
  margin: 0;
  padding: 0;
  width: 720pt;
  height: 405pt;
  background-color: var(--paper);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16pt;
}

body {
  /* Do not rely on CSS gradients or remote web fonts for final PPTX conversion.
     For final PPTX texture, use one of:
     1. Pre-generated PNG texture, for example paper-dots.png or paper-lines.png
     2. PptxGenJS native dot/line shapes
     3. Flat background-color fallback */
  background-color: var(--paper);
}

.slide {
  position: relative;
  width: 720pt;
  height: 405pt;
  box-sizing: border-box;
  padding: 24pt 30pt;
  overflow: hidden;
}

h1, h2, h3, .slide-title, .hero-headline, .section-title {
  margin: 0;
  color: var(--ink);
  font-family: var(--font-display);
  font-weight: 900;
  letter-spacing: -0.03em;
}

h1, .hero-headline {
  font-size: 48pt;
  line-height: 0.92;
}

h2, .slide-title {
  font-size: 32pt;
  line-height: 1.0;
}

h3, .section-title {
  font-size: 24pt;
  line-height: 1.05;
}

p, li, .body {
  font-family: var(--font-body);
  font-size: 16pt;
  line-height: 1.35;
}

.caption, .source, .label, .footer, .meta, .badge {
  font-family: var(--font-ui);
  font-size: 14pt;
  line-height: 1.2;
}

.meta, .badge, .label, .fig-label {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 700;
}

.mono, .metric, .date, .edition, .code {
  font-family: var(--font-mono);
}

.cn, .zh, .chinese {
  font-family: var(--font-cn);
}

.math, .symbol, .model-symbol {
  font-family: var(--font-math);
  font-size: 18pt;
  line-height: 1.2;
  font-style: italic;
}

/* Full equations should be rendered as SVG/PNG assets, not typed as plain text. */
.equation-img {
  display: block;
  max-width: 100%;
  height: auto;
}

.equation-block {
  background: var(--white);
  border-top: 2pt solid var(--ink);
  border-bottom: 2pt solid var(--ink);
  padding: 10pt 12pt;
}

.equation-block .equation-img {
  width: 100%;
}

.rule-thin {
  border-top: 1pt solid var(--ink);
}

.rule-heavy {
  border-top: 4pt solid var(--ink);
}

.editorial-frame {
  background: var(--paper);
  border: 1.2pt solid var(--ink);
  border-radius: 0;
  padding: 12pt 14pt;
}

.editorial-card {
  background: var(--white);
  border: 1.5pt solid var(--ink);
  border-radius: 0;
  padding: 14pt 16pt;
  box-shadow: 4pt 4pt 0 0 var(--ink);
}

.grid-shell {
  border-left: 1.2pt solid var(--ink);
  border-top: 1.2pt solid var(--ink);
}

.grid-cell {
  border-right: 1.2pt solid var(--ink);
  border-bottom: 1.2pt solid var(--ink);
  border-radius: 0;
  padding: 12pt;
}

.inverted {
  background: var(--ink);
  color: var(--paper);
}

.inverted h1,
.inverted h2,
.inverted h3,
.inverted p,
.inverted li,
.inverted .label,
.inverted .meta {
  color: var(--paper);
}

.accent {
  color: var(--red);
}

.badge {
  display: inline-block;
  background: var(--red);
  color: var(--paper);
  padding: 3pt 6pt;
  border-radius: 0;
}

.visual-raw,
.figure-raw,
.table-raw {
  background: transparent;
  border: 0;
  box-shadow: none;
  padding: 0;
}

.visual-rule {
  background: transparent;
  border-top: 1.5pt solid var(--ink);
  border-bottom: 1.5pt solid var(--ink);
  padding: 8pt 0;
}

.placeholder {
  background: var(--neutral-100);
  border: 1.5pt solid var(--ink);
  border-radius: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neutral-600);
  font-size: 14pt;
  text-align: center;
  font-family: var(--font-ui);
}

.source {
  position: absolute;
  left: 30pt;
  bottom: 12pt;
  color: var(--neutral-600);
}
```

Important conversion constraints:

- Do not use CSS `border-radius` other than `0`.
- Do not use CSS `transform` for final PPTX layout. Use PptxGenJS rotation only if rotation is truly needed.
- Do not use CSS gradients as required visual content. Convert texture to PNG or native shapes.
- Do not use web-hosted font imports for final PPTX. Local fonts must be installed on the machine that generates/opens the deck.
- Do not depend on hover effects in PPTX.

---

## 5. Component vocabulary

Use these components to make decks resemble the Newsprint reference while staying academic.

### 5.1 Front page / cover

Use for cover and section opening slides.

- Huge `Playfair Display` title.
- Off-white paper background.
- Top and bottom newspaper metadata rules.
- Optional red `BREAKING`, `METHOD`, `RESULT`, or `FINDING` badge.
- Small metadata strip: paper title, authors, venue, presenter, date.

### 5.2 Editorial headline slide

Use for thesis, key insight, or a major paper claim.

- One massive serif headline.
- One short deck-level claim.
- Optional drop-cap paragraph if the slide is explanatory.
- Avoid more than 2 supporting bullets.

### 5.3 Newspaper column grid

Use for background, related work, assumptions, or comparison slides.

- 2-3 vertical columns.
- Shared borders rather than separated cards.
- Each column has a small uppercase label.
- Text is compact but never below 14 pt.

### 5.4 Evidence focus

Use for original paper figures and tables.

Preferred modes:

1. **Borderless large figure** for dense architecture diagrams or original paper figures.
2. **Light editorial rule** for visuals that need separation but not a full card.
3. **Annotated evidence** for one red highlight or callout.
4. **Grid panel** only when multiple visuals remain readable.

Do not automatically put every figure inside a card or frame.

### 5.5 Result table treatment

Use for main tables.

- Prefer full-width or large cropped table screenshots.
- Do not paste huge dense tables unless the important cells remain readable.
- Highlight 1-2 rows / columns.
- Put a short takeaway near the table only if there is enough space.
- If exact values are unreadable, use the original screenshot and mark the issue rather than redrawing numbers.

### 5.6 Method / pipeline grid

Use for method overview or algorithm stages.

- Use sharp rectangular boxes connected by straight lines.
- Use numbered mono labels such as `01`, `02`, `03`.
- Use one red accent to indicate the method's core novelty.
- If the paper architecture figure is available, prefer it large and annotated.

### 5.7 Inverted section slide

Use sparingly for section breaks or strong conclusions.

- Black background.
- Off-white text.
- Red accent only for a small badge or number.
- Do not put red paragraph text on black.

### 5.8 Three-column conclusion

Use for final slide:

1. Contribution
2. Limitation
3. Takeaway

Each column should contain at most 2 short bullets.

---

## 6. Handoff workflow

Use this workflow when the user asks to generate a deck from an output directory containing handoff files.

Expected files:

```text
paper_summary.md
slides_plan.md
images_needed.md
speaker_notes.md
review_checklist.md
assets/extracted/
assets/manual/
assets/generated/
```

### 6.1 Read files in this order

1. `slides_plan.md` — primary structure and slide content.
2. `images_needed.md` — figure/table/image requirements.
3. `speaker_notes.md` — notes to add or preserve.
4. `paper_summary.md` — for verification only, not for inventing extra content.
5. `review_checklist.md` — update after PPT generation.

If `slides_plan.md` is missing, do not generate the final deck yet. Ask for it or create it from `paper_summary.md` only if the user explicitly requests that.

### 6.2 Treat slides_plan.md as authoritative

For each slide, map fields as follows:

```yaml
slide_number: determines order
title: slide headline
key_message: main visual claim or editorial deck
bullet_points: short supporting bullets
visual_suggestion: layout and visual asset plan
speaker_note: notes fallback if speaker_notes.md is missing
source_reference: on-slide short source marker and factual verification
```

Do not add new claims that are not in `slides_plan.md` or `paper_summary.md`.

If a needed factual detail is missing, mark it as:

```text
待核实
```

### 6.3 English-first conversion rules

When `slides_plan.md` is Chinese but the user wants the default style:

- Convert slide titles into short English newspaper-style headlines.
- Convert bullets into short English phrases.
- Keep Chinese only when needed for proper nouns, task names, or short clarification.
- Keep speaker notes Chinese unless the user asks for English notes.
- Preserve every `source_reference` exactly in notes or references.
- Use a shortened on-slide source marker if full references do not fit at 14 pt.
- Do not add claims during translation.

### 6.4 Image and table resolution rules

For each visual in `images_needed.md`:

- If `extraction_status: ready`, use `current_file`.
- If `need_manual_crop`, first check `assets/manual/` for the requested filename.
- If missing, create a visible placeholder in the slide.
- If `failed` or `not_available`, create a placeholder and keep the missing item in `review_checklist.md`.
- Never fabricate a paper figure, table, chart, or experimental result.

Placeholder text format:

```text
Missing visual: PDF p.X Fig. X / Table X
Save as assets/manual/item_id.png
```

If the deck is mainly Chinese, use:

```text
待补图：PDF p.X Fig. X / Table X
请保存为 assets/manual/item_id.png
```

Placeholder text must be at least 14 pt.

### 6.5 Speaker notes

If feasible, add speaker notes to the PPT using the original OOXML workflow.

If not feasible or risky:

- Keep `speaker_notes.md` as the official notes file.
- Do not corrupt the PPTX by editing notes XML unsafely.
- Mark the limitation in `review_checklist.md`.

---

## 7. Creating report.pptx from slides_plan.md

When working inside a handoff output directory, use these paths:

```text
html_slides/
report.pptx
thumbnails/
review_checklist.md
```

Generation steps:

1. Parse `slides_plan.md`.
2. Validate every slide has:

```yaml
slide_number
title
key_message
bullet_points
visual_suggestion
speaker_note
source_reference
```

3. Apply English-first conversion if appropriate.
4. Read `images_needed.md` and map available assets.
5. Build a visual inventory from all figures, tables, formulas, and generated diagrams.
6. Choose a layout recipe for each slide.
7. Generate one HTML file per slide under `html_slides/`.
8. Apply the Newsprint editorial CSS tokens.
9. Convert HTML to PPTX through `html2pptx.js`.
10. Render recreated formulas to SVG/PNG assets before final layout; add figures, charts, tables, highlights, arrows, equation assets, panel labels, and texture PNGs with PptxGenJS when needed.
11. Save as `report.pptx`.
12. Generate thumbnails.
13. Inspect thumbnails and fix issues.
14. Update `review_checklist.md`.

---

## 8. Layout recipes

### 8.1 Cover slide

Use:

- Off-white paper background.
- Large `Playfair Display` title.
- Strong top/bottom rules.
- Metadata strip in `Inter` or `JetBrains Mono`.
- Optional red section badge.

Must include:

- Paper title.
- Authors if provided.
- Presenter if provided.
- Venue / class / group meeting if provided.

### 8.2 Background slide

Use:

- Left: editorial headline and 2-3 short bullets.
- Right: large figure, task illustration, or newspaper-column explanation.
- Source marker at 14 pt or larger.

### 8.3 Existing bottleneck slide

Use:

- Three sharp grid cells for three problems, if there is no dense figure.
- Red labels such as `Pain Point 1 / Pain Point 2 / Pain Point 3`.
- Avoid over-explaining.

### 8.4 Core insight slide

Use:

- A massive headline for the key insight.
- Optional black inverted side panel.
- One compact explanatory paragraph or 2 bullets.
- Keep this slide visually memorable.

### 8.5 Method overview slide

Use:

- Numbered grid cells for verified pipeline stages, or a large figure-focus layout if the paper architecture figure is available.
- If the paper architecture figure is available, use it large and usually borderless.
- If not, draw a conservative sharp-rectangle flowchart from verified method steps.
- Add red annotations only to clarify the verified novelty.

### 8.6 Formula slide

Use:

- Formula screenshot when exact paper reproduction matters.
- Recreated formula only when valid LaTeX is available or can be confidently reconstructed.
- Render recreated formulas to SVG or high-resolution transparent PNG before inserting them.
- Do not place raw formula text directly in HTML or PPTX text boxes.
- Right side: symbol explanations at 14 pt or larger.
- Bottom note: `Why it matters`.

If formula is unreadable or ambiguous, use placeholder and mark `待核实`.

### 8.7 Experiment setup slide

Use:

- Three columns: `Datasets` / `Baselines` / `Metrics`.
- Use shared borders and editorial labels.
- Avoid dense tables.
- Put implementation details only if essential.

### 8.8 Main result slide

Use:

- Large result table or chart, usually borderless or full-width.
- Red editorial highlight for key comparison.
- One short takeaway.
- Do not redraw exact charts unless numeric values are verified.

### 8.9 Ablation / analysis slide

Use:

- Before/after comparison.
- Module contribution grid.
- Short conclusion note.
- Avoid cards if they make figures too small.

### 8.10 Multi-figure analysis slide

Use when visual evidence consists of several related figures.

- Use 2-panel compare for before/after, baseline/method, or method/ablation comparisons.
- Use 3-4 panel board only when each panel remains readable.
- Label panels A/B/C/D at 14 pt or larger.
- Add one shared conclusion.
- Keep bullet text minimal.
- Split into multiple slides if readability suffers.

### 8.11 Multi-table result slide

Use when evidence spans several datasets or metrics.

- Prefer one evidence question per slide.
- Use cropped table images rather than full unreadable tables.
- Use as much slide area as needed; do not force the table into a card.
- Highlight only the key rows or columns.
- Add short source references for each table.
- If exact values are required but not readable, mark `待核实`.

### 8.12 Conclusion slide

Use three columns:

1. Contribution
2. Limitation
3. Takeaway

End with a question or discussion prompt if appropriate.

---

## 9. Quality checklist before final response

Before saying the PPT is done, verify:

- `report.pptx` exists.
- The deck is 16:9.
- Thumbnails were generated.
- `Playfair Display` appears in title text where possible.
- `Lora` appears in body text where possible.
- `Inter` appears in metadata, labels, and captions where possible.
- `JetBrains Mono` appears in data/date/code/edition labels where possible.
- `FangSong` / `仿宋` is used for Chinese text where possible.
- Recreated equations are rendered as SVG/PNG equation assets, not plain text; short inline symbols use a math/scientific font, not Newsprint display/body/UI fonts.
- No newly created text is smaller than 14 pt.
- Text does not overflow.
- Figures are not stretched beyond recognition.
- Figures and tables are not unnecessarily constrained by frames or cards.
- Tables and multi-panel figures remain readable.
- Chinese text is readable.
- Newsprint style is visible through high-contrast typography, sharp grid borders, editorial metadata, sparse red accents, and subtle paper texture.
- Each slide has one key message.
- Every factual slide has a source reference or a full reference in notes/checklist.
- Missing figures are visible placeholders, not fabricated replacements.
- `review_checklist.md` is updated.
- The final response reminds the user to install `Playfair Display`, `Lora`, `Inter`, and `JetBrains Mono` locally if they are not already installed.

If any item is not complete, state it clearly.

---

## 10. User override rules

User instructions override the default Newsprint style when they explicitly ask for:

- Corporate style.
- Journal club minimal style.
- A specific template.
- A specific brand design.
- A different color palette.
- Handwritten style.
- Rounded / soft / playful style.
- No newspaper / editorial style.

When overriding style, still preserve handoff discipline:

- Use `slides_plan.md` as the source of truth.
- Do not invent content.
- Keep source references.
- Update `review_checklist.md`.
