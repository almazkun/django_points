FROM python:3.11-slim

LABEL org.opencontainers.image.source=https://github.com/almazkun/django_points

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile ./Pipfile.lock ./

RUN pip3 install pipenv gunicorn && pipenv install --system

COPY points ./points
COPY settings ./settings
COPY manage.py ./

ENTRYPOINT [ "gunicorn" ]

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1", "--threads", "10", "--limit-request-line", "0" ]