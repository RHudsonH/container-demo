# syntax=docker/dockerfile:1

FROM python:3.10.4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY resize.py ./

CMD [ "python", "./resize.py" ]