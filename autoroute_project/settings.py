import os
from pathlib import Path

STRIPE_PUBLISHABLE_KEY = 'pk_test_51QiYbvBXMMkPWU9DyR5zfOeJ1W83GBInB05JRheYinz842Bz95ZpyVExHKkLrtkUMqKKp38JD2d4wz5tZoPEHFtH00tL7ptyMo'
STRIPE_SECRET_KEY = 'sk_test_51QiYbvBXMMkPWU9D4Hv9jp6xHTEWUmGzpq77KMy3eBero6UhNb1Ai9j88XBQNvrHADQNBCnVWtinaPamd1lZzZjv008K4PfJQ0'


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-hm-edy4e)2c06m##smqybu$%-o4ck-!6@jr*t(6ph9tzo0v=iw'


DEBUG = True

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autouroute_api',
    'rest_framework', 
    'rest_framework_simplejwt',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 'drf_spectacular.openapi.AutoSchema',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


ROOT_URLCONF = 'autoroute_project.urls' 
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "YOUR_DEFAULT_KEY")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'autouroute_api/templates')],
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

WSGI_APPLICATION = 'autoroute_project.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Highway_management',
        'USER': 'postgres',
        'PASSWORD': 'Sallouma21.',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True



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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'