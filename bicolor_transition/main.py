import matplotlib.pyplot as plt
import numpy as np
import random

N_rows = 25
N_circumference = 100

coeff = np.pi / N_rows
prob = (1 + np.cos(np.arange(N_rows) * coeff)) / 2
matrix = np.zeros((N_rows, N_circumference))

for ir, p in zip(range(N_rows), prob):
    for ic in range(N_circumference):
        matrix[ir, ic] = 1 if random.random() > p else 0

plt.pcolormesh(matrix)
plt.show()
