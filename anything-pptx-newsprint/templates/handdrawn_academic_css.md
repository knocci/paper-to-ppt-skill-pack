# Hand-drawn academic CSS tokens

Use this CSS as the default shared style block for `html2pptx` slides.

Important defaults:

- English headings: `Kalam`
- English body: `Patrick Hand`
- Chinese: `FangSong` / `仿宋`
- Equations and paper symbols: `Cambria Math` or another math/scientific font
- Minimum added text size: 14 pt
- Figures/tables are not framed by default; use borderless or full-width placement when readability matters

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
  --wobbly: 14pt;
  --wobbly-md: 10pt;
  /* Elliptical border-radius (slash syntax) does not convert to PPTX.
     Simple pt/px/% values produce uniform rounded corners in PowerPoint.
     The hand-drawn irregularity is preserved via hard shadows, wobbly borders,
     and PptxGenJS shape adjustments where needed. */
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
  /* CSS radial-gradient does not convert to PPTX.
     Paper texture for final PPTX must use one of:
     1. Pre-generated PNG: background-image: url('paper-dots.png')
     2. PptxGenJS native shapes with dot/line/grid patterns
     3. Flat background-color as fallback
     The gradient here serves as HTML preview only. */
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
  /* CSS transform (rotate) does not convert to PPTX.
     For final output, apply slight rotation via PptxGenJS shape rotation
     or accept flat post-it cards as a clean fallback. */
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
  border-radius: 12pt;
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
