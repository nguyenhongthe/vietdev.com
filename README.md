# VietDev Project
High Quality Developer Profiles in Vietnam

## Introduction

This is a typical Django project with ORM design running on top of PostgresSQL. I solve problems by using combination of many technologies include MongoDB (mongoengine), Redis and Elasticsearch. This project also is a very good example of site has the real-time parts inside. The code is not perfect but clean and precise.

## Requirements

- Python 3.5 or 3.6.
- Redis for websocket tasks.
- Elasticsearch 2.4.x.
- MongoDB for saving chat messages.
- PostgreSQL 9.x.
- Django 1.10.x.
- Bootstrap 4 alpha.6
- node-sass
- gulp

### Third-party services

- Mailgun: easy to send email by using simple APIs.
- Recaptcha for anti-spam.

## Instructions

1. Run `npm install`.
2. Get statics: `bower install`.
3. Change file `vietdev/local_settings_example.py` to `vietdev/local_settings.py`.
4. Edit `vietdev/local_settings.py` with your configurations.
5. Create a virtualenv then run `pip install -r requirements.txt`.
6. Run `python manage.py migrate`.
7. Make sure MongoDB and Redis are running.
8. Make sure Elasticsearch version is 2.4.x (at dev time, `django-haystack` does not support Elasticsearch 5.x yet).
6. Finally run `python manage.py runserver`.

## Customize

- CSS: run `gulp build:sass` or watch on changes by just `gulp`.

## Deployment

- I'm using `supervisord` for managing processes; using `gunicorn` for WSGI server, nginx as a proxy.
- You should create a virtualenv by running `python3 -m venv myvenv`.
- Package `channels` needs workers to push messages. For example: `python manage.py runworker --threads 4`.
- Run daphne server: `daphne -p 8001 vietdev.asgi:channel_layer`. Find more: [https://github.com/django/daphne](https://github.com/django/daphne)

## Licenses
MIT license is applied for source code except the name `Vietdev` and/or its logo.