# pptx skill customization: Newsprint editorial presentation style

This package overwrites `.claude/skills/pptx/SKILL.md` with a Newsprint editorial style for paper-to-PPT and general PPTX generation.

Defaults:

- Display headlines: Playfair Display
- Body text: Lora
- UI labels / captions / metadata: Inter
- Data / code / dates / metrics: JetBrains Mono
- Chinese fallback: FangSong / 仿宋
- Equations and paper-defined symbols: Cambria Math or another math/scientific font, not display/body/UI fonts
- Minimum newly added font size: 14 pt
- Style: off-white newsprint background, ink-black typography, strict rectangular grids, visible borders, sparse editorial red accents, subtle paper texture
- Figures/tables: do not wrap every figure/table in a card; use borderless, full-width, cropped, or lightly annotated layouts when readability matters
- Handoff input: reads `slides_plan.md`, `images_needed.md`, `speaker_notes.md`, `paper_summary.md`, and `review_checklist.md`

This package does not include font files. Install Playfair Display, Lora, Inter, and JetBrains Mono locally before generating or opening PPTX files.

Suggested Windows installation:

1. Download the font families from Google Fonts or each font's official release page.
2. Extract the `.zip` files.
3. Select the `.ttf` / `.otf` files.
4. Right-click and choose **Install for all users**.
