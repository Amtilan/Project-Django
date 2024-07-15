from pathlib import Path

import environ


BASE_DIR=Path(__file__).resolve().parent.parent.parent.parent
env=environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY=env('DJANGO_SECRET_KEY', default='secret')

DEBUG=False

ALLOWED_HOSTS=[]

INSTALLED_APPS=[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
     # third party
    'elasticapm.contrib.django',

    
    # First Party
    'core.apps.products.apps.ProductsConfig',
    'core.apps.customers.apps.CustomersConfig',
]

MIDDLEWARE=[
    "core.project.middlewares.ElasticApmMiddleware",
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF='core.project.urls'

TEMPLATES=[
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

WSGI_APPLICATION='core.project.wsgi.application'

DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env("POSTGRES_PORT"),
    },
}

AUTH_PASSWORD_VALIDATORS=[
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

LANGUAGE_CODE='ru'

TIME_ZONE='Europe/Moscow'

USE_I18N=True

USE_TZ=True

STATIC_URL='static/'
STATIC_ROOT=BASE_DIR / 'static'

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'


ELASTIC_APM = {
    'SERVICE_NAME': 'reviews',
    'SERVER_URL': env('APM_URL', default='http://apm-server:8200'),
    'DEBUG': DEBUG,
    'CAPTURE_BODY': 'all',
    "ENVIRONMENT": 'prod',
    'USE_ELASTIC_EXCEPTHOOK': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                        '%(thread)d %(message)s error_meta:\n%(error_meta)s',
        },
    },
    'handlers': {
        'elasticapm': {
            'level': 'WARNING',
            'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'mysite': {
            'level': 'WARNING',
            'handlers': ['elasticapm'],
            'propagate': False,
        },
        # Log errors from the Elastic APM module to the console (recommended)
        'elasticapm.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

ELASTIC_URL = env('ELASTIC_URL')
ELASTIC_PRODUCT_INDEX = env('ELASTIC_PRODUCT_INDEX', default='product-index')