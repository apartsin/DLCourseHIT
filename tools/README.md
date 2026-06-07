# Build tools

Generators for the course site and packages.

```bash
python tools/build_site.py        # index + prereq + labs + references + lessons
python tools/build_notebooks.py   # Colab notebooks
python tools/build_hit_package.py # HIT catalogue .docx package
```

Content lives in `content.py`, `lessons.py`, `selfcheck.py`, `prereq.py`, and `refs.json`.
