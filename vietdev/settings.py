import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from urllib.parse import urljoin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your key here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'profiles',
    'registration',
    'pure_pagination',
    'chat',
    'contact',
    'static_pages',

    'imagekit',
    'crispy_forms',
    'captcha',
    'simplemde',
    'rest_framework',
    'channels',
    'haystack',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vietdev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vietdev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SITE_ID = 1

SITE_DOMAIN = 'vietdev.com'

ADMIN_EMAIL = ['admin@domain.com']

PERSON_DEFAULT = urljoin(STATIC_URL, 'img/default-avatar.png')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'


# Redis Server
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
        "ROUTING": "vietdev.routing.channel_routing",
    },
}

WS_HOST = 'vietdev.com'
WS_PORT = '8889'
WS_PORT_SECURE = '8887'


# Mongo
MONGO_SERVER_URL = 'mongodb://{}:{}/'.format('127.0.0.1', '27017')
MONGO_DB_NAME = 'vietdev'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'vietdev_haystack',
    },
}


CRISPY_TEMPLATE_PACK = 'bootstrap4'


SIMPLEMDE_OPTIONS = {
    'placeholder': '',
    'spellChecker': False,
    'status': False,
    'autosave': {
        'enabled': False
    }
}


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 8,
    'MARGIN_PAGES_DISPLAYED': 3,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}


RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True


MAILGUN_API_KEY = "key-xxx"
MAILGUN_DOMAIN = 'mg.example.com'
DEFAULT_FROM_EMAIL = 'no.reply@example.com'


FORGOT_PASSWORD_EMAIL_BODY = '''Hi {username},

A request to reset your password on Vietdev.com has been made. 
If you did not make this request, simply ignore this email. 
If you did make this request, please follow the link below.

{link}

---
Vietdev Team
'''

WELCOME_EMAIL_BODY = '''Hi {username},

Thank you for signing-up!

Below is the email address you've registered with on Vietdev.com. 
Use it reset your password, if you happen to forget it ;).

`{email}`

---
Vietdev Team
'''

REQUEST_EMAIL_BODY = '''Hi,

A request to get email address of a developer on Vietdev.com has been made. 

Name: {dev_name}
Profile: {profile_url}
Email: {dev_email}

---
Vietdev Team
'''


try:
    from vietdev.local_settings import *
except ImportError:
    pass