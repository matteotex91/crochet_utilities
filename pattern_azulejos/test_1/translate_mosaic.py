import csv
import numpy as np
import os
# this script translates the 2d binary pattern to a crochet constructive pattern readable by the ipad app


def translate_mosaic(csv_in_path: str, csv_out_path: str):
    pattern = []
    with open(csv_in_path) as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            p_row = []
            for r in row:
                for i in r.split("\t"):
                    if i == "0":
                        p_row.append(0)
                    elif i == "1":
                        p_row.append(1)
            pattern.append(p_row)

    pattern = 1 - np.array(pattern).T
    rows = pattern.shape[0]
    cols = pattern.shape[1]

    stitches = np.zeros(shape=(rows + 2, cols), dtype=np.int32)
    # 0 -> colore 1
    # 1 -> colore 2
    # +2 -> +
    # +4 -> -
    # +8 -> F
    # +16 -> B
    frontCount = 0
    backCount = 0
    for i in range(rows):
        for j in range(cols):
            stitches[i + 2, j] = pattern[i, j]
            if i % 2 == 0:
                if pattern[i, j] == 0:
                    stitches[i, j] += 8
                    stitches[i + 1, j] += 8
                    frontCount += 2
                    stitches[i + 2, j] += 2
                else:
                    stitches[i + 2, j] += 2
            else:
                if pattern[i, j] == 1:
                    stitches[i, j] += 16
                    stitches[i + 1, j] += 16
                    backCount += 2
                    stitches[i + 2, j] += 4
                else:
                    stitches[i + 2, j] += 2
    print(f"front stitches : {frontCount} - back stitches : {backCount}")
    flat = np.flip(np.flip(stitches, axis=0), axis=1).flatten()
    flat = np.append(arr=flat, values=rows)
    flat = np.append(arr=flat, values=cols)
    with open(csv_out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)


if __name__ == "__main__":
    # pic_n = 1
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # csv_in_path = current_dir + f"/patterns_csv/pat{pic_n}.csv"
    # csv_out_path = current_dir + f"/mosaic_patterns_csv/mos{pic_n}.csv"
    csv_in_path = current_dir + "/patterns_csv/final.csv"
    csv_out_path = current_dir + "/definitive_patterns/azulejos.csv"
    translate_mosaic(csv_in_path=csv_in_path, csv_out_path=csv_out_path)
