import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "your-very-secure-secret-key-here"

DEBUG = True    # Production ready

# --- Allowed Hosts ---
ALLOWED_HOSTS = [
    "urbansofaskenya.com",
    "www.urbansofaskenya.com",
    "urban-sofas.onrender.com",
    "127.0.0.1",
    "localhost",
]

# --- CSRF ---
CSRF_TRUSTED_ORIGINS = [
    "https://urbansofaskenya.com",
    "https://www.urbansofaskenya.com",
    "https://urban-sofas.onrender.com",
]

# --- Installed Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mptt",
    "rest_framework",
    "menu",
    "orders",
    "users",
    "reviews",
    "cart",
    "profiles",
    "checkout",
    "gallery",
    "contact",
    "core",
    "stores",
    "widget_tweaks",
    "cloudinary",
    "cloudinary_storage",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.db_reconnect.DBReconnectMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urban.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            #    "core.context_processors.location_context",
            ],
        },
    },
]

WSGI_APPLICATION = "urban.wsgi.application"

# --- Database (Render Postgres) ---
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=300,
        ssl_require=True,
    )
}
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

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

# --- Static & Media ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# --- Cloudinary ---
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET", ""),
}

STORAGES = {
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Auth Redirects ---
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --- Sessions ---
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600

# --- Cache ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "urban-cache",
    }
}

# --- Emails ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Auto-superuser on Render ---
if os.environ.get("RENDER", None):
    import django
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = "admin"
    email = "admin@urban-sofas.com"
    password = "admin1234"

    if not User.objects.filter(username=username).exists():
        print("Creating default superuser for Render deployment...")
        User.objects.create_superuser(username, email, password)
    else:
        print("Superuser already exists.")
