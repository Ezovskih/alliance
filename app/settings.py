from pathlib import Path


DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

INSTALLED_APPS = [
    'daphne',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.gis',
    'channels',
    'polygons',
    'intersections',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
    'redis': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': { 'hosts': [('127.0.0.1', 6379)], },
    },
}

ROOT_URLCONF = 'app.urls'
# WSGI_APPLICATION = 'app.wsgi.application'
ASGI_APPLICATION = 'app.asgi.application'  # Daphne

STATIC_URL = '/static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path.joinpath(APP_DIR, 'templates'),
        ],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'alliance',
        'USER': 'postgres',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

# GDAL_LIBRARY_PATH = r'C:/OSGeo4W/bin/gdal309.dll'
# GEOS_LIBRARY_PATH = r'C:/OSGeo4W/bin/geos_c.dll'
GDAL_LIBRARY_PATH = 'C:/Program Files/GDAL/gdal.dll'
GEOS_LIBRARY_PATH = 'C:/Program Files/GDAL/geos_c.dll'
# PROJ_LIB = 'C:/Program Files/GDAL/projlib'

SECRET_KEY = 'app-secret-key-1'
ALLOWED_HOSTS = ['*']
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
]

# SESSION_COOKIE_AGE = 10

INTERSECTIONS_API_URL = 'http://localhost:8000/intersections/check/'
INTERSECTIONS_API_KEY = 'intersections-api-key-1'

LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
