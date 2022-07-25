# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /pulsebook

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#copy secrets keys
COPY /testy/.env /pulsebook/testy/.env

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]