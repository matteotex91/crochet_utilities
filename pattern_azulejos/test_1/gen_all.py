import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
from gen import gen_pattern

negative = True
pattern_size = 120
ptr = np.zeros((pattern_size, pattern_size))

for pic_n in range(1, 19):
    gen_pattern(pic_n, negative=negative, pattern_size=pattern_size)
