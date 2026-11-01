"""Unit tests for fill algorithms."""
# English comments only in this file.

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fill_algorithms import (
    boundary_fill, flood_fill, scanline_flood_fill, BOUNDARY, EMPTY,
)
from maps import MAPS


def small_box():
    """Make 6x6 box for fast tests."""
    g = [[EMPTY] * 6 for _ in range(6)]
    for x in range(6):
        g[0][x] = BOUNDARY
        g[5][x] = BOUNDARY
    for y in range(6):
        g[y][0] = BOUNDARY
        g[y][5] = BOUNDARY
    return g


class TestFill(unittest.TestCase):
    """Check main fill behavior."""

    def test_flood_fills_inside(self):
        """Flood fill colors inside area only."""
        g = small_box()
        st = flood_fill(g, 2, 2, 2)
        self.assertEqual(g[2][2], 2)
        self.assertEqual(g[0][0], BOUNDARY)
        self.assertGreater(st.filled, 0)

    def test_boundary_stops_at_wall(self):
        """Boundary fill never paints wall cells."""
        g = small_box()
        st = boundary_fill(g, 2, 2, 3)
        self.assertEqual(g[0][1], BOUNDARY)
        self.assertGreater(st.filled, 0)

    def test_scanline_same_area(self):
        """Scanline gives same area as flood fill."""
        g1 = small_box()
        g2 = small_box()
        s1 = scanline_flood_fill(g1, 2, 2, 4)
        s2 = flood_fill(g2, 2, 2, 4)
        self.assertEqual(s1.filled, s2.filled)

    def test_click_on_wall_does_nothing(self):
        """Click on wall keeps grid unchanged."""
        g = small_box()
        before = [row[:] for row in g]
        flood_fill(g, 0, 0, 5)
        self.assertEqual(g, before)

    def test_all_maps_load(self):
        """All demo maps build without error."""
        for name, func in MAPS.items():
            data = func()
            self.assertIn("grid", data)
            self.assertIn("spots", data)


if __name__ == "__main__":
    unittest.main()
