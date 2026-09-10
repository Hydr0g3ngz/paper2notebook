# paper2notebook

`paper2notebook` is a Codex skill for turning a research paper into a self-contained, executable Jupyter Notebook that teaches both the paper and its research direction from first principles.

It is designed for readers who know basic programming, linear algebra, and machine learning but are new to the paper's field.

## What it enforces

- Explain the real problem and prior paradigm before presenting model code.
- Derive each important module from the problem it solves.
- Document tensor shapes, equations, design alternatives, and ablation evidence.
- Include useful original-paper figures with figure number, page, provenance, reading order, and interpretation limits.
- Separate sanity checks, toy experiments, teaching-scale implementations, paper reproduction, and research extensions.
- Execute the notebook from a fresh kernel and validate local image links before delivery.

## Structure

```text
paper2notebook/
├── SKILL.md
├── references/
│   ├── pedagogy-contract.md
│   ├── figure-workflow.md
│   └── notebook-qa.md
└── scripts/
    ├── scaffold_notebook.py
    ├── extract_pdf_figure.py
    └── validate_notebook.py
```

## Installation

Clone the repository into your Codex skills directory:

```powershell
git clone https://github.com/Hydr0g3ngz/paper2notebook.git "$env:USERPROFILE\.codex\skills\paper2notebook"
```

Restart Codex if the skill is not discovered immediately.

## Example requests

- “把这篇论文做成一个从零入门、可运行的 Notebook。”
- “Use paper2notebook to explain this architecture and its research direction.”
- “Turn this PDF into an explorable paper tutorial with the useful original figures.”

## Helper scripts

Create a notebook outline:

```powershell
python scripts/scaffold_notebook.py --title "Paper title" --citation "Authors (Year)" --output tutorial.ipynb
```

Crop a figure from a PDF using normalized page coordinates:

```powershell
python scripts/extract_pdf_figure.py --input paper.pdf --page 3 --bbox 0.04,0.05,0.96,0.45 --output assets/figure.png
```

Validate an executed notebook:

```powershell
python scripts/validate_notebook.py tutorial.ipynb --require-executed
```
