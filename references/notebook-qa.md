# Notebook QA

## Structural checks

- Include a three-lane navigation block: 3-minute map, deep-reading path, and research/reproduction path.
- Record the source/version manifest and distinguish paper, supplement, official code, and external background.
- State learner assumptions, outcomes, and reproduction boundary near the top.
- Define the task before presenting the architecture.
- Introduce the previous paradigm and its bottleneck before the paper's solution.
- Include a whole-system map and per-module explanations.
- Include a realistic tensor-shape or data-flow trace.
- Explain the objective and ambiguity/alignment rules.
- Distinguish toy evidence from paper evidence.
- Include limitations, common misconceptions, self-checks, and next experiments.
- Include a claim-evidence ledger and delayed answer checkpoints for retrieval/teach-back questions.

## Execution checks

1. Restart the kernel and execute all cells in order.
2. Require zero error outputs.
3. Check deterministic seeds where practical.
4. Keep the default run reasonable on CPU; mark optional expensive cells.
5. Avoid hidden state, undeclared files, network-only dependencies, and silent downloads.
6. Inspect numerical outputs for invariants and plausible ranges.
7. Include dependency fallbacks or a clear setup cell.

Run:

```powershell
python scripts/validate_notebook.py path/to/notebook.ipynb --require-executed --depth-mode full-onramp --reference-profile reference-profile.json
```

## Visual checks

- Open the executed notebook or render it to HTML.
- Inspect all paper-figure crops at native resolution.
- Check plots for clipped titles, missing units, unreadable legends, misleading axes, and overlapping text.
- Check for tofu boxes or missing glyphs. When the environment lacks a reliable CJK font, use English labels inside generated plots and keep the surrounding Markdown explanation in the user's language.
- Check Markdown equations, tables, local links, audio widgets, and long outputs.
- Prefer a few purposeful visuals over repeated waveform or loss plots.

## Scientific checks

- Tie claims to the source figure, equation, section, or table.
- Treat abstract statements as claims awaiting evidence, not as findings by themselves.
- Verify the load-bearing ablation or state that the paper did not report one.
- Label implementation facts as paper-stated, code-confirmed, discrepant, or teaching inference.
- Mark interpretations and teaching simplifications.
- Define the baseline and oracle precisely before saying “better.”
- State what each major experiment supports and does not prove.
- List data shortcuts, leakage risks, evaluation caveats, and excluded real-world conditions.
- Never claim successful reproduction from architecture similarity alone.

## Delivery checks

- Deliver the executed `.ipynb` and its required `assets/` directory, or embed small images as notebook attachments. Test the notebook from its delivered location.
- Keep filenames stable and descriptive.
- Mention runtime, important optional dependencies, and restricted-data boundaries.
- Link directly to the local notebook and any packaged skill artifact.
