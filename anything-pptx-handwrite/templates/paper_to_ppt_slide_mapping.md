# Handoff slide mapping

When generating a deck from `slides_plan.md`, map fields like this:

```yaml
slide_number: slide order
title: English `Kalam` headline
key_message: sticky note, central handwritten claim, or concise takeaway
bullet_points: short `Patrick Hand` bullets
visual_suggestion: layout recipe and asset placement
speaker_note: speaker notes; Chinese is acceptable
source_reference: short on-slide source marker at 14 pt or larger; full references may go in notes/checklist
```

Default language:

```yaml
slide_titles: English
main_bullets: English
speaker_notes: Chinese allowed
chinese_on_slides: FangSong / 仿宋 only
equations_and_symbols: Cambria Math / Latin Modern Math / STIX Two Math / Times New Roman
```

Figure/table policy:

```yaml
figures:
  default: borderless_large or light_annotation
  avoid: automatic card/frame around every figure

tables:
  default: full_bleed_crop or borderless_large
  avoid: shrinking dense tables into small cards

equations:
  default: original screenshot or math-font recreation
  avoid: Kalam / Patrick Hand for symbols

minimum_font_size: 14pt
```

If a required figure/table is missing, use a placeholder instead of inventing content.
