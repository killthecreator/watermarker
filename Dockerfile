FROM python

WORKDIR /app

COPY . .

RUN pip3 install PyPDF2 reportlab pillow

ENV DISPLAY=192.168.0.30:0

CMD ["python3", "src/app.py"]