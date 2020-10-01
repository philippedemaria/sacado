import os
from PIL import Image
from django.urls import reverse_lazy
from django.conf import global_settings
 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



PRODUCTION = os.environ.get('PRODUCTION')

if PRODUCTION:
    # configuration production
    DEBUG = os.environ.get('DEBUG') == 'True'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALLOWED_HOSTS = ['sacado.xyz', 'ressources.sacado.xyz']

    # configuation bdd
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_PORT = os.environ.get('MYSQL_PORT')

    # configuration email
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
    DEFAULT_FROM_EMAIL = 'SacAdo < info@sacado.xyz >'

    # social_django
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE')
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE')
    SECURE_REFERRER_POLICY = os.environ.get('SECURE_REFERRER_POLICY')
    CONN_MAX_AGE = os.environ.get('CONN_MAX_AGE')

else:
    # configuration dévellopement
    DEBUG = False
    ALLOWED_HOSTS = ["*"]
    SECRET_KEY = '85umr_$zf2bd58xl)nzf)i*jh)o5h*dp%*3e@pqg+ijem=t1xq'

    # configuation bdd
    MYSQL_DATABASE = 'sacado'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_PORT = 3306
    DEFAULT_FROM_EMAIL = 'SacAdo < info@sacado.xyz >'
    # configuration email : affichés dans la console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    CONN_MAX_AGE = 3600
    SECURE_REFERRER_POLICY = 'same-origin'
 
# REDIRECT_URL
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
#LOGIN_URL = reverse_lazy('login')
LOGIN_URL = '/'

# Application definition


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap_breadcrumbs',
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    'bootstrap3',
    'setup',
    'social_django',
    'account',
    'group',
    'socle',
    'qcm',
    'sendmail',
    'schedule',
    'school',
    "django_cron",
    'corsheaders',
    ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]


if PRODUCTION:
    pass
    #INSTALLED_APPS = ['whitenoise.runserver_nostatic', ] + INSTALLED_APPS
else:
    INSTALLED_APPS += ['debug_toolbar', ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INTERNAL_IPS = ['127.0.0.1', ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

CRON_CLASSES = [
    "setup.cron.MyCronJob",
]

ROOT_URLCONF = 'sacado.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'sacado.context_processors.menu',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]



WSGI_APPLICATION = 'sacado.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': 'localhost',
        'PORT': MYSQL_PORT,
        'OPTIONS': {
            'sql_mode': 'traditional',
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },
}

AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'sacado.pipeline.get_usertype',
    'social_core.pipeline.user.create_user',
    'sacado.pipeline.complete_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Africa/Algiers' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
 
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)

FILE_UPLOAD_PERMISSIONS = 0o775

MEDIA_URL = 'https://ressources.sacado.xyz/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT')


########################################################################################################################

CKEDITOR_UPLOAD_PATH = ''

CKEDITOR_CONFIGS = {
    'default': {
        'height': 200,
        'width': '100%',
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ], 
    }
}




 

########################################################################################################################
if not PRODUCTION :
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/debug.log',
                'backupCount': 10,  # keep at most 10 log files
                'maxBytes': 1048576,  # 1*1024*1024 bytes (1MB)
            },

        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
