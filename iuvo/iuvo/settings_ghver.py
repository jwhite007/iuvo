from configurations import Configuration, values
from urlparse import urljoin
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Base(Configuration):

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'SECRET'

    ALLOWED_HOSTS = ['localhost']

    # Application definition
    DEFAULT_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'bootstrap3',
        'django_crontab',
    )

    LOCAL_APPS = (
        'iuvo_app',
    )

    ALLAUTH_APPS = (
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
    )

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS + ALLAUTH_APPS

    # ACCOUNT_ACTIVATION_DAYS = 3

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'XXXX'
    EMAIL_HOST_PASSWORD = 'XXXX'
    DEFAULT_FROM_EMAIL = 'Iuvo Staff <XXXX>'
    EMAIL_PORT = 587

    # Allauth config settings
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_EMAIL_REQUIRED = True
    # ACCOUNT_UNIQUE_EMAIL = False
    SOCIALACCOUNT_EMAIL_REQUIRED = True
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    SOCIALACCOUNT_PROVIDERS = {
        'google':
            {'SCOPE': ['profile',],
             'AUTH_PARAMS': {'access_type': 'online'}}
    }


    TEMPLATE_DIRS = (
        'iuvo_app/templates/allauth',
        )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'iuvo.urls'

    WSGI_APPLICATION = 'iuvo.wsgi.application'

    DEBUG = False
    TEMPLATE_DEBUG = False

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'iuvodb',
            'USER': 'iuvo_user',
            'PASSWORD': 'XXXX',
            'HOST': 'localhost',
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    SITE_ID = 2

    LOGIN_URL = 'login'
    LOGOUT_URL = 'logout'
    LOGIN_REDIRECT_URL = '/'

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.messages.context_processors.messages',
        'django.contrib.auth.context_processors.auth',
        # Required by allauth template tags
        'django.core.context_processors.request',
        # allauth specific context processors
        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
        )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',)


class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    INSTALLED_APPS = Base.INSTALLED_APPS + ('debug_toolbar',)

    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        '/var/www/iuvo/static',
        )

    BOOTSTRAP3 = {
    'jquery_url': urljoin(STATIC_URL, 'jquery.min.js'),
    'base_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/'),
    'css_url': urljoin(STATIC_URL, 'bootstrap.css'),
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': True,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
    'set_required': True,
    'form_required_class': '',
    'form_error_class': '',
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
        },
    'formset_renderers':{
        'default': 'bootstrap3.renderers.FormsetRenderer',
        },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        },
    }

    # run "python manage.py crontab add" to add jobs to crontab
    # run "python manage.py crontab remove" to remove jobs
    CRONJOBS = [
        # ('*/1 * * * *', 'iuvo_app.cron.send_with_username'),
        ('*/1 * * * *', 'iuvo_app.cron.send_notifications'),
        ('*/1 * * * *', 'iuvo_app.cron.send_3day_notifications'),
        # ('*/1 * * * *', 'iuvo_app.cron.test'),
        # # runs every day at midnight.
        # ('0 0 * * *', 'iuvo_app.cron.send_3day_notifications'),
    ]

class Prod(Base):
    ALLOWED_HOSTS = ['*']
    ADMINS = (
        ('James White', 'jwhite007@gmail.com'),
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211'
        }
    }
    # Allauth setting
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

    INSTALLED_APPS = Base.INSTALLED_APPS + ('s3_folder_storage',)

    # DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    # DEFAULT_S3_PATH = "media"
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = "static"
    AWS_ACCESS_KEY_ID = 'XXXX'
    AWS_SECRET_ACCESS_KEY = 'XXXX'
    AWS_STORAGE_BUCKET_NAME = 'XXXX'

    # MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    # For use with http:
    # MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
    # For use with https:
    # MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    # For use with http:
    # STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
    # For use with https:
    STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    BOOTSTRAP3 = {
    'jquery_url': urljoin(STATIC_URL, 'jquery.min.js'),
    'base_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/'),
    'css_url': urljoin(STATIC_URL, 'bootstrap.css'),
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': True,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
    'set_required': True,
    'form_required_class': '',
    'form_error_class': '',
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
        },
    'formset_renderers':{
        'default': 'bootstrap3.renderers.FormsetRenderer',
        },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        },
    }

    # run "python manage.py crontab add" to add jobs to crontab
    # run "python manage.py crontab remove" to remove jobs
    CRONJOBS = [
        ('*/15 * * * *', 'iuvo_app.cron.send_notifications'),
        # # runs every day at midnight.
        ('0 0 * * *', 'iuvo_app.cron.send_3day_notifications'),
    ]