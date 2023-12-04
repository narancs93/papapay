# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bullseye as python-base

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


FROM python-base as builder

RUN pip install -U pip setuptools
RUN apt-get update && apt-get install -y build-essential python3-dev libpq-dev
RUN mkdir -p /install

# Install dependencies
COPY requirements.txt .

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-warn-script-location --prefix=/install -r requirements.txt


FROM alpine:3.18.5 AS minify-static

RUN apk add --no-cache npm tini
WORKDIR /usr/src/app
COPY package.json .
RUN npm install
COPY papapay/static static
RUN npx uglifyjs static/js/*.js -m --toplevel -o app.min.js
RUN npx uglifycss static/css/*.css > app.min.css


FROM python-base

RUN apt-get update && apt-get install -y libpq-dev
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY --from=builder /install /usr/local
COPY --from=minify-static /usr/src/app/app.min.js /usr/src/app/app.min.css papapay/static/
RUN python manage.py collectstatic --no-input --clear

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${GUNICORN_SERVICE_PORT} config.wsgi:application"]