import random
import numpy as np
import matplotlib.pyplot as plt


def genera_labirinto(larghezza_celle, altezza_celle):
    """
    Genera un labirinto con camminamenti larghi 2 e muri larghi 1.
    larghezza_celle, altezza_celle = dimensione della griglia logica.
    Restituisce una matrice numpy di 0 (muri) e 1 (camminamenti).
    """

    # dimensioni reali della matrice
    W = larghezza_celle * 3 + 1
    H = altezza_celle * 3 + 1

    # inizializza tutto a muro
    maze = np.zeros((H, W), dtype=int)

    # mappa per visitati
    visited = [[False] * larghezza_celle for _ in range(altezza_celle)]

    def carve(cx, cy):
        """Scava un blocco 2x2 nella posizione logica (cx, cy)."""
        x0, y0 = cx * 3 + 1, cy * 3 + 1
        maze[y0 : y0 + 2, x0 : x0 + 2] = 1

    def dfs(cx, cy):
        visited[cy][cx] = True
        carve(cx, cy)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < larghezza_celle
                and 0 <= ny < altezza_celle
                and not visited[ny][nx]
            ):
                # apri il muro tra le celle
                wx, wy = cx * 3 + 2 * dx + 1, cy * 3 + 2 * dy + 1
                maze[wy : wy + 2, wx : wx + 2] = 1
                dfs(nx, ny)

    # inizia dalla cella (0,0)
    dfs(0, 0)

    return maze


# esempio di utilizzo
lab = genera_labirinto(25, 25)  # 6x4 celle logiche
plt.pcolormesh(lab)
plt.show()
