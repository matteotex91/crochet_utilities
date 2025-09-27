import matplotlib.pyplot as plt
import numpy as np
import random

N_rows = 100
N_circumference = 100

target_rate = 0.5

curr_rate = 0
matrix = np.zeros((N_rows, N_circumference))


def condizione(x, y, x0, y0, x1, y1, spessore=1.5):
    """
    Restituisce True se il punto (x,y) appartiene alla linea infinita
    passante per (x0,y0)-(x1,y1), con spessore 1 o 2 pixel.
    """
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0 and dy == 0:
        # linea degenere (un punto)
        return x == x0 and y == y0

    # distanza punto–retta
    num = abs(dx * (y0 - y) - (x0 - x) * dy)
    den = np.linalg.norm([dx, dy])
    dist = num / den

    # appartiene alla linea se distanza ≤ spessore/2
    return dist <= spessore / 2.0


while curr_rate < target_rate:
    x0 = np.random.rand() * N_rows
    y0 = np.random.rand() * N_circumference

    x1 = np.random.rand() * N_rows
    y1 = np.random.rand() * N_circumference

    for i in range(N_rows):
        for j in range(N_circumference):
            if condizione(i, j, x0, y0, x1, y1):
                matrix[i, j] = 1
    curr_rate = 1.0 * np.sum(np.sum(matrix)) / (N_rows * N_circumference)


plt.pcolormesh(matrix)
plt.show()
