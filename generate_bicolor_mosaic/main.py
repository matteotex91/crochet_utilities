import csv
import numpy as np
import random
import matplotlib.pyplot as plt


def genera_labirinto_iter(larghezza_celle, altezza_celle):
    """
    Genera un labirinto con camminamenti e muri larghi 1.
    Versione iterativa (niente ricorsione).
    """
    W = larghezza_celle * 2 + 1
    H = altezza_celle * 2 + 1

    # inizializza tutto a muro (0)
    maze = np.zeros((H, W), dtype=int)
    visited = [[False] * larghezza_celle for _ in range(altezza_celle)]

    def carve(cx, cy):
        """Scava una singola cella nella posizione logica (cx, cy)."""
        x0, y0 = cx * 2 + 1, cy * 2 + 1
        maze[y0, x0] = 1  # cella "vuota"

    # stack per DFS iterativo
    stack = [(0, 0)]

    visited[0][0] = True

    carve(0, 0)

    while stack:
        cx, cy = stack[-1]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        found = False
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < larghezza_celle
                and 0 <= ny < altezza_celle
                and not visited[ny][nx]
            ):
                # rimuovi muro tra celle
                wx, wy = cx * 2 + 1 + dx, cy * 2 + 1 + dy
                maze[wy, wx] = 1  # apri passaggio

                visited[ny][nx] = True
                carve(nx, ny)
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()  # backtrack
    maze = np.array(maze)
    # maze = maze[1:-1, 1:-1]
    # maze = np.pad(maze, ((1, 1), (1, 1)), "constant", constant_values=((0, 0), (0, 0)))

    return maze


def generate_mosaic(lab: np.ndarray) -> np.ndarray:
    mosaic = np.empty_like(lab, dtype=str)
    for j in range(lab.shape[1]):
        mosaic[0, j] = "+"
    for i in range(1, lab.shape[0] - 1):
        current_row_color = np.mod(i, 2)
        for j in range(lab.shape[1]):
            if mosaic[i - 1, j] == "F" and lab[i, j] != current_row_color:
                raise ValueError((i, j))
            elif mosaic[i - 1, j] == "F":
                mosaic[i, j] = "B"
            elif lab[i, j] != current_row_color:
                mosaic[i, j] = "F"
            else:
                mosaic[i, j] = "+"
    return mosaic


def longest_chain(mosaic) -> int:
    o_count = 0
    longest_chain = 0
    for i in range(1, mosaic.shape[0] - 1):
        o_count = 0
        for j in range(mosaic.shape[1]):
            if mosaic[i, j] == "F":
                o_count += 1
            else:
                o_count = 0
            longest_chain = longest_chain if longest_chain > o_count else o_count
    return o_count


def salva_labirinto_csv(sx, sy, matrice, filename):
    """
    Salva la matrice linearizzata (righe concatenate) in un CSV a singola riga.
    """
    flat = matrice.flatten()  # linearizza in un array 1D
    flat = np.append(arr=flat, values=sx * 2 + 1)
    flat = np.append(arr=flat, values=sy * 2 + 1)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


if __name__ == "__main__":
    # esempio di utilizzo
    sx = 110  # instead of 130
    sy = 130  # instead of 150
    lab = genera_labirinto_iter(sx, sy)

    plt.figure(figsize=(6, 6))
    plt.pcolormesh(1 - lab, cmap="gray_r", edgecolors="none")
    plt.axis("equal")
    plt.axis("off")
    plt.show()

    lab_mosaic = "/Users/matteotessarolo/Documents/coding/crochet_utilities/coperta.csv"
    mosaic = generate_mosaic(lab)
    salva_labirinto_csv(sx, sy, mosaic, lab_mosaic)
    # longest_o_chain = longest_chain(mosaic)
    # print(np.sum(lab) / (lab.shape[0] * lab.shape[1]))
    # print("stop here")
