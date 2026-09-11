#!/usr/bin/env python3
"""Create a minimal paper-onramp notebook outline."""

import argparse
from pathlib import Path
from textwrap import dedent

import nbformat as nbf


METHOD_SECTIONS = [
    ("0. Reading lanes and learning contract", "Link a 3-minute map, deep-reading path, and research/reproduction path; state outcomes, runtime, and boundary."),
    ("1. Source and version manifest", "Record the exact paper, rendered PDF, supplement, official code revision, and unavailable sources."),
    ("2. Three-minute paper map", "Give the problem, thesis, system figure, decisive result, and strongest limitation."),
    ("3. The real problem", "Define inputs, outputs, assumptions, and why the problem is difficult."),
    ("4. Terminology and variable ledger", "Define terms and every load-bearing symbol's type, shape, units, observability, and role."),
    ("5. Previous paradigm and bottleneck", "Explain the strongest prior mental model and make one limitation observable."),
    ("6. Paper thesis and argument map", "State falsifiable claims and map them to evidence rather than repeating the abstract."),
    ("7. Architecture overview", "Insert the original architecture figure and a simplified teaching schematic."),
    ("8. Module-by-module derivation", "For each module: purpose, interface, mechanism, design choice, evidence/failure."),
    ("9. Equations, checks, and code crosswalk", "Explain assumptions and run dimensional, limit, invariance, or numerical checks; label paper/code/inference status."),
    ("10. Objective and training", "Explain alignment, loss, optimization, and full data flow."),
    ("11. Minimal executable experiments", "Run sanity, mechanism, and structure-faithful teaching experiments."),
    ("12. Claim-evidence ledger", "For each major claim record source, support status, scope, non-implications, and missing evidence."),
    ("13. Load-bearing ablations and red flags", "Identify the decisive component test and audit baselines, uncertainty, leakage, and discrepancies."),
    ("14. Limitations and research map", "Separate paper-stated limits from proposed extensions and define a cheapest falsifying experiment."),
    ("15. Feynman teach-back and retrieval checks", "Ask reconstruction questions and place compact answer checkpoints later."),
]

EMPIRICAL_SECTIONS = [
    ("0. Reading lanes and learning contract", "Link the three reading paths; state outcomes, runtime, and reproduction boundary."),
    ("1. Source and version manifest", "Record the exact paper, supplement/data/code surfaces, and unavailable sources."),
    ("2. Three-minute paper map", "Give the question, thesis, decisive evidence, and strongest limitation."),
    ("3. Scientific question and variables", "Define the question, typed variables, measurements, assumptions, and why it matters."),
    ("4. Experimental design", "Map controls, changed factors, measurements, sampling, and possible confounds."),
    ("5. Data-generation conditions", "Explain each condition and intended fidelity difference."),
    ("6. Minimal mechanism experiment", "Make one data or measurement difference observable."),
    ("7. Claim-evidence ledger", "Anchor each claim to a result and state support, non-implications, and missing evidence."),
    ("8. Decisive evidence and load-bearing tests", "Interpret original figures/tables and recompute one quantity where possible."),
    ("9. Uncertainty, red flags, and alternatives", "Inspect intervals, effects, confounds, leakage, and external validity."),
    ("10. Research decisions", "State reusable ideas, fragile assumptions, cheapest falsifying test, and continuation threshold."),
    ("11. Feynman teach-back and retrieval checks", "Test whether the evidence chain can be reconstructed from memory."),
]

EVALUATOR_SECTIONS = [
    ("0. Reading lanes and learning contract", "Link the three paths; state outcomes, source status, and reproduction boundary."),
    ("1. Source and version manifest", "Record the paper, data/annotation details, official code revision, and unavailable sources."),
    ("2. Three-minute paper map", "Give the evaluation gap, thesis, decisive result, and strongest limitation."),
    ("3. What existing metrics miss", "Define the evaluation failure and information available at deployment."),
    ("4. Score semantics and variables", "Define each dimension, typed variables, observability, and counterexamples."),
    ("5. Annotation and data pipeline", "Explain raters, aggregation, sampling, uncertainty, and pseudo-labels."),
    ("6. Model information flow", "Map inputs, encoders, alignment, fusion, heads, equations, and code status."),
    ("7. Minimal metric experiment", "Compare a proxy with a multidimensional judge."),
    ("8. Claim-evidence ledger", "Anchor each claim and state support, non-implications, and missing evidence."),
    ("9. Evidence, ablations, and red flags", "Interpret correlations, errors, domains, component tests, leakage, and gaming."),
    ("10. Calibration, shift, and research decisions", "Design audits, a cheapest falsifying test, and a continuation threshold."),
    ("11. Feynman teach-back and retrieval checks", "Reconstruct score semantics and evidence without copying prose."),
]

REQUIRED_COVERAGE = {
    "quick_map": False,
    "field_foundations": False,
    "paper_reconstruction": False,
    "evidence_ledger": False,
    "equation_or_mechanism_checks": False,
    "reproduction_boundary": False,
    "research_bridge": False,
    "retrieval_practice": False,
    "plain_language_bridges": False,
    "output_interpretation": False,
    "comprehension_audit": False,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--citation", default="[Add full citation]")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--paper-type", choices=["method", "empirical", "evaluator"], default="method")
    parser.add_argument("--depth-mode", choices=["survey", "full-onramp", "reproduction"], default="full-onramp")
    parser.add_argument("--grounding-mode", choices=["page_grounded", "structure_grounded", "source_limited"], default="page_grounded")
    parser.add_argument("--source", default="[Add exact PDF, DOI, arXiv version, or official URL]")
    args = parser.parse_args()

    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["paper2notebook"] = {
        "schema_version": "0.5",
        "depth_mode": args.depth_mode,
        "grounding_mode": args.grounding_mode,
        "primary_route": args.paper_type,
        "coverage": REQUIRED_COVERAGE.copy(),
        "source_manifest": [
            {"kind": "paper", "locator": args.source, "version": "[verify]", "status": "needs_review"},
            {"kind": "official_code", "locator": "[add URL/revision or explain absence]", "version": "[pin revision]", "status": "needs_review"},
        ],
        "claim_evidence": [],
        "reader_model": {
            "prior_knowledge": [],
            "not_assumed": [],
            "target_capabilities": [],
        },
        "concept_bridges": [],
    }
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
