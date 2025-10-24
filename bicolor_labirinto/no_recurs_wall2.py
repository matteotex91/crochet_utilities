import csv
import random
import numpy as np
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

    return maze


def salva_labirinto_csv(sx, sy, matrice, filename):
    """
    Salva la matrice linearizzata (righe concatenate) in un CSV a singola riga.
    """
    flat = matrice.T.flatten()
    flat = np.append(flat, sx * 2 + 1)
    flat = np.append(flat, sy * 2 + 1)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


# esempio di utilizzo
sx = 130
sy = 150
lab = genera_labirinto_iter(sx, sy)

salva_labirinto_csv(sx, sy, lab, "labirinto_1x1.csv")

# Visualizzazione (facoltativa)
plt.figure(figsize=(6, 6))
plt.pcolormesh(lab, cmap="gray_r", edgecolors="none")
plt.axis("equal")
plt.axis("off")
plt.show()
