import os
from PIL import Image
from django.urls import reverse_lazy
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '85umr_$zf2bd58xl)nzf)i*jh)o5h*dp%*3e@pqg+ijem=t1xq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




# REDIRECT_URL 
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/' 
# Application definition

#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = ['127.0.0.1','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',  
    'django_bootstrap_breadcrumbs',  
    'widget_tweaks',
    'ckeditor',   
    'ckeditor_uploader' ,
    'bootstrap3',          
    'setup',
    'account',
    'group',    
    'socle',
    'qcm',
    'sendmail',
    'schedule',
    "django_cron",
    ]
#'social_django',

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
 
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
            ],
 
        },
    },
]



WSGI_APPLICATION = 'sacado.wsgi.application'

 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Backends disponibles : 'postgresql', 'mysql', 'sqlite3' et 'oracle'.
        'NAME': 'sacado',             # Nom de la base de données   new_sacado_clone
        'USER': 'root',
        'PASSWORD': 'root',        
        'HOST': 'localhost',                    # Utile si votre base de données est sur une autre machine
        'PORT': '3306',                         # ... et si elle utilise un autre port que celui par défaut
        'OPTIONS': {
            'sql_mode': 'traditional',
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },


}
 

 

AUTH_USER_MODEL = 'account.User'

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

STATICFILES_DIRS = (  os.path.join(BASE_DIR, 'staticfiles'),)

FILE_UPLOAD_PERMISSIONS = 0o775

MEDIA_URL = 'static/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads')

## For whiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

#################################################################################################################################
 
CKEDITOR_UPLOAD_PATH =  ''
 
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

 

EMAIL_HOST = 'mail.sacado.xyz'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@sacado.xyz'
EMAIL_HOST_PASSWORD = 'VT92KLv;orDN'
EMAIL_USE_TLS = True
