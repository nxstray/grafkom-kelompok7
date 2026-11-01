# PostToolUse - GK_M8 Kelompok 6

Auto checks after each tool use.
Cline reads this file on PostToolUse event.

## Rules
1. After editing src/*.py: run
   python -m py_compile src/*.py
2. After editing src/fill_algorithms.py or src/maps.py: run
   python -m unittest discover -s tests -v
3. After editing docs/laporan.tex: check em dash and en dash
   with python search, then run python docs/make_pdf.py
4. After editing .clinerules/*.md: list .clinerules folder
   to confirm no skill folder returns.
5. Never commit .pyc or __pycache__ folders.
