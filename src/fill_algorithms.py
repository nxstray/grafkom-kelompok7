# Core fill algorithms (GUI independent, testable).
# English comments only in source code.

from collections import deque
import time

# Color codes used in the grid model.
# 0 = empty (white), 1 = boundary (black), 2+ = fill colors.
BOUNDARY = 1
EMPTY = 0


class FillStats:
    """Simple container for fill execution statistics."""

    def __init__(self):
        self.visited = 0
        self.filled = 0
        self.max_stack = 0
        self.elapsed_ms = 0.0
        self.start = (0, 0)
        self.algorithm = ""

    def to_dict(self):
        """Convert stats to plain dict for UI and tests."""
        return {
            "visited": self.visited,
            "filled": self.filled,
            "max_stack": self.max_stack,
            "elapsed_ms": round(self.elapsed_ms, 3),
            "start": self.start,
            "algorithm": self.algorithm,
        }


def in_bounds(grid, x, y):
    """Check grid bounds safely."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def neighbors_4(x, y):
    """Return 4-direction neighbors (right, left, down, up)."""
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def neighbors_8(x, y):
    """Return 8-direction neighbors (includes diagonals)."""
    return [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
    ]


def boundary_fill(grid, sx, sy, fill_color, boundary_color=BOUNDARY,
                  connectivity=4, trace=None):
    """Boundary Fill with explicit stack."""
    import time
    stats = FillStats()
    stats.algorithm = "Boundary Fill"
    stats.start = (sx, sy)
    t0 = time.perf_counter()
    h = len(grid)
    w = len(grid[0]) if h else 0
    if not in_bounds(grid, sx, sy):
        stats.elapsed_ms = 0.0
        return stats
    if grid[sy][sx] == boundary_color or grid[sy][sx] == fill_color:
        stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return stats
    pick = neighbors_4 if connectivity == 4 else neighbors_8
    stack = [(sx, sy)]
    seen = set([(sx, sy)])
    while stack:
        if len(stack) > stats.max_stack:
            stats.max_stack = len(stack)
        x, y = stack.pop()
        if not in_bounds(grid, x, y):
            continue
        cur = grid[y][x]
        stats.visited += 1
        if trace is not None:
            trace.append((x, y))
        if cur == boundary_color or cur == fill_color:
            continue
        grid[y][x] = fill_color
        stats.filled += 1
        for nx, ny in pick(x, y):
            if (nx, ny) not in seen and in_bounds(grid, nx, ny):
                seen.add((nx, ny))
                stack.append((nx, ny))
    stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return stats


def flood_fill(grid, sx, sy, fill_color, connectivity=4, trace=None):
    """Flood Fill with explicit stack."""
    stats = FillStats()
    stats.algorithm = "Flood Fill"
    stats.start = (sx, sy)
    t0 = time.perf_counter()
    if not in_bounds(grid, sx, sy):
        stats.elapsed_ms = 0.0
        return stats
    target = grid[sy][sx]
    if target == BOUNDARY or target == fill_color:
        stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return stats
    pick = neighbors_4 if connectivity == 4 else neighbors_8
    stack = [(sx, sy)]
    seen = set([(sx, sy)])
    while stack:
        if len(stack) > stats.max_stack:
            stats.max_stack = len(stack)
        x, y = stack.pop()
        if not in_bounds(grid, x, y):
            continue
        stats.visited += 1
        if trace is not None:
            trace.append((x, y))
        if grid[y][x] != target:
            continue
        grid[y][x] = fill_color
        stats.filled += 1
        for nx, ny in pick(x, y):
            if (nx, ny) not in seen and in_bounds(grid, nx, ny):
                seen.add((nx, ny))
                stack.append((nx, ny))
    stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return stats




def scanline_flood_fill(grid, sx, sy, fill_color):
    """Scanline Flood Fill for comparison in report."""
    from collections import deque
    stats = FillStats()
    stats.algorithm = "Scanline Flood Fill"
    stats.start = (sx, sy)
    t0 = time.perf_counter()
    h = len(grid)
    w = len(grid[0]) if h else 0
    if not in_bounds(grid, sx, sy):
        stats.elapsed_ms = 0.0
        return stats
    target = grid[sy][sx]
    if target == BOUNDARY or target == fill_color:
        stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return stats
    queue = deque([(sx, sy)])
    while queue:
        if len(queue) > stats.max_stack:
            stats.max_stack = len(queue)
        x, y = queue.popleft()
        if not in_bounds(grid, x, y) or grid[y][x] != target:
            continue
        xl = x
        while xl >= 0 and grid[y][xl] == target:
            xl -= 1
        xl += 1
        xr = x
        while xr < w and grid[y][xr] == target:
            xr += 1
        xr -= 1
        for xi in range(xl, xr + 1):
            grid[y][xi] = fill_color
            stats.filled += 1
            stats.visited += 1
        for ny in (y - 1, y + 1):
            if 0 <= ny < h:
                xi = xl
                while xi <= xr:
                    if grid[ny][xi] == target:
                        queue.append((xi, ny))
                        while xi <= xr and grid[ny][xi] == target:
                            xi += 1
                    else:
                        xi += 1
    stats.elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return stats

