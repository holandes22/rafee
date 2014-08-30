from rafee.settings.base  import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'fake'

XS_SHARING_ALLOWED_ORIGINS = 'http://localhost:4200'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rafee_db',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': '',
        'PORT': '',
    }
}

API_PREFIX = 'api/v1'
