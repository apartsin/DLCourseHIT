# -*- coding: utf-8 -*-
"""Generate per-week Colab-ready PRACTICE notebooks under notebooks/weekNN.ipynb.
These are for the instructor to run during the 2-hour practice lesson: each carries an
Open-in-Colab badge and one section per live demonstration. The student homework is the lab."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import COURSE, PARTS, WEEKS
from notebook_code import NB

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
        f'**Instructor practice notebook** for the 2-hour practice lesson. Work through the sections below '
        f'live, running each cell and trying the variations. The student homework is the weekly lab.'
    ))
    cells.append(md("### Goals\n\n" + "\n".join(f"- {g}" for g in w["goals"])))
    cells.append(md("### Setup\nRun this first. On Colab, set Runtime > Change runtime type > GPU for the later weeks."))
    cells.append(code(
        "import torch\n"
        "import torch.nn as nn\n"
        "import torch.nn.functional as F\n"
        "import matplotlib.pyplot as plt\n\n"
        "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n"
        "torch.manual_seed(0)\n"
        "print('PyTorch', torch.__version__, '| device:', device)"
    ))
    for kind, text in NB.get(n, []):
        cells.append(md(text) if kind == "md" else code(text))
    cells.append(md(
        f"---\nStudent materials for this week: the lab handout (`labs/{w2(n)}.html`) and the curated "
        f"references (`references/{w2(n)}.html`) in the course site."))
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
