# -*- coding: utf-8 -*-
"""Generate the DLCourseHIT site: index.html + labs/weekNN.html + references/weekNN.html
from content.py (lab handouts) and refs.json (scouted references). Shared CSS in assets/style.css."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import COURSE, PARTS, WEEKS
from lessons import LESSONS, PRACTICE, PEDAGOGY
from selfcheck import SELFCHECK
from prereq import PREREQ, ORDER as PREREQ_ORDER
from projects import PROJECTS, ORDER as PROJECTS_ORDER

OUTCOMES = [
    ("&#127919;", "Frame ML tasks as networks (tensors in, a loss out)."),
    ("&#129518;", "Represent data as tensors and use them fluently."),
    ("&#128256;", "Build data pipelines with Dataset and DataLoader."),
    ("&#128201;", "Use automatic differentiation to compute gradients."),
    ("&#129504;", "Implement neural networks in PyTorch."),
    ("&#9881;&#65039;", "Reason about optimization (SGD, Adam, learning rates)."),
    ("&#129658;", "Diagnose training issues (overfitting, instability)."),
    ("&#127959;&#65039;", "Build MLPs, CNNs, RNNs, LSTMs/GRUs, and autoencoders."),
    ("&#129516;", "Apply representation learning and transfer learning."),
    ("&#128279;", "Carry a transferable base into advanced LLM and vision courses."),
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)

REFS = json.load(open(P("tools", "refs.json"), encoding="utf-8"))

REPO, BRANCH = "apartsin/DLCourseHIT", "main"
def colab_url(n): return f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/notebooks/week{n:02d}.ipynb"

def esc(s): return html.escape(str(s), quote=True)
def dom(url):
    h = url.split("://", 1)[-1].split("/", 1)[0]
    return h[4:] if h.startswith("www.") else h
def w2(n): return f"week{n:02d}"

def topnav(depth):
    up = "../" if depth else ""
    return (f'<div class="topnav"><div class="inner">'
            f'<a class="brand" href="{up}index.html">Introduction to Deep Learning <span>&middot; HIT</span></a>'
            f'<nav><a href="{up}index.html">Home</a>'
            f'<a href="{up}prereq/index.html">Prerequisites</a>'
            f'<a href="{up}index.html#weekly">Weekly materials</a>'
            f'<a href="{up}projects/index.html">Projects</a></nav></div></div>')

def page(title, depth, inner):
    css = ("../" if depth else "") + "assets/style.css"
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><link rel="stylesheet" href="{css}"></head><body>'
            f'{topnav(depth)}<div class="wrap">{inner}</div>'
            f'<footer>Introduction to Deep Learning &middot; HIT &middot; Foundation Course &middot; course materials</footer>'
            f'</body></html>')

def li(items): return "".join(f"<li>{esc(x)}</li>" for x in items)

def pager(kind, w):
    n = w["num"]
    prev = next((x for x in WEEKS if x["num"] == n - 1), None)
    nxt = next((x for x in WEEKS if x["num"] == n + 1), None)
    L = ""
    if prev:
        L += (f'<a href="{w2(prev["num"])}.html"><span class="lbl">Previous</span>'
              f'Week {prev["num"]}: {esc(prev["title"])}</a>')
    if nxt:
        L += (f'<a class="nx" href="{w2(nxt["num"])}.html"><span class="lbl">Next</span>'
              f'Week {nxt["num"]}: {esc(nxt["title"])}</a>')
    return f'<div class="pager">{L}</div>'

def whead(w):
    return (f'<div class="whead">'
            f'<p class="eyebrow"><span class="wbadge">Week {w["num"]}</span> &nbsp; Part {w["part"]} &middot; {esc(PARTS[w["part"]])}</p>'
            f'<h1>{esc(w["title"])}</h1><p class="sub">{esc(w["sub"])}</p></div>')

def lab_html(w):
    steps = (
        f'<div class="step a"><h3><span class="tag">Part A &middot; AI assistant welcome</span>Build</h3><ol>{li(w["build"])}</ol></div>'
        f'<div class="step b"><h3><span class="tag">Part B &middot; student reasoning</span>Predict &amp; probe</h3><ol>{li(w["predict"])}</ol></div>'
        f'<div class="step c"><h3><span class="tag">Part C &middot; in plain language</span>Explain &amp; defend</h3><ol>{li(w["explain"])}</ol></div>'
    )
    inner = (
        whead(w)
        + f'<div class="goals"><h2>Learning goals</h2><ul class="clean">{li(w["goals"])}</ul></div>'
        + '<div class="callout">This is the weekly <b>homework lab</b>, completed independently after the lecture and the practice lesson. '
          'It follows the course\'s <b>Build / Predict &amp; probe / Explain &amp; defend</b> model: '
          'use an AI assistant freely for the Build; the graded learning is in Predict and Explain. '
          'See the <a href="../index.html#ai-usage">AI-use policy</a> and a '
          '<a href="../sample-submission.html">fully worked sample submission</a>.</div>'
        + '<h2><span class="ic">&#9881;</span>Exercise</h2>' + f'<div class="steps">{steps}</div>'
        + '<h2><span class="ic">&#10003;</span>Deliverables</h2>' + f'<ul class="clean">{li(w["deliverables"])}</ul>'
        + f'<div class="callout hint"><b>Hints.</b><ul class="clean" style="margin-bottom:0">{li(w["hints"])}</ul></div>'
        + selfcheck_block(w)
        + ('<p style="margin-top:22px">'
           f'<a class="btn" href="../lessons/{w2(w["num"])}.html">Instructor lesson plan (with references)</a></p>')
        + pager("lab", w)
    )
    return page(f'Week {w["num"]} Lab: {w["title"]}', 1, inner)

def selfcheck_block(w):
    qa = SELFCHECK.get(w["num"], [])
    if not qa:
        return ""
    items = "".join(
        f'<details><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>'
        for q, a in qa)
    return ('<h2 id="self-check"><span class="ic">&#10067;</span>Self-check</h2>'
            '<p>Answer each before expanding it. If one is unclear, revisit the lab and the references.</p>'
            f'<div class="selfcheck">{items}</div>')

def timeline(segs):
    rows, t = "", 0
    for mins, title, detail in segs:
        s, e = f"{t//60}:{t%60:02d}", f"{(t+mins)//60}:{(t+mins)%60:02d}"
        if isinstance(detail, (list, tuple)):
            dt = '<ul class="dt-list">' + "".join(f"<li>{esc(x)}</li>" for x in detail) + "</ul>"
        else:
            dt = f'<span class="dt">{esc(detail)}</span>' if detail else ""
        rows += (f'<tr><td class="tm">{s}–{e}</td><td class="mn">{mins} min</td>'
                 f'<td><b>{esc(title)}</b>{dt}</td></tr>')
        t += mins
    return f'<table class="timeline">{rows}</table>'

def lesson_html(w):
    n = w["num"]; L = LESSONS[n]; P = PEDAGOGY.get(n, {})
    def pts(block): return "; ".join(block["points"])
    lecture = [
        (10, "Recap & retrieval", "Open with two quick questions on last week's material (retrieval practice), then state this week's objectives."),
        (15, "Motivation", L["motivation"]),
        (45, L["conceptA"]["title"], L["conceptA"]["points"]),
        (10, "Break", ""),
        (45, L["conceptB"]["title"], L["conceptB"]["points"]),
        (30, "Live demo (predict, then run)", (P["predict"] + " " + L["demo"]) if P.get("predict") else L["demo"]),
        (15, "Wrap-up & practice preview", "Revisit the misconception and concept checks below, recap the takeaways, and preview the practice lesson."),
        (10, "Buffer & questions", ""),
    ]
    miss = P.get("misconception")
    miss_html = ("" if not miss else
        '<div class="callout miss"><b>Common misconception to confront.</b> '
        f'<p style="margin:6px 0 0"><i>Students often think:</i> {esc(miss[0])}<br>'
        f'<i>Set it straight:</i> {esc(miss[1])}</p></div>')
    checks = P.get("checks", [])
    checks_html = ("" if not checks else
        '<div class="callout check"><b>Check for understanding</b> (pose during the concept blocks; let students '
        'answer before revealing).'
        + '<div class="selfcheck" style="margin-top:8px">'
        + "".join(f'<details><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>'
                  for q, a in checks)
        + '</div></div>')
    demos = PRACTICE[n]
    half = (len(demos) + 1) // 2
    practice = [
        (10, "Setup & recap", "Recap the lecture's key ideas and open the working notebook."),
        (50, "Instructor demonstrations", demos[:half]),
        (5, "Break", ""),
        (40, "Instructor demonstrations (continued)", demos[half:]),
        (15, "Wrap-up & lab brief", "Summarize the patterns shown and brief the weekly lab (homework), which students complete on their own."),
    ]
    inner = (
        f'<div class="whead"><p class="eyebrow"><span class="wbadge">Week {n}</span> &nbsp; '
        f'Part {w["part"]} &middot; {esc(PARTS[w["part"]])}</p>'
        f'<h1>{esc(w["title"])}</h1>'
        f'<p class="sub">Instructor lesson plan: lecture (3 h) and practice (2 h).</p></div>'
        + '<div class="goals"><h2>Learning objectives</h2><ul class="clean">' + li(w["goals"]) + '</ul></div>'
        + '<h2><span class="ic">&#127891;</span><span class="secttag">Lecture &middot; 3 hours</span></h2>'
        + timeline(lecture)
        + miss_html
        + checks_html
        + f'<div class="callout"><b>Key takeaways.</b><ul class="clean" style="margin-bottom:0">{li(L["takeaways"])}</ul></div>'
        + '<h2><span class="ic">&#128187;</span><span class="secttag prac">Practice &middot; 2 hours</span></h2>'
        + f'<p>In the practice lesson the instructor demonstrates implementations, runs code, and works through examples, using the practice notebook linked below. The weekly <a href="../labs/{w2(n)}.html">lab</a> is then set as homework, where students apply this themselves.</p>'
        + timeline(practice)
        + f'<div class="callout hint"><b>Common pitfalls to pre-empt.</b><ul class="clean" style="margin-bottom:0">{li(w["hints"])}</ul></div>'
        + ('<p style="margin-top:22px">'
           f'<a class="btn" href="{colab_url(n)}" target="_blank" rel="noopener">Open the practice notebook in Colab</a> '
           f'<a class="btn" href="../references/{w2(n)}.html">Curated references</a> '
           f'<a class="btn" href="../labs/{w2(n)}.html">Lab (homework)</a></p>')
        + pager("lesson", w)
    )
    return page(f'Week {n} Lesson Plan: {w["title"]}', 1, inner)

def prereq_pager(key):
    i = PREREQ_ORDER.index(key)
    L = ""
    if i > 0:
        p = PREREQ_ORDER[i-1]
        L += f'<a href="{p}.html"><span class="lbl">Previous</span>{esc(PREREQ[p]["title"])}</a>'
    if i < len(PREREQ_ORDER)-1:
        nk = PREREQ_ORDER[i+1]
        L += f'<a class="nx" href="{nk}.html"><span class="lbl">Next</span>{esc(PREREQ[nk]["title"])}</a>'
    return f'<div class="pager">{L}</div>'

def prereq_page_html(key):
    pr = PREREQ[key]
    secs = ""
    for s in pr["sections"]:
        secs += f'<h2>{esc(s["h"])}</h2><ul class="clean">{li(s["points"])}</ul>'
    res = "".join(
        f'<div class="refcard"><div class="kind">Refresh</div><div class="body">'
        f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["title"])}</a> '
        f'<span class="dom">{esc(dom(r["url"]))}</span></div></div>'
        for r in pr["resources"])
    sc = ""
    for i, m in enumerate(pr["mcq"], 1):
        opts = "".join(f'<li>{esc(o)}</li>' for o in m["options"])
        correct = chr(65 + m["answer"])
        sc += (f'<div class="mcq"><p class="q"><b>{i}.</b> {esc(m["q"])}</p>'
               f'<ol class="opts" type="A">{opts}</ol>'
               f'<details><summary>Show answer</summary><div class="ans"><b>Correct: {correct}.</b> {esc(m["why"])}</div></details></div>')
    inner = (
        f'<div class="whead"><p class="eyebrow"><span class="wbadge">Prerequisite</span> &nbsp; Review &amp; refresh</p>'
        f'<h1>{pr["icon"]} {esc(pr["title"])}</h1><p class="sub">{esc(pr["intro"])}</p></div>'
        + secs
        + '<div class="goals"><h2>Readiness check</h2><ul class="clean">' + li(pr["checklist"]) + '</ul></div>'
        + '<h2 id="self-check"><span class="ic">&#10067;</span>Self-check questions</h2>'
          '<p>Multiple-choice questions on the topic itself. Pick an answer, then reveal it. '
          'If several are unclear, work through the review above first.</p>'
          '<div class="mcqs">' + sc + '</div>'
        + '<h2><span class="ic">&#128218;</span>Refresher resources</h2>' + f'<div class="refgrid">{res}</div>'
        + '<p style="margin-top:22px"><a class="btn" href="index.html">&larr; All prerequisites</a> '
          '<a class="btn" href="../index.html">Course home</a></p>'
        + prereq_pager(key)
    )
    return page(f'Prerequisite: {pr["title"]}', 1, inner)

def prereq_index_html():
    cards = ""
    for k in PREREQ_ORDER:
        pr = PREREQ[k]
        cards += (f'<div class="refcard"><div class="kind">{pr["icon"]}</div><div class="body">'
                  f'<a href="{k}.html">{esc(pr["title"])}</a>'
                  f'<p class="note">{esc(pr["intro"])}</p></div></div>')
    inner = (
        '<div class="whead"><p class="eyebrow"><span class="wbadge">Prerequisites</span></p>'
        '<h1>Prerequisites: review and self-check</h1>'
        '<p class="sub">The course assumes a prior machine-learning course and comfort with the mathematics '
        'and Python below. These pages support self-assessment and a refresher before Week 1.</p></div>'
        + f'<div class="refgrid">{cards}</div>'
        + '<p style="margin-top:22px"><a class="btn" href="../index.html">&larr; Course home</a> '
          '<a class="btn" href="../syllabus/syllabus.html">Syllabus</a></p>'
    )
    return page("Prerequisites: Introduction to Deep Learning", 1, inner)

def project_page_html(kind):
    pj = PROJECTS[kind]
    cards = ""
    for i, ex in enumerate(pj["examples"], 1):
        flds = "".join(f'<p class="fld"><b>{esc(label)}:</b> {esc(ex[key])}</p>'
                       for key, label in pj["fields"] if ex.get(key))
        cards += (f'<div class="pcard"><h3><span class="n">{i:02d}</span>{esc(ex["title"])}</h3>{flds}</div>')
    other = "final" if kind == "midterm" else "midterm"
    inner = (
        f'<div class="whead"><p class="eyebrow"><span class="wbadge">{esc(pj["badge"])}</span> &nbsp; {esc(pj["meta"])}</p>'
        f'<h1>{esc(pj["title"])}</h1><p class="sub">{esc(pj["intro"])}</p></div>'
        + f'<div class="callout"><b>Deliverables.</b><ul class="clean" style="margin-bottom:0">{li(pj["deliverables"])}</ul></div>'
        + f'<h2><span class="ic">&#128203;</span>Ten examples</h2>{cards}'
        + '<p style="margin-top:22px">'
          f'<a class="btn" href="{other}.html">{esc(PROJECTS[other]["title"])}</a> '
          '<a class="btn" href="../syllabus/syllabus.html">Syllabus</a> '
          '<a class="btn" href="../index.html">Course home</a></p>'
    )
    return page(pj["title"], 1, inner)

def projects_index_html():
    cards = ""
    for k in PROJECTS_ORDER:
        pj = PROJECTS[k]
        cards += (f'<div class="refcard"><div class="kind">{esc(pj["badge"])}</div><div class="body">'
                  f'<a href="{k}.html">{esc(pj["title"])}</a> <span class="dom">{esc(pj["meta"])}</span>'
                  f'<p class="note">{esc(pj["intro"])}</p></div></div>')
    inner = (
        '<div class="whead"><p class="eyebrow"><span class="wbadge">Projects</span></p>'
        '<h1>Project examples</h1>'
        '<p class="sub">Worked example briefs for the mid-term mini-project and the final project. '
        'Use one as given or adapt it; students may also propose another in the same spirit.</p></div>'
        + f'<div class="refgrid">{cards}</div>'
        + '<p style="margin-top:22px"><a class="btn" href="../index.html">&larr; Course home</a> '
          '<a class="btn" href="../syllabus/syllabus.html">Syllabus</a></p>'
    )
    return page("Projects: Introduction to Deep Learning", 1, inner)

KINDS = [("course", "Course"), ("book", "Book"), ("video", "Video"), ("blog", "Blog / Docs")]

def ref_html(w):
    r = REFS[f'week{w["num"]}']
    cards = ""
    for key, label in KINDS:
        e = r.get(key)
        if not e:
            continue
        cards += (f'<div class="refcard"><div class="kind">{label}</div><div class="body">'
                  f'<a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["title"])}</a> '
                  f'<span class="dom">{esc(dom(e["url"]))}</span>'
                  f'<p class="note">{esc(e["note"])}</p></div></div>')
    inner = (
        whead(w)
        + '<p>Curated, free, canonical references for this week: a course or lecture, a book chapter, a video, '
          'and an authoritative blog post or official tutorial. Each opens in a new tab.</p>'
        + f'<div class="refgrid">{cards}</div>'
        + f'<p style="margin-top:22px"><a class="btn" href="../labs/{w2(w["num"])}.html">&larr; Back to the Week {w["num"]} lab</a></p>'
        + pager("ref", w)
    )
    return page(f'Week {w["num"]} References: {w["title"]}', 1, inner)

def index_html():
    rows = ""
    seen = set()
    for w in WEEKS:
        if w["part"] not in seen:
            seen.add(w["part"])
            rows += (f'<tr class="part"><td colspan="3">Part {w["part"]} &middot; {esc(PARTS[w["part"]])}</td></tr>')
        rows += (f'<tr><td class="wk">{w["num"]}</td>'
                 f'<td class="t"><b>{esc(w["title"])}</b><span>{esc(w["sub"])}</span></td>'
                 f'<td class="lk"><a href="lessons/{w2(w["num"])}.html">Lesson plan</a>'
                 f'<a href="{colab_url(w["num"])}" target="_blank" rel="noopener">Practice notebook</a>'
                 f'<a href="labs/{w2(w["num"])}.html#self-check">Self-check</a>'
                 f'<a href="labs/{w2(w["num"])}.html">Homework lab</a></td></tr>')
    hero = (
        '<div class="hero">'
        '<img class="hitlogo" src="assets/hit-logo.png" alt="Holon Institute of Technology">'
        f'<p class="eyebrow">{esc(COURSE["code"])} &middot; HIT &middot; Foundation Course &middot; 13 Weeks</p>'
        f'<h1>{esc(COURSE["title"])}</h1>'
        f'<p class="sub">{esc(COURSE["subtitle"])}</p>'
        '<div class="meta"><span><b>Prerequisite:</b> Introduction to Machine Learning</span>'
        '<span><b>Required for:</b> all CS specializations (mandatory)</span>'
        '<span><b>Feeds into:</b> Advanced LLMs and Computer Vision</span>'
        '<span><b>Format:</b> 3 h lecture + 2 h practice + a homework lab</span>'
        '<span><b>Assessment:</b> labs and projects, no written exams</span></div></div>'
    )
    rationale = (
        '<h2>About this course</h2>'
        '<p>This is the foundational deep-learning course, <b>required of every computer-science student</b> '
        'and taught across all specializations. It turns an introductory machine-learning background into '
        'working neural-network skill in PyTorch: framing a task in tensor terms, then building, training, and '
        'debugging networks. The emphasis is on building and experimentation, not on watching. Each week has a '
        '3-hour lecture (theory), a 2-hour instructor-led practice lesson (live implementation and worked '
        'examples), and a hands-on lab set as homework.</p>'
        '<p><b>Rationale.</b> Modern AI rests on a shared deep-learning foundation. This course provides that '
        'common base for continued specialization in artificial intelligence, including <b>computer vision</b>, '
        '<b>large language models</b>, and others. It is valuable in its own right, not only as a step toward '
        'later courses. It is project- and lab-based and designed for the way students will actually work, with '
        'an AI coding assistant at hand, while keeping the learning genuine through a Build, Predict, and Explain '
        'model.</p>'
    )
    ocards = "".join(
        f'<div class="ocard"><span class="n">{i}</span><span class="oi">{icon}</span>'
        f'<span class="ot">{esc(text)}</span></div>'
        for i, (icon, text) in enumerate(OUTCOMES, 1))
    outcomes = ('<h2>Expected outcomes</h2><p>By the end of the course, students will be able to:</p>'
                f'<div class="ocards">{ocards}</div>')
    prereq_cta = (
        '<h2>Prerequisites: review and self-check</h2>'
        '<p>The course assumes a prior machine-learning course and the background below. Each row links a short '
        'refresher and a set of self-check questions, so readiness can be confirmed before Week 1.</p>'
        '<table class="prereqs"><thead><tr><th>Subject</th><th>Background topics</th><th>Material</th></tr></thead><tbody>'
        '<tr><td class="subj"><span class="pi">&#8721;</span>Mathematics</td>'
        '<td class="top">Linear algebra, probability, multivariable calculus, gradients, optimization</td>'
        '<td class="lk"><a href="prereq/math.html">Review</a><a href="prereq/math.html#self-check">Self-check</a></td></tr>'
        '<tr><td class="subj"><span class="pi">&#128013;</span>Python</td>'
        '<td class="top">Comprehensions, generators, dunder methods, NumPy versus lists, PyTorch idioms</td>'
        '<td class="lk"><a href="prereq/python.html">Review</a><a href="prereq/python.html#self-check">Self-check</a></td></tr>'
        '<tr><td class="subj"><span class="pi">&#129518;</span>Machine learning</td>'
        '<td class="top">Regression, classification, loss versus metric, overfitting, regularization, bias-variance</td>'
        '<td class="lk"><a href="prereq/ml.html">Review</a><a href="prereq/ml.html#self-check">Self-check</a></td></tr>'
        '</tbody></table>'
    )
    table = ('<h2 id="weekly">Weekly materials</h2><table class="weeks"><thead><tr><th>Wk</th><th>Topic</th>'
             '<th>Materials</th></tr></thead><tbody>' + rows + '</tbody></table>')
    hitpkg = (
        '<h2>HIT course catalogue package</h2>'
        '<p>Department submission documents in the HIT form, on the official letterhead (Word, downloadable):</p>'
        '<p class="btnrow">'
        '<a class="btn" href="hit-catalogue/syllabus_en.docx">Syllabus (English)</a>'
        '<a class="btn" href="hit-catalogue/syllabus_he.docx">Syllabus (Hebrew)</a>'
        '<a class="btn" href="hit-catalogue/rationale.docx">Rationale</a>'
        '<a class="btn" href="hit-catalogue/catalogue_summary.docx">Catalogue summary</a></p>'
    )
    ai = (
        '<h2 id="ai-usage">AI usage</h2>'
        '<p>Using an AI assistant is <b>highly encouraged</b> in this course; it reflects how the work is really '
        'done. Two conditions keep the learning genuine: students keep <b>full ownership of, and responsibility '
        'for, everything they submit</b>, and must be able to <b>explain and defend</b> any part of it. The '
        'Predict, Explain, and short oral-defense steps verify understanding rather than authorship; where an '
        'assistant was used, it should be disclosed.</p>'
        '<p>For what a strong submission looks like in practice, see a '
        '<a href="sample-submission.html">fully worked sample submission</a> that follows this model end to end.</p>'
    )
    format_sec = (
        '<h2>Course format</h2>'
        '<p>Each week has three parts: a <b>3-hour lecture</b> (theory), a <b>2-hour practice lesson</b> in which '
        'the instructor demonstrates implementations and works through examples, and a <b>weekly lab</b> set as '
        'homework. The thirteen weeks form four parts: Foundations (weeks 1 to 3), Training Infrastructure '
        '(4 to 7), Architectures and Representation Learning (8 to 12), and Integration (13). A mid-term '
        'mini-project consolidates Parts I and II; a final project consolidates the whole course.</p>'
    )
    lab_model = (
        '<p>Every weekly lab follows a three-part model:</p>'
        '<div class="steps">'
        '<div class="step a"><h3><span class="tag">Part A &middot; AI assistant welcome</span>Build</h3>'
        '<p>Produce working code that meets a specification or reaches a target metric; an AI assistant may be used freely.</p></div>'
        '<div class="step b"><h3><span class="tag">Part B &middot; reasoning</span>Predict &amp; probe</h3>'
        '<p>Before running anything, write down the expected outcome, then run controlled experiments and compare.</p></div>'
        '<div class="step c"><h3><span class="tag">Part C &middot; in plain language</span>Explain &amp; defend</h3>'
        '<p>Explain why the solution works, where it would break, and what changed; be ready to defend any line.</p></div>'
        '</div>'
    )
    assessment = (
        '<h2>Assessment and grading</h2>'
        '<p>Grading is project- and lab-based, with weight on the parts an AI assistant cannot do for the student: '
        'reasoning, interpretation, and defense. There are no written exams.</p>'
        '<table class="gtab"><thead><tr><th>Component</th><th>What it covers</th><th>Weight</th></tr></thead><tbody>'
        '<tr><td><b>Weekly labs</b></td><td>Eleven labs (best 10 count), graded mostly on the Predict and Explain parts.</td><td class="pct">40%</td></tr>'
        '<tr><td><b>Mid-term mini-project</b></td><td>A CNN-based project (around weeks 9 to 10): build, train, ablate, and report.</td><td class="pct">20%</td></tr>'
        '<tr><td><b>Final project</b></td><td>Implementation, a written report, an AI-use reflection, and a short oral defense.</td><td class="pct">35%</td></tr>'
        '<tr><td><b>Participation</b></td><td>In-class exercises and lab engagement.</td><td class="pct">5%</td></tr>'
        '</tbody></table>'
    )
    midterm_sec = (
        '<h2 id="midterm">Mid-term mini-project</h2>'
        f'<p class="projmeta">{esc(PROJECTS["midterm"]["meta"])}</p>'
        f'<p>{esc(PROJECTS["midterm"]["intro"])}</p>'
        '<p class="btnrow"><a class="btn" href="projects/midterm.html">Mid-term project examples &rarr;</a></p>'
    )
    final_sec = (
        '<h2 id="final">Final project</h2>'
        f'<p class="projmeta">{esc(PROJECTS["final"]["meta"])}</p>'
        f'<p>{esc(PROJECTS["final"]["intro"])}</p>'
        '<p>Deliverables are a one-page proposal (around week 8), a code submission, a short report, a half-page '
        'AI-use reflection, and a short oral defense where understanding, rather than authorship, is confirmed.</p>'
        '<p class="btnrow"><a class="btn" href="projects/final.html">Final project examples &rarr;</a></p>'
    )
    tools = (
        '<h2>Tools and resources</h2>'
        '<ul class="clean">'
        '<li><b>Core stack:</b> Python 3.11+, PyTorch, NumPy, and Matplotlib; Jupyter notebooks or Google Colab.</li>'
        '<li><b>AI assistant:</b> part of the toolkit, expected for the Build portion of the labs.</li>'
        '<li><b>Compute:</b> a GPU helps but is not required; Colab provides free GPU access.</li>'
        '<li><b>Reference reading:</b> <i>Dive into Deep Learning</i> (d2l.ai) and the official PyTorch tutorials.</li>'
        '<li><b>Course materials:</b> lecture slides, exercise notebooks, and starter code are posted weekly.</li>'
        '</ul>'
    )
    inner = (hero + hitpkg + rationale + format_sec + outcomes
             + prereq_cta + table + ai + lab_model + assessment + midterm_sec + final_sec + tools)
    return page(f'{COURSE["title"]} (HIT)', 0, inner)

def sample_submission_html():
    def cb(src):
        return f'<pre class="code"><code>{esc(src)}</code></pre>'
    build_code = (
        "import torch, torch.nn as nn\n"
        "torch.manual_seed(0)\n\n"
        "# Synthetic task: the label depends on only the first 6 of 40 features;\n"
        "# the other 34 are pure noise the model can latch onto and overfit.\n"
        "def make(n, d=40, k=6):\n"
        "    X = torch.randn(n, d)\n"
        "    w = torch.zeros(d)\n"
        "    w[:k] = torch.tensor([2.0, -1.8, 1.5, -1.4, 1.2, -1.0])\n"
        "    y = (X @ w + 0.2 * torch.randn(n) > 0).long()\n"
        "    return X, y\n\n"
        "Xtr, ytr   = make(60)      # small training set  -> easy to overfit\n"
        "Xval, yval = make(2000)    # large validation set -> stable estimate\n\n"
        "def mlp(p_drop=0.0):\n"
        "    return nn.Sequential(\n"
        "        nn.Linear(40, 256), nn.ReLU(), nn.Dropout(p_drop),\n"
        "        nn.Linear(256, 256), nn.ReLU(), nn.Dropout(p_drop),\n"
        "        nn.Linear(256, 2))\n\n"
        "def train(model, weight_decay=0.0, epochs=600):\n"
        "    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=weight_decay)\n"
        "    loss_fn = nn.CrossEntropyLoss()\n"
        "    for _ in range(epochs):\n"
        "        model.train(); opt.zero_grad()\n"
        "        loss_fn(model(Xtr), ytr).backward(); opt.step()\n"
        "    model.eval()\n"
        "    with torch.no_grad():\n"
        "        tr = (model(Xtr).argmax(1) == ytr).float().mean().item()\n"
        "        va = (model(Xval).argmax(1) == yval).float().mean().item()\n"
        "    return tr, va\n\n"
        "torch.manual_seed(0)\n"
        "tr, va = train(mlp())          # baseline: no regularization\n"
        'print(f"baseline  train {tr:.2f}  val {va:.3f}")\n'
        "# -> baseline  train 1.00  val 0.717"
    )
    probe_code = (
        "configs = [\n"
        '    ("dropout 0.5",           dict(p_drop=0.5)),\n'
        '    ("weight decay 5e-2",     dict(weight_decay=5e-2)),\n'
        '    ("dropout 0.5 + wd 5e-2", dict(p_drop=0.5, weight_decay=5e-2)),\n'
        '    ("over-regularized",      dict(p_drop=0.8, weight_decay=5e-1)),\n'
        "]\n"
        "for name, kw in configs:\n"
        "    torch.manual_seed(0)\n"
        '    p = kw.get("p_drop", 0.0); wd = kw.get("weight_decay", 0.0)\n'
        "    tr, va = train(mlp(p), weight_decay=wd)\n"
        '    print(f"{name:22s} train {tr:.2f}  val {va:.3f}")'
    )
    pred_table = (
        '<table class="predtab"><thead><tr><th>#</th><th>Hypothesis (written before running)</th>'
        '<th>Predicted outcome</th></tr></thead><tbody>'
        '<tr><td>H1</td><td>Dropout 0.5 regularizes the network.</td>'
        '<td>Validation accuracy rises; training accuracy may dip.</td></tr>'
        '<tr><td>H2</td><td>Weight decay 5e-2 suppresses the 34 noise features.</td>'
        '<td>Validation rises more than dropout alone.</td></tr>'
        '<tr><td>H3</td><td>Dropout and weight decay together.</td>'
        '<td>Best validation accuracy of all configurations.</td></tr>'
        '<tr><td>H4</td><td>Very strong regularization (dropout 0.8 + wd 5e-1).</td>'
        '<td>The model underfits; training accuracy collapses.</td></tr>'
        '</tbody></table>')
    result_table = (
        '<table class="predtab"><thead><tr><th>Configuration</th><th>Train acc</th><th>Val acc</th>'
        '<th>vs baseline</th></tr></thead><tbody>'
        '<tr><td>baseline (no regularization)</td><td>1.00</td><td>0.717</td><td>&ndash;</td></tr>'
        '<tr><td>dropout 0.5</td><td>1.00</td><td>0.740</td><td class="ok">+0.023</td></tr>'
        '<tr><td>weight decay 5e-2</td><td>1.00</td><td><b>0.759</b></td><td class="ok">+0.042</td></tr>'
        '<tr><td>dropout 0.5 + weight decay 5e-2</td><td>1.00</td><td>0.757</td><td class="ok">+0.040</td></tr>'
        '<tr><td>over-regularized (drop 0.8 + wd 5e-1)</td><td>0.52</td><td>0.502</td><td class="no">&minus;0.215</td></tr>'
        '</tbody></table>')
    verdicts = (
        '<table class="predtab"><thead><tr><th>#</th><th>Predicted</th><th>Observed</th><th>Verdict</th></tr></thead><tbody>'
        '<tr><td>H1</td><td>Val rises, train may dip.</td><td>Val +0.023; train stayed 1.00 (60 points still memorized).</td>'
        '<td class="verdict y">confirmed</td></tr>'
        '<tr><td>H2</td><td>Weight decay beats dropout.</td><td>Weight decay best single regularizer (+0.042).</td>'
        '<td class="verdict y">confirmed</td></tr>'
        '<tr><td>H3</td><td>Combining is best.</td><td>0.757, just below weight decay alone (0.759). Dropout added nothing on top.</td>'
        '<td class="verdict n">refuted</td></tr>'
        '<tr><td>H4</td><td>Underfits, train collapses.</td><td>Train fell to 0.52, val to chance (0.50).</td>'
        '<td class="verdict y">confirmed</td></tr>'
        '</tbody></table>')
    inner = (
        '<div class="whead"><p class="eyebrow"><span class="wbadge">Sample submission</span> &nbsp; '
        'Week 7 lab &middot; Regularization and generalization</p>'
        '<h1>Closing the generalization gap on a small classifier</h1>'
        '<p class="sub">An illustrative, complete lab submission following the course\'s '
        'Build / Predict &amp; probe / Explain &amp; defend model. It shows the expected structure, depth, and '
        'tone of a strong submission, including a prediction that turned out wrong and what was learned from it.</p></div>'

        '<div class="callout"><b>Lab task.</b> Train a classifier on a small dataset that overfits, then reduce the '
        'overfitting with regularization. Report validation accuracy before and after, design an ablation that '
        'isolates each regularizer, and justify the final choice.</div>'

        '<div class="steps"><div class="step a"><h3><span class="tag">Part A &middot; AI assistant welcome</span>Build</h3>'
        '<p>The training pipeline below was drafted with an AI assistant and then read line by line. The dataset is '
        'deliberately small (60 training points) with 34 uninformative noise features, so an unregularized network '
        'memorizes the training set and generalizes poorly.</p></div></div>'
        + cb(build_code) +
        '<p>The baseline reaches <b>100% training accuracy but only 71.7% validation accuracy</b>: a 28-point gap, '
        'the signature of overfitting. The network has fit the noise features.</p>'

        '<div class="steps"><div class="step b"><h3><span class="tag">Part B &middot; reasoning</span>Predict &amp; probe</h3>'
        '<p>Four hypotheses were written down <i>before</i> running anything, then tested with a controlled ablation '
        'that changes one regularizer at a time.</p></div></div>'
        '<h3>Predictions (before running)</h3>' + pred_table +
        '<h3>The experiment</h3>' + cb(probe_code) +
        '<h3>Results</h3>' + result_table +
        '<h3>Predicted vs observed</h3>' + verdicts +
        '<div class="callout hint"><b>The instructive miss (H3).</b> Combining dropout with weight decay was '
        'predicted to be best, but it did not beat weight decay alone. With weight decay already constraining the '
        'weights, the extra dropout removed capacity the model could not spare on 60 points; the two regularizers '
        'overlap here rather than stack. Catching this is the point of writing the prediction down first.</div>'

        '<div class="steps"><div class="step c"><h3><span class="tag">Part C &middot; in plain language</span>Explain &amp; defend</h3>'
        '<p><b>Why regularization helped.</b> A 60-point training set with 34 noise features is a high-variance '
        'regime: the unregularized network fits the noise (training accuracy 1.00) and carries it to validation. '
        'Weight decay penalizes large weights, shrinking the reliance on the noise features; dropout forces the '
        'network to spread its prediction across redundant units. Both lower variance, so validation accuracy '
        'rises from 0.72 to 0.76.</p>'
        '<p><b>Where it would break.</b> With abundant training data the gap would be small and regularization '
        'would matter little. Too strong, and the model underfits, the 0.50 validation case, no better than '
        'guessing. Dropout must be off at evaluation (<code>model.eval()</code>); leaving it on would corrupt the '
        'reported validation accuracy.</p>'
        '<p><b>What changed and the final choice.</b> Validation accuracy improved by 4 points (0.717 to 0.759) by '
        'suppressing reliance on the 34 noise features. The chosen configuration is <b>weight decay 5e-2 alone</b>: '
        'it gives the best validation accuracy with the simplest setup, and the ablation shows dropout adds nothing '
        'on top of it for this dataset.</p></div></div>'

        '<div class="callout"><b>AI-use disclosure.</b> An AI assistant drafted the training loop and the metric '
        'code (Part A). The ablation design, the four predictions, the interpretation of the H3 surprise, and the '
        'final choice are the author\'s own work, and every line can be explained and defended on request.</div>'

        '<div class="callout check"><b>How this maps to the rubric.</b> Part A shows working, understood code. '
        'Part B shows reasoning made falsifiable: predictions first, a clean one-variable-at-a-time ablation, and an '
        'honest account of the prediction that failed. Part C shows mechanism, failure modes, and a defended '
        'decision. The graded weight is on Parts B and C, the parts an assistant cannot do for the student.</div>'

        '<p style="margin-top:22px"><a class="btn" href="index.html">&larr; Course home</a> '
        '<a class="btn" href="labs/week07.html">The Week 7 lab</a> '
        '<a class="btn" href="' + colab_url(7) + '" target="_blank" rel="noopener">Week 7 practice notebook</a></p>'
    )
    return page("Sample submission: Build, Predict and probe, Explain and defend", 0, inner)

def main():
    for d in ("labs", "references", "lessons", "prereq", "projects"):
        os.makedirs(P(d), exist_ok=True)
    n = 0
    for w in WEEKS:
        open(P("labs", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(lab_html(w)); n += 1
        open(P("references", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(ref_html(w)); n += 1
        open(P("lessons", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(lesson_html(w)); n += 1
    open(P("prereq", "index.html"), "w", encoding="utf-8").write(prereq_index_html()); n += 1
    for k in PREREQ_ORDER:
        open(P("prereq", f"{k}.html"), "w", encoding="utf-8").write(prereq_page_html(k)); n += 1
    open(P("projects", "index.html"), "w", encoding="utf-8").write(projects_index_html()); n += 1
    for k in PROJECTS_ORDER:
        open(P("projects", f"{k}.html"), "w", encoding="utf-8").write(project_page_html(k)); n += 1
    open(P("index.html"), "w", encoding="utf-8").write(index_html()); n += 1
    open(P("sample-submission.html"), "w", encoding="utf-8").write(sample_submission_html()); n += 1
    write_folder_readmes()
    print(f"generated {n} pages (index + {len(WEEKS)} x3 weekly + {len(PREREQ_ORDER)+1} prereq) and folder READMEs")

PAGES = "https://apartsin.github.io/DLCourseHIT"

def _wk_list(folder):
    return "\n".join(f"- Week {w['num']:02d}: [{w['title']}]({PAGES}/{folder}/{w2(w['num'])}.html)" for w in WEEKS)

def write_folder_readmes():
    rm = {
        "prereq": "# Prerequisites\n\nReview-and-refresh pages for the background the course assumes: "
                  "mathematics, Python, and basic machine learning.\n\n"
                  f"View: {PAGES}/prereq/\n\n- [Mathematics]({PAGES}/prereq/math.html)\n"
                  f"- [Python]({PAGES}/prereq/python.html)\n- [Machine learning]({PAGES}/prereq/ml.html)\n",
        "syllabus": "# Syllabus\n\nThe course syllabus. `syllabus.html` is the source of truth; the DOCX and "
                    "PDF are regenerated from it.\n\n"
                    f"- [HTML]({PAGES}/syllabus/syllabus.html)\n- [Word (.docx)](syllabus.docx)\n- [PDF](syllabus.pdf)\n",
        "labs": "# Labs\n\nWeekly student lab handouts, each with goals, a Build / Predict & probe / Explain & "
                "defend exercise, deliverables, and self-check questions.\n\n" + _wk_list("labs") + "\n",
        "references": "# References\n\nPer-week curated, free, canonical resources (a course, a book chapter, a "
                      "video, and an authoritative blog or tutorial).\n\n" + _wk_list("references") + "\n",
        "lessons": "# Lesson plans\n\nInstructor lesson plans: a timed 3-hour lecture outline and a 2-hour "
                   "practice outline per week.\n\n" + _wk_list("lessons") + "\n",
        "notebooks": "# Practice notebooks\n\nColab notebooks for the instructor to run during the 2-hour "
                     "practice lessons (one section per live demonstration). The student homework is the lab.\n\n" +
                     "\n".join(f"- Week {w['num']:02d}: [Open in Colab]({colab_url(w['num'])}) &middot; [`{w2(w['num'])}.ipynb`]({w2(w['num'])}.ipynb)" for w in WEEKS) + "\n",
        "hit-catalogue": "# HIT catalogue package\n\nDepartment submission package in the HIT form, with the "
                         "official HIT letterhead.\n\n- `syllabus_en.docx` (English syllabus)\n- `syllabus_he.docx` "
                         "(Hebrew syllabus)\n- `rationale.docx`\n- `catalogue_summary.docx`\n- `committee_questionnaire.docx`\n",
        "projects": "# Projects\n\nExample briefs for the mid-term mini-project (CNN-based) and the final "
                    "project (any architecture family), ten examples each.\n\n"
                    f"View: {PAGES}/projects/\n\n- [Mid-term examples]({PAGES}/projects/midterm.html)\n"
                    f"- [Final examples]({PAGES}/projects/final.html)\n",
        "assets": "# Assets\n\nShared stylesheet (`style.css`) for the course site (index, prerequisites, labs, "
                  "references, lesson plans, projects).\n",
        "tools": "# Build tools\n\nGenerators for the course site and packages.\n\n```bash\n"
                 "python tools/build_site.py        # index + prereq + labs + references + lessons\n"
                 "python tools/build_notebooks.py   # Colab notebooks\n"
                 "python tools/build_hit_package.py # HIT catalogue .docx package\n```\n\n"
                 "Content lives in `content.py`, `lessons.py`, `selfcheck.py`, `prereq.py`, and `refs.json`.\n",
    }
    for folder, text in rm.items():
        os.makedirs(P(folder), exist_ok=True)
        open(P(folder, "README.md"), "w", encoding="utf-8").write(text)

if __name__ == "__main__":
    main()
