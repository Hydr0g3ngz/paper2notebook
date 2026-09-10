#!/usr/bin/env python3
"""Validate notebook execution state and local image links."""

import argparse
import re
from pathlib import Path

import nbformat


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--require-executed", action="store_true")
    args = parser.parse_args()

    if not args.notebook.is_file():
        parser.error(f"notebook does not exist: {args.notebook}")
    nb = nbformat.read(args.notebook, as_version=4)
    failures, warnings = [], []
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    errors = [
        (i, out.get("ename", "Error"), out.get("evalue", ""))
        for i, cell in enumerate(nb.cells)
        if cell.cell_type == "code"
        for out in cell.get("outputs", [])
        if out.output_type == "error"
    ]
    if errors:
        failures.append(f"error outputs: {errors}")
    if args.require_executed:
        missing = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and c.source.strip()
                   and c.get("execution_count") is None]
        if missing:
            failures.append(f"unexecuted code cells: {missing}")

    headings = [c.source.splitlines()[0] for c in nb.cells
                if c.cell_type == "markdown" and c.source.lstrip().startswith("#")]
    if len(headings) < 6:
        warnings.append(f"only {len(headings)} heading cells; inspect pedagogical structure")

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        for link in IMAGE_RE.findall(cell.source):
            clean = link.strip().split()[0].strip("<>")
            if clean.startswith(("http://", "https://", "data:")):
                continue
            target = (args.notebook.parent / clean).resolve()
            if not target.is_file():
                failures.append(f"cell {i}: missing local image {clean}")

    print(f"cells={len(nb.cells)}, code={len(code_cells)}, headings={len(headings)}, errors={len(errors)}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in failures:
        print(f"FAIL: {item}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
