# GK_M8 Kelompok 7
Coloring app with Boundary Fill and Flood Fill.
Run: python src/app.py. Test: python -m unittest discover -s tests -v.
Report: docs/laporan.tex. PDF: python docs/make_pdf.py.
Rules: .clinerules folder.

## Boundary Fill vs Flood Fill

| Aspect | Boundary Fill | Flood Fill |
|--------|---------------|------------|
| Fill condition | Stops when cell equals boundary color or fill color | Stops when cell differs from target color |
| Cell equals target color | Treated as boundary, not filled | Filled with fill color |
| Target color | Not needed (uses boundary color) | Needed (the color to replace) |
| Stack | LIFO stack | LIFO stack |
| Connectivity | 4 or 8 neighbors | 4 or 8 neighbors |

Both Boundary Fill and Flood Fill use a LIFO stack.
The stack starts with the seed point. While the stack is not empty:
- pop a cell from the stack,
- check its four neighbors (4-connectivity: left, right, up, down),
- push valid neighbors that match the fill condition,
- repeat until the stack is empty.

4-connectivity means only the four direct neighbors are checked, not the diagonals.
