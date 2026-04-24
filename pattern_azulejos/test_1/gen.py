import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import csv

# convertire : 1, 7, 11, 13, 14, 17 ,18


def gen_pattern(pic_n: int, negative: bool, pattern_size: int):

    # pic_n = 18
    # negative = True
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pic_path = current_dir + f"/pic{pic_n}.png"
    out_path = current_dir + f"/patterns/pic{pic_n}.png"
    out_csv_path = current_dir + f"/patterns_csv/pat{pic_n}.csv"
    # pattern_size = 120
    ptr = np.zeros((pattern_size, pattern_size))

    with Image.open(pic_path) as im:
        mono = (
            im.convert("L")
            .resize((pattern_size, pattern_size))
            .point(lambda p: 1 if p > 200 else 0)
        )
        # mono.show()
        for i in range(pattern_size):
            for j in range(pattern_size):
                if i % 2 == 0 and j % 2 == 0:
                    ptr[i, j] = 0
                elif i % 2 == 1 and j % 2 == 1:
                    ptr[i, j] = 1
                else:
                    ptr[i, j] = mono.im[i + j * pattern_size]

        with open(out_csv_path, "w+", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(ptr.astype(int))

        fig, ax = plt.subplots()
        ax.pcolormesh(ptr, cmap="Blues_r" if negative else "Blues")
        ax.axis("equal")

        plt.savefig(out_path, dpi=150)
        plt.show()


if __name__ == "__main__":
    pic_n = 18
    negative = True
    gen_pattern(pic_n=pic_n, negative=negative, pattern_size=121)
