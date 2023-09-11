"""
Django settings for Proyecto_RTDF project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b$%#mw8_62v-q!t9(9noi_xo(5&fjnq(s^(q0%1*rp@#3f5-=)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


#LOCAL
ALLOWED_HOSTS = []


# #ENTORNO PYTHONANYWHERE
# ALLOWED_HOSTS = ['farmaciadigital.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rtdf',
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

ROOT_URLCONF = 'Proyecto_RTDF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Proyecto_RTDF.wsgi.application'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  
)

AUTH_USER_MODEL = 'rtdf.Usuario'  # Reemplaza 'tu_app' con el nombre de tu aplicación

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

##LOCAL DATABASE
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'rtdf',
         'USER': 'root',
         'PASSWORD': 'practica',
         'HOST': 'localhost',
         'PORT': '3306',
         'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
     }
 }


# ##PYTHON ANYWHERE DATABASE
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'farmaciadigital$rtdf',
#          'USER': 'farmaciadigital',
#          'PASSWORD': 'rtdfdev2023',
#          'HOST': 'farmaciadigital.mysql.pythonanywhere-services.com',
#          'PORT': '3306',
#          'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
#      }
#  }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'  # Esta es la URL de inicio de sesión que has definido