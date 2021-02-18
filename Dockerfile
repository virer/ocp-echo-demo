FROM python:3.7-alpine

RUN addgroup -S myapp && adduser -H -D -S -G myapp myapp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8080

COPY . /

RUN pip install -r /requirements.txt

USER myapp
WORKDIR /app

CMD [ "sh", "echo.sh" ]