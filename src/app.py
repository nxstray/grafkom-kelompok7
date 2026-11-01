"""Tkinter coloring demo. Run with: python src/app.py."""
# English comments only in this file.

import copy
import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fill_algorithms import (
    boundary_fill, flood_fill, scanline_flood_fill, BOUNDARY, EMPTY,
)
from maps import MAPS

COLS, ROWS, CELL = 40, 26, 18
PALETTE = {0: "white", 1: "black", 2: "red", 3: "green",
           4: "blue", 5: "yellow", 6: "orange", 7: "purple"}
NAMES = {0: "empty", 1: "wall", 2: "red", 3: "green",
         4: "blue", 5: "yellow", 6: "orange", 7: "purple"}


class App:
    """Main window with canvas, buttons, and stats."""

    def __init__(self, root):
        self.root = root
        root.title("Kelompok 6 - Boundary Fill dan Flood Fill")
        self.map_name = tk.StringVar(value="rooms")
        self.algo = tk.StringVar(value="Flood Fill")
        self.conn = tk.IntVar(value=4)
        self.color = tk.IntVar(value=2)
        self.speed = tk.IntVar(value=1)
        self.grid = []
        self.history = []
        self.trace = []
        self.trace_idx = 0
        self.after_id = None
        self.build_widgets()
        self.load_map()

    def build_widgets(self):
        """Build control panel and canvas."""
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=6, pady=4)
        tk.Label(top, text="Map:").pack(side="left")
        for name in ("rooms", "circle", "leak"):
            tk.Radiobutton(top, text=name, value=name,
                           variable=self.map_name,
                           command=self.load_map).pack(side="left")
        tk.Label(top, text="Algo:").pack(side="left")
        for name in ("Flood Fill", "Boundary Fill", "Scanline"):
            tk.Radiobutton(top, text=name, value=name,
                           variable=self.algo).pack(side="left")
        mid = tk.Frame(self.root)
        mid.pack(fill="x", padx=6)
        tk.Label(mid, text="Conn:").pack(side="left")
        tk.Radiobutton(mid, text="4", value=4,
                       variable=self.conn).pack(side="left")
        tk.Radiobutton(mid, text="8", value=8,
                       variable=self.conn).pack(side="left")
        tk.Label(mid, text="Color:").pack(side="left")
        for code in (2, 3, 4, 5, 6, 7):
            tk.Radiobutton(mid, text=NAMES[code], value=code,
                           variable=self.color).pack(side="left")
        tk.Label(mid, text="Anim:").pack(side="left")
        tk.Scale(mid, from_=0, to=5, orient="h",
                 variable=self.speed).pack(side="left")
        btn = tk.Frame(self.root)
        btn.pack(fill="x", padx=6, pady=2)
        tk.Button(btn, text="Reset", command=self.load_map).pack(side="left")
        tk.Button(btn, text="Undo", command=self.undo).pack(side="left")
        tk.Button(btn, text="Play trace",
                  command=self.play).pack(side="left")
        tk.Button(btn, text="Stop",
                  command=self.stop).pack(side="left")
        tk.Button(btn, text="Auto fill 3 spots",
                  command=self.auto).pack(side="left")
        self.canvas = tk.Canvas(self.root, width=COLS * CELL,
                                height=ROWS * CELL, bg="gray")
        self.canvas.pack(padx=6, pady=4)
        self.canvas.bind("<Button-1>", self.click)
        self.info = tk.Label(self.root, text="Click a room to fill.",
                             anchor="w", justify="left")
        self.info.pack(fill="x", padx=6)
        self.stat = tk.Label(self.root, text="-", anchor="w")
        self.stat.pack(fill="x", padx=6, pady=4)
    def load_map(self):
        """Load fresh grid from selected map."""
        self.stop()
        data = MAPS[self.map_name.get()]()
        self.grid = data["grid"]
        self.spots = data["spots"]
        self.history = []
        self.trace = []
        self.draw_all()
        self.stat.config(text="Map reset. Click canvas to fill.")
        self.info.config(
            text="Input: mouse click. Process: " + self.algo.get()
            + ". Output: colored area plus stats.")

    def draw_all(self):
        """Draw full grid on canvas."""
        self.canvas.delete("all")
        for y in range(ROWS):
            for x in range(COLS):
                v = self.grid[y][x]
                self.canvas.create_rectangle(
                    x * CELL, y * CELL, (x + 1) * CELL, (y + 1) * CELL,
                    fill=PALETTE.get(v, "white"), outline="#cccccc")

    def draw_trace_step(self):
        """Draw one animation step then schedule next."""
        if self.trace_idx >= len(self.trace):
            self.draw_all()
            return
        x, y = self.trace[self.trace_idx]
        v = self.grid[y][x]
        self.canvas.create_rectangle(
            x * CELL, y * CELL, (x + 1) * CELL, (y + 1) * CELL,
            fill=PALETTE.get(v, "white"), outline="#cccccc")
        self.trace_idx += 1
        delay = max(0, 60 - self.speed.get() * 12)
        self.after_id = self.root.after(delay, self.draw_trace_step)

    def click(self, event):
        """Handle mouse click as fill input point."""
        x = event.x // CELL
        y = event.y // CELL
        self.run_fill(x, y)

    def run_fill(self, x, y):
        """Run selected algorithm and show stats."""
        if not (0 <= x < COLS and 0 <= y < ROWS):
            return
        self.stop()
        self.history.append(copy.deepcopy(self.grid))
        if len(self.history) > 20:
            self.history.pop(0)
        name = self.algo.get()
        c = self.color.get()
        self.trace = []
        if name == "Boundary Fill":
            st = boundary_fill(self.grid, x, y, c,
                               connectivity=self.conn.get(),
                               trace=self.trace)
        elif name == "Scanline":
            st = scanline_flood_fill(self.grid, x, y, c)
            self.trace = []
        else:
            st = flood_fill(self.grid, x, y, c,
                            connectivity=self.conn.get(),
                            trace=self.trace)
        d = st.as_dict() if hasattr(st, "as_dict") else st.to_dict()
        self.stat.config(text=(
            "%s start=(%d,%d) filled=%d visited=%d "
            "maxstack=%d time=%s ms conn=%d color=%s" % (
                d["algorithm"], x, y, d["filled"], d["visited"],
                d["max_stack"], d["elapsed_ms"],
                self.conn.get(), NAMES[c])))
        if self.speed.get() > 0 and self.trace:
            self.trace_idx = 0
            self.draw_trace_step()
        else:
            self.draw_all()

    def play(self):
        """Replay last trace animation."""
        self.stop()
        if self.trace:
            self.trace_idx = 0
            self.draw_trace_step()

    def stop(self):
        """Stop running animation."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def undo(self):
        """Restore grid before last fill."""
        self.stop()
        if self.history:
            self.grid = self.history.pop()
            self.draw_all()
            self.stat.config(text="Undo done.")

    def auto(self):
        """Fill sample spots for demo and screenshots."""
        for (sx, sy) in self.spots:
            self.run_fill(sx, sy)
            self.root.update()
        self.draw_all()


def main():
    """Start Tkinter app."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
