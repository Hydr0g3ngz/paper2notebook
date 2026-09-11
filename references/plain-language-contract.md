# Plain-language teaching contract

Plain language is not shorter jargon. It gives the reader enough intermediate steps to build the right mental model without weakening the science.

## 1. Model the reader explicitly

Record three lists before outlining:

- `prior_knowledge`: ideas the notebook may use without reteaching;
- `not_assumed`: field-specific ideas that must be introduced;
- `target_capabilities`: observable actions such as explain, draw, predict, implement, compare, or critique.

Avoid outcomes such as “understand the model.” Prefer “predict how the receptive field changes when dilation doubles” or “trace one sample through encoder, separator, and decoder.”

## 2. Build a concept dependency map

Introduce concepts in dependency order. Each central concept needs a bridge with:

1. **reader question** — the concrete question now blocking progress;
2. **familiar start** — a phenomenon, prior concept, or small worked example already available to the reader;
3. **plain mechanism** — what changes, what information moves, and why that helps, without using the new term as its own definition;
4. **canonical term** — Chinese description plus the field's English term at first use;
5. **formal anchor** — equation, tensor shape, algorithm step, or source figure;
6. **observable anchor** — code output, plot, audio, table, or hand calculation the reader can inspect;
7. **failure boundary** — where the intuition, analogy, or method stops being reliable.

Do not ask the reader to hold more than two unexplained new concepts at once. If a sentence needs three unfamiliar nouns, split the dependency chain and add an example before continuing.

## 3. Use the explanation ladder

For a difficult mechanism, use this order unless the learner model justifies skipping a rung:

`concrete situation -> question -> prediction -> plain mechanism -> term -> visual or toy numbers -> formalism -> code -> observed result -> paper implication`

“Concrete before abstract” does not mean dumping code first. The reader should know what the cell is testing before running it.

### Before a code cell

State:

- the single question this cell answers;
- which quantity or behavior to watch;
- the predicted outcome and the reason for that prediction.

### After a code cell

State:

- what was observed, using an actual value, shape, curve region, image feature, or audible difference;
- why it happened;
- what it establishes and what it does not establish about the paper.

Never leave a plot, tensor printout, audio widget, or metric table to “speak for itself.”

## 4. Define instead of renaming

Bad explanations attach a familiar verb to an unexplained noun: “the encoder extracts features,” “attention captures dependencies,” or “normalization improves stability.” These sentences are labels, not mechanisms.

Use the noun-replacement test. Replace the model or module name with “this box.” A useful explanation still states:

- what arrives;
- what operation or comparison occurs;
- what changes in the representation;
- what downstream decision becomes easier;
- what information may be lost.

Expand acronyms and define technical terms inline on first use. Keep one stable name afterward. Do not exile definitions to a glossary that the reader must repeatedly search.

## 5. Use analogies with a map and a break

Use an analogy only when it removes a real comprehension bottleneck. Immediately state:

- **map:** which parts of the analogy correspond to which mathematical or computational objects;
- **break:** the first important way the analogy is false or incomplete.

An analogy is a temporary bridge to the mechanism, not evidence and not a replacement for shapes or equations. Prefer small numerical examples when an analogy would introduce a second story the reader must remember.

## 6. Make prose easy to parse

- Put the answer or causal claim at the start of the paragraph; follow with evidence and qualification.
- Keep one main idea per paragraph and one conceptual jump per Markdown cell.
- Prefer subjects that perform visible actions: “the mask multiplies each encoded channel” over “masking is performed.”
- Remove filler such as “值得注意的是”, “众所周知”, “显而易见”, “不难发现”, and ceremonial section previews.
- Use lists for parallel items and numbered lists only for genuine sequences.
- Use descriptive headings that answer a question or state a conclusion; avoid bare headings such as “背景”, “方法”, or “结果”.
- Preserve necessary uncertainty. Replace vague hedging with the exact condition or missing evidence.

Sentence-length scores designed for English public prose are diagnostics, not scientific truth and do not transfer cleanly to Chinese. Prefer dependency clarity, concrete referents, and read-aloud inspection over optimizing one readability number.

## 7. Test understanding, not recognition

Use prediction and reconstruction prompts:

- predict an ablation before showing its result;
- draw the data flow from memory;
- explain a module without using its name;
- contrast two easily confused concepts on the same example;
- diagnose a deliberately wrong shape, assumption, or result;
- change one condition and predict what fails first.

Place answers later or in collapsed details. A nearby answer turns retrieval into recognition.

## 8. Comprehension audit

Before delivery, inspect each major section with these tests:

1. **Prerequisite test:** every concept used was introduced earlier or declared as prior knowledge.
2. **Noun-replacement test:** explanations survive removal of branded module names.
3. **Referent test:** pronouns such as “它/这/该模块” have one unambiguous referent.
4. **Example test:** every central abstraction has a worked number, shape, visual, audio, or counterexample.
5. **Output test:** every substantive output is interpreted in prose.
6. **Compression test:** remove filler and repetition, but restore any causal step whose removal makes the reasoning jump.
7. **Teach-back test:** the supplied answer explains why, not merely repeats terminology.

When an explanation fails, narrow to the first missing dependency. Do not respond by adding a longer summary after the difficult section.
