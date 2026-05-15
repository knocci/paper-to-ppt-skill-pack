# pptx skill customization: Kalam / Patrick Hand hand-drawn academic sketch

This package overwrites `.claude/skills/pptx/SKILL.md` with an English-first hand-drawn academic style.

Defaults:

- English headings: Kalam
- English body: Patrick Hand
- Chinese fallback: FangSong / 仿宋
- Equations and paper-defined symbols: Cambria Math or another math/scientific font, not handwritten fonts
- Minimum newly added font size: 14 pt
- Style: warm paper, dotted texture, selective wobbly borders, hard offset shadows, red marker highlights, blue pen annotations
- Figures/tables: do not wrap every figure/table in a card; use borderless, full-width, or cropped layouts when readability matters
- Handoff input: reads `slides_plan.md`, `images_needed.md`, `speaker_notes.md`, `paper_summary.md`, and `review_checklist.md`

This package does not include font files. Install Kalam and Patrick Hand locally before generating or opening PPTX files.
