# Ep 13 — Commands

Everything below was run and checked on the recording machine, except where marked.

## Start from episode 12's end state

```bash
git checkout ep12-end
```

## 1. See where the generated settings stand

```powershell
$env:DJANGO_SETTINGS_MODULE = "studio.settings.production"
python manage.py check --deploy
```

```
System check identified 6 issues (0 silenced).
```

## 2. Production dependencies

```bash
pip install whitenoise==6.12.0 dj-database-url==3.1.2 "psycopg[binary]==3.3.6"
```

Add them to **both** `requirements.txt` (repo root) and `site/requirements.txt` — the second is
the one the Dockerfile installs. While you're there, make `site/requirements.txt` pin
`Django==6.1.1`: as generated it says `Django>=6,<6.1`.

## 3. `studio/settings/production.py`

Replace it. The full file, commented, is in the repo:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/studio/settings/production.py

The parts that matter:

```python
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = False

def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable.")
    return value

def env_list(name, default=""):
    return [item.strip() for item in env(name, default).split(",") if item.strip()]

SECRET_KEY = env("DJANGO_SECRET_KEY", required=True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("Set DJANGO_ALLOWED_HOSTS, e.g. 'studio.example'.")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

DATABASES = {"default": dj_database_url.config(
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600, conn_health_checks=True)}
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    INSTALLED_APPS = [*INSTALLED_APPS, "django.contrib.postgres"]   # or postgres.E005
    DATABASES["default"].setdefault("OPTIONS", {})["connect_timeout"] = 10

MIDDLEWARE = list(MIDDLEWARE)
MIDDLEWARE.insert(MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
                  "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", "true").lower() != "false"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(env("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 4. Make the server fail closed — `studio/wsgi.py`

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio.settings.production")
```

`manage.py` keeps `studio.settings.dev`, so `runserver` on your laptop doesn't change.

## 5. The Dockerfile — `site/Dockerfile`

Add the settings module to the `ENV` block:

```dockerfile
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=studio.settings.production
```

and give `collectstatic` throwaway values — it needs no real secret:

```dockerfile
RUN DJANGO_SECRET_KEY=collectstatic-only DJANGO_ALLOWED_HOSTS=localhost \
    python manage.py collectstatic --noinput --clear
```

*Not built here — Docker Desktop wasn't running. The collectstatic step was run locally with the
same values.*

## 6. Ignore the collected files — `.gitignore`

```gitignore
/site/static/
```

Anchored with a leading `/`, so `site/studio/static/` (your real CSS) stays tracked.

## 7. Try production settings on your laptop

Generate a key:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

PowerShell:

```powershell
$env:DJANGO_SETTINGS_MODULE   = "studio.settings.production"
$env:DJANGO_SECRET_KEY        = "<paste the key>"
$env:DJANGO_ALLOWED_HOSTS     = "127.0.0.1"
$env:DJANGO_SECURE_SSL_REDIRECT = "false"     # no HTTPS on a laptop
python manage.py collectstatic --noinput
python manage.py check --deploy
python manage.py runserver 127.0.0.1:8003
```

bash / zsh:

```bash
export DJANGO_SETTINGS_MODULE=studio.settings.production
export DJANGO_SECRET_KEY='<paste the key>'
export DJANGO_ALLOWED_HOSTS=127.0.0.1
export DJANGO_SECURE_SSL_REDIRECT=false
python manage.py collectstatic --noinput
python manage.py check --deploy
python manage.py runserver 127.0.0.1:8003
```

Then http://127.0.0.1:8003/ — styled (WhiteNoise), images broken (media isn't served when
`DEBUG = False` — episode 14), and http://127.0.0.1:8003/no-such-page/ shows the real 404 page.

Close the terminal afterwards, or remove the variables, before going back to `runserver` for
development.

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 13"
git tag ep13-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Live site shows Django's yellow debug page | Server loaded dev settings | `DJANGO_SETTINGS_MODULE=studio.settings.production` — steps 4–5 |
| `Set the DJANGO_SECRET_KEY environment variable.` | Working as intended | Set it |
| Every page, even the admin, is a 500 | `Missing staticfiles manifest entry` — no `collectstatic` | `python manage.py collectstatic --noinput` |
| Site unstyled with `DEBUG = False` | Nothing serving static | WhiteNoise middleware — step 3 |
| Images broken with `DEBUG = False` | Django doesn't serve media in production | Host's web server or object storage — episode 14 |
| `postgres.E005 … django.contrib.postgres` | Postgres URL without the contrib app | Step 3, the `if` block |
| Commands hang, then `connection timeout expired` | Wrong or unreachable `DATABASE_URL` | Check the URL; `connect_timeout` makes it fail in ~10s |
| 400 Bad Request for every page | Hostname not in `DJANGO_ALLOWED_HOSTS` | Add it |
| Redirect loop on the host | Proxy terminates HTTPS, Django doesn't know | `SECURE_PROXY_SSL_HEADER` — and the host must send `X-Forwarded-Proto` |
| 403 CSRF on admin login in production | Origin not trusted | `DJANGO_CSRF_TRUSTED_ORIGINS=https://your.domain` |
| Can't log in over plain HTTP locally | `SESSION_COOKIE_SECURE = True` | Expected; test logins on the real HTTPS host |
