---
name: pptx
description: Presentation creation, editing, analysis, and PowerPoint generation. Customized to default to an English-first Kalam / Patrick Hand hand-drawn academic sketch style and to consume paper-to-ppt handoff files such as slides_plan.md, images_needed.md, speaker_notes.md, paper_summary.md, and review_checklist.md.
---

# PPTX creation, editing, analysis, and paper-to-ppt handoff

This skill extends the base `pptx` workflow with two defaults:

1. **Default visual style**: English-first hand-drawn academic sketchbook style using `Kalam` and `Patrick Hand`.
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
4. Use PptxGenJS for precise insertion of figures, charts, tables, equations, shapes, highlights, and annotations when HTML conversion is insufficient.
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

## 2. Default design style: Kalam / Patrick Hand academic sketch

Unless the user explicitly requests another style or provides a template that must be followed, use this style.

### 2.1 Design intent

The deck should feel like:

- A clear academic whiteboard explanation.
- A professor's annotated notebook.
- A research idea sketched during group discussion.
- Human, approachable, creative, but still readable and rigorous.

For paper presentations, this is **not** a childish doodle style. Prioritize clarity and figure readability over decoration.

### 2.2 Language policy

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

### 2.3 Color tokens

Use this palette by default:

```yaml
background: "#fdfbf7"       # warm paper
foreground: "#2d2d2d"       # soft pencil black
muted: "#e5e0d8"            # old paper / erased pencil
accent: "#ff4d4d"           # red correction marker
border: "#2d2d2d"           # pencil lead
secondary_accent: "#2d5da1" # blue ballpoint pen
post_it: "#fff9c4"          # yellow sticky note
white: "#ffffff"
```

Never use pure black unless required by imported paper figures.

### 2.4 Typography policy

This customized skill is intentionally strict about the hand-drawn font choice while protecting equations and scientific notation.

Use this rule by default:

```yaml
english_headings:
  primary: Kalam
  preferred_weight: 700 / Bold
english_body:
  primary: Patrick Hand
  preferred_weight: 400 / Regular
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
last_resort_fallback:
  - Comic Sans MS
  - Georgia
  - serif
```

Mandatory defaults:

- Use `Kalam` for English slide titles, major callouts, section headers, step numbers, and large handwritten claims.
- Use `Patrick Hand` for English body text, bullet points, captions, table notes, and annotations.
- Use `FangSong` / `仿宋` for Chinese text.
- Use math/scientific fonts such as `Cambria Math`, `Latin Modern Math`, `STIX Two Math`, or `Times New Roman` for equations, variables, Greek letters, tensor symbols, loss functions, model notation, and paper-defined symbols.
- Do **not** render equations or paper symbols in `Kalam` or `Patrick Hand`.
- Do **not** default to Microsoft YaHei, Source Han Sans, or Noto Sans CJK unless the user explicitly requests a clean corporate / formal academic style.
- Do **not** depend on remote web fonts for a portable PPTX.
- Do **not** embed, copy, or distribute font files.
- If `Kalam` or `Patrick Hand` is not installed, still write those font names into the deck and tell the user to install them, then regenerate or reopen the deck.

### 2.5 Minimum font size policy

Never use text smaller than **14 pt** anywhere in the deck.

This applies to:

- Slide titles.
- Bullets.
- Captions.
- Source references.
- Figure labels.
- Table notes.
- Axis labels in recreated charts.
- Placeholders.
- Footers.
- Appendix notes.

If a source reference or caption does not fit at 14 pt:

1. Shorten it on the slide, for example `Source: PDF p.6, Fig. 3`.
2. Put the full reference in speaker notes or `review_checklist.md`.
3. Do not reduce the font below 14 pt.

Imported screenshots may contain smaller text from the original paper, but the deck must not add new text smaller than 14 pt. If a table or figure screenshot becomes unreadable, crop, enlarge, split the slide, or move low-priority visuals to appendix.

