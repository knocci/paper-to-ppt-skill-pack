#!/usr/bin/env node
/**
 * Render LaTeX equations to standalone SVG files using MathJax v4.
 *
 * Usage:
 *   npm install @mathjax/src@4
 *   node scripts/render-equations-svg.mjs --input equations.json --out assets/generated/equations
 *
 * Input JSON:
 * [
 *   {
 *     "id": "eq_method_objective",
 *     "latex": "\\min_{\\tau}\\; F_{\\mathrm{task}}(T,l) + F_{\\mathrm{control}}(\\tau)",
 *     "display": true
 *   }
 * ]
 */

import fs from 'node:fs/promises';
import path from 'node:path';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--input' || key === '-i') args.input = argv[++i];
    else if (key === '--out' || key === '-o') args.out = argv[++i];
    else if (key === '--em') args.em = Number(argv[++i]);
    else if (key === '--ex') args.ex = Number(argv[++i]);
    else if (key === '--width') args.width = Number(argv[++i]);
  }
  if (!args.input || !args.out) {
    throw new Error('Missing required args. Usage: node render-equations-svg.mjs --input equations.json --out assets/generated/equations');
  }
  args.em = Number.isFinite(args.em) ? args.em : 16;
  args.ex = Number.isFinite(args.ex) ? args.ex : 8;
  args.width = Number.isFinite(args.width) ? args.width : 80 * args.em;
  return args;
}

function safeId(id) {
  return String(id || 'equation')
    .replace(/[^\w.-]+/g, '_')
    .replace(/^_+|_+$/g, '') || 'equation';
}

async function loadMathJax() {
  global.MathJax = {
    loader: {
      paths: { mathjax: '@mathjax/src/bundle' },
      load: ['adaptors/liteDOM'],
      require: (file) => import(file),
    },
    tex: {
      packages: {'[+]': ['ams', 'newcommand', 'configmacros']},
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
    },
    svg: {
      fontCache: 'none',
    },
    output: {
      font: 'mathjax-newcm',
    },
  };

  try {
    await import('@mathjax/src/bundle/tex-svg.js');
  } catch (err) {
    console.error('Failed to load @mathjax/src. Install it first:');
    console.error('  npm install @mathjax/src@4');
    throw err;
  }

  await MathJax.startup.promise;
}

async function renderSvg(latex, display, opts) {
  const node = await MathJax.tex2svgPromise(latex, {
    display,
    em: opts.em,
    ex: opts.ex,
    containerWidth: opts.width,
  });

  const adaptor = MathJax.startup.adaptor;
  const svgNode = adaptor.tags(node, 'svg')[0];
  let svg = adaptor.serializeXML(svgNode);

  // Force deterministic ink color for Newsprint style.
  svg = svg.replace(/currentColor/g, '#111111');

  if (!svg.includes('xmlns=')) {
    svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ');
  }

  return `<?xml version="1.0" encoding="UTF-8"?>\n${svg}\n`;
}

async function main() {
  const args = parseArgs(process.argv);
  await fs.mkdir(args.out, { recursive: true });

  const raw = await fs.readFile(args.input, 'utf8');
  const parsed = JSON.parse(raw);
  const equations = Array.isArray(parsed) ? parsed : parsed.equations;

  if (!Array.isArray(equations)) {
    throw new Error('Input must be an array or an object with an "equations" array.');
  }

  await loadMathJax();

  const manifest = [];

  for (const item of equations) {
    if (!item || !item.latex) continue;

    const id = safeId(item.id);
    const outFile = path.join(args.out, `${id}.svg`);
    const svg = await renderSvg(String(item.latex), item.display !== false, args);

    await fs.writeFile(outFile, svg, 'utf8');
    manifest.push({
      id,
      latex: item.latex,
      display: item.display !== false,
      file: outFile.replaceAll('\\', '/'),
    });

    console.log(`Rendered ${id} -> ${outFile}`);
  }

  await fs.writeFile(path.join(args.out, 'equations.rendered.json'), JSON.stringify(manifest, null, 2), 'utf8');

  if (global.MathJax?.done) {
    MathJax.done();
  }
}

main().catch((err) => {
  console.error(err?.stack || err);
  process.exit(1);
});
