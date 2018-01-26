DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database name (change),
        'USER': user (change),
        'PASSWORD': password,
        'HOST': 'localhost',
        'PORT': '',
    }
}