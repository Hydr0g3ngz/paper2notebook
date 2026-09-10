# Source-figure workflow

## Contents

1. Select figures
2. Extract safely
3. Place and explain
4. Validate

## 1. Select figures

Inventory every figure and table before selecting. Score candidates by whether they answer one of these questions:

- What is the complete architecture or experimental setup?
- What happens inside the novel module?
- What is the decisive comparison supporting the main claim?
- What ablation explains a design choice?
- What failure case or learned representation changes interpretation?

For a method paper, normally include:

1. the main architecture/algorithm figure;
2. one internal-module or learned-representation figure if useful;
3. one decisive result or ablation figure/table.

Avoid decorative photos, redundant plots, unreadable multi-panel composites, and large result tables that are clearer when transcribed selectively.

## 2. Extract safely

Use only user-provided or lawfully accessible sources. Render the source PDF page, inspect it visually, and crop tightly enough to keep all panel labels, legends, axes, and caption text needed for interpretation. Prefer 180-220 dpi PNG for notebooks.

Use:

```powershell
python scripts/extract_pdf_figure.py --input paper.pdf --page 3 --bbox 0.04,0.04,0.96,0.46 --output assets/fig1_architecture.png
```

The bounding box uses normalized page coordinates `left,top,right,bottom`. Inspect the result; adjust rather than accepting an automatic crop blindly.

Do not alter scientific content. Permitted edits are crop, uniform scale, whitespace removal, and clearly disclosed panel extraction. Do not erase labels or recombine panels in ways that change meaning.

## 3. Place and explain

Place each source figure immediately before or after its first substantive explanation. Use this block:

```markdown
### Original paper Figure 1 - [descriptive title]

![Original paper Figure 1](assets/fig1_architecture.png)

**Source:** Figure 1, PDF p.3, [full citation]. Crop from the user-provided PDF.

**Why it is here:** [the one question this figure answers]

**How to read it:**
1. Start at [...].
2. Follow [...].
3. Compare [...].

**Key inference:** [claim supported by the figure].

**Do not over-interpret:** [claim the figure does not establish].
```

Follow the source figure with a simplified original diagram when the paper figure assumes too much background. Label the new diagram “teaching schematic,” not “paper figure.”

## 4. Validate

- Open every crop at native resolution.
- Confirm figure number and PDF page.
- Confirm axes, panel labels, legends, equations, and captions are legible.
- Confirm relative links resolve from the notebook directory.
- Confirm the explanation names every panel actually used.
- Confirm the notebook can still be shared with an `assets/` directory or embeds images intentionally.
