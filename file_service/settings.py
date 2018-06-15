import os
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(*x):
    return os.path.normpath(os.path.join(BASE_DIR, * x))


class BaseConfiguration(Configuration):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fileservice',
            'USER': 'fileservice',
            'PASSWORD': 'fileservice',
            'HOST': 'fileservice_postgres',
        }
    }

    SECRET_KEY = '783ae16754d4ce6d1de0a749fb0744f4'

    ALLOWED_HOSTS = ['*', ]

    INSTALLED_APPS = [
        'django.contrib.admin',

        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',

        'rest_framework',

        'file_service.files',
    ]

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]

    ROOT_URLCONF = 'file_service.urls'

    TROOD_AUTH_SERVICE_URL = os.environ.get('TROOD_AUTH_SERVICE_URL', 'http://authorization.trood:8000/')

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'trood_auth_client.authentication.TroodTokenAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.OrderingFilter',
            'rest_framework.filters.SearchFilter',
        )
    }

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.contrib.messages.context_processors.messages',
                    'django.contrib.auth.context_processors.auth',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'file_service.wsgi.application'

    LANGUAGES = (
        ('ru-RU', 'Russian'),
        ('en-US', 'English'),
    )

    LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-US')

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    DATE_FORMAT = '%d-%m-%Y'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.environ.get('FILE_SERVICE_MEDIA_ROOT', rel('media'))

    STATIC_URL = '/static/'
    STATIC_ROOT = os.environ.get('FILE_SERVICE_STATIC_ROOT', rel('static'))

    # Absolute url
    FILES_BASE_URL = os.environ.get('FILES_BASE_URL', '/media/')


    IMAGE_SIZES = {
        'small': 128,
        'medium': 320,
        'large': 640,
        'xlarge': 1200
    }

    DOMAIN = 'FILESERVICE'


class Development(BaseConfiguration):
    DEBUG = True


class Production(BaseConfiguration):
    DEBUG = False
