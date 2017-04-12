# This file will override values from settings.py
# It's useful for separating configurations

DEBUG = False

SECRET_KEY = 'your key here'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
    }
}

SITE_DOMAIN = 'example.com'

ADMIN_EMAIL = ['admin@domain.com']

ALLOWED_HOSTS = ['example.com']


# Websocket
WS_HOST = '127.0.0.1'
WS_PORT = '8000'
WS_PORT_SECURE = '8004'


# Mongo
MONGO_SERVER_URL = 'mongodb://{}:{}/'.format('127.0.0.1', '27017')
MONGO_DB_NAME = 'example'


# Recaptcha
# https://www.google.com/recaptcha/admin
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''


# Mailgun
# https://www.mailgun.com/
MAILGUN_API_KEY = "key-xxx"
MAILGUN_DOMAIN = 'mg.example.com'
DEFAULT_FROM_EMAIL = 'no.reply@example.com'