# -*- coding: utf-8 -*-
"""Generate the DLCourseHIT site: index.html + labs/weekNN.html + references/weekNN.html
from content.py (lab handouts) and refs.json (scouted references). Shared CSS in assets/style.css."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import COURSE, PARTS, WEEKS
from lessons import LESSONS
from selfcheck import SELFCHECK

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
            f'<a href="{up}syllabus/syllabus.html">Syllabus</a></nav></div></div>')

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
        '<div class="btnrow"><a class="btn" href="syllabus/syllabus.html">Syllabus (HTML)</a>'
        '<a class="btn" href="syllabus/syllabus.docx">Syllabus (DOCX)</a>'
        '<a class="btn" href="syllabus/syllabus.pdf">Syllabus (PDF)</a></div></div>'
    )
    intro = (
        '<p>This is the foundation deep-learning course in the program. It turns an introductory '
        'machine-learning background into working neural-network skill in PyTorch: framing a task, then '
        'building, training, and debugging networks. It is the bridge to the advanced electives in large '
        'language models and computer vision.</p>'
        '<p>The course is project- and exercise-based, designed for working with an AI assistant. Every week '
        'has a <b>lab</b> (Build with Claude, then Predict and Explain) and a <b>reference page</b> of curated '
        'free resources.</p>'
    )
    inner = hero + intro + '<h2>Weekly materials</h2><table class="weeks"><thead><tr><th>Wk</th><th>Topic</th><th>Materials</th></tr></thead><tbody>' + rows + '</tbody></table>'
    return page(f'{COURSE["title"]} (HIT)', 0, inner)

def main():
    for d in ("labs", "references", "lessons"):
        os.makedirs(P(d), exist_ok=True)
    n = 0
    for w in WEEKS:
        open(P("labs", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(lab_html(w)); n += 1
        open(P("references", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(ref_html(w)); n += 1
        open(P("lessons", f'{w2(w["num"])}.html'), "w", encoding="utf-8").write(lesson_html(w)); n += 1
    open(P("index.html"), "w", encoding="utf-8").write(index_html()); n += 1
    print(f"generated {n} pages: index + {len(WEEKS)} labs + {len(WEEKS)} references + {len(WEEKS)} lessons")

if __name__ == "__main__":
    main()
