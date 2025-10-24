import csv
import numpy as np


def import_lab(path) -> np.ndarray:
    lab = []
    with open(path) as file:
        csvreader = csv.reader(file, delimiter=" ")
        for row in csvreader:
            for s in row:
                for i in s.split(","):
                    lab.append(int(i))
    sx = lab[-1]
    sy = lab[-2]
    lab = np.array(lab[:-2]).reshape((sx, sy))
    return lab


def generate_mosaic(lab: np.ndarray) -> np.ndarray:
    mosaic = np.empty_like(lab, dtype=str)
    for i in range(1, lab.shape[0] - 1):
        current_row_color = np.mod(i, 2)
        for j in range(lab.shape[1]):
            if mosaic[i - 1, j] == "o" and lab[i, j] != current_row_color:
                raise ValueError((i, j))
            elif mosaic[i - 1, j] == "o":
                mosaic[i, j] = "T"
            elif lab[i, j] != current_row_color:
                mosaic[i, j] = "o"
            else:
                mosaic[i, j] = "+"
    return mosaic


def longest_chain(mosaic) -> int:
    o_count = 0
    longest_chain = 0
    for i in range(1, mosaic.shape[0] - 1):
        o_count = 0
        for j in range(mosaic.shape[1]):
            if mosaic[i, j] == "o":
                o_count += 1
            else:
                o_count = 0
            longest_chain = longest_chain if longest_chain > o_count else o_count
    return o_count


if __name__ == "__main__":
    lab_path = "/Users/matteotessarolo/Documents/coding/crochet_utilities/labirinto_con_loop.csv"
    lab = import_lab(lab_path)
    mosaic = generate_mosaic(lab)
    longest_o_chain = longest_chain(mosaic)
    print(np.sum(lab) / (lab.shape[0] * lab.shape[1]))
    print("stop here")
