from pathlib import Path
import os

# BASE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY

SECRET_KEY = 'django-insecure-change-this-key'
DEBUG = False

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# APPLICATIONS

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'business',
]

# MIDDLEWARE

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT URL

ROOT_URLCONF = 'SokoConnect.urls'

# TEMPLATES

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]

# WSGI

WSGI_APPLICATION = 'SokoConnect.wsgi.application'

# DATABASE (SQLite for now)

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}

# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [
{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES (IMPORTANT FOR RENDER)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA FILES

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DEFAULT FIELD

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL (DEV MODE)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = '[noreply@sokoconnect.com](mailto:noreply@sokoconnect.com)'

# ===============================

# OPTIONAL PAYMENT CONFIG (KEEP SAFE)

# ===============================

# Stripe

STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = ''

# PayPal

PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = ''
PAYPAL_CLIENT_SECRET = ''

# M-Pesa

MPESA_CONSUMER_KEY = ''
MPESA_CONSUMER_SECRET = ''
