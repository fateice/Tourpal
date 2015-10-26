import os
import os.path
from os import environ
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

debug = not environ.get("APP_NAME", "")   
if debug:  
    MYSQL_DB = 'bookdb'      
    MYSQL_USER = 'root'   
    MYSQL_PASS = '123456'   
    MYSQL_HOST_M = '127.0.0.1'   
    MYSQL_HOST_S = '127.0.0.1'   
    MYSQL_PORT = '3306'   
else:   
#SAE   
    import sae.const   
    MYSQL_DB = sae.const.MYSQL_DB   
    MYSQL_USER = sae.const.MYSQL_USER   
    MYSQL_PASS = sae.const.MYSQL_PASS  
    MYSQL_HOST_M = sae.const.MYSQL_HOST
    MYSQL_HOST_S = sae.const.MYSQL_HOST_S   
    MYSQL_PORT = sae.const.MYSQL_PORT
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sh6)+e2crkh9_0p2nv$i1hst%bixt5bn@*6c0$qkkttk_5^amf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hiker.hithiker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hiker.urls'

WSGI_APPLICATION = 'hiker.wsgi.application'


DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': MYSQL_DB,
    'USER': MYSQL_USER,
    'PASSWORD': MYSQL_PASS,
    'HOST': MYSQL_HOST_M,
    'PORT': MYSQL_PORT,
    }
}

DEFAULT_CHARSET='utf-8'

ALLOWED_HOSTS = [
                 '.sinaapp.com',
                 ]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    './templates',
)