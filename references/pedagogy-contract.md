# Pedagogy contract

## Contents

1. Learner model
2. Required narrative
3. Module explanation template
4. Experiment ladder
5. Failure patterns learned from practice

## 1. Learner model

Assume the learner has basic programming, linear algebra, and general neural-network familiarity unless the user says otherwise. Do not assume field-specific representations, metrics, datasets, or conventions.

State prerequisites explicitly. Introduce no acronym before its first-use expansion. Define each tensor axis, not only its rank.

## 2. Required narrative

Use this default sequence, adapting only when the paper genre requires it:

1. Why the real-world problem matters.
2. Formal input, desired output, assumptions, and why the problem is difficult.
3. The dominant previous approach as an analysis-allocation-synthesis or hypothesis-test pipeline.
4. A concrete failure demonstration of the previous approach.
5. The paper's thesis in one sentence.
6. A whole-system map before any implementation.
7. One module at a time, each derived from a need.
8. A full shape trace through a realistic paper configuration.
9. Objective, ambiguity handling, and training loop.
10. A minimal experiment, then the paper's actual evidence.
11. Limitations, failure cases, and research map.

## 3. Module explanation template

For every central module, answer in this order:

### Purpose

Name the specific upstream difficulty. Avoid empty descriptions such as “extracts features.”

### Interface

Give mathematical symbols, concrete example shapes, axis meanings, units, stride, padding, and causality where relevant.

### Mechanism

Give the shortest sufficient equation, a plain-language mental model, and a tiny numerical or visual example.

### Design choice

Compare the selected design with the closest alternative used in the paper or field. Explain the tradeoff rather than declaring one universally better.

### Evidence and failure

Connect to a paper ablation, a counterexample, or an executable switch. State what failure is expected if the component is removed.

## 4. Experiment ladder

Separate these levels visibly:

- Level 0 - sanity check: shapes, invariances, reconstruction, or a tiny hand calculation.
- Level 1 - mechanism demo: synthetic or tiny data that isolates one idea.
- Level 2 - teaching model: structure-faithful but scaled down.
- Level 3 - paper reproduction: matching dataset, split, preprocessing, optimizer, budget, metric, and seeds.
- Level 4 - research extension: one falsifiable hypothesis and controlled ablation.

Never label Levels 0-2 as a reproduction.

## 5. Failure patterns learned from practice

- Code-first notebooks force readers to reverse-engineer motivation.
- An architecture box diagram without shapes and axis meanings creates false familiarity.
- Listing component names does not explain why the architecture has that form.
- A toy dataset can introduce an easy shortcut and make the model look more capable than it is.
- Showing only training curves hides whether outputs are meaningful; include qualitative inspection.
- Quoting headline metrics without explaining the baseline or oracle leads to incorrect claims.
- A pasted source figure without a reading guide is usually skipped.
- A notebook that has never run from a fresh kernel is not a deliverable.
