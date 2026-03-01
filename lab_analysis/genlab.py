from __future__ import annotations

import csv
import random
from typing import List, Tuple


Matrix = List[List[int]]


def generate_maze(
    rows: int, cols: int, seed: int | None = None
) -> Tuple[Matrix, Matrix]:
    """
    Genera un labirinto perfetto su griglia rows x cols.

    Restituisce:
    - walls_v: matrice muri verticali di dimensione [rows][cols + 1]
      walls_v[r][c] = 1 se il muro verticale tra le colonne c-1 e c esiste.
      (c=0 bordo sinistro, c=cols bordo destro)

    - walls_h: matrice muri orizzontali di dimensione [rows + 1][cols]
      walls_h[r][c] = 1 se il muro orizzontale tra le righe r-1 e r esiste.
      (r=0 bordo alto, r=rows bordo basso)
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("rows e cols devono essere > 0")

    rng = random.Random(seed)

    # Inizialmente tutti i muri sono presenti.
    walls_v: Matrix = [[1 for _ in range(cols + 1)] for _ in range(rows)]
    walls_h: Matrix = [[1 for _ in range(cols)] for _ in range(rows + 1)]

    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # DFS iterativo: per ogni cella, rimuove muri verso celle non visitate.
    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        r, c = stack[-1]

        neighbors = []
        if r > 0 and not visited[r - 1][c]:
            neighbors.append((r - 1, c, "N"))
        if r < rows - 1 and not visited[r + 1][c]:
            neighbors.append((r + 1, c, "S"))
        if c > 0 and not visited[r][c - 1]:
            neighbors.append((r, c - 1, "W"))
        if c < cols - 1 and not visited[r][c + 1]:
            neighbors.append((r, c + 1, "E"))

        if not neighbors:
            stack.pop()
            continue

        nr, nc, direction = rng.choice(neighbors)

        if direction == "N":
            walls_h[r][c] = 0
        elif direction == "S":
            walls_h[r + 1][c] = 0
        elif direction == "W":
            walls_v[r][c] = 0
        elif direction == "E":
            walls_v[r][c + 1] = 0

        visited[nr][nc] = True
        stack.append((nr, nc))

    return walls_v, walls_h


def save_maze_to_csv(
    path: str, rows: int, cols: int, walls_v: Matrix, walls_h: Matrix
) -> None:
    """
    Salva su CSV:
    - dimensioni
    - matrice muri verticali
    - matrice muri orizzontali
    """
    if len(walls_v) != rows or any(len(row) != cols + 1 for row in walls_v):
        raise ValueError("walls_v deve avere dimensioni [rows][cols+1]")
    if len(walls_h) != rows + 1 or any(len(row) != cols for row in walls_h):
        raise ValueError("walls_h deve avere dimensioni [rows+1][cols]")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["rows", rows])
        writer.writerow(["cols", cols])
        writer.writerow([])

        writer.writerow(["vertical_walls", rows, cols + 1])
        writer.writerows(walls_v)
        writer.writerow([])

        writer.writerow(["horizontal_walls", rows + 1, cols])
        writer.writerows(walls_h)


def main() -> None:
    # Esempio: labirinto 200x200
    rows, cols = 25, 25
    walls_v, walls_h = generate_maze(rows, cols, seed=42)
    save_maze_to_csv("lab_analysis/labirinto_200x200.csv", rows, cols, walls_v, walls_h)
    print("Labirinto salvato in labirinto_200x200.csv")


if __name__ == "__main__":
    main()
