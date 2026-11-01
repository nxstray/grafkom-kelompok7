"""Demo maps used by the app and the report."""
# English comments only in this file.

from fill_algorithms import EMPTY, BOUNDARY


def blank(w, h):
    """Create empty grid."""
    return [[EMPTY for _ in range(w)] for _ in range(h)]


def rect_border(grid, x0, y0, x1, y1, color=BOUNDARY):
    """Draw rectangle border on grid."""
    for x in range(x0, x1 + 1):
        grid[y0][x] = color
        grid[y1][x] = color
    for y in range(y0, y1 + 1):
        grid[y][x0] = color
        grid[y][x1] = color


def circle(grid, cx, cy, r, color=BOUNDARY):
    """Draw rough circle with midpoint style loop."""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if abs(d - r) < 0.7:
                grid[y][x] = color


def map_rooms():
    """Two rooms plus corridor, good for 4 vs 8 demo."""
    g = blank(40, 26)
    rect_border(g, 2, 2, 17, 12)
    rect_border(g, 22, 2, 37, 12)
    rect_border(g, 8, 14, 31, 23)
    for x in range(17, 23):
        g[7][x] = BOUNDARY
    g[7][19] = EMPTY
    g[7][20] = EMPTY
    return {"grid": g, "spots": [(5, 5), (25, 5), (15, 18)]}


def map_circle():
    """Circle in box for coloring game style."""
    g = blank(40, 26)
    rect_border(g, 1, 1, 38, 24)
    circle(g, 20, 13, 8)
    circle(g, 20, 13, 4)
    return {"grid": g, "spots": [(20, 13), (20, 7), (5, 5)]}


def map_leak():
    """Box with one hole, shows leak to outside."""
    g = blank(40, 26)
    rect_border(g, 5, 4, 34, 21)
    g[4][20] = EMPTY
    return {"grid": g, "spots": [(15, 10), (2, 2)]}


MAPS = {"rooms": map_rooms, "circle": map_circle, "leak": map_leak}
