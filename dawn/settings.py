"""
Django settings for dawn project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
# Build paths inside the project like this: BASE_DIR / 'subdir'.

from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hours.apps.HoursConfig',
    'account.apps.AccountConfig',
    'tailwind',
    'theme',
    'django_browser_reload',
    'crispy_forms',
    'crispy_tailwind',
    'impersonate',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# Needed for Tailwind
TAILWIND_APP_NAME = 'theme'

# Needed for Tailwind
INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dawn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'dawn/templates'],  # noqa
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

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/hours/'
LOGOUT_REDIRECT_URL = '/hours/'

WSGI_APPLICATION = 'dawn.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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


LOCALE_PATHS = [
    BASE_DIR / 'dawn',
    BASE_DIR / 'account',
    BASE_DIR / 'hours',
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

FORMAT_MODULE_PATH = [
    "dawn.formats",
]

DATE_FORMAT = "Y-m-d"

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ("uk", _("Ukrainian")),
    ("en-us", _("English")),
]

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / 'dawn/static']
STATIC_URL = 'static/'

IMPERSONATE = {
    'REDIRECT_URL': '/hours/',
    'PAGINATE_COUNT': 10,
    'REQUIRE_SUPERUSER': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

from .settings_local import *  # noqa
