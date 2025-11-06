import csv
import numpy as np

pattern = []

with open(
    "/Users/matteotessarolo/Documents/coding/crochet_utilities/carpet/data.csv"
) as file:
    csvreader = csv.reader(file, delimiter=" ")
    for row in csvreader:
        print(np.size(row[0].split("\t")))
        p_row = []
        for i in row[0].split("\t"):
            p_row.append(0 if i == "0" else 1)
        pattern.append(p_row)

pattern = np.array(pattern)
print("stop here")

rows = pattern.shape[0]
cols = pattern.shape[1]

stitches = np.zeros(shape=(rows + 2, cols), dtype=np.int32)
# 0 -> colore 1
# 1 -> colore 2
# +2 -> +
# +4 -> -
# +8 -> F
# +16 -> B
for i in range(rows):
    for j in range(cols):
        stitches[i + 2, j] = pattern[i, j]
        if i % 2 == 1:
            if pattern[i, j] == 1:
                stitches[i, j] += 8
                stitches[i + 1, j] += 8
                stitches[i + 2, j] += 2
            else:
                stitches[i + 2, j] += 2
        else:
            if pattern[i, j] == 0:
                stitches[i, j] += 16
                stitches[i + 1, j] += 16
                stitches[i + 2, j] += 4
            else:
                stitches[i + 2, j] += 2

print("stop here")


def salva_tappeto(matrice, filename):
    """
    Salva la matrice linearizzata (righe concatenate) in un CSV a singola riga.
    """
    sizex = matrice.shape[0]
    sizey = matrice.shape[1]
    flat = np.flip(
        np.flip(matrice, axis=0), axis=1
    ).flatten()  # linearizza in un array 1D
    flat = np.append(arr=flat, values=sizex)
    flat = np.append(arr=flat, values=sizey)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


salva_tappeto(
    stitches,
    "/Users/matteotessarolo/Documents/coding/crochet_utilities/carpet/tappeto.csv",
)
