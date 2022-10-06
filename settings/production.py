import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    '135.181.241.102',
    '188.121.107.24',
    'localhost',
    'sina.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': os.environ.get("DATABASE_USER"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}
