#!/usr/bin/env python3
"""Create a minimal paper-onramp notebook outline."""

import argparse
from pathlib import Path
from textwrap import dedent

import nbformat as nbf


SECTIONS = [
    ("0. How to use this notebook", "Assumed background, learning outcomes, runtime, and reproduction boundary."),
    ("1. The real problem", "Define inputs, outputs, assumptions, and why the problem is difficult."),
    ("2. Terminology ledger", "Define canonical field terms, symbols, datasets, and metrics."),
    ("3. Previous paradigm and bottleneck", "Explain the strongest prior mental model and make one limitation observable."),
    ("4. Paper thesis and argument map", "State the contribution and map sections to evidence."),
    ("5. Architecture overview", "Insert the original architecture figure and a simplified teaching schematic."),
    ("6. Module-by-module derivation", "For each module: purpose, interface, mechanism, design choice, evidence/failure."),
    ("7. Objective and training", "Explain alignment, loss, optimization, and full data flow."),
    ("8. Minimal executable experiment", "Run a mechanism demo or teaching-scale implementation."),
    ("9. What the paper's evidence proves", "Interpret results, ablations, baselines, and uncertainty."),
    ("10. Limitations and research map", "Separate paper-stated limits from proposed extensions."),
    ("11. Misconceptions and self-check", "Test conceptual understanding before concluding."),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--citation", default="[Add full citation]")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.cells.append(nbf.v4.new_markdown_cell(f"# {args.title}\n\n**Paper:** {args.citation}"))
    for heading, prompt in SECTIONS:
        nb.cells.append(nbf.v4.new_markdown_cell(f"## {heading}\n\n> TODO: {prompt}"))
    nb.cells.insert(8, nbf.v4.new_code_cell(dedent("""
        # Minimal dependency and reproducibility cell
        import random
        import numpy as np
        random.seed(7)
        np.random.seed(7)
    """).strip()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, args.output)
    print(f"created {args.output} with {len(nb.cells)} cells")


if __name__ == "__main__":
    main()
