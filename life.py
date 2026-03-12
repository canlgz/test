#!/usr/bin/env python3
"""
Conway's Game of Life — Terminal Edition
按 Ctrl+C 退出 | Press Ctrl+C to quit
"""

import time
import os
import random
import sys

# --- 顏色 ANSI codes ---
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
DIM    = "\033[2m"

CELL_ALIVE = f"{GREEN}██{RESET}"
CELL_DEAD  = f"{DIM}  {RESET}"

PRESETS = {
    "glider": [
        (0, 1), (1, 2), (2, 0), (2, 1), (2, 2)
    ],
    "blinker": [
        (1, 0), (1, 1), (1, 2)
    ],
    "pulsar": [
        (2,4),(2,5),(2,6),(2,10),(2,11),(2,12),
        (4,2),(4,7),(4,9),(4,14),
        (5,2),(5,7),(5,9),(5,14),
        (6,2),(6,7),(6,9),(6,14),
        (7,4),(7,5),(7,6),(7,10),(7,11),(7,12),
        (9,4),(9,5),(9,6),(9,10),(9,11),(9,12),
        (10,2),(10,7),(10,9),(10,14),
        (11,2),(11,7),(11,9),(11,14),
        (12,2),(12,7),(12,9),(12,14),
        (14,4),(14,5),(14,6),(14,10),(14,11),(14,12),
    ],
    "random": [],
}


def get_terminal_size():
    size = os.get_terminal_size()
    # each cell is 2 chars wide
    cols = size.columns // 2
    rows = size.lines - 5  # leave room for header
    return max(rows, 10), max(cols, 20)


def make_grid(rows, cols, pattern="random", offset_r=0, offset_c=0):
    grid = set()
    if pattern == "random":
        for r in range(rows):
            for c in range(cols):
                if random.random() < 0.3:
                    grid.add((r, c))
    else:
        cells = PRESETS.get(pattern, [])
        for (r, c) in cells:
            grid.add((r + offset_r, c + offset_c))
    return grid


def step(grid, rows, cols):
    neighbor_count = {}
    for (r, c) in grid:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = (r + dr) % rows, (c + dc) % cols
                neighbor_count[(nr, nc)] = neighbor_count.get((nr, nc), 0) + 1

    new_grid = set()
    for cell, count in neighbor_count.items():
        if count == 3 or (count == 2 and cell in grid):
            new_grid.add(cell)
    return new_grid


def render(grid, rows, cols, generation, population):
    lines = []

    # Header
    lines.append(
        f"{BOLD}{CYAN}✦ Conway's Game of Life{RESET}  "
        f"{YELLOW}Gen:{RESET} {generation:>6}  "
        f"{YELLOW}Pop:{RESET} {population:>6}  "
        f"{DIM}Ctrl+C to quit{RESET}"
    )
    lines.append(f"{DIM}{'─' * (cols * 2)}{RESET}")

    # Grid
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            row_str += CELL_ALIVE if (r, c) in grid else CELL_DEAD
        lines.append(row_str)

    lines.append(f"{DIM}{'─' * (cols * 2)}{RESET}")

    # Move cursor to top and print all at once (flicker-free)
    sys.stdout.write("\033[H" + "\n".join(lines))
    sys.stdout.flush()


def choose_pattern():
    print(f"\n{BOLD}{CYAN}✦ Conway's Game of Life{RESET}\n")
    print("選擇起始圖案 / Choose a starting pattern:\n")
    options = list(PRESETS.keys())
    for i, name in enumerate(options, 1):
        print(f"  {YELLOW}{i}{RESET}. {name}")
    print()
    try:
        choice = input("輸入數字 (預設 random): ").strip()
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except (ValueError, EOFError):
        pass
    return "random"


def main():
    pattern = choose_pattern()

    # Hide cursor & clear screen
    sys.stdout.write("\033[?25l\033[2J")
    sys.stdout.flush()

    try:
        rows, cols = get_terminal_size()
        grid = make_grid(rows, cols, pattern,
                         offset_r=rows // 2 - 8,
                         offset_c=cols // 2 - 8)
        generation = 0

        while True:
            rows, cols = get_terminal_size()
            population = len(grid)
            render(grid, rows, cols, generation, population)
            grid = step(grid, rows, cols)
            generation += 1

            # Auto-seed if population dies out
            if population == 0:
                grid = make_grid(rows, cols, "random")
                generation = 0

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor & print goodbye
        sys.stdout.write("\033[?25h\033[2J\033[H")
        print(f"\n{BOLD}{CYAN}感謝遊玩！生命遊戲永遠繼續...{RESET}")
        print(f"{DIM}Thanks for playing. Life goes on...{RESET}\n")


if __name__ == "__main__":
    main()