### 2.6 Visual language

Use:

- Wobbly borders where they help create hand-drawn feel.
- Slight rotations from `-2deg` to `2deg` on non-critical decorative elements.
- Hard offset shadows, no blur.
- Paper texture background.
- Dashed lines and hand-drawn arrows.
- Sticky-note cards for key ideas.
- Red correction-marker highlights.
- Blue ballpoint annotations for secondary explanations.
- Big square step numbers like hand-sketched cards.

Avoid:

- Corporate gradient backgrounds.
- Glassmorphism.
- Heavy blurred shadows.
- Dense paragraphs.
- Perfect sterile grids.
- Random doodles that distract from research content.
- Framing every figure/table by default.

---

## 3. Figure, table, and equation display policy

### 3.1 Do not frame every figure or table

Figures and tables do **not** need to be placed inside cards by default. A card frame can restrict size and reduce readability.

Choose the least intrusive visual treatment:

```yaml
borderless_large:
  use_when: the figure/table is already visually complete or contains dense text
  treatment: place directly on paper background, maximize size, add only minimal highlight or label

light_annotation:
  use_when: the original figure/table needs one takeaway or one highlighted region
  treatment: no outer card; use red marker circle/box, blue arrow, or short label

wobbly_frame:
  use_when: placeholder, conceptual sketch, small cropped figure, or a figure needing separation from background
  treatment: thin wobbly border and hard shadow, but never at the cost of readability

full_bleed_crop:
  use_when: a large table or dense architecture figure must be readable
  treatment: crop to the important region and use most of the slide area
```

Default choice for paper figures and tables:

```yaml
figures: borderless_large or light_annotation
tables: full_bleed_crop or borderless_large
placeholders: wobbly_frame
conceptual diagrams: wobbly_frame or sticky-note layout
```

### 3.2 Large tables

For large tables:

- Do not shrink a full paper table until it becomes unreadable.
- Prefer cropped screenshots of key rows/columns.
- Use red marker boxes to highlight the relevant rows/columns.
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
  layout: two_panel_compare
  rule: side-by-side only if both remain readable at 14 pt added labels

three_or_four_visuals:
  layout: multi_panel_board
  rule: use A/B/C/D labels, one shared takeaway, minimal bullets

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

For equations:

- Prefer the paper's original equation screenshot when reliability matters.
- If recreating equations, use a math-capable font such as `Cambria Math`.
- Use italic math font for variables where appropriate.
- Keep operators, functions, and subscripts readable.
- Never use `Kalam` or `Patrick Hand` for equations, Greek letters, loss functions, model notation, or paper-defined symbols.
- For inline symbols inside handwritten body text, wrap the symbol in a math-font span or use a separate text box with the math font.
- If an equation cannot be reliably read, use a placeholder and mark `待核实`.

---

## 4. HTML slide CSS tokens

When creating HTML slides, define a shared CSS block like this. Keep only CSS that survives the `html2pptx` workflow; approximate unsupported effects with PptxGenJS shapes.

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
  --shadow-lg: 8px 8px 0px 0px #2d2d2d;
  --wobbly: 255px 15px 225px 15px / 15px 225px 15px 255px;
  --wobbly-md: 18px 28px 20px 24px / 24px 20px 28px 18px;
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

