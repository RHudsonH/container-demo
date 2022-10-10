# syntax=docker/dockerfile:1

FROM python:3.10.4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6 -y \
    && pip install --upgrade pip wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY vignette.py .

CMD [ "python", "./vignette.py" ]