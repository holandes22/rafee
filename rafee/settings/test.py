from rafee.settings.base  import *

SECRET_KEY = 'fake'

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

BROKER_TRANSPORT = 'memory'
BROKER_URL = 'memory://'
CELERY_CACHE_BACKEND = 'memory'
CELERY_RESULT_BACKEND = 'cache'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
