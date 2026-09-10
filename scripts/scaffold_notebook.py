#!/usr/bin/env python3
"""Create a minimal paper-onramp notebook outline."""

import argparse
from pathlib import Path
from textwrap import dedent

import nbformat as nbf


METHOD_SECTIONS = [
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

EMPIRICAL_SECTIONS = [
    ("0. How to use this notebook", "Assumptions, outcomes, runtime, source status, and reproduction boundary."),
    ("1. Scientific question", "Define the causal or comparative question and why it matters."),
    ("2. Terminology ledger", "Define variables, datasets, conditions, and metrics."),
    ("3. Experimental design", "Map controlled variables, changed factors, measurements, and possible confounds."),
    ("4. Data-generation conditions", "Explain each condition and the intended fidelity difference."),
    ("5. Minimal mechanism experiment", "Make one data or measurement difference observable."),
    ("6. Decisive evidence", "Interpret source figures/tables and recompute one quantity where possible."),
    ("7. Uncertainty and alternative explanations", "Inspect intervals, effect sizes, confounds, and external validity."),
    ("8. Next discriminating experiments", "Turn unresolved factors into controlled follow-ups."),
    ("9. Misconceptions and self-check", "Test whether the evidence chain is understood."),
]

EVALUATOR_SECTIONS = [
    ("0. How to use this notebook", "Assumptions, outcomes, source status, and reproduction boundary."),
    ("1. What existing metrics miss", "Define the evaluation failure and information available at deployment."),
    ("2. Score semantics", "Define each predicted dimension and counterexamples."),
    ("3. Annotation and data pipeline", "Explain raters, aggregation, sampling, uncertainty, and pseudo-labels."),
    ("4. Model information flow", "Map inputs, encoders, alignment, fusion, and heads."),
    ("5. Minimal metric experiment", "Compare a proxy with a multidimensional judge."),
    ("6. Evidence and ablations", "Interpret correlations, errors, domains, and component tests."),
    ("7. Calibration, shift, and gaming", "Show what headline correlation does not prove."),
    ("8. Research map and self-check", "Design audits and safer deployment tests."),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--citation", default="[Add full citation]")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--paper-type", choices=["method", "empirical", "evaluator"], default="method")
    args = parser.parse_args()

    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.cells.append(nbf.v4.new_markdown_cell(f"# {args.title}\n\n**Paper:** {args.citation}"))
    routes = {"method": METHOD_SECTIONS, "empirical": EMPIRICAL_SECTIONS, "evaluator": EVALUATOR_SECTIONS}
    for heading, prompt in routes[args.paper_type]:
        nb.cells.append(nbf.v4.new_markdown_cell(f"## {heading}\n\n> TODO: {prompt}"))
    insert_at = min(8, len(nb.cells))
    nb.cells.insert(insert_at, nbf.v4.new_code_cell(dedent("""
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
