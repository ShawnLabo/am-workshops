# Use golang image as a builder
FROM python:3.8-alpine

RUN apk --update add python3

WORKDIR /app
COPY . .
RUN pip3 install --upgrade -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--capture-output", "--access-logfile", "-", "main:app"]

