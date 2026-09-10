#!/usr/bin/env python3
"""Measure notebook depth signals without treating them as a quality score."""

import argparse
import json
from pathlib import Path

import nbformat


def profile(path: Path):
    nb = nbformat.read(path, as_version=4)
    markdown = [cell for cell in nb.cells if cell.cell_type == "markdown"]
    code = [cell for cell in nb.cells if cell.cell_type == "code" and cell.source.strip()]
    headings = [line for cell in markdown for line in cell.source.splitlines() if line.startswith("#")]
    rich_outputs = 0
    for cell in code:
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if any(key in data for key in ("image/png", "image/jpeg", "audio/wav", "text/html")):
                rich_outputs += 1
    return {
        "path": str(path.resolve()),
        "cells": len(nb.cells),
        "markdown_cells": len(markdown),
        "markdown_chars": sum(len(cell.source) for cell in markdown),
        "code_cells": len(code),
        "code_chars": sum(len(cell.source) for cell in code),
        "heading_lines": len(headings),
        "rich_outputs": rich_outputs,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path, help="write a frozen JSON profile for later validation")
    args = parser.parse_args()
    if not args.notebook.is_file():
        parser.error(f"notebook does not exist: {args.notebook}")
    result = profile(args.notebook)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved frozen profile: {args.output}")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n".join(f"{key}={value}" for key, value in result.items()))


if __name__ == "__main__":
    main()
