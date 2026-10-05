import csv
import os
import re

import numpy as np
from PIL import Image
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def create_pattern_pdf(pix_arr, pat_arr, output_path):
    page_width, page_height = landscape(A5)
    margin = 20
    column_gap = 18
    left_width = (page_width - 2 * margin - column_gap) * 0.52
    image_left = margin + left_width + column_gap
    image_area_width = page_width - margin - image_left
    body_top = page_height - margin - 54
    body_height = body_top - margin
    n_rows, n_columns = pix_arr.shape
    palette = np.array([[239, 222, 190], [190, 35, 45]], dtype=np.uint8)
    rotated_pixels = np.rot90(palette[np.flip(pix_arr.astype(int), axis=1)], k=-1)
    display_pixels = np.concatenate((rotated_pixels[:, -1:], rotated_pixels), axis=1)
    image = ImageReader(Image.fromarray(display_pixels))
    image_area_height = page_height - 2 * margin
    image_scale = min(image_area_width / (n_rows + 1), image_area_height / n_columns)
    image_width = (n_rows + 1) * image_scale
    image_height = n_columns * image_scale
    image_x = image_left + (image_area_width - image_width) / 2
    image_y = page_height - margin - image_height
    font_name = "Courier-Bold"
    number_color = HexColor("#202020")
    pattern_color = HexColor("#F4CE46")
    highlight_color = HexColor("#00852B")
    odd_row_color = HexColor("#EFDEBE")
    even_row_color = HexColor("#BE232D")
    pdf = canvas.Canvas(output_path, pagesize=(page_width, page_height))
    pdf.setTitle("Crochet Pattern")

    for row_index, row_pattern in enumerate(pat_arr):
        elements = []
        for token in row_pattern.split("/", 1)[1].split("/"):
            if not token:
                continue
            match = re.fullmatch(r"(\d+)([+F]+)", token)
            if match is None:
                raise ValueError(f"Invalid pattern token: {token}")
            elements.append(match.groups())

        font_size = 28
        while True:
            padding = font_size * 0.35
            space_width = pdf.stringWidth(" ", font_name, font_size)
            box_height = font_size * 1.65
            line_height = box_height + font_size * 0.5
            lines = [[]]
            line_width = 0
            max_element_width = 0
            for number, pattern in elements:
                number_width = (
                    pdf.stringWidth(number, font_name, font_size) + 2 * padding
                )
                pattern_width = (
                    pdf.stringWidth(pattern, font_name, font_size) + 2 * padding
                )
                element_width = number_width + pattern_width
                max_element_width = max(max_element_width, element_width)
                gap = space_width if lines[-1] else 0
                if lines[-1] and line_width + gap + element_width > left_width:
                    lines.append([])
                    line_width = 0
                    gap = 0
                lines[-1].append((number, pattern, number_width, pattern_width))
                line_width += gap + element_width
            if (
                max_element_width <= left_width
                and len(lines) * line_height <= body_height
            ):
                break
            font_size *= 0.9

        pdf.setFillColor(number_color)
        pdf.setFont("Helvetica-Bold", 24)
        row_label = f"Row {row_index + 1}"
        label_padding = 10
        label_width = (
            pdf.stringWidth(row_label, "Helvetica-Bold", 24) + 2 * label_padding
        )
        label_height = 40
        label_y = page_height - margin - label_height
        pdf.roundRect(margin, label_y, label_width, label_height, 6, stroke=0, fill=1)
        pdf.setFillColor(white)
        pdf.drawString(margin + label_padding, label_y + 12, row_label)
        swatch_size = 24
        swatch_x = margin + label_width + 10
        swatch_y = label_y + (label_height - swatch_size) / 2
        pdf.setFillColor(odd_row_color if (row_index + 1) % 2 else even_row_color)
        pdf.roundRect(swatch_x, swatch_y, swatch_size, swatch_size, 4, stroke=0, fill=1)
        pdf.setFont(font_name, font_size)
        for line_index, line in enumerate(lines):
            text_x = margin
            box_y = body_top - box_height - line_index * line_height
            text_y = box_y + (box_height - font_size) / 2 + font_size * 0.18
            for token_index, (
                number,
                pattern,
                number_width,
                pattern_width,
            ) in enumerate(line):
                if token_index:
                    pdf.setFillColor(number_color)
                    pdf.drawString(text_x, text_y, " ")
                    text_x += space_width
                pdf.setFillColor(number_color)
                pdf.roundRect(
                    text_x, box_y, number_width, box_height, 4, stroke=0, fill=1
                )
                pdf.setFillColor(white)
                pdf.drawString(text_x + padding, text_y, number)
                text_x += number_width
                pdf.setFillColor(pattern_color)
                pdf.roundRect(
                    text_x, box_y, pattern_width, box_height, 4, stroke=0, fill=1
                )
                pdf.setFillColor(number_color)
                pdf.drawString(text_x + padding, text_y, pattern)
                text_x += pattern_width

        pdf.drawImage(image, image_x, image_y, width=image_width, height=image_height)
        pdf.setStrokeColor(black)
        pdf.setLineWidth(0.1)
        for column_boundary in range(1, display_pixels.shape[1]):
            grid_x = image_x + column_boundary * image_scale
            pdf.line(grid_x, image_y, grid_x, image_y + image_height)
        for row_boundary in range(1, display_pixels.shape[0]):
            grid_y = image_y + row_boundary * image_scale
            pdf.line(image_x, grid_y, image_x + image_width, grid_y)
        highlight_x = image_x + (row_index + 1) * image_scale
        pdf.setStrokeColor(highlight_color)
        pdf.setLineWidth(0.75)
        pdf.rect(
            highlight_x,
            image_y,
            image_scale,
            image_height,
            stroke=1,
            fill=0,
        )
        pdf.showPage()

    pdf.save()


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

    create_pattern_pdf(
        pix_arr,
        pat_arr,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "pattern.pdf"),
    )
