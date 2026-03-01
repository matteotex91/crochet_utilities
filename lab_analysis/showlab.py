from __future__ import annotations

import argparse
import csv
import heapq
import sys
import numpy as np
from tqdm import tqdm
from dataclasses import dataclass
import matplotlib.pyplot as plt
from typing import Dict, Iterable, List, Optional, Tuple


Coord = Tuple[int, int]
Matrix = List[List[int]]


@dataclass
class Maze:
    rows: int
    cols: int
    walls_v: Matrix  # [rows][cols+1]
    walls_h: Matrix  # [rows+1][cols]


def parse_coord(text: str) -> Coord:
    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError(f"Coordinata non valida: {text}. Usa formato riga,colonna")
    return int(parts[0]), int(parts[1])


def load_maze_from_csv(path: str) -> Maze:
    with open(path, "r", newline="", encoding="utf-8") as f:
        rows_data = [row for row in csv.reader(f) if row]

    if len(rows_data) < 4:
        raise ValueError("CSV non valido: righe insufficienti")

    if rows_data[0][0] != "rows" or rows_data[1][0] != "cols":
        raise ValueError("CSV non valido: intestazioni rows/cols mancanti")

    rows = int(rows_data[0][1])
    cols = int(rows_data[1][1])

    idx = 2
    if rows_data[idx][0] != "vertical_walls":
        raise ValueError("CSV non valido: sezione vertical_walls mancante")
    v_rows = int(rows_data[idx][1])
    v_cols = int(rows_data[idx][2])
    idx += 1

    walls_v: Matrix = []
    for _ in range(v_rows):
        row = [int(x) for x in rows_data[idx]]
        walls_v.append(row)
        idx += 1

    if rows_data[idx][0] != "horizontal_walls":
        raise ValueError("CSV non valido: sezione horizontal_walls mancante")
    h_rows = int(rows_data[idx][1])
    h_cols = int(rows_data[idx][2])
    idx += 1

    walls_h: Matrix = []
    for _ in range(h_rows):
        row = [int(x) for x in rows_data[idx]]
        walls_h.append(row)
        idx += 1

    if v_rows != rows or v_cols != cols + 1:
        raise ValueError("Dimensioni vertical_walls non coerenti")
    if h_rows != rows + 1 or h_cols != cols:
        raise ValueError("Dimensioni horizontal_walls non coerenti")

    return Maze(rows=rows, cols=cols, walls_v=walls_v, walls_h=walls_h)


def valid_coord(maze: Maze, coord: Coord) -> bool:
    r, c = coord
    return 0 <= r < maze.rows and 0 <= c < maze.cols


def neighbors(maze: Maze, node: Coord) -> Iterable[Coord]:
    r, c = node

    if r > 0 and maze.walls_h[r][c] == 0:
        yield (r - 1, c)
    if r < maze.rows - 1 and maze.walls_h[r + 1][c] == 0:
        yield (r + 1, c)
    if c > 0 and maze.walls_v[r][c] == 0:
        yield (r, c - 1)
    if c < maze.cols - 1 and maze.walls_v[r][c + 1] == 0:
        yield (r, c + 1)


def heuristic(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: Dict[Coord, Coord], current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar_shortest_path(maze: Maze, start: Coord, goal: Coord) -> Optional[List[Coord]]:
    if not valid_coord(maze, start) or not valid_coord(maze, goal):
        raise ValueError("Start/goal fuori dai limiti del labirinto")

    open_heap: List[Tuple[int, int, Coord]] = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start))

    came_from: Dict[Coord, Coord] = {}
    g_score: Dict[Coord, int] = {start: 0}
    closed = set()

    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for nb in neighbors(maze, current):
            tentative_g = current_g + 1
            if tentative_g < g_score.get(nb, 10**15):
                came_from[nb] = current
                g_score[nb] = tentative_g
                f = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_heap, (f, tentative_g, nb))

    return None


def print_centrality(
    maze: Maze,
    wall_px: int = 1,
    cell_px: int = 1,
    path: Optional[List[Coord]] = None,
    path_px: int = 1,
) -> None:
    if wall_px <= 0 or cell_px <= 0 or path_px <= 0:
        raise ValueError("wall_px, cell_px, path_px devono essere > 0")

    height = maze.rows * cell_px + (maze.rows + 1) * wall_px
    width = maze.cols * cell_px + (maze.cols + 1) * wall_px
    centrality = np.zeros_like(maze.walls_h)

    for i0 in tqdm(range(maze.rows)):
        for j0 in range(maze.cols):
            for i1 in range(maze.rows):
                for j1 in range(maze.cols):
                    if not (i0 == i1 and j0 == j1):
                        p = astar_shortest_path(
                            maze=maze, start=(i0, j0), goal=(i1, j1)
                        )
                        for step in p:  # type: ignore
                            centrality[step[0], step[1]] += 1

    plt.pcolormesh(centrality)
    plt.show()
    print("stop here")


