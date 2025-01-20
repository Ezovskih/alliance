from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.messages',
    # 'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'polygons',
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

APPEND_SLASH = True
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

STATIC_URL = 'static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # path.join(BASE_DIR, 'polygons', 'templates'),
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

LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
