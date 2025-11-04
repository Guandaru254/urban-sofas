# settings.py - FINALIZED FOR LOCAL + RENDER DEPLOYMENT WITH CLOUDINARY

import os
from pathlib import Path
import dj_database_url
import environ

# Initialize environment variables
env = environ.Env()

# --- BASE_DIR ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load .env File ---
try:
    env_file_path = os.path.join(BASE_DIR, '.env')
    environ.Env.read_env(env_file=env_file_path)
except FileNotFoundError:
    print(f"DEBUG: .env not found, using OS environment variables")

# --- Security ---
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-if-not-in-env')
DJANGO_DEVELOPMENT = env.bool('DJANGO_DEVELOPMENT', default=True)
DEBUG = env.bool('DEBUG', default=True)

# --- Allowed Hosts & CSRF ---
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=['http://localhost:8000', 'http://127.0.0.1:8000']
)

# --- Security Settings ---
if DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# --- Installed Apps ---
INSTALLED_APPS = [
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
    'contact',
    'core',
    'stores',
    'widget_tweaks',
]

# --- Add Cloudinary only in production ---
if not DJANGO_DEVELOPMENT:
    INSTALLED_APPS += [
        'cloudinary',
        'cloudinary_storage',
    ]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URL and Template Settings ---
ROOT_URLCONF = 'urban.urls'

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

WSGI_APPLICATION = 'urban.wsgi.application'

# --- Database ---
if DJANGO_DEVELOPMENT:
    DATABASES = {
        "default": env.db_url(
            "DATABASE_URL",
            default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
        )
    }
else:
    DATABASE_URL_VALUE = env.str('DATABASE_URL')
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL_VALUE)
    }
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=600)
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Localization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Media Files (Local by default) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Cloudinary Storage (Render only) ---
if not DJANGO_DEVELOPMENT:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
        'API_KEY': env('CLOUDINARY_API_KEY', default=''),
        'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
    }

# --- Default PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Authentication Redirects ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --- Session Settings ---
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600

# --- Cache ---
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-urban-cache',
    }
}

# --- Email Settings ---
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
# --- Auto-create superuser on Render (only runs once) ---
if os.environ.get('RENDER', None):  # Only run in Render environment
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = "admin"
    email = "admin@urban-sofas.com"
    password = "admin1234"

    if not User.objects.filter(username=username).exists():
        print("Creating default superuser for Render deployment...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Superuser already exists. Skipping creation.")
