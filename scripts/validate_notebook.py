#!/usr/bin/env python3
"""Validate notebook execution state and local image links."""

import argparse
import json
import re
from pathlib import Path

import nbformat


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
REQUIRED_COVERAGE = {
    "quick_map",
    "field_foundations",
    "paper_reconstruction",
    "evidence_ledger",
    "equation_or_mechanism_checks",
    "reproduction_boundary",
    "research_bridge",
    "retrieval_practice",
}
CLAIM_FIELDS = {"claim", "location", "evidence", "status", "supports", "does_not_support", "missing"}
CLAIM_STATUSES = {"direct", "partial", "background_only", "unsupported", "unverified"}
SOURCE_STATUSES = {"inspected", "not_found", "not_applicable", "needs_review"}


def validate_contract(nb, depth_mode):
    failures = []
    contract = nb.metadata.get("paper2notebook")
    if not isinstance(contract, dict):
        return ["missing notebook metadata: paper2notebook contract"]
    if str(contract.get("schema_version", "")) != "0.4":
        failures.append("paper2notebook.schema_version must be 0.4")
    recorded_depth = contract.get("depth_mode")
    if recorded_depth not in {"survey", "full-onramp", "reproduction"}:
        failures.append("paper2notebook.depth_mode is missing or invalid")
    if contract.get("grounding_mode") not in {"page_grounded", "structure_grounded", "source_limited"}:
        failures.append("paper2notebook.grounding_mode is missing or invalid")
    if depth_mode and recorded_depth != depth_mode:
        failures.append(f"contract depth_mode={recorded_depth!r} does not match --depth-mode={depth_mode!r}")
    if not contract.get("primary_route"):
        failures.append("paper2notebook.primary_route is missing")

    coverage = contract.get("coverage")
    if not isinstance(coverage, dict):
        failures.append("paper2notebook.coverage must be an object")
    else:
        missing = sorted(key for key in REQUIRED_COVERAGE if coverage.get(key) is not True)
        if missing:
            failures.append(f"contract coverage not completed: {missing}")

    manifest = contract.get("source_manifest")
    if not isinstance(manifest, list) or not manifest:
        failures.append("paper2notebook.source_manifest must contain inspected sources")
    else:
        paper_sources = [item for item in manifest if isinstance(item, dict) and item.get("kind") == "paper"]
        if not paper_sources:
            failures.append("source_manifest has no primary paper entry")
        for index, item in enumerate(manifest):
            if not isinstance(item, dict):
                failures.append(f"source_manifest[{index}] must be an object")
                continue
            status = item.get("status")
            if status not in SOURCE_STATUSES:
                failures.append(f"source_manifest[{index}] has invalid status {status!r}")
            if not item.get("locator"):
                failures.append(f"source_manifest[{index}] has no locator")
        if any(item.get("status") == "needs_review" for item in paper_sources):
            failures.append("primary paper source still has status needs_review")
        if recorded_depth in {"full-onramp", "reproduction"}:
            code_entries = [item for item in manifest if isinstance(item, dict) and item.get("kind") == "official_code"]
            if not code_entries:
                failures.append("source_manifest must record official_code as inspected, not_found, or not_applicable")
            elif any(item.get("status") == "needs_review" for item in code_entries):
                failures.append("official_code source still has status needs_review")

    claims = contract.get("claim_evidence")
    minimum_claims = 1 if recorded_depth == "survey" else 3
    if not isinstance(claims, list) or len(claims) < minimum_claims:
        failures.append(f"claim_evidence must contain at least {minimum_claims} material claim(s)")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                failures.append(f"claim_evidence[{index}] must be an object")
                continue
            missing_fields = sorted(field for field in CLAIM_FIELDS if field not in claim or claim[field] in (None, ""))
            if missing_fields:
                failures.append(f"claim_evidence[{index}] missing fields: {missing_fields}")
            if claim.get("status") not in CLAIM_STATUSES:
                failures.append(f"claim_evidence[{index}] has invalid status {claim.get('status')!r}")
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--require-executed", action="store_true")
    parser.add_argument("--require-local-figures", type=int, default=0)
    parser.add_argument("--require-contract", action="store_true")
    parser.add_argument("--depth-mode", choices=["survey", "full-onramp", "reproduction"])
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--reference-profile", type=Path, help="frozen JSON from profile_notebook.py")
    args = parser.parse_args()

    if not args.notebook.is_file():
        parser.error(f"notebook does not exist: {args.notebook}")
    nb = nbformat.read(args.notebook, as_version=4)
    failures, warnings = [], []
    if args.require_contract:
        failures.extend(validate_contract(nb, args.depth_mode))
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

    markdown_cells = [c for c in nb.cells if c.cell_type == "markdown"]
    headings = [line for c in markdown_cells for line in c.source.splitlines() if line.startswith("#")]
    if len(headings) < 6:
        warnings.append(f"only {len(headings)} heading cells; inspect pedagogical structure")

    local_figures = 0
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        for link in IMAGE_RE.findall(cell.source):
            clean = link.strip().split()[0].strip("<>")
            if clean.startswith(("http://", "https://", "data:", "attachment:")):
                continue
            local_figures += 1
            target = (args.notebook.parent / clean).resolve()
            if not target.is_file():
                failures.append(f"cell {i}: missing local image {clean}")

    if local_figures < args.require_local_figures:
        failures.append(f"only {local_figures} local figures; require {args.require_local_figures}")
    markdown_chars = sum(len(c.source) for c in markdown_cells)
    rich_outputs = sum(
        1 for c in code_cells for out in c.get("outputs", [])
        if any(key in out.get("data", {}) for key in ("image/png", "image/jpeg", "audio/wav", "text/html"))
    )
    if args.depth_mode in ("full-onramp", "reproduction"):
        floors = {"cells": 28, "code": 8, "headings": 12, "markdown_chars": 7000, "rich_outputs": 3}
        observed = {"cells": len(nb.cells), "code": len(code_cells), "headings": len(headings),
                    "markdown_chars": markdown_chars, "rich_outputs": rich_outputs}
        reference_metrics = None
        if args.reference_profile:
            if not args.reference_profile.is_file():
                failures.append(f"reference profile does not exist: {args.reference_profile}")
            else:
                reference_metrics = json.loads(args.reference_profile.read_text(encoding="utf-8"))
        elif args.reference:
            if not args.reference.is_file():
                failures.append(f"reference notebook does not exist: {args.reference}")
            else:
                ref = nbformat.read(args.reference, as_version=4)
                ref_md = [c for c in ref.cells if c.cell_type == "markdown"]
                ref_code = [c for c in ref.cells if c.cell_type == "code" and c.source.strip()]
                reference_metrics = {"cells": len(ref.cells), "code_cells": len(ref_code),
                                     "markdown_chars": sum(len(c.source) for c in ref_md)}
        if reference_metrics:
            floors["cells"] = max(floors["cells"], int(reference_metrics["cells"] * 0.70 + 0.999))
            floors["code"] = max(floors["code"], int(reference_metrics["code_cells"] * 0.70 + 0.999))
            floors["markdown_chars"] = max(floors["markdown_chars"], int(reference_metrics["markdown_chars"] * 0.70 + 0.999))
        for key, floor in floors.items():
            if observed[key] < floor:
                failures.append(f"depth gate {key}: observed {observed[key]}, require {floor}")
    print(f"cells={len(nb.cells)}, code={len(code_cells)}, headings={len(headings)}, markdown_chars={markdown_chars}, rich_outputs={rich_outputs}, local_figures={local_figures}, errors={len(errors)}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in failures:
        print(f"FAIL: {item}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
