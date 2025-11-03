# settings.py - FINALIZED FOR RENDER DEPLOYMENT

import os
from pathlib import Path

import dj_database_url
import environ

# Initialize the environment variables
env = environ.Env()

# --- BASE_DIR Calculation (Kept as is) ---
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"DEBUG: BASE_DIR resolved to: {BASE_DIR}") 

# --- .env File Loading (Kept as is) ---
try:
    env_file_path = os.path.join(BASE_DIR, '.env')
    environ.Env.read_env(env_file=env_file_path)
    print(f"DEBUG: Loaded environment variables from: {env_file_path}") 
except FileNotFoundError:
    print(f"DEBUG: Warning: .env file not found at {env_file_path}. Using OS env vars or defaults.")


# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-if-not-in-env')

# Development/Debug Flags (read from .env)
DJANGO_DEVELOPMENT = env.bool('DJANGO_DEVELOPMENT', default=True)
DEBUG = env.bool('DEBUG', default=True)

# Allowed hosts and CSRF trusted origins (read from .env)
# On Render, ALLOWED_HOSTS will be read from OS ENV
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://localhost:8000', 'http://127.0.0.1:8000'])

# --- Security Settings ---
if DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else: # Production settings
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # Proxy headers removed

# --- Application definition ---
INSTALLED_APPS = [
    # ... (all existing apps)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", 
    'mptt',
    'rest_framework',
    'menu',
    'orders',
    'users',
    'reviews',
    'cart',
    'profiles',
    'checkout',
    'gallery',
    'payments',
    'contact',
    'core',
    'stores',
]

# --- MIDDLEWARE (WhiteNoise ADDED) ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # *** ADD WHITE NOISE HERE ***
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- CORRECT ROOT_URLCONF ---
ROOT_URLCONF = 'urban.urls'

# --- CORRECT TEMPLATES (Kept as is) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.location_context',
            ],
        },
    },
]

# --- CORRECT WSGI_APPLICATION ---
WSGI_APPLICATION = 'urban.wsgi.application'

# --- Database Configuration (Updated for Render/Postgres SSL) ---
if DJANGO_DEVELOPMENT:
    # Reads DATABASE_URL from .env file in BASE_DIR
    DATABASES = { "default": env.db_url('DATABASE_URL', default="postgres://user:pass@host:port/db") }
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=600)
else:
    # PRODUCTION FIX: Retrieve the VALUE of the URL and pass it to the parser.
    # The previous code passed the VALUE to a function expecting a KEY NAME, causing KeyError.
    
    # 1. Safely get the connection string VALUE from the environment
    DATABASE_URL_VALUE = env.str('DATABASE_URL') 
    
    # 2. Pass the VALUE directly to the dj_database_url parser.
    DATABASES = { 
        "default": dj_database_url.parse(DATABASE_URL_VALUE)
    }
    
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=600)
    
    # *** CRITICAL RENDER FIX: SSL is REQUIRED for external Postgres connections ***
    DATABASES["default"]["OPTIONS"] = {'sslmode': 'require'}

# --- Password validation (Kept as is) ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization (Kept as is) ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi" 
USE_I18N = True
USE_TZ = True 

# --- Static files ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# *** NEW: Configure WhiteNoise Storage Backend ***
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Media files (User Uploads - Kept as is) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Default primary key field type (Kept as is) ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Login/Logout URLs (Kept as is) ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --- Session Settings (Kept as is) ---
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600 

# --- Caches (Kept as is) ---
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-samakisamaki-cache',
    }
}

# --- Email Settings (Kept as is) ---
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')