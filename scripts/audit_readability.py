#!/usr/bin/env python3
"""Report observable readability risks in a teaching notebook.

This is a diagnostic, not a grade-level oracle. It deliberately avoids English-only
readability formulae so that Chinese and mixed technical prose remain meaningful.
"""

import argparse
import json
import re
from pathlib import Path

import nbformat


VAGUE_HEADINGS = {
    "introduction", "background", "overview", "method", "methods", "results",
    "discussion", "简介", "介绍", "背景", "概述", "方法", "结果", "讨论",
}
FILLER_PATTERNS = {
    "值得注意的是": "state the exact observation or condition",
    "需要指出的是": "state the point directly",
    "众所周知": "name the prerequisite or give evidence",
    "显而易见": "show the causal step",
    "不难看出": "show the causal step",
    "it is worth noting": "state the exact observation or condition",
    "obviously": "show the causal step",
    "as we all know": "name the prerequisite or give evidence",
}
BRIDGE_CUES = re.compile(
    r"(也就是|换句话说|可以把|想象|例如|比如|具体地|意味着|对应|失败|局限|"
    r"in other words|think of|for example|for instance|means|corresponds|fails|limitation)",
    re.IGNORECASE,
)
TODO_RE = re.compile(r"\bTODO\b|\[Add |\[verify\]|待补|待验证", re.IGNORECASE)
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_TECH_RE = re.compile(r"`[^`]+`|\$[^$]+\$|\b[A-Z][A-Z0-9-]{1,}\b")


def prose_paragraphs(source):
    source = CODE_BLOCK_RE.sub("", source)
    for raw in re.split(r"\n\s*\n", source):
        paragraph = raw.strip()
        if not paragraph or paragraph.startswith(("#", "|", "![", "$$", ">")):
            continue
        yield re.sub(r"\s+", " ", paragraph)


def next_markdown(cells, start):
    for cell in cells[start + 1:]:
        if cell.cell_type == "markdown" and cell.source.strip():
            return cell.source.strip()
        if cell.cell_type == "code" and cell.source.strip():
            return None
    return None


def audit(nb, max_cell_chars, max_paragraph_chars):
    severe, warnings = [], []
    markdown_cells = [(i, cell) for i, cell in enumerate(nb.cells) if cell.cell_type == "markdown"]

    for index, cell in markdown_cells:
        if TODO_RE.search(cell.source):
            severe.append({"cell": index, "kind": "unfinished_marker", "detail": "TODO or verification placeholder remains"})
        if len(cell.source) > max_cell_chars:
            severe.append({"cell": index, "kind": "long_markdown_cell", "detail": f"{len(cell.source)} characters; limit {max_cell_chars}"})

        for paragraph in prose_paragraphs(cell.source):
            if len(paragraph) > max_paragraph_chars:
                severe.append({"cell": index, "kind": "long_paragraph", "detail": f"{len(paragraph)} characters; limit {max_paragraph_chars}"})
            tech_tokens = INLINE_TECH_RE.findall(paragraph)
            if len(tech_tokens) >= 6 and not BRIDGE_CUES.search(paragraph):
                warnings.append({
                    "cell": index,
                    "kind": "jargon_cluster",
                    "detail": f"{len(tech_tokens)} technical tokens without an obvious example, mapping, or boundary cue",
                })
        for phrase, repair in FILLER_PATTERNS.items():
            if phrase.lower() in cell.source.lower():
                warnings.append({"cell": index, "kind": "filler_or_skipped_reasoning", "detail": f"{phrase!r}: {repair}"})

        for line in cell.source.splitlines():
            match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if match and re.sub(r"^\d+[.、:]?\s*", "", match.group(1)).strip().lower() in VAGUE_HEADINGS:
                warnings.append({"cell": index, "kind": "vague_heading", "detail": match.group(1).strip()})

    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code" or len(cell.source.strip().splitlines()) < 5:
            continue
        previous = nb.cells[index - 1].source.strip() if index and nb.cells[index - 1].cell_type == "markdown" else ""
        if len(previous) < 40:
            warnings.append({"cell": index, "kind": "unframed_code", "detail": "substantive code lacks a nearby question/prediction"})
        if cell.get("outputs"):
            following = next_markdown(nb.cells, index)
            if not following or len(following) < 60:
                warnings.append({"cell": index, "kind": "uninterpreted_output", "detail": "executed output lacks a nearby prose interpretation"})

    metrics = {
        "cells": len(nb.cells),
        "markdown_cells": len(markdown_cells),
        "severe_findings": len(severe),
        "warnings": len(warnings),
    }
    return metrics, severe, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--max-markdown-cell-chars", type=int, default=2800)
    parser.add_argument("--max-paragraph-chars", type=int, default=700)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--strict", action="store_true", help="fail on severe findings; warnings remain diagnostic")
    args = parser.parse_args()

    if not args.notebook.is_file():
        parser.error(f"notebook does not exist: {args.notebook}")
    nb = nbformat.read(args.notebook, as_version=4)
    metrics, severe, warnings = audit(nb, args.max_markdown_cell_chars, args.max_paragraph_chars)
    report = {"notebook": str(args.notebook), "metrics": metrics, "severe": severe, "warnings": warnings}

    print(json.dumps(metrics, ensure_ascii=False))
    for item in severe:
        print(f"FAIL cell {item['cell']}: {item['kind']} — {item['detail']}")
    for item in warnings:
        print(f"WARN cell {item['cell']}: {item['kind']} — {item['detail']}")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    raise SystemExit(1 if args.strict and severe else 0)


if __name__ == "__main__":
    main()
