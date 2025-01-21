from pathlib import Path


DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            # path.join(BASE_DIR, 'templates'),
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

SECRET_KEY = 'django-insecure-twn=0dnvdbjchq1y+lh05^0-0rm$u(v9f+(#aqygtu1!4+iuyp'
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
ALLOWED_HOSTS = []

INTERSECT_API_URL = ''
INTERSECT_API_KEY = ''

LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
