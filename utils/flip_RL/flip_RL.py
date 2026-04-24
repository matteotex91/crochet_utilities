import os
import csv


def flip_rl(csv_path: str, out_path: str):
    data = []
    with open(csv_path) as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            p_row = []
            for r in row:
                for i in r.split("\t"):
                    if i == "0":
                        p_row.append(0)
                    elif i == "1":
                        p_row.append(1)
            data.append(p_row)

    flipped_data = [row[::-1] for row in data]

    with open(out_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(flipped_data)


datapath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = datapath + "/data_in.csv"
out_path = datapath + "/data_out.csv"
flip_rl(csv_path, out_path)
