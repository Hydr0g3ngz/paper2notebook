# Online paper-reading skill benchmark — 2026-09

This note records the public designs used to challenge `paper2notebook` v0.3 before the v0.4 redesign. Public install counts are adoption signals, not proof of output quality; the mechanisms below were accepted only when they addressed a failure observed in notebook generation.

## Sources inspected

| Public skill/project | Public signal at review time | Mechanism inspected | Decision |
|---|---:|---|---|
| [`karpathy/nanochat@read-arxiv-paper`](https://www.skills.sh/karpathy/nanochat/read-arxiv-paper) | 2.7K skills.sh installs | obtain arXiv TeX/source rather than relying only on PDF extraction | adopt source-role hierarchy while retaining PDF for visual/page anchors |
| [`yuan1z0825/nature-skills@nature-paper-card`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-paper-card) | 5.9K skills.sh installs | page/structure/source-limited grounding modes, claim–evidence matrix, machine audit | adopt grounding mode and contract validation; keep notebook-specific pedagogy and experiments |
| [`mizoreww/...@paper-reading`](https://github.com/Mizoreww/awesome-claude-code-config/blob/main/skills/paper-reading/SKILL.md) | 240 skills.sh installs | complete argument, module anatomy, official-code inspection, evidence coordinates | adopt paper/code labels and explicit missing fields; avoid mandatory HTML/SVG output |
| [`jxtse/scientific-research-skills@paper-reading`](https://github.com/jxtse/scientific-research-skills/tree/main/skills/paper-reading) | 80 skills.sh installs | multi-level reading and structured synthesis | adapt as three navigation lanes within one complete notebook |
| [`UCL-ERL paper-reading-card`](https://github.com/UCL-ERL/skills/blob/main/skills/research/paper-reading-card/SKILL.md) | public repository | bibliographic verification, safe/unsafe citation scope, `not found` discipline | adopt explicit non-implications and missing-evidence fields |
| [`fuxiao13/paper-reading-guide`](https://github.com/fuxiao13/paper-reading-guide/blob/main/SKILL.md) | public repository | three passes, checkpoints, formula/module selection, project connection | adapt checkpoints and project transfer; reject mandatory conversational pauses in an offline notebook |
| [`iagomsouza/adhd-paper-reader`](https://github.com/iagomsouza/adhd-paper-reader) | public repository | cognitive stop points, red flags, Feynman teach-back, reimplementation as a deliberate decision | adopt retrieval practice and red-flag audit; keep reproduction available when the user asks |
| [`ddhh-gif/paper-reading-skill`](https://github.com/ddhh-gif/paper-reading-skill/blob/main/SKILL.md) | public repository | idealization, variable typing, dimensional meaning, words between equations | adopt the equation-reading contract and executable sanity checks |

## v0.3 failure model

The previous skill strongly guarded length, figures, module explanations, toy-versus-reproduction boundaries, and execution. It could still pass a notebook that:

1. repeated abstract claims without first locating decisive evidence;
2. used a PDF as a monolithic source and lost TeX, supplement, version, or official-code facts;
3. presented equations without typed variables, assumptions, or limiting checks;
4. offered self-check questions that measured recognition rather than reconstruction;
5. described results in prose without a machine-auditable claim–evidence ledger.

## v0.4 acceptance decisions

The redesign therefore adds:

- a versioned source manifest and grounding mode;
- evidence-first triage before method exposition;
- a claim–evidence ledger with `supports`, `does_not_support`, and `missing` fields;
- load-bearing ablation and red-flag checks;
- paper/code crosswalk labels;
- three reader routes through one full notebook;
- typed-equation and executable sanity-check rules;
- Feynman/retrieval prompts and research continuation thresholds;
- a `--require-contract` validator that fails incomplete provenance, coverage, or evidence metadata.

Features not adopted include arbitrary fixed section counts for every paper type, decorative diagram quotas, mandatory HTML output, and mandatory interactive pauses. Those mechanisms conflict with paper-type adaptation or executable-notebook delivery.
