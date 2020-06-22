"""
Django settings for OdinApi_v03 project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

def gettext_noop(s):
    return s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$o5kp+^d!#na==76*0o0g2hgo4c#mhc2%#d6%-b8fu(=z#d^!2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'social_django',
    'apps.autenticacion',
    'apps.core',
    'apps.empresa',
    'apps.taxis',
    'apps.periodico',
    'apps.ecommerce',
    'drf_yasg',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # revisar
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# tipos de autenticacion que tendra la api
AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.autenticacion.backends.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
}

# habilitar CORS para todos los dominios agregando la siguiente configuración
CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'autenticacion.Usuario'

ROOT_URLCONF = 'OdinApi_v03.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'OdinApi_v03.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'OdinApi_v03',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-BO'

LANGUAGES = [
    ('es-BO', gettext_noop('Bolivia')),
]

TIME_ZONE = 'America/La_Paz'
# TIME_ZONE = 'UTC−04:00'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'temp')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MAXIMO_TAM_ARCHIVOS = 3
DATE_FORMAT = '%Y-%m-%d'
BASE_STATIC_FILES = BASE_DIR


# SCHEDULER
APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"  # Default
SCHEDULER_AUTOSTART = True


# variables globales
URL_MATRIX = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
API_KEY_MATRIX = 'AIzaSyC5UY7bQchG2hQ8FzvWe50DEcF-G3uqkxY'

# twilio SMS
SMS_SSID = 'AC22d75fb487a8cedc696aa248fb9a100f'
SMS_TOKEN = 'accd14e4c298d5dad315959ef7bf9314'

GRUPO_ENCARGADO_CIUDAD = 'responsable_region'
GRUPO_EMPRESARIO = 'empresario'
GRUPO_CLIENTE = 'cliente'
GRUPO_ADMINISTRADOR = 'administrador'
GRUPO_REPARTIDOR = 'repartidor'
GRUPO_TAXISTA = 'taxista'

# categoria empresas
COMIDA = 'comida'
ECOMMERCE = 'ecommerce'

# categoria productos
_COMIDA_ = '_comida_'
_ECOMMERCE_ = '_ecommerce_'
MAXIMO_HORARIOS = 2

# PIN
PIN_LENGTH = 5




# social configuration

# # Force https redirect
# SECURE_SSL_REDIRECT = False
# # Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# # Force HTTPS in the final URIs
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = False


# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = 3452209874852482
SOCIAL_AUTH_FACEBOOK_SECRET = 'a2c4f4ae190567eea6bb461131147113'

# Google
# 361118566155-v9dmji3smvutr7cph26k15ndbd3ea763.apps.googleusercontent.com
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '361118566155-v9dmji3smvutr7cph26k15ndbd3ea763'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'JCzBITr8ntAP7Z0b-CmFAfbE'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# FACEBOOK_EXTENDED_PERMISSIONS = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email,age_range' 
    }
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
# SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True



SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    # 'social_core.pipeline.user.get_username',
    'apps.autenticacion.custom_pipeline.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'apps.autenticacion.custom_pipeline.create_user',
    # 'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'apps.autenticacion.custom_pipeline.save_profile',
)

