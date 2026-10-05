import csv
import os
import numpy as np

if __name__ == "__main__":
    pix_arr = np.array([])
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "pattern_2.csv"),
        newline="",
    ) as csvfile:
        reader = csv.reader(csvfile)
        n_rows = 0
        for row in reader:
            n_rows += 1
            n_columns = len(row)
            pix_arr = np.append(pix_arr, np.array(row, dtype=int))
        pix_arr = np.reshape(pix_arr, (-1, n_columns))
        stitch_arr = np.empty((n_rows, n_columns), dtype=str)
        for i in range(n_rows):
            for j in range(n_columns):
                if pix_arr[(i + 1) % n_rows, j] == i % 2:
                    stitch_arr[i, j] = "+"
                else:
                    stitch_arr[i, j] = "F"
        stitch_arr = np.flip(stitch_arr, axis=0)
        pat_arr = []
        row_ind = 0

        # sanity check
        for i in range(n_rows - 1):
            for j in range(n_columns):
                if stitch_arr[i, j] == "F" and stitch_arr[i + 1, j] == "F":
                    print(
                        f"Illegal consecutive 'F' found at ({i},{j}) and ({i + 1},{j})"
                    )

        for row in stitch_arr:
            # Optimal segmentation via DP: minimize (sum of block lengths, number of tokens)
            s = "".join(row)
            n = len(s)
            INF = (float("inf"), float("inf"))
            dp = [INF] * (n + 1)
            choice = [None] * (n + 1)  # (start, block_length, count)
            dp[0] = (0, 0)
            for start in range(n):
                if dp[start] == INF:
                    continue
                base_cost, base_tokens = dp[start]
                for length in range(1, n - start + 1):
                    block = s[start : start + length]
                    count = 1
                    while True:
                        end = start + count * length
                        cand = (base_cost + length, base_tokens + 1)
                        if cand < dp[end]:
                            dp[end] = cand
                            choice[end] = (start, length, count)
                        if s[end : end + length] != block:
                            break
                        count += 1

            tokens = []
            end = n
            while end > 0:
                start, length, count = choice[end]
                tokens.append(f"{count}{s[start : start + length]}/")
                end = start
            row_pattern = "".join(reversed(tokens))

            pat_arr.append(f"R{row_ind + 1}/" + row_pattern)
            row_ind += 1
        for row in pat_arr:
            print(row)
