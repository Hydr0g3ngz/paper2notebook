# Depth contract

Depth is a user-facing product choice, not an accidental consequence of batch size or runtime pressure.

## Modes

### `survey`

Use only when the user asks for a quick overview, reading companion, or triage notebook. It may contain one mechanism demo and a compact evidence section. Label it as a survey.

### `full-onramp` — default

Build three connected passes:

1. **Field foundations** — enough signal processing, mathematics, representations, terminology, and prior paradigms that the paper is not the learner's first unexplained object.
2. **Paper reconstruction** — whole-system map, module contracts, realistic shapes/data flow, objective/training, structure-faithful implementation, mechanism experiments, source evidence, ablations, and failures.
3. **Research transition** — reproduction ladder, open questions, shortcut/confound audit, falsifiable extensions, and a practical first-week plan.

Use both implementation layers when code is appropriate: a structure-faithful teaching implementation and separate mechanism experiments. A forward-shape skeleton alone is not the first layer.

As a QA floor rather than a writing target, a typical full-onramp should have at least 28 cells, 8 substantive code cells, 12 heading cells, 7,000 Markdown characters, two source figures, and three executed visual/audio outputs. These floors prevent premature delivery; they do not justify filler.

### `reproduction`

Use when the user asks to reproduce results. In addition to `full-onramp`, match or explicitly account for dataset version/split, preprocessing, model configuration, optimizer/schedule, random seeds, checkpointing, metrics, compute budget, and expected deviations.

## Reference calibration

When the user identifies an earlier notebook as the quality/depth reference:

1. Profile it with `scripts/profile_notebook.py --output reference-profile.json` before generation. Treat this JSON as the frozen acceptance baseline; do not re-read a reference file that may change during a long task.
2. Inspect its narrative, experiment ladder, and code granularity; counts alone are insufficient.
3. For a comparable `full-onramp`, do not silently deliver less than 70% of its cell count, Markdown volume, or substantive code-cell count unless the paper type genuinely makes that dimension irrelevant. Explain any exception before delivery.
4. Compare section coverage and learner workload, not serialized file size or embedded-output size.

## Coverage blueprint gate

Before generating cells, record:

- learner starting point and final capability;
- primary/secondary paper route;
- 4–8 field-foundation lessons;
- whole-system and per-module lessons;
- shape/data-flow trace;
- objective/training lesson;
- at least three runnable experiments across Levels 0–2;
- source architecture/setup figure plus decisive evidence/ablation figures;
- evidence questions and limitations;
- research-transition exercises.

Do not start prose generation until the blueprint has all applicable items. In a batch, make one blueprint per paper.

## Honest self-evaluation

Score against the selected mode and any reference notebook. A polished survey is not a high-scoring full-onramp. Report missing reproduction elements separately from tutorial quality. Treat user feedback about insufficient depth as a failed scope gate, not a request to pad the existing artifact.
