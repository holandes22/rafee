# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Rafee specific

RAFEE_REPO_DIR = ''
RAFEE_REPO_POLLING_INTERVAL = os.environ.get('RAFEE_REPO_POLLING_INTERVAL', 45)

# Celery

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'pull_all_repos_periodically': {
        'task': 'rafee.repositories.tasks.pull_all_repos',
        'schedule': timedelta(seconds=RAFEE_REPO_POLLING_INTERVAL),
    },
}

# Django

APPEND_SLASH = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.User'

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'djangosecure',
    'rest_framework_swagger',
    'django_extensions',
)

LOCAL_APPS = (
    'rafee.teams',
    'rafee.users',
    'rafee.slideshows',
    'rafee.repositories',
    'rafee.templates',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rafee.middleware.xssharing.XsSharingMiddleware',
)

ROOT_URLCONF = 'rafee.urls'

WSGI_APPLICATION = 'rafee.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (mainly used for API docs)

STATIC_URL = '/static/'

# Allow CORS

XS_SHARING_ALLOWED_HEADERS = ['Content-Type', 'Authorization']


# REST Framework
API_VERSION = 'v1'
API_PREFIX = API_VERSION

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend',
}

# Swagger (API Docs)

SWAGGER_SETTINGS = {
    'enabled_methods': [],
    'api_version': API_VERSION,
}
