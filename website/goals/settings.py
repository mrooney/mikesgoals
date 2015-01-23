# Django settings for goals project.
import os
import sys

DEBUG = sys.platform == 'darwin'
TESTING = 'test' in sys.argv
TEMPLATE_DEBUG = True

PROJECT_DIR = os.path.dirname(__file__)
WEBSITE_DIR = os.path.dirname(PROJECT_DIR)
PUBLIC_DIR = os.path.join(WEBSITE_DIR, 'public')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ["goals.rowk.com", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'goals.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=4!qasvek(=4&amp;40u(4s+8*#xa44i)hbb2tlrstk$c=_8py&amp;2%f'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'goals.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'goals.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'gunicorn',
    'compressor',
    'django_nose',
    'goals',
    #'social_auth',
)
if not (DEBUG or TESTING):
    INSTALLED_APPS += (
        'raven.contrib.django',
    )

AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_COOKIE_AGE = 24*60*60*30

FOURSQUARE_CONSUMER_KEY = 'foo'
# TODO: read these from an unversioned file like open(os.path.join(WEBSITE_DIR, "foursquare.secret")).read()
FOURSQUARE_CONSUMER_SECRET = 'bar'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGIN_ERROR_URL = 'login'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if not DEBUG:
    SENTRY_DSN = open(os.path.join(WEBSITE_DIR, 'sentry.dsn')).read()

JINJA2_EXTENSIONS = [
    'compressor.contrib.jinja2ext.CompressorExtension',
]
COMPRESS_ENABLED = True
COMPRESS_PARSER = 'compressor.parser.LxmlParser'

WEBSITE_NAME = "Mike's Goals"
from settings_deploy import SERVICES
if DEBUG:
    WEBSITE_URL = "http://localhost:{}".format(SERVICES['nginx']['port'])
else:
    WEBSITE_URL = "http://goals.rowk.com"

LOGIN_URL = "/login"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(WEBSITE_DIR, 'run', 'gunicorn.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

if DEBUG:
    # Show emails in the console during developement.
    DEFAULT_FROM_EMAIL = "mrooney@gmail.com"
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    DEFAULT_FROM_EMAIL = "mrooney@gmail.com"
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = True
    AWS_CREDENTIALS_PATH = os.path.join(WEBSITE_DIR, 'aws.credentials')
    if os.path.exists(AWS_CREDENTIALS_PATH):
        EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = open(AWS_CREDENTIALS_PATH).read().splitlines()


