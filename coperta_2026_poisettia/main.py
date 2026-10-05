import csv
import os
import numpy as np

if __name__ == "__main__":
    pix_arr = np.array([])
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "pattern.csv"),
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

        for row in stitch_arr:
            row_pattern = ""
            start = 0

            while start < len(row):
                best_pattern = row[start : start + 1]
                best_count = 1
                best_length = 1

                for pattern_length in range(1, 4):
                    if start + pattern_length > len(row):
                        break

                    pattern = row[start : start + pattern_length]
                    count = 1

                    while start + (count + 1) * pattern_length <= len(
                        row
                    ) and np.array_equal(
                        row[
                            start + count * pattern_length : start
                            + (count + 1) * pattern_length
                        ],
                        pattern,
                    ):
                        count += 1

                    consumed = count * pattern_length
                    best_consumed = best_count * best_length

                    if count > 1 and (
                        consumed > best_consumed
                        or (consumed == best_consumed and count > best_count)
                    ):
                        best_pattern = pattern
                        best_count = count
                        best_length = pattern_length
                # if best_count == 1 or pattern_length == 1:
                row_pattern += f"{best_count}{''.join(best_pattern)}/"
                # else:
                #     row_pattern += f"{best_count}({''.join(best_pattern)}) "
                start += best_count * best_length

            pat_arr.append(f"R{row_ind + 1} - " + row_pattern)
            row_ind += 1
        for row in pat_arr:
            print(row)