def maze_to_rgb(
    maze: Maze,
    wall_px: int = 1,
    cell_px: int = 1,
    path: Optional[List[Coord]] = None,
    path_px: int = 1,
) -> List[List[List[int]]]:
    if wall_px <= 0 or cell_px <= 0 or path_px <= 0:
        raise ValueError("wall_px, cell_px, path_px devono essere > 0")

    height = maze.rows * cell_px + (maze.rows + 1) * wall_px
    width = maze.cols * cell_px + (maze.cols + 1) * wall_px

    # 0=nero (muri), 255=bianco (corridoi)
    gray: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]

    def fill_gray(y0: int, y1: int, x0: int, x1: int, value: int) -> None:
        for y in range(max(0, y0), min(height, y1)):
            row = gray[y]
            for x in range(max(0, x0), min(width, x1)):
                row[x] = value

    # Cella aperta
    for r in range(maze.rows):
        y0 = wall_px + r * (cell_px + wall_px)
        y1 = y0 + cell_px
        for c in range(maze.cols):
            x0 = wall_px + c * (cell_px + wall_px)
            x1 = x0 + cell_px
            fill_gray(y0, y1, x0, x1, 255)

    # Aperture muri verticali
    for r in range(maze.rows):
        y0 = wall_px + r * (cell_px + wall_px)
        y1 = y0 + cell_px
        for c in range(maze.cols + 1):
            if maze.walls_v[r][c] == 0:
                x0 = c * (cell_px + wall_px)
                x1 = x0 + wall_px
                fill_gray(y0, y1, x0, x1, 255)

    # Aperture muri orizzontali
    for r in range(maze.rows + 1):
        y0 = r * (cell_px + wall_px)
        y1 = y0 + wall_px
        for c in range(maze.cols):
            if maze.walls_h[r][c] == 0:
                x0 = wall_px + c * (cell_px + wall_px)
                x1 = x0 + cell_px
                fill_gray(y0, y1, x0, x1, 255)

    rgb: List[List[List[int]]] = [[[v, v, v] for v in row] for row in gray]

    if path:
        half = max(path_px // 2, 0)

        def center(cell: Coord) -> Coord:
            rr, cc = cell
            cy = wall_px + rr * (cell_px + wall_px) + (cell_px // 2)
            cx = wall_px + cc * (cell_px + wall_px) + (cell_px // 2)
            return cy, cx

        def fill_rgb(
            y0: int, y1: int, x0: int, x1: int, color: Tuple[int, int, int]
        ) -> None:
            rch, gch, bch = color
            for y in range(max(0, y0), min(height, y1)):
                row = rgb[y]
                for x in range(max(0, x0), min(width, x1)):
                    row[x][0] = rch
                    row[x][1] = gch
                    row[x][2] = bch

        def paint_segment(p1: Coord, p2: Coord, color: Tuple[int, int, int]) -> None:
            y1, x1 = p1
            y2, x2 = p2
            if y1 == y2:
                xa, xb = sorted((x1, x2))
                fill_rgb(y1 - half, y1 + half + 1, xa, xb + 1, color)
            elif x1 == x2:
                ya, yb = sorted((y1, y2))
                fill_rgb(ya, yb + 1, x1 - half, x1 + half + 1, color)

        red = (220, 20, 60)
        green = (46, 204, 113)
        blue = (52, 152, 219)

        centers = [center(cell) for cell in path]
        for i in range(len(centers) - 1):
            paint_segment(centers[i], centers[i + 1], red)

        # Evidenzia start/goal
        sy, sx = centers[0]
        gy, gx = centers[-1]
        fill_rgb(sy - half, sy + half + 1, sx - half, sx + half + 1, green)
        fill_rgb(gy - half, gy + half + 1, gx - half, gx + half + 1, blue)

    return rgb


def maze_to_rgb_centrality(
    maze: Maze,
    wall_px: int = 1,
    cell_px: int = 1,
    path: Optional[List[Coord]] = None,
    path_px: int = 1,
) -> List[List[List[int]]]:
    if wall_px <= 0 or cell_px <= 0 or path_px <= 0:
        raise ValueError("wall_px, cell_px, path_px devono essere > 0")

    centrality = np.zeros_like(maze.walls_h)

    for i0 in tqdm(range(maze.rows)):
        for j0 in range(maze.cols):
            for i1 in range(maze.rows):
                for j1 in range(maze.cols):
                    if not (i0 == i1 and j0 == j1):
                        p = astar_shortest_path(
                            maze=maze, start=(i0, j0), goal=(i1, j1)
                        )
                        for step in p:  # type: ignore
                            centrality[step[0], step[1]] += 1
    centrality = np.int_(centrality * 255 / np.max(centrality))

    height = maze.rows * cell_px + (maze.rows + 1) * wall_px
    width = maze.cols * cell_px + (maze.cols + 1) * wall_px

    # 0=nero (muri), 255=bianco (corridoi)
    gray: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]

    def fill_gray(y0: int, y1: int, x0: int, x1: int, value: int) -> None:
        for y in range(max(0, y0), min(height, y1)):
            row = gray[y]
            for x in range(max(0, x0), min(width, x1)):
                row[x] = value

    # Cella aperta
    for r in range(maze.rows):
        y0 = wall_px + r * (cell_px + wall_px)
        y1 = y0 + cell_px
        for c in range(maze.cols):
            x0 = wall_px + c * (cell_px + wall_px)
            x1 = x0 + cell_px
            fill_gray(y0, y1, x0, x1, centrality[r][c])

    # Aperture muri verticali
    for r in range(maze.rows):
        y0 = wall_px + r * (cell_px + wall_px)
        y1 = y0 + cell_px
        for c in range(maze.cols + 1):
            if maze.walls_v[r][c] == 0:
                x0 = c * (cell_px + wall_px)
                x1 = x0 + wall_px
                fill_gray(y0, y1, x0, x1, centrality[r][c])

    # Aperture muri orizzontali
    for r in range(maze.rows + 1):
        y0 = r * (cell_px + wall_px)
        y1 = y0 + wall_px
        for c in range(maze.cols):
            if maze.walls_h[r][c] == 0:
                x0 = wall_px + c * (cell_px + wall_px)
                x1 = x0 + cell_px
                fill_gray(y0, y1, x0, x1, centrality[r][c])

    plt.pcolormesh(gray)
    plt.show()
    rgb: List[List[List[int]]] = [[[v, v, v] for v in row] for row in gray]

    if path:
        half = max(path_px // 2, 0)

        def center(cell: Coord) -> Coord:
            rr, cc = cell
            cy = wall_px + rr * (cell_px + wall_px) + (cell_px // 2)
            cx = wall_px + cc * (cell_px + wall_px) + (cell_px // 2)
            return cy, cx

        def fill_rgb(
            y0: int, y1: int, x0: int, x1: int, color: Tuple[int, int, int]
        ) -> None:
            rch, gch, bch = color
            for y in range(max(0, y0), min(height, y1)):
                row = rgb[y]
                for x in range(max(0, x0), min(width, x1)):
                    row[x][0] = rch
                    row[x][1] = gch
                    row[x][2] = bch

        def paint_segment(p1: Coord, p2: Coord, color: Tuple[int, int, int]) -> None:
            y1, x1 = p1
            y2, x2 = p2
            if y1 == y2:
                xa, xb = sorted((x1, x2))
                fill_rgb(y1 - half, y1 + half + 1, xa, xb + 1, color)
            elif x1 == x2:
                ya, yb = sorted((y1, y2))
                fill_rgb(ya, yb + 1, x1 - half, x1 + half + 1, color)

        red = (220, 20, 60)
        green = (46, 204, 113)
        blue = (52, 152, 219)

        centers = [center(cell) for cell in path]
        for i in range(len(centers) - 1):
            paint_segment(centers[i], centers[i + 1], red)

        # Evidenzia start/goal
        sy, sx = centers[0]
        gy, gx = centers[-1]
        fill_rgb(sy - half, sy + half + 1, sx - half, sx + half + 1, green)
        fill_rgb(gy - half, gy + half + 1, gx - half, gx + half + 1, blue)

    return rgb


def plot_maze(
    maze: Maze,
    wall_px: int = 1,
    cell_px: int = 1,
    path: Optional[List[Coord]] = None,
    path_px: int = 1,
    dpi: int = 100,
    save_png: Optional[str] = None,
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "matplotlib non installato. Installa con: pip install matplotlib"
        ) from exc

    ################################################
    # img = maze_paths_to_rgb(
    #     maze, wall_px=wall_px, cell_px=cell_px, path=path, path_px=path_px
    # )
    ################################################
    img = maze_to_rgb_centrality(
        maze, wall_px=wall_px, cell_px=cell_px, path=path, path_px=path_px
    )

    plt.imshow(img)

    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualizza un labirinto CSV e calcola percorso A*."
    )
    parser.add_argument(
        "--csv",
        default="lab_analysis/labirinto_200x200.csv",
        help="Percorso del file CSV",
    )
    parser.add_argument("--wall-px", type=int, default=1, help="Spessore muri in pixel")
    parser.add_argument(
        "--cell-px", type=int, default=1, help="Spessore corridoi in pixel"
    )
    parser.add_argument(
        "--path-px", type=int, default=1, help="Spessore tracciato soluzione in pixel"
    )
    parser.add_argument("--start", type=str, help="Start: riga,colonna")
    parser.add_argument("--goal", type=str, help="Goal: riga,colonna")
    parser.add_argument("--save-png", type=str, help="Salva immagine in PNG")
    args = parser.parse_args()

    maze = load_maze_from_csv(args.csv)

    solution: Optional[List[Coord]] = None
    if args.start is not None or args.goal is not None:
        if args.start is None or args.goal is None:
            raise ValueError("Specifica sia --start che --goal")
        start = parse_coord(args.start)
        goal = parse_coord(args.goal)
        solution = astar_shortest_path(maze, start, goal)
        if solution is None:
            print("Nessun percorso trovato")
        else:
            print(f"Percorso trovato: {len(solution) - 1} passi, {len(solution)} celle")

    plot_maze(
        maze,
        wall_px=args.wall_px,
        cell_px=args.cell_px,
        path=solution,
        path_px=args.path_px,
        save_png=args.save_png,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        sys.exit(1)
