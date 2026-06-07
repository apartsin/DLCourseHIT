# -*- coding: utf-8 -*-
"""Generate the DLCourseHIT site: index.html + labs/weekNN.html + references/weekNN.html
from content.py (lab handouts) and refs.json (scouted references). Shared CSS in assets/style.css."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import COURSE, PARTS, WEEKS
from lessons import LESSONS
from selfcheck import SELFCHECK
from prereq import PREREQ, ORDER as PREREQ_ORDER
from projects import PROJECTS, ORDER as PROJECTS_ORDER

OUTCOMES = [
    "Frame ML tasks as networks (tensors in, a loss out).",
    "Represent data as tensors and use them fluently.",
    "Build data pipelines with Dataset and DataLoader.",
    "Use automatic differentiation to compute gradients.",
    "Implement neural networks in PyTorch.",
    "Reason about optimization (SGD, Adam, learning rates).",
    "Diagnose training issues (overfitting, instability).",
    "Build MLPs, CNNs, RNNs, LSTMs/GRUs, and autoencoders.",
    "Apply representation learning and transfer learning.",
    "Carry a transferable base into advanced LLM and vision courses.",
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
            f'<a href="{up}syllabus/syllabus.html">Syllabus</a>'
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
        f'<div class="step a"><h3><span class="tag">Part A &middot; Claude welcome</span>Build</h3><ol>{li(w["build"])}</ol></div>'
        f'<div class="step b"><h3><span class="tag">Part B &middot; your reasoning</span>Predict &amp; probe</h3><ol>{li(w["predict"])}</ol></div>'
        f'<div class="step c"><h3><span class="tag">Part C &middot; in plain language</span>Explain &amp; defend</h3><ol>{li(w["explain"])}</ol></div>'
    )
    inner = (
        whead(w)
        + f'<div class="goals"><h2>Learning goals</h2><ul class="clean">{li(w["goals"])}</ul></div>'
        + '<div class="callout">This lab follows the course\'s <b>Build / Predict &amp; probe / Explain &amp; defend</b> model. '
          'Use Claude freely for the Build; the graded learning is in Predict and Explain. '
          'See <a href="../syllabus/syllabus.html">the syllabus</a> for the AI-use policy.</div>'
        + '<h2><span class="ic">&#9881;</span>Exercise</h2>' + f'<div class="steps">{steps}</div>'
        + '<h2><span class="ic">&#10003;</span>Deliverables</h2>' + f'<ul class="clean">{li(w["deliverables"])}</ul>'
        + f'<div class="callout hint"><b>Hints.</b><ul class="clean" style="margin-bottom:0">{li(w["hints"])}</ul></div>'
        + selfcheck_block(w)
        + ('<p style="margin-top:22px">'
           f'<a class="btn" href="{colab_url(w["num"])}" target="_blank" rel="noopener">Open practice notebook in Colab</a> '
           f'<a class="btn" href="../references/{w2(w["num"])}.html">Reference material</a> '
           f'<a class="btn" href="../lessons/{w2(w["num"])}.html">Instructor lesson plan</a></p>')
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
    return ('<h2><span class="ic">&#10067;</span>Self-check</h2>'
            '<p>Try to answer each before expanding it. If one is unclear, revisit the lab and the references.</p>'
            f'<div class="selfcheck">{items}</div>')

def timeline(segs):
    rows, t = "", 0
    for mins, title, detail in segs:
        s, e = f"{t//60}:{t%60:02d}", f"{(t+mins)//60}:{(t+mins)%60:02d}"
        dt = f'<span class="dt">{esc(detail)}</span>' if detail else ""
        rows += (f'<tr><td class="tm">{s}–{e}</td><td class="mn">{mins} min</td>'
                 f'<td><b>{esc(title)}</b>{dt}</td></tr>')
        t += mins
    return f'<table class="timeline">{rows}</table>'

def lesson_html(w):
    n = w["num"]; L = LESSONS[n]
    def pts(block): return "; ".join(block["points"])
    lecture = [
        (10, "Recap & objectives", "Connect to the previous week; state this week's objectives."),
        (15, "Motivation", L["motivation"]),
        (45, L["conceptA"]["title"], pts(L["conceptA"])),
        (10, "Break", ""),
        (45, L["conceptB"]["title"], pts(L["conceptB"])),
        (30, "Live demo", L["demo"]),
        (15, "Wrap-up & lab preview", "Recap the takeaways and brief this week's lab."),
        (10, "Buffer & questions", ""),
    ]
    practice = [
        (10, "Setup & brief", "Confirm environments run; restate the lab goal and deliverables."),
        (15, "Predict", "Students write predictions before coding. " + "; ".join(w["predict"])),
        (45, "Build (Claude welcome)", "; ".join(w["build"])),
        (5, "Break", ""),
        (25, "Probe", "Run controlled experiments and compare results against the predictions."),
        (15, "Explain & defend", "; ".join(w["explain"])),
        (5, "Wrap & deliverable check", "; ".join(w["deliverables"])),
    ]
    inner = (
        f'<div class="whead"><p class="eyebrow"><span class="wbadge">Week {n}</span> &nbsp; '
        f'Part {w["part"]} &middot; {esc(PARTS[w["part"]])}</p>'
        f'<h1>{esc(w["title"])}</h1>'
        f'<p class="sub">Instructor lesson plan: lecture (3 h) and practice (2 h).</p></div>'
        + '<div class="goals"><h2>Learning objectives</h2><ul class="clean">' + li(w["goals"]) + '</ul></div>'
        + '<h2><span class="ic">&#127891;</span><span class="secttag">Lecture &middot; 3 hours</span></h2>'
        + timeline(lecture)
        + f'<div class="callout"><b>Key takeaways.</b><ul class="clean" style="margin-bottom:0">{li(L["takeaways"])}</ul></div>'
        + '<h2><span class="ic">&#128187;</span><span class="secttag prac">Practice &middot; 2 hours</span></h2>'
        + '<p>The practice class follows the lab\'s Build / Predict &amp; probe / Explain &amp; defend model.</p>'
        + timeline(practice)
        + f'<div class="callout hint"><b>Common pitfalls to pre-empt.</b><ul class="clean" style="margin-bottom:0">{li(w["hints"])}</ul></div>'
        + ('<p style="margin-top:22px">'
           f'<a class="btn" href="../labs/{w2(n)}.html">Student lab</a> '
           f'<a class="btn" href="../references/{w2(n)}.html">References</a></p>')
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
    sc = "".join(f'<details><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>'
                 for q, a in pr["selfcheck"])
    inner = (
        f'<div class="whead"><p class="eyebrow"><span class="wbadge">Prerequisite</span> &nbsp; Review &amp; refresh</p>'
        f'<h1>{pr["icon"]} {esc(pr["title"])}</h1><p class="sub">{esc(pr["intro"])}</p></div>'
        + secs
        + '<div class="goals"><h2>You should be able to</h2><ul class="clean">' + li(pr["checklist"]) + '</ul></div>'
        + '<h2><span class="ic">&#10067;</span>Self-check</h2><div class="selfcheck">' + sc + '</div>'
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
        '<div class="whead"><p class="eyebrow"><span class="wbadge">Before you start</span></p>'
        '<h1>Prerequisites review</h1>'
        '<p class="sub">This course assumes a prior machine-learning course plus comfort with the math '
        'and Python below. Use these pages to self-assess and refresh before Week 1.</p></div>'
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
        'Use one as given or adapt it; you may also propose your own in the same spirit.</p></div>'
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
                 f'<td class="lk"><a href="labs/{w2(w["num"])}.html">Lab</a>'
                 f'<a href="references/{w2(w["num"])}.html">References</a>'
                 f'<a href="lessons/{w2(w["num"])}.html">Lesson plan</a>'
                 f'<a href="{colab_url(w["num"])}" target="_blank" rel="noopener">Notebook</a></td></tr>')
    hero = (
        '<div class="hero">'
        f'<p class="eyebrow">{esc(COURSE["code"])} &middot; HIT &middot; Foundation Course &middot; 13 Weeks</p>'
        f'<h1>{esc(COURSE["title"])}</h1>'
        f'<p class="sub">{esc(COURSE["subtitle"])}</p>'
        '<div class="meta"><span><b>Prerequisite:</b> Introduction to Machine Learning</span>'
        '<span><b>Leads to:</b> Advanced LLMs &middot; Advanced Computer Vision</span>'
        '<span><b>Format:</b> 3 h lecture + 2 h exercise / week</span></div>'
        '<div class="btnrow"><a class="btn" href="prereq/index.html">Prerequisites</a>'
        '<a class="btn" href="syllabus/syllabus.html">Syllabus (HTML)</a>'
        '<a class="btn" href="syllabus/syllabus.docx">DOCX</a>'
        '<a class="btn" href="syllabus/syllabus.pdf">PDF</a></div></div>'
    )
    rationale = (
        '<h2>About this course</h2>'
        '<p>This is the foundation deep-learning course in the program. It turns an introductory '
        'machine-learning background into working neural-network skill in PyTorch: framing a task in tensor '
        'terms, then building, training, and debugging networks. The emphasis is on building and '
        'experimentation, not on watching.</p>'
        '<p><b>Rationale.</b> Modern AI in vision and language rests on a shared deep-learning foundation. '
        'This course provides that common base and is the bridge to the advanced electives in <b>large '
        'language models</b> and <b>computer vision</b>: once you can frame, build, train, and debug a '
        'network, those courses can focus on what is specific to their domains. It is project- and '
        'exercise-based and designed for the way you will actually work, with an AI coding assistant at '
        'hand, while keeping the learning genuine through a Build, Predict, and Explain model.</p>'
    )
    outcomes = ('<div class="goals"><h2>Expected outcomes</h2><p>By the end of the course you will be able to:</p>'
                '<ol class="clean" style="columns:2;column-gap:32px">' + li(OUTCOMES) + '</ol></div>')
    prereq_cta = (
        '<h2>Before you start</h2>'
        '<p>The course assumes a prior ML course plus comfort with the math and Python it relies on. '
        'Review and self-assess with the prerequisite pages:</p>'
        '<p class="btnrow">'
        '<a class="btn" href="prereq/math.html">Mathematics</a>'
        '<a class="btn" href="prereq/python.html">Python</a>'
        '<a class="btn" href="prereq/ml.html">Machine learning</a></p>'
    )
    table = ('<h2>Weekly materials</h2><table class="weeks"><thead><tr><th>Wk</th><th>Topic</th>'
             '<th>Materials</th></tr></thead><tbody>' + rows + '</tbody></table>')
    explore = (
        '<h2>Explore</h2>'
        '<p>Everything in this course site, by section:</p>'
        '<ul class="clean">'
        '<li><a href="prereq/index.html">Prerequisites</a>: math, Python, and ML refreshers.</li>'
        '<li><a href="syllabus/syllabus.html">Syllabus</a>: full course outline (also DOCX and PDF).</li>'
        '<li><a href="labs/week01.html">Labs</a>: weekly student handouts with self-check questions.</li>'
        '<li><a href="references/week01.html">References</a>: curated free courses, books, videos, and blogs.</li>'
        '<li><a href="lessons/week01.html">Lesson plans</a>: instructor lecture and practice outlines.</li>'
        '<li><a href="' + colab_url(1) + '" target="_blank" rel="noopener">Notebooks</a>: Colab-ready practice notebooks.</li>'
        '<li><a href="projects/index.html">Projects</a>: example briefs for the mid-term and final projects.</li>'
        '</ul>'
    )
    inner = hero + rationale + outcomes + prereq_cta + table + explore
    return page(f'{COURSE["title"]} (HIT)', 0, inner)

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
        "notebooks": "# Notebooks\n\nColab-ready practice notebooks with an Open-in-Colab badge and the "
                     "Build / Predict / Explain scaffolding.\n\n" +
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
