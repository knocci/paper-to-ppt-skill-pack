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


## Equation rendering

Do not rely on plain HTML text plus a math font for formulas. Full equations should be written as LaTeX, rendered to SVG/PNG assets, then inserted into both HTML previews and PPTX slides as images.

Recommended dependency for the included helper script:

```powershell
cd "$env:USERPROFILE\.claude\skills\pptx"
npm install @mathjax/src@4
```

The helper script path is:

```text
pptx/scripts/render-equations-svg.mjs
```

Example equation manifest:

```json
[
  {
    "id": "eq_method_objective",
    "latex": "\\min_{\\tau}\\; F_{\\mathrm{task}}(T,l) + F_{\\mathrm{control}}(\\tau) \\quad \\mathrm{s.t.}\\quad C(T)",
    "display": true
  }
]
```

Example command:

```powershell
node "$env:USERPROFILE\.claude\skills\pptx\scripts\render-equations-svg.mjs" `
  --input .\assets\generated\equations\equations.json `
  --out .\assets\generated\equations
```
