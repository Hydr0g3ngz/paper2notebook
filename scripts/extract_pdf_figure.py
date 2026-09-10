#!/usr/bin/env python3
"""Render a tightly cropped PDF page region to PNG using normalized coordinates."""

import argparse
from pathlib import Path


def parse_bbox(value: str):
    parts = [float(x) for x in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be left,top,right,bottom")
    left, top, right, bottom = parts
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise argparse.ArgumentTypeError("bbox coordinates must satisfy 0<=left<right<=1 and 0<=top<bottom<=1")
    return parts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--page", required=True, type=int, help="1-based PDF page number")
    parser.add_argument("--bbox", type=parse_bbox, default=[0, 0, 1, 1],
                        help="normalized left,top,right,bottom")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"input does not exist: {args.input}")
    if args.page < 1:
        parser.error("page must be >= 1")
    if args.dpi < 72:
        parser.error("dpi must be >= 72")

    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("PyMuPDF is required: python -m pip install pymupdf") from exc

    doc = fitz.open(args.input)
    if args.page > len(doc):
        raise SystemExit(f"page {args.page} exceeds document length {len(doc)}")
    page = doc[args.page - 1]
    rect = page.rect
    left, top, right, bottom = args.bbox
    clip = fitz.Rect(
        rect.x0 + left * rect.width,
        rect.y0 + top * rect.height,
        rect.x0 + right * rect.width,
        rect.y0 + bottom * rect.height,
    )
    pix = page.get_pixmap(matrix=fitz.Matrix(args.dpi / 72, args.dpi / 72),
                          clip=clip, alpha=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pix.save(args.output)
    print(f"saved {args.output} ({pix.width}x{pix.height}), source page {args.page}")


if __name__ == "__main__":
    main()