body {
  background-color: var(--paper);
  background-image: radial-gradient(var(--muted) 1px, transparent 1px);
  background-size: 24px 24px;
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
p, li, .body, .caption, .source, .annotation { font-family: var(--font-body); }
p, li { font-size: 16pt; line-height: 1.35; }
.caption, .source, .annotation, .label, .footer { font-size: 14pt; line-height: 1.2; }

.cn, .zh, .chinese {
  font-family: var(--font-cn);
}

.math, .equation, .symbol, .model-symbol, .latex, .formula {
  font-family: var(--font-math);
  font-size: 18pt;
  line-height: 1.2;
  font-style: italic;
}

.equation-block {
  font-family: var(--font-math);
  font-size: 20pt;
  line-height: 1.25;
  background: rgba(255, 255, 255, 0.72);
  padding: 10pt 12pt;
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
  transform: rotate(-1deg);
}

.visual-raw,
.figure-raw,
.table-raw {
  background: transparent;
  border: 0;
  box-shadow: none;
  padding: 0;
}

.visual-frame,
.placeholder-frame {
  background: var(--white);
  border: 2pt solid var(--ink);
  border-radius: var(--wobbly-md);
  box-shadow: var(--shadow-sm);
  padding: 8pt;
}

.step-number {
  width: 44pt;
  height: 44pt;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--white);
  border: 2.5pt solid var(--ink);
  border-radius: 8px 16px 10px 14px / 14px 8px 16px 10px;
  box-shadow: var(--shadow);
  font-size: 24pt;
}

.panel-label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24pt;
  height: 24pt;
  border: 2pt solid var(--ink);
  border-radius: var(--wobbly);
  background: var(--white);
  box-shadow: var(--shadow-sm);
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 14pt;
}

.marker {
  color: var(--red);
  font-family: var(--font-heading);
  font-weight: 700;
}

.red-dot {
  width: 14pt;
  height: 14pt;
  border-radius: 50%;
  background: var(--red);
  border: 1.8pt solid var(--ink);
  display: inline-block;
}

.source {
  position: absolute;
  left: 34pt;
  bottom: 14pt;
  font-size: 14pt;
  color: rgba(45,45,45,0.72);
}

