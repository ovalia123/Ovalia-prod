from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_filters",

    "gestion",
    "myapp",
]

AUTH_USER_MODEL = "gestion.User"

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==================================================
# URL / WSGI
# ==================================================

ROOT_URLCONF = "ovalia2.urls"
WSGI_APPLICATION = "ovalia2.wsgi.application"

# ==================================================
# DATABASE (LOCAL)
# ==================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==================================================
# STATIC FILES (LOCAL)
# ==================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ==================================================
# MEDIA FILES (LOCAL)
# ==================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==================================================
# I18N
# ==================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==================================================
# DEFAULT PK
# ==================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==================================================
# STRIPE (TEST MODE)
# ==================================================

STRIPE_SECRET_KEY = "sk_test_51Smxkz8FV4nmYpJpatkpeMdJXMqWUQC7onhw8zJ2bTYMFgg5pV7VBeGS6yRDXRUrBQAZy2Uk1q9Bf5ezJytKbAnF007FUWrSMp"
STRIPE_PUBLISHABLE_KEY = "pk_test_51Smxkz8FV4nmYpJpITr8cdAiylrpJ553xDFC3n9eRsSMrQ2JgaImG8kDtBV1pUBFVkapuTD3RMV6rhqmzWtxqQUZ00HoHnhR6H"
STRIPE_WEBHOOK_SECRET = "whsec_454e99e0325808a48e12a20fe05d6d710b97266cb3ee3b0da6776b54015be8df"

# ==================================================
# CSRF (LOCAL)
# ==================================================

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]
