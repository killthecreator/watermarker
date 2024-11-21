import os
import tkinter as tk
from io import BytesIO
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter, PdfMerger, PageRange
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
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


stamp_img("example.pdf", "example.jpg", "out.pdf")


def upload_file(event=None):
    filename = filedialog.askopenfilename()
    print("Selected:", filename)


def run_app():
    window = tk.Tk()

    window.title("Watermarker")
    window.geometry("520x300")

    upload_btn = tk.Button(window, text="Выберите файл", command=upload_file)
    upload_btn.pack()

    # Title input
    title_label = tk.Label(window, text="Введите основную надпись")
    title_label.pack()
    title_input = tk.Entry(window)
    title_input.pack()

    # Subtitle input
    subtitle_label = tk.Label(window, text="Введите дополнительную надпись")
    subtitle_label.pack()
    subtitle_input = tk.Entry(window)
    subtitle_input.pack()

    # Save button
    submit_btn = tk.Button(window, text="Сохранить", command=window.quit)
    submit_btn.pack()

    window.mainloop()

    # pdf reader
    reader = PdfReader("example.pdf")
    print(reader)
    number_of_pages = len(reader.pages)


# run_app()
