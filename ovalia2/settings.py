from pathlib import Path
import os
import dj_database_url
from botocore.client import Config
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]

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
    "storages",
]

AUTH_USER_MODEL = "gestion.User"

# ==================================================
# MIDDLEWARE
# ==================================================

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

# ==================================================
# URL / WSGI
# ==================================================

ROOT_URLCONF = "ovalia2.urls"
WSGI_APPLICATION = "ovalia2.wsgi.application"

# ==================================================
# DATABASE
# ==================================================

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
# STATIC FILES
# ==================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==================================================
# MEDIA FILES (LOCAL — WORKING)
# ==================================================


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = "media"
AWS_S3_REGION_NAME = "auto"
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
AWS_S3_ENDPOINT_URL = f"https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"


AWS_S3_ADDRESSING_STYLE = "path"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_CLIENT_CONFIG = Config(
    region_name="auto",
    signature_version="s3v4",
)

MEDIA_URL = os.getenv("R2_PUBLIC_URL")

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
# STRIPE
# ==================================================

CSRF_TRUSTED_ORIGINS = [
    "https://ovalia-prod-production.up.railway.app",
    "https://www.bijouxovalia.com",
    "https://bijouxovalia.com",
]

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
