# Introduction to Deep Learning (HIT)

**DL 201 · Foundation course · 13 weeks · PyTorch**

Foundations of neural networks: framing a task in tensor terms, then building, training, and
debugging networks in PyTorch. This is the foundation deep-learning course in the program and the
bridge to the advanced electives in **Large Language Models** and **Computer Vision**.

- **Prerequisite:** Introduction to Machine Learning
- **Leads to:** Advanced LLMs · Advanced Computer Vision
- **Format:** 3 h lecture + 2 h practice lesson per week (+ a homework lab)
- **Assessment:** project- and lab-based (no written exams)

**Each week has three parts:** a **lecture** (theory), an instructor-led **practice lesson** (live
implementation and worked examples), and a **lab** set as homework (the graded Build/Predict/Explain work).

**Course site (GitHub Pages):** https://apartsin.github.io/DLCourseHIT/

## Syllabus

- [HTML](syllabus/syllabus.html) · [Word (.docx)](syllabus/syllabus.docx) · [PDF](syllabus/syllabus.pdf)

## Working with an AI assistant (the lab model)

The weekly lab (homework) is built for the way students actually work, with an AI coding assistant at hand.
Each lab has three parts:

1. **Build** (AI assistant welcome): produce working code that meets a spec or hits a target metric.
2. **Predict & probe** (the reasoning step): predict outcomes before running, then run controlled experiments.
3. **Explain & defend** (in plain language): explain why it works, where it breaks, and what changed.

Grading weight sits on **Predict** and **Explain**, the parts an AI assistant cannot do for the student.

## Weekly materials

Each week has a **lab** handout (with self-check questions), a **reference page** of curated free
sources, an instructor **lesson plan** (3 h lecture + 2 h practice), and a Colab **practice notebook**.

| Wk | Topic | Materials |
|----|-------|-----------|
| | **Part I · Foundations** | |
| 1 | Deep Learning Overview & ML-to-Network Framing | [Lesson](lessons/week01.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week01.ipynb) · [Self-check](labs/week01.html#self-check) · [Homework lab](labs/week01.html) |
| 2 | Tensors & Data Representation | [Lesson](lessons/week02.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week02.ipynb) · [Self-check](labs/week02.html#self-check) · [Homework lab](labs/week02.html) |
| 3 | MLPs & Backpropagation | [Lesson](lessons/week03.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week03.ipynb) · [Self-check](labs/week03.html#self-check) · [Homework lab](labs/week03.html) |
| | **Part II · Training Infrastructure** | |
| 4 | Data Pipelines | [Lesson](lessons/week04.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week04.ipynb) · [Self-check](labs/week04.html#self-check) · [Homework lab](labs/week04.html) |
| 5 | Loss Functions & Metrics | [Lesson](lessons/week05.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week05.ipynb) · [Self-check](labs/week05.html#self-check) · [Homework lab](labs/week05.html) |
| 6 | Optimization | [Lesson](lessons/week06.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week06.ipynb) · [Self-check](labs/week06.html#self-check) · [Homework lab](labs/week06.html) |
| 7 | Regularization & Generalization | [Lesson](lessons/week07.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week07.ipynb) · [Self-check](labs/week07.html#self-check) · [Homework lab](labs/week07.html) |
| | **Part III · Architectures & Representation Learning** | |
| 8 | Convolutional Networks I | [Lesson](lessons/week08.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week08.ipynb) · [Self-check](labs/week08.html#self-check) · [Homework lab](labs/week08.html) |
| 9 | Convolutional Networks II | [Lesson](lessons/week09.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week09.ipynb) · [Self-check](labs/week09.html#self-check) · [Homework lab](labs/week09.html) |
| 10 | Recurrent Networks (RNNs) | [Lesson](lessons/week10.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week10.ipynb) · [Self-check](labs/week10.html#self-check) · [Homework lab](labs/week10.html) |
| 11 | LSTMs, GRUs & Sequence Tasks | [Lesson](lessons/week11.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week11.ipynb) · [Self-check](labs/week11.html#self-check) · [Homework lab](labs/week11.html) |
| 12 | Representation Learning | [Lesson](lessons/week12.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week12.ipynb) · [Self-check](labs/week12.html#self-check) · [Homework lab](labs/week12.html) |
| | **Part IV · Integration** | |
| 13 | Integration & Transfer Learning | [Lesson](lessons/week13.html) · [Practice nb](https://colab.research.google.com/github/apartsin/DLCourseHIT/blob/main/notebooks/week13.ipynb) · [Self-check](labs/week13.html#self-check) · [Homework lab](labs/week13.html) |

> The `.html` pages render best via the GitHub Pages site above. The notebook links open directly in
> Google Colab.

## Repository layout

```
index.html            Course home (links every week's lab, references, lesson plan, notebook)
syllabus/             Syllabus in HTML, Word, and PDF
labs/                 week01..week13 student lab handouts (with self-check questions)
references/           week01..week13 curated reference pages
lessons/              week01..week13 instructor lesson plans (lecture + practice)
notebooks/            week01..week13 Colab practice notebooks (instructor, run during the practice lessons)
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
