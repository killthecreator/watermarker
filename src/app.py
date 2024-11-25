import os
import tkinter as tk
from io import BytesIO
from tkinter import filedialog, StringVar, colorchooser
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageTk, ImageDraw, ImageFont
from typing import List, Union


if os.environ.get("DISPLAY", "") == "":
    print("no display found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")


def image_to_pdf(stamp_img: Union[Path, str]) -> PdfReader:
    img = Image.open(stamp_img)
    img_as_pdf = BytesIO()
    img.save(img_as_pdf, "pdf")
    img_as_pdf.seek(0)
    return PdfReader(img_as_pdf)


def stamp_img(
    content_pdf: Union[Path, str],
    stamp_img: Union[Path, str],
    pdf_result: Union[Path, str],
):
    # Convert the image to a PDF
    stamp_pdf = image_to_pdf(stamp_img)

    # Then use the same stamp code from above
    stamp_page = stamp_pdf.pages[0]

    reader = PdfReader(content_pdf)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        pdf_page = reader.pages[i]
        pdf_page.merge_page(stamp_page)
        writer.add_page(pdf_page)

    with open(pdf_result, "wb") as merged_file:
        writer.write(merged_file)


stamp_img("example.pdf", "example.jpg", "/app/output/out.pdf")


def upload_file(event=None):
    filename = filedialog.askopenfilename()
    print("Selected:", filename)


def update_image(var, index, mode):
    global img, image_tk, image_label

    # Reload the original image to clear previous text
    img = Image.open("example.jpg")

    # Draw text on the image
    draw = ImageDraw.Draw(img)
    draw.text((28, 36), title_text.get(), fill=(255, 0, 0))  # Title text
    draw.text((28, 60), subtitle_text.get(), fill=(0, 0, 255))  # Subtitle text

    # Update the Tkinter image object
    image_tk = ImageTk.PhotoImage(img)

    # Update the image in the label
    image_label.config(image=image_tk)

    return True


def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title="Choose color")
    print(color_code)


window = tk.Tk()
title_text = StringVar()

title_text.trace_add("write", update_image)

subtitle_text = StringVar()

subtitle_text.trace_add("write", update_image)


def run_app():
    global title_input, subtitle_input, img, image_tk, image_label

    window.title("Watermarker")
    window.geometry("520x300")

    upload_btn = tk.Button(window, text="Выберите файл", command=upload_file)
    upload_btn.pack()

    # Title input
    title_label = tk.Label(
        window,
        text="Введите основную надпись",
    )
    title_label.pack()
    title_input = tk.Entry(window, textvariable=title_text)
    title_input.pack()

    # Subtitle input
    subtitle_label = tk.Label(window, text="Введите дополнительную надпись")
    subtitle_label.pack()
    subtitle_input = tk.Entry(window, textvariable=subtitle_text)
    subtitle_input.pack()

    # Save button
    submit_btn = tk.Button(window, text="Сохранить", command=window.quit)
    submit_btn.pack()

    color_picker_btn = tk.Button(window, text="Select color", command=choose_color)
    color_picker_btn.pack()

    img = Image.open("example.jpg")
    width, height = img.size  # Canvas size
    font_size = 100
    text_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    draw = ImageDraw.Draw(text_img)

    # throws error, need to investigate
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)  # Use a TrueType font
    except IOError:
        print("ERROR LOADING FONT")
        font = ImageFont.load_default()

    mock_title = "Title"
    mock_subtitle = "Subtitle"

    multi_line_string = mock_title + "\n" + mock_subtitle
    bbox = draw.textbbox(
        (0, 0), text=multi_line_string, font=font
    )  # Bounding box of the text
    gap_x, gap_y = 200, 200
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    text_width_with_gap, text_height_with_gap = text_width + gap_x, text_height + gap_y

    list_x = list(range((width // (text_width_with_gap)) + 1))
    list_y = list(range((height // (text_height_with_gap)) + 1))

    for i in list_x:
        for j in list_y:
            x = i * text_width_with_gap
            y = j * text_height_with_gap
            draw.text(
                (x, y),
                align="center",
                text=multi_line_string,
                fill=(255, 255, 255, 128),
                font_size=font_size,
            )

    mask_angle = 0
    rotated_mask = text_img.rotate(mask_angle, expand=False, fillcolor="white")

    img.paste(rotated_mask, (0, 0), rotated_mask)

    img.save("output/text_mask_debug.png")

    image_tk = ImageTk.PhotoImage(img)

    image_label = tk.Label(window, image=image_tk)
    image_label.pack()

    # window.mainloop()

    return


run_app()
