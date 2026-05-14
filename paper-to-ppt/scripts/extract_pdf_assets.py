#!/usr/bin/env python3
"""
extract_pdf_assets.py

用途：
1. 使用 PyMuPDF 打开 PDF。
2. 渲染每一页为 PNG，便于后续人工裁剪图表。
3. 尝试提取 PDF 内嵌图片。
4. 输出 assets_manifest.md。

推荐依赖：
    pip install pymupdf pillow

用法：
    python extract_pdf_assets.py path/to/paper.pdf output/assets/extracted

注意：
- 该脚本不判断图片含义。
- 自动提取的图片可能不是完整论文图表，仍需人工检查。
- 如果提取失败，请在 images_needed.md 中要求用户手动截图。
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

try:
    import fitz  # PyMuPDF
except ImportError as exc:
    raise SystemExit(
        "缺少依赖 PyMuPDF。请先运行：pip install pymupdf pillow"
    ) from exc


def safe_name(name: str) -> str:
    keep = []
    for ch in name.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in {" ", "-", "_", "."}:
            keep.append("-")
    text = "".join(keep).strip("-")
    while "--" in text:
        text = text.replace("--", "-")
    return text or "paper"


def render_pages(doc: fitz.Document, out_dir: Path, zoom: float = 2.0) -> List[str]:
    page_dir = out_dir / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    matrix = fitz.Matrix(zoom, zoom)
    for index, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        file_path = page_dir / f"page-{index:03d}.png"
        pix.save(file_path)
        outputs.append(str(file_path))
    return outputs


def extract_images(doc: fitz.Document, out_dir: Path) -> List[str]:
    image_dir = out_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        for image_index, image_info in enumerate(image_list, start=1):
            xref = image_info[0]
            try:
                extracted = doc.extract_image(xref)
                image_bytes = extracted["image"]
                ext = extracted.get("ext", "png")
                file_path = image_dir / f"page-{page_index + 1:03d}-image-{image_index:02d}.{ext}"
                file_path.write_bytes(image_bytes)
                outputs.append(str(file_path))
            except Exception as err:  # noqa: BLE001
                outputs.append(f"FAILED page {page_index + 1} image {image_index}: {err}")
    return outputs


def write_manifest(pdf_path: Path, out_dir: Path, rendered: List[str], images: List[str]) -> None:
    manifest = out_dir / "assets_manifest.md"
    lines = [
        "# Assets Manifest",
        "",
        f"PDF: `{pdf_path}`",
        "",
        "## Rendered Pages",
        "",
    ]
    for item in rendered:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Extracted Images", ""])
    if images:
        for item in images:
            lines.append(f"- `{item}`")
    else:
        lines.append("- 未提取到内嵌图片，建议使用 rendered pages 手动裁剪。")
    lines.extend([
        "",
        "## Notes",
        "",
        "- 自动提取图片不等于已经得到完整论文图表。",
        "- 请人工检查每张图片是否完整、清晰、含义正确。",
        "- 缺失或不清晰图表请记录到 images_needed.md。",
    ])
    manifest.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--zoom", type=float, default=2.0)
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF 不存在：{args.pdf}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    rendered = render_pages(doc, args.output_dir, zoom=args.zoom)
    images = extract_images(doc, args.output_dir)
    write_manifest(args.pdf, args.output_dir, rendered, images)
    print(f"Rendered pages: {len(rendered)}")
    print(f"Extracted images: {len([x for x in images if not x.startswith('FAILED')])}")
    print(f"Manifest: {args.output_dir / 'assets_manifest.md'}")


if __name__ == "__main__":
    main()
