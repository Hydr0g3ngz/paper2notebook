# Reading lanes, equations, and retrieval practice

## 1. Three lanes through one notebook

Place a short navigation block near the top. It should link to sections rather than duplicate summaries.

- **3-minute map:** problem, thesis, whole-system figure, decisive result, strongest limitation.
- **Deep-reading path:** prerequisites, previous paradigm, module derivation, equations, shapes, training, evidence.
- **Research/reproduction path:** source manifest, paper/code crosswalk, reproduction boundary, ablations, open questions, first experiment.

Add optional stop markers after the problem map, architecture map, and evidence audit. At each marker, give one retrieval question and the section to revisit if the answer is unclear. Do not interrupt a notebook with mandatory conversational pauses.

## 2. Equation reading contract

For every load-bearing equation:

1. State why the equation is needed and which problem choice it formalizes.
2. Define every symbol, index, operator, and set. Include type/domain, concrete shape, units when meaningful, observability, and whether it is learned or fixed.
3. Explain the assumption or idealization that made this formulation possible.
4. Explain what changed from the previous equation; do not omit the prose between equations.
5. Give a plain-language causal or geometric interpretation.
6. Check at least one of: dimensions/units, limiting case, invariance/equivariance, range, sign, conservation, or a tiny numerical example.
7. Show where the equation appears in code and flag any implementation approximation.

For theory papers, additionally map theorem dependencies, assumption use, proof strategy, and a counterexample when an assumption is removed.

## 3. Retrieval instead of recognition

End major conceptual arcs with questions that require reconstruction rather than copying a sentence:

- Draw the system from memory and label interfaces.
- Predict the failure when one component is removed before revealing the ablation.
- Explain the strongest claim, its evidence, and the closest stronger claim that is not established.
- Change one assumption and predict which equation, module, or metric breaks first.
- Teach the paper in five sentences without using its module names as unexplained nouns.

Provide compact answer checkpoints after sufficient spacing, for example in collapsed HTML details or a later answer section. Include 5–12 durable flashcard-style prompts for a full-onramp; avoid trivia about author names or isolated metric digits.

## 4. Transfer to a research decision

Conclude with four explicit judgments:

- what is reusable as a representation, objective, module, dataset practice, or evaluation idea;
- what depends on fragile assumptions or unavailable resources;
- the cheapest experiment that could falsify the most interesting extension;
- the evidence threshold that would justify continuing beyond the first experiment.

This converts reading into a research decision without pretending that every paper deserves reproduction.
