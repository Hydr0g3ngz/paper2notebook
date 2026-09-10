# Paper-type routing

Choose a primary route after reading the whole paper. A paper may have a secondary route, but one route should control the notebook's spine.

## Method or architecture paper

Use: problem → prior bottleneck → whole-system map → module contracts → objective/data flow → mechanism experiment → ablations → compute and failure modes.

Require a shape trace and a structure-faithful interface when code is appropriate. Do not confuse a skeleton forward pass with benchmark reproduction.

## Empirical or data-fidelity paper

Use: scientific question → controlled variables → data-generation conditions → measurement pipeline → decisive plots/tables → uncertainty → confounds → next discriminating experiment.

The central visual may be an experimental-design diagram rather than a network architecture. Recompute at least one reported quantity when the paper provides enough data.

## Evaluator or learned-metric paper

Use: what existing metrics miss → score semantics → annotation protocol → model inputs and information boundaries → training/evaluation metrics → correlation versus calibration → distribution shift and gaming risks.

Include a counterexample where a high aggregate correlation or score hides an important failure. Treat human ratings as measurements with uncertainty, not ground truth without noise.

## Benchmark or resource paper

Use: intended use → collection and filtering → splits → label process → leakage audit → baselines → valid and invalid comparisons → access/licensing → minimal loader or audit experiment.

## Theory paper

Use: motivating failure → definitions → assumptions → theorem dependency graph → proof intuition → boundary counterexample → numerical sanity check → what the theorem does not claim.

## Mixed papers

Name the primary and secondary routes near the top. Keep the primary claim in control. For example, a new evaluator with a new dataset is usually evaluator-first and resource-second; a standard model trained on a new simulator is empirical-first, not architecture-first.
