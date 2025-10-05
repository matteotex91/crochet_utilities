import csv
import random
import numpy as np
import matplotlib.pyplot as plt


def genera_labirinto_iter(larghezza_celle, altezza_celle):
    """
    Genera un labirinto con camminamenti larghi 2 e muri larghi 1.
    Versione iterativa (niente ricorsione).
    """
    W = larghezza_celle * 3 + 1
    H = altezza_celle * 3 + 1

    # inizializza tutto a muro (0)
    maze = np.zeros((H, W), dtype=int)
    visited = [[False] * larghezza_celle for _ in range(altezza_celle)]

    def carve(cx, cy):
        """Scava un blocco 2x2 nella posizione logica (cx, cy)."""
        x0, y0 = cx * 3 + 1, cy * 3 + 1
        maze[y0 : y0 + 2, x0 : x0 + 2] = 1

    # stack per DFS iterativo
    stack = [(0, 0)]
    visited[0][0] = True
    carve(0, 0)

    while stack:
        cx, cy = stack[-1]

        # trova vicini non visitati
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
                # apri muro tra celle
                wx, wy = (
                    cx * 3 + (dx == 1) * 2 + (dx == -1) * -1 + 1,
                    cy * 3 + (dy == 1) * 2 + (dy == -1) * -1 + 1,
                )
                maze[wy : wy + 2, wx : wx + 2] = 1

                visited[ny][nx] = True
                carve(nx, ny)
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()  # backtrack

    return maze


def salva_labirinto_csv(sx, sy, matrice, filename):
    """
    Salva la matrice linearizzata (righe concatenate) in un CSV a singola riga.
    """
    flat = matrice.T.flatten()  # linearizza in un array 1D
    flat = np.append(arr=flat, values=sx * 3 + 1)
    flat = np.append(arr=flat, values=sy * 3 + 1)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


# esempio di utilizzo
sx = 18
sy = 39
lab = genera_labirinto_iter(sx, sy)  # 6x4 celle logiche

salva_labirinto_csv(sx, sy, lab, "labirinto.csv")
# plt.pcolormesh(lab)
# plt.show()
