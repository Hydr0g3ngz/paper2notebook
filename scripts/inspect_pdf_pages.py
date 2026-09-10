#!/usr/bin/env python3
"""Render a labeled PDF contact sheet before selecting figure crops."""

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--scale", type=float, default=0.72)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"PDF does not exist: {args.input}")
    if args.columns < 1 or args.scale <= 0:
        parser.error("columns and scale must be positive")

    doc = fitz.open(args.input)
    pages = []
    for index, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(args.scale, args.scale), alpha=False)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        tile = Image.new("RGB", (image.width, image.height + 30), "white")
        tile.paste(image, (0, 30))
        ImageDraw.Draw(tile).text((8, 7), f"PDF page {index + 1}", fill="red")
        pages.append(tile)
    if not pages:
        parser.error("PDF has no pages")

    width = max(page.width for page in pages)
    height = max(page.height for page in pages)
    rows = (len(pages) + args.columns - 1) // args.columns
    sheet = Image.new("RGB", (args.columns * width, rows * height), "white")
    for index, page in enumerate(pages):
        sheet.paste(page, ((index % args.columns) * width, (index // args.columns) * height))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"saved {args.output} with {len(pages)} labeled pages")


if __name__ == "__main__":
    main()
