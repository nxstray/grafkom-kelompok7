# PreToolUse - GK_M8 Kelompok 6

Block risky tool use before it runs.
Cline reads this file on PreToolUse event.

## Rules
1. Deny edit to docs/laporan.pdf directly. Regenerate with
   python docs/make_pdf.py instead.
2. Deny pip install. Project uses stdlib only (tkinter).
3. Ask user first before deleting .clinerules, src, tests, or docs.
4. Ask user first before renaming folder GK_M8.
5. Warn when editing src/app.py above 250 lines. Suggest split
   or reduce COLS or ROWS for demo speed.
