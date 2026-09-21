"""Production settings. Everything secret or host-specific comes from the
environment, so the same code runs on any host and nothing sensitive is in git.

Required:
    DJANGO_SECRET_KEY        a long random string (see commands.md)
    DJANGO_ALLOWED_HOSTS     comma-separated, e.g. "studio.example,www.studio.example"

Optional:
    DATABASE_URL             e.g. postgres://user:pass@host:5432/dbname
                             (defaults to the local SQLite file)
    DJANGO_CSRF_TRUSTED_ORIGINS  comma-separated, with scheme: "https://studio.example"
    WAGTAILADMIN_BASE_URL    e.g. "https://studio.example" -- used in admin emails
    EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL
    DJANGO_SECURE_SSL_REDIRECT  "false" only if the host already redirects to HTTPS
"""

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable.")
    return value


def env_list(name, default=""):
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


# ---------------------------------------------------------------- secrets & hosts

SECRET_KEY = env("DJANGO_SECRET_KEY", required=True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    # Django would start and then answer every request with 400 Bad Request.
    # Refuse to start instead, with a message that says why.
    raise ImproperlyConfigured("Set DJANGO_ALLOWED_HOSTS, e.g. 'studio.example'.")

# Django 4+ checks the full origin, scheme included, for POSTs such as the admin
# login and the contact form when the site is behind an HTTPS proxy.
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", f"https://{ALLOWED_HOSTS[0]}")

# ---------------------------------------------------------------- database

# One variable, any database. Unset means the local SQLite file, so these
# settings can be tried on a laptop before any server exists.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",  # noqa: F405
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# On Postgres, Wagtail's database search backend switches to Postgres full-text
# search -- which needs django.contrib.postgres, or every system check fails
# with postgres.E005 before a single query runs.
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    INSTALLED_APPS = [*INSTALLED_APPS, "django.contrib.postgres"]  # noqa: F405
    # A wrong DATABASE_URL otherwise hangs for minutes before failing. Fail fast.
    DATABASES["default"].setdefault("OPTIONS", {})["connect_timeout"] = 10

# ---------------------------------------------------------------- static files

# runserver and Django stop serving static files when DEBUG is False. WhiteNoise
# serves them from the app itself, straight after SecurityMiddleware.
MIDDLEWARE = list(MIDDLEWARE)  # noqa: F405 -- a copy, so base.MIDDLEWARE is untouched
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)
# Compressed, hashed filenames -- the "manifest" means {% static %} fails loudly
# for any file that collectstatic didn't see. Run collectstatic on every deploy.
STORAGES["staticfiles"]["BACKEND"] = (  # noqa: F405
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# Media (uploads) is NOT static and WhiteNoise won't serve it. That needs the
# host's web server or object storage -- decided with the host, in episode 14.

# ---------------------------------------------------------------- email

if env("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = int(env("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", f"website@{ALLOWED_HOSTS[0]}")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ---------------------------------------------------------------- HTTPS

# The host terminates TLS and forwards plain HTTP with this header. Without it,
# Django thinks every request is insecure and SECURE_SSL_REDIRECT loops forever.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", "true").lower() != "false"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Start HSTS short. A long max-age is a promise browsers keep even if HTTPS breaks.
SECURE_HSTS_SECONDS = int(env("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = True

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
