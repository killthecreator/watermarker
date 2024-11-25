FROM python

RUN apt-get update && apt-get install -y \
    ttf-mscorefonts-installer \
    fontconfig \
    && fc-cache -f -v \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip3 install PyPDF2 reportlab pillow

ENV DISPLAY=192.168.0.30:0

CMD ["python3", "src/app.py"]