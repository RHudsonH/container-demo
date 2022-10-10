# syntax=docker/dockerfile:1

FROM python:3.9.2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY img2sep.py ./

CMD [ "python", "./img2sep.py" ]