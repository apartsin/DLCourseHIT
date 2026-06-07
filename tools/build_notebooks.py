# -*- coding: utf-8 -*-
"""Generate per-week Colab-ready practice notebooks under notebooks/weekNN.ipynb.
Each notebook carries an Open-in-Colab badge and the Build / Predict & probe /
Explain & defend scaffolding, mirroring the lab pages."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import COURSE, PARTS, WEEKS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "apartsin/DLCourseHIT"
BRANCH = "main"

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}
def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text}
def w2(n): return f"week{n:02d}"

def colab_url(n):
    return f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/notebooks/{w2(n)}.ipynb"

def bullets(items): return "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1))

def notebook(w):
    n = w["num"]
    cells = []
    cells.append(md(
        f'[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(n)})\n\n'
        f'# Week {n}: {w["title"]}\n'
        f'**{COURSE["title"]} (HIT)** &middot; Part {w["part"]}: {PARTS[w["part"]]}\n\n'
        f'{w["sub"]}\n\n'
        f'This is the weekly lab notebook (homework). It follows the course\'s **Build / Predict & probe / Explain & defend** '
        f'model. Use an AI assistant freely for the Build; the graded learning is in Predict and Explain.'
    ))
    cells.append(md("## Goals\n\n" + "\n".join(f"- {g}" for g in w["goals"])))
    cells.append(md("## Setup\nRun this first. On Colab, set Runtime > Change runtime type > GPU for the later weeks."))
    cells.append(code(
        "import torch\n"
        "import torch.nn as nn\n"
        "import torch.nn.functional as F\n"
        "import matplotlib.pyplot as plt\n\n"
        "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n"
        "torch.manual_seed(0)\n"
        "print('PyTorch', torch.__version__, '| device:', device)"
    ))
    cells.append(md("## Part A: Build  *(AI assistant welcome)*\n\n" + bullets(w["build"])))
    cells.append(code("# Your build code here.\n"))
    cells.append(md(
        "## Part B: Predict & probe  *(your reasoning)*\n\n"
        "Before running experiments, write your predictions, then test them.\n\n" + bullets(w["predict"])))
    cells.append(md("**Your predictions (write before running):**\n\n- ...\n"))
    cells.append(code("# Experiments to test your predictions.\n"))
    cells.append(md(
        "## Part C: Explain & defend  *(in plain language)*\n\n" + bullets(w["explain"]) +
        "\n\n**Your explanation:**\n\n_Write here. You must be able to defend any line you submit._"))
    cells.append(md(
        "## Deliverables\n\n" + "\n".join(f"- [ ] {d}" for d in w["deliverables"]) +
        f"\n\n---\nLab page and curated references for this week: "
        f"`labs/{w2(n)}.html` and `references/{w2(n)}.html` in the course site."))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
            "colab": {"name": f'{w2(n)}.ipynb', "provenance": []},
            "accelerator": "GPU",
        },
        "nbformat": 4, "nbformat_minor": 5,
    }

def main():
    out = os.path.join(ROOT, "notebooks")
    os.makedirs(out, exist_ok=True)
    for w in WEEKS:
        with open(os.path.join(out, f'{w2(w["num"])}.ipynb'), "w", encoding="utf-8") as f:
            json.dump(notebook(w), f, ensure_ascii=False, indent=1)
    print(f"generated {len(WEEKS)} notebooks in notebooks/")

if __name__ == "__main__":
    main()
