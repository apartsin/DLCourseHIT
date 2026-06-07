# Introduction to Deep Learning (HIT)

**DL 201 · Foundation course · 13 weeks · PyTorch**

Foundations of neural networks: framing a task in tensor terms, then building, training, and
debugging networks in PyTorch. This is the foundation deep-learning course in the program and the
bridge to the advanced electives in **Large Language Models** and **Computer Vision**.

- **Prerequisite:** Introduction to Machine Learning
- **Leads to:** Advanced LLMs · Advanced Computer Vision
- **Format:** 3 h lecture + 2 h exercise lab per week
- **Assessment:** project- and exercise-based (no written exams)

**Course site (GitHub Pages):** https://apartsin.github.io/DLCourseHIT/

## Syllabus

- [HTML](syllabus/syllabus.html) · [Word (.docx)](syllabus/syllabus.docx) · [PDF](syllabus/syllabus.pdf)

## Working with Claude (the exercise model)

Every week is built for the way students actually work, with an AI coding assistant at hand.
Each lab and notebook has three parts:

1. **Build** (Claude welcome): produce working code that meets a spec or hits a target metric.
2. **Predict & probe** (your reasoning): predict outcomes before running, then run controlled experiments.
3. **Explain & defend** (in plain language): explain why it works, where it breaks, and what changed.

Grading weight sits on **Predict** and **Explain**, the parts an AI assistant cannot do for the student.

## Weekly materials

Each week has a **lab** handout (with self-check questions), a **reference page** of curated free
sources, an instructor **lesson plan** (3 h lecture + 2 h practice), and a Colab **notebook**.

| Wk | Topic | Materials |
|----|-------|-----------|
| | **Part I · Foundations** | |
| 1 | Deep Learning Overview & ML-to-Network Framing | [Lab](labs/week01.html) · [Refs](references/week01.html) · [Lesson](lessons/week01.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week01.ipynb) |
| 2 | Tensors & Data Representation | [Lab](labs/week02.html) · [Refs](references/week02.html) · [Lesson](lessons/week02.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week02.ipynb) |
| 3 | MLPs & Backpropagation | [Lab](labs/week03.html) · [Refs](references/week03.html) · [Lesson](lessons/week03.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week03.ipynb) |
| | **Part II · Training Infrastructure** | |
| 4 | Data Pipelines | [Lab](labs/week04.html) · [Refs](references/week04.html) · [Lesson](lessons/week04.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week04.ipynb) |
| 5 | Loss Functions & Metrics | [Lab](labs/week05.html) · [Refs](references/week05.html) · [Lesson](lessons/week05.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week05.ipynb) |
| 6 | Optimization | [Lab](labs/week06.html) · [Refs](references/week06.html) · [Lesson](lessons/week06.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week06.ipynb) |
| 7 | Regularization & Generalization | [Lab](labs/week07.html) · [Refs](references/week07.html) · [Lesson](lessons/week07.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week07.ipynb) |
| | **Part III · Architectures & Representation Learning** | |
| 8 | Convolutional Networks I | [Lab](labs/week08.html) · [Refs](references/week08.html) · [Lesson](lessons/week08.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week08.ipynb) |
| 9 | Convolutional Networks II | [Lab](labs/week09.html) · [Refs](references/week09.html) · [Lesson](lessons/week09.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week09.ipynb) |
| 10 | Recurrent Networks (RNNs) | [Lab](labs/week10.html) · [Refs](references/week10.html) · [Lesson](lessons/week10.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week10.ipynb) |
| 11 | LSTMs, GRUs & Sequence Tasks | [Lab](labs/week11.html) · [Refs](references/week11.html) · [Lesson](lessons/week11.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week11.ipynb) |
| 12 | Representation Learning | [Lab](labs/week12.html) · [Refs](references/week12.html) · [Lesson](lessons/week12.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week12.ipynb) |
| | **Part IV · Integration** | |
| 13 | Integration & Transfer Learning | [Lab](labs/week13.html) · [Refs](references/week13.html) · [Lesson](lessons/week13.html) · [Notebook](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week13.ipynb) |

> The `.html` pages render best via the GitHub Pages site above. The notebook links open directly in
> Google Colab.

## Repository layout

```
index.html            Course home (links every week's lab, references, lesson plan, notebook)
syllabus/             Syllabus in HTML, Word, and PDF
labs/                 week01..week13 student lab handouts (with self-check questions)
references/           week01..week13 curated reference pages
lessons/              week01..week13 instructor lesson plans (lecture + practice)
notebooks/            week01..week13 Colab-ready practice notebooks
prereq/               Math, Python, and ML prerequisite review pages
projects/             Example briefs: 10 mid-term + 10 final projects
hit-catalogue/        HIT submission package (EN + HE syllabus, rationale, summary, questionnaire)
assets/style.css      Shared house style
tools/                Generators: build_site.py, build_notebooks.py, build_hit_package.py, content.py, refs.json, lessons.py, selfcheck.py
```

## Building

```bash
python tools/build_site.py          # index + labs + references + lessons
python tools/build_notebooks.py     # Colab notebooks
python tools/build_hit_package.py   # HIT catalogue .docx package
```

The syllabus (`syllabus/`) is maintained from `syllabus/syllabus.html` as the source of truth; the
Word and PDF versions are regenerated from it.

## HIT catalogue package

`hit-catalogue/` holds the department submission package in the HIT form: English syllabus, Hebrew
syllabus, rationale, catalogue summary, and committee questionnaire.

## Status

Complete: syllabus, 13 lab handouts with self-check questions, 13 reference pages, 13 instructor
lesson plans, 13 Colab notebooks, and the HIT catalogue package. Lab starter solutions will be added
over the term.
