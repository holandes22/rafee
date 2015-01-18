import uwsgi
from uwsgidecorators import timer
from django.utils import autoreload

from rafee.settings.base  import *


# Register func to reload uwsgi on code changes.
# Taken from http://projects.unbit.it/uwsgi/wiki/TipsAndTricks
# If you see it does not reload on views or urls tocuh here is why
# https://code.djangoproject.com/ticket/22729
@timer(3)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'fake'

CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)(0.0.0.0|127.0.0.1|localhost):4200$',
)

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


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].extend(
    [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
)
