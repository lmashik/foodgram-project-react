FROM python:3.7-slim

RUN apt-get update && apt-get install -y fonts-dejavu fonts-dejavu-core

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

RUN ln -s /usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf /usr/local/lib/python3.7/site-packages/reportlab/fonts

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]