# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bullseye

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install -U pip setuptools
RUN apt-get update && apt-get install -y build-essential python3-dev libpq-dev

# Install dependencies
WORKDIR /usr/src/app
COPY . .

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-warn-script-location -r requirements.txt

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${GUNICORN_SERVICE_PORT} config.wsgi:application"]