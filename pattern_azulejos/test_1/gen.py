import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm


def gen_pattern(pic_n: int, negative: bool = True, pattern_size: int = 120):

    # pic_n = 18
    # negative = True
    pic_path = f"/Users/matteotessarolo/Documents/coding/crochet_utilities/pattern_azulejos/pic{pic_n}.png"
    out_path = f"/Users/matteotessarolo/Documents/coding/crochet_utilities/pattern_azulejos/patterns/pic{pic_n}.png"
    # pattern_size = 120
    ptr = np.zeros((pattern_size, pattern_size))

    with Image.open(pic_path) as im:
        mono = (
            im.convert("L")
            .resize((pattern_size, pattern_size))
            .point(lambda p: 1 if p > 200 else 0)
        )
        mono.show()
        for i in range(pattern_size):
            for j in range(pattern_size):
                if i % 2 == 0 and j % 2 == 0:
                    ptr[i, j] = 0
                elif i % 2 == 1 and j % 2 == 1:
                    ptr[i, j] = 1
                else:
                    ptr[i, j] = mono.im[i + j * pattern_size]
        fig, ax = plt.subplots()
        ax.pcolormesh(ptr, cmap="Blues_r" if negative else "Blues")
        ax.axis("equal")
        plt.savefig(out_path, dpi=150)
        plt.show()
