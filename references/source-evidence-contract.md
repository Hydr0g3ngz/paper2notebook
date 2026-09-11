# Source and evidence contract

## 1. Source manifest before interpretation

Verify the paper's identity and record the exact version used. Build a manifest with these source roles:

| Role | Preferred surface | What it can establish |
|---|---|---|
| paper text | author TeX/source or official full text | wording, equations, section structure, stated method |
| rendered paper | stable PDF | page anchors, visual layout, figures and tables |
| qualification | appendix or supplement | omitted details, extra ablations, assumptions, failures |
| implementation | official repository at a pinned revision | defaults, shapes, preprocessing, actual execution path |
| background | primary external sources | field context only, not evidence for this paper's results |

For arXiv papers, prefer TeX/source for equations and cross-references when obtainable, but keep the PDF as the authority for page and figure anchors. Hash or otherwise identify local source files. Never replace missing official code with an unofficial repository without an explicit label.

Allowed source status values are `inspected`, `not_found`, `not_applicable`, and `needs_review`. A final full-onramp must not retain `needs_review` for its primary paper.

Record one grounding mode and downgrade honestly when anchors are unavailable:

- `page_grounded` — stable PDF pages support page, figure, table, and equation anchors;
- `structure_grounded` — section/equation/figure identifiers are stable but page anchors are not;
- `source_limited` — only partial text or unstable extraction is available, so some judgments remain unassessable.

## 2. Evidence-first triage

The abstract supplies candidate claims, not proof. Before spending most of the reading budget on the method:

1. Write the one-sentence thesis and 3–7 load-bearing claims.
2. Locate the headline result and its strongest baseline or control.
3. Locate the ablation, sensitivity test, or counterfactual that bears most directly on the proposed mechanism.
4. Locate limitations, failure cases, negative results, and materially qualifying appendix results.
5. Decide whether each claim currently has direct, partial, background-only, unsupported, or unverified support.

This triage controls emphasis, not whether a requested full notebook is completed. Weak evidence should produce a more critical notebook, not a shorter one.

## 3. Claim-evidence ledger

Keep the following fields for every material claim:

- `claim`: a falsifiable statement, not a topic label;
- `location`: figure/table/equation/section and page when stable;
- `evidence`: experiment, theorem, ablation, qualitative example, or code inspection;
- `status`: `direct`, `partial`, `background_only`, `unsupported`, or `unverified`;
- `supports`: the narrow conclusion licensed by the evidence;
- `does_not_support`: a nearby stronger conclusion that remains unjustified;
- `missing`: missing control, uncertainty, seed, domain, baseline, or implementation detail;
- `notebook_cell`: where the learner can inspect or test it.

A result table is not self-interpreting. Name the comparison, controlled factors, uncertainty, and alternative explanations. Exact numbers require an exact anchor. If a field is absent, write `not_reported` rather than inferring it.

## 4. Load-bearing ablations and red flags

For each claimed mechanism, identify the experiment whose outcome would most weaken it. Prefer ablations that isolate the component over bundles of simultaneous changes. If no such evidence exists, say so.

Audit at least these red flags where applicable:

- no meaningful baseline or an outdated/unequal comparison;
- no uncertainty, seed variation, or statistical support where stochasticity matters;
- no component-isolating ablation for the central mechanism;
- train/test leakage, shortcut features, domain overlap, or cherry-picked subsets;
- metric improvement without qualitative or task-relevant confirmation;
- missing failures, limitations, compute accounting, or public implementation;
- paper/code disagreement in preprocessing, shapes, defaults, loss, or inference.

Red flags are prompts for inspection, not automatic verdicts.

## 5. Paper/code crosswalk

Official code is secondary evidence for implementation, never retrospective proof of a paper claim. Pin the inspected revision and label each implementation statement:

- `paper_stated` — explicit in the paper;
- `code_confirmed` — observed in official code;
- `discrepant` — paper and code differ;
- `teaching_inference` — introduced to make the notebook executable or understandable.

The notebook must make discrepancies visible and keep teaching defaults separate from benchmark defaults.
