from rafee.settings.base  import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'fake'

XS_SHARING_ALLOWED_ORIGINS = 'http://0.0.0.0:4200'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rafee_db',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '',
    }
}

API_PREFIX = 'api/v1'

RAFEE_REPO_DIR = '/var/www/rafee/repos'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].extend(
    [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
)