.placeholder {
  background: rgba(229, 224, 216, 0.65);
  border: 2pt dashed var(--ink);
  border-radius: var(--wobbly-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(45,45,45,0.72);
  font-size: 14pt;
  text-align: center;
  font-family: var(--font-body);
}
```

---

## 5. Component vocabulary

Use these components to make decks resemble the hand-drawn reference while staying academic.

### 5.1 Wobbly title card

Use for cover, section opening, and core insight slides.

- Large `Kalam` claim.
- Warm paper background.
- Optional red correction-marker exclamation or underline.
- Optional dashed arrow pointing toward the main figure.

### 5.2 Sticky-note key message

Use for each slide's `key_message` when it improves clarity.

- Yellow post-it card.
- Slight rotation.
- Hard offset shadow.
- Keep it short: one sentence only.
- Use `Patrick Hand` unless it is a large headline.

Do not use a sticky note if it competes with a dense figure or table.

### 5.3 Numbered step cards

Use for process, pipeline, method stages, or story flow.

- 2-4 numbered square cards, similar to the reference demo.
- Each number in a wobbly square with hard shadow.
- Use dashed or squiggly connector lines between steps.
- Keep each step label short.

### 5.4 Figure treatment

Use the paper figure as large as possible.

Preferred modes:

1. **Borderless large figure** for dense architecture diagrams or original paper figures.
2. **Light annotation** for figures that need one red highlight or blue arrow.
3. **Wobbly frame** only for placeholders, small crops, or conceptual diagrams.

Do not automatically put every figure inside a card or frame.

### 5.5 Result table treatment

Use for main tables.

- Prefer full-width or large cropped table screenshots.
- Do not paste huge dense tables unless the important cells remain readable.
- Highlight 1-2 rows / columns.
- Put a short takeaway near the table only if there is enough space.
- If exact values are unreadable, use the original screenshot and mark the issue rather than redrawing numbers.

### 5.6 Multi-panel figure board

Use for multiple related figures.

- 2 figures: side-by-side comparison.
- 3-4 figures: labeled A/B/C/D grid only if each panel remains readable.
- Each panel gets a small handwritten panel label, at least 14 pt.
- Use only one shared takeaway.
- If panels become too small, split across slides.

### 5.7 Three-card conclusion

Use for final slide:

1. Contribution
2. Limitation
3. Takeaway

Each card should contain at most 2 short bullets.

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
key_message: main visual claim or sticky note
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

- Convert slide titles into short English claim-style titles.
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
8. Apply the Kalam / Patrick Hand hand-drawn academic CSS tokens.
9. Convert HTML to PPTX through `html2pptx.js`.
10. Add figures, charts, tables, highlights, arrows, equations, and panel labels with PptxGenJS when needed.
11. Save as `report.pptx`.
12. Generate thumbnails.
13. Inspect thumbnails and fix issues.
14. Update `review_checklist.md`.

---

## 8. Layout recipes

### 8.1 Cover slide

Use:

- Warm paper background.
- Large `Kalam` title claim.
- Small metadata sticky note.
- Optional red correction marker underline under the core topic.

Must include:

- Paper title.
- Authors if provided.
- Presenter if provided.
- Venue / class / group meeting if provided.

### 8.2 Background slide

Use:

- Left: 2-3 short English bullets.
- Right: sketchy diagram or task illustration.
- Source marker at 14 pt or larger.

### 8.3 Existing bottleneck slide

Use:

- Three wobbly cards for three problems, if there is no dense figure.
- Red marker labels such as `Pain Point 1 / Pain Point 2 / Pain Point 3`.
- Avoid over-explaining.

### 8.4 Core insight slide

Use:

- Large sticky note for the key insight.
- A simple arrow from `Old View` to `New View`.
- Keep this slide visually memorable.

### 8.5 Method overview slide

Use:

- Numbered step cards for verified pipeline stages, or a large figure-focus layout if the paper architecture figure is available.
- If the paper architecture figure is available, use it large and usually borderless.
- If not, draw a conservative flowchart from verified method steps.
- Add red or blue hand-drawn annotations only to clarify the verified process.

### 8.6 Formula slide

Use:

- Formula screenshot or recreated formula only if reliable.
- Math font for any recreated symbols or equations.
- Right side: symbol explanations at 14 pt or larger.
- Bottom note: `Why it matters`.

If formula is unreadable, use placeholder and mark `待核实`.

### 8.7 Experiment setup slide

Use:

- Three cards: `Datasets` / `Baselines` / `Metrics`.
- Avoid dense tables.
- Put implementation details only if essential.

### 8.8 Main result slide

Use:

- Large result table or chart, usually borderless or full-width.
- Red marker highlight for key comparison.
- One short takeaway.
- Do not redraw exact charts unless numeric values are verified.

### 8.9 Ablation / analysis slide

Use:

- Before/after comparison.
- Module contribution diagram.
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

Use three cards:

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
- `Kalam` appears in title text where possible.
- `Patrick Hand` appears in body text where possible.
- `FangSong` / `仿宋` is used for Chinese text where possible.
- Equations and paper-defined symbols use a math/scientific font, not handwritten fonts.
- No newly created text is smaller than 14 pt.
- Text does not overflow.
- Figures are not stretched beyond recognition.
- Figures and tables are not unnecessarily constrained by frames or cards.
- Tables and multi-panel figures remain readable.
- Chinese text is readable.
- Hand-drawn style is visible through paper texture, selective wobbly borders, hard shadows, marker highlights, and annotation arrows.
- Each slide has one key message.
- Every factual slide has a source reference or a full reference in notes/checklist.
- Missing figures are visible placeholders, not fabricated replacements.
- `review_checklist.md` is updated.

If any item is not complete, state it clearly.

---

## 10. User override rules

User instructions override the default hand-drawn style when they explicitly ask for:

- Corporate style.
- Journal club minimal style.
- A specific template.
- A specific brand design.
- A different color palette.
- No handwritten style.

When overriding style, still preserve handoff discipline:

- Use `slides_plan.md` as the source of truth.
- Do not invent content.
- Keep source references.
- Update `review_checklist.md`.
