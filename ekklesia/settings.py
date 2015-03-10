# -*- coding:utf-8 -*-
# Django settings for ekklesia project.

# DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ekklesia.db',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Guayaquil'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-EC'

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"





import os
#STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]+['static'])
#STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# STATICFILES_STORAGE = (
# 'require.storage.OptimizedStaticFilesStorage',
#     )

REQUIRE_BUILD_PROFILE = 'app.build.js'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z4216vitey^y6957)&wytdee!6w4dmc-=x!9r4uh-#l2ua@8p)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'sacramentos.middleware.ConfiguracionMiddleware',
    'sacramentos.middleware.ParroquiaSessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'sacramentos.middleware.AdminLocaleURLMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ekklesia.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ekklesia.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'mockups',
)

LOCAL_APPS = (
    'ciudades',
    'core',
    'home',
    'sacramentos',
    'usuarios',
)

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



# Settings Personalizados de ekklesia

# Sirve para vincular el User con un Perfil de Usuario customizado
# Se debe poner el nombre de la aplicacion donde esta el perfil 
# mas la clase que administra el perfil
AUTH_PROFILE_MODULE = 'sacramentos.PerfilUsuario'

#Sirve para indicar a donde se debe redirigir cada vez que se logue
LOGIN_REDIRECT_URL = '/home/'

# Configuración para el envío de email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'floysinternacional@gmail.com'
EMAIL_HOST_PASSWORD = '13cordova'
EMAIL_USE_TLS = True

#Sirve para expirar la sesion al cerrar el navegador
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Para que la sesión expire en una hora
# SESSION_COOKIE_AGE = 3600

#Sirve para subir datos al servidor
# FIXTURE_DIRS = (
#    'ciudades',
# )

# DATETIME_INPUT_FORMATS = (
#     '%Y-%m-%dT%H:%M:%S',
#     '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
#     '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
#     '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
#     '%Y-%m-%d',              # '2006-10-25'
#     '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
#     '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
#     '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
#     '%m/%d/%Y',              # '10/25/2006'
#     '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
#     '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
#     '%m/%d/%y %H:%M',        # '10/25/06 14:30'
#     '%m/%d/%y',              # '10/25/06'
#     )


# El siguiente código permite añadir nuevos procesadores de contexto
# a los que vienen por defecto en Django

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "sacramentos.context_processors.parametros_diocesis",
    "core.context_processors.menu",
    "sacramentos.context_processors.menu",
    'django.core.context_processors.request',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#Habilita los tipos de authenticacion para django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}