import numpy as np
from gen import gen_pattern

negative = True
pattern_size = 121

for pic_n in range(1, 19):
    gen_pattern(pic_n, negative=negative, pattern_size=pattern_size)
