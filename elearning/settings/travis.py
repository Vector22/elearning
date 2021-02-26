from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database for travis
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
