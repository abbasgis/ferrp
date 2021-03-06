"""
Django settings for ferrp project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib.messages import constants as messages

from ferrp.local_settings import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from ferrp.account_settings import *

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#swql99-*$u7^#&ufvtl-6a(dfglh602_d9gp549d9(dw5!pj7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
# Set to True to load non-minified versions of (static) client dependencies
# Requires to set-up Node and tools that are required for static development
# otherwise it will raise errors for the missing non-minified dependencies
DEBUG_STATIC = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '127.0.1.1', '172.104.141.250', '172.104.180.176', 'pnddch.info', 'www.pnddch.info']
SITE_NAME = 'FERRP'
SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_mptt_admin',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.google',
    'mptt',
    'simple_history',
    'bootstrap3',
    'bootstrap_ui',
    'searchableselect',
    'tinymce',
    'ferrp',
    'ferrp.layers',
    'ferrp.maps',
    'ferrp.map_3d',
    'ferrp.irrigation',
    'ferrp.adp',
    'ferrp.pc1',
    'ferrp.climate_change',
    'ferrp.dia',
    'ferrp.site_selection',
    # 'ferrp.local_MHVRA',
    # 'ferrp.remote_MHVRA',
    'ferrp.survey_stats_app',
    'ferrp.documents',
    'ferrp.projects',
    'ferrp.integration',
    'ferrp.indus_basin',
    'ferrp.meeting_management',
    'ferrp.boundaries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ferrp.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ferrp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ferrp_admin',
        'USER': DB_USER,
        'HOST': DB_HOST,
        'PASSWORD': DB_PASSWORD,  # 'postr2vdhagres', 'postgres'
        'PORT': DB_PORT,
    },
    'adp': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'adp',
        'USER': DB_USER,
        'HOST': '172.104.141.250',
        # 'HOST': 'localhost',
        'PASSWORD': 'postpndgres7%6',  # 'postgres'
        # 'PASSWORD':'idreesgis',
        'PORT': DB_PORT,
    },
    'spatialds': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ferrp_data',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,  # 'postr2vdhagres', 'postgres'
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'irrigation': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'irrigation',
        'USER': 'postgres',
        # 'PASSWORD': 'idreesgis',  # 'postr2vdhagres', 'postgres'
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': DB_PORT,
    },
    'pc1_db': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pc1',
        # 'USER': 'postgres',
        # 'PASSWORD': 'idreesgis',
        # 'HOST': 'localhost',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    },
    'mhvra_local_db': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mhvra_reporting_2',
        # 'USER': 'postgres',
        # 'PASSWORD': 'idreesgis',
        # 'HOST': 'localhost',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    },
    'mhvra_reporting': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mhvra_reporting',
        'USER': 'pcu',
        'PASSWORD': 'pcu1234',
        'HOST': '125.209.112.206',
        'PORT': '5432',
    },
    'db_mm': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'meeting_management',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    },
	'db_dia': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dia',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
proxy_read_timeout = 1000
DATABASE_ROUTERS = ['ferrp.routers.SpatialDatabaseHandling']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ferrp.pnd@gmail.com'
EMAIL_HOST_PASSWORD = 'ferrp@pnd'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ferrp.pnd@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'

#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = '/static/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "ferrp/static_root")
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = '/media/'

ICON_PATH = os.path.join(BASE_DIR, 'ferrp/static/ferrp/icons')
SHAPEFILE_PATH = os.path.join(MEDIA_ROOT, 'shp')  # BASE_DIR + '/uploaded/shp/'
SHAPEFILE_URL = os.path.join(MEDIA_URL, 'shp')
RASTER_PATH = os.path.join(MEDIA_ROOT, 'raster')  # BASE_DIR + '/uploaded/shp/'
RASTER_URL = os.path.join(MEDIA_URL, 'raster')
THUMBNAILS_PATH = os.path.join(MEDIA_ROOT, 'thumbnails')
THUMBNAILS_URL = os.path.join(MEDIA_URL, 'thumbnails')
DOCUMENT_PATH = os.path.join(MEDIA_ROOT, 'documents')
DOCUMENT_URL = os.path.join(MEDIA_URL, 'documents')

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

LOGIN_URL = "/account_login/"

LOGOUT_REDIRECT_URL = "/"

# For social User authentication
AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

SOCIALACCOUNT_PROVIDERS = {
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/calendar',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            'prompt': 'consent'
        }
    }
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'width': '70%',
    'height': 400,
    # 'plugins': "table,spellchecker,paste,searchreplace",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

