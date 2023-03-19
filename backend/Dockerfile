FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

RUN apt update && apt install fonts-dejavu fonts-dejavu-core

RUN ln -s /usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf /usr/local/lib/python3.7/site-packages/reportlab/fonts

COPY . /app

WORKDIR /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]