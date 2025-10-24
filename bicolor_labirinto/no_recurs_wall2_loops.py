import csv
import random
import numpy as np
import matplotlib.pyplot as plt


def genera_labirinto_iter(larghezza_celle, altezza_celle, prob_loop=0.04):
    """
    Genera un labirinto con camminamenti e muri larghi 1.
    - Prima genera un labirinto perfetto (tutte le celle collegate)
    - Poi aggiunge loop interni con probabilità controllata.
    """
    W = larghezza_celle * 2 + 1
    H = altezza_celle * 2 + 1

    maze = np.zeros((H, W), dtype=int)
    visited = [[False] * larghezza_celle for _ in range(altezza_celle)]

    def carve(cx, cy):
        x0, y0 = cx * 2 + 1, cy * 2 + 1
        maze[y0, x0] = 1

    # --- Fase 1: labirinto perfetto (DFS)
    stack = [(0, 0)]
    visited[0][0] = True
    carve(0, 0)

    while stack:
        cx, cy = stack[-1]
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(dirs)

        found = False
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < larghezza_celle
                and 0 <= ny < altezza_celle
                and not visited[ny][nx]
            ):
                # scava muro intermedio
                wx, wy = cx * 2 + 1 + dx, cy * 2 + 1 + dy
                maze[wy, wx] = 1
                visited[ny][nx] = True
                carve(nx, ny)
                stack.append((nx, ny))
                found = True
                break
        if not found:
            stack.pop()

    # --- Fase 2: aggiungi loop (collegamenti extra)
    for cy in range(1, altezza_celle - 1):
        for cx in range(1, larghezza_celle - 1):
            if random.random() < prob_loop:
                dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                wx, wy = cx * 2 + 1 + dx, cy * 2 + 1 + dy
                if 0 <= wx < W and 0 <= wy < H:
                    # Apri muro interno solo se separa due celle già scavate
                    if maze[wy, wx] == 0:
                        x1, y1 = cx * 2 + 1, cy * 2 + 1
                        x2, y2 = x1 + 2 * dx, y1 + 2 * dy
                        if (
                            0 <= x2 < W
                            and 0 <= y2 < H
                            and maze[y1, x1] == 1
                            and maze[y2, x2] == 1
                        ):
                            maze[wy, wx] = 1  # apri varco -> loop interno

    return maze


def salva_labirinto_csv(sx, sy, matrice, filename):
    flat = matrice.T.flatten()
    flat = np.append(flat, sx * 2 + 1)
    flat = np.append(flat, sy * 2 + 1)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


# --- Esempio di utilizzo
sx, sy = 80, 80
lab = genera_labirinto_iter(sx, sy, prob_loop=0.08)  # 5% di probabilità di loop

salva_labirinto_csv(sx, sy, lab, "labirinto_con_loop.csv")

plt.figure(figsize=(7, 7))
plt.pcolormesh(1 - lab, cmap="gray_r", edgecolors="none")
plt.axis("equal")
plt.axis("off")
plt.show()
