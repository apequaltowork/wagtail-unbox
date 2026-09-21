# Ep 13 — Build notes & gotchas

## Verified on this machine

Everything below ran against `studio.settings.production` locally, with `DEBUG = False`, using
the test client and a local `runserver` on port 8003. There is **no Postgres server on this
machine** and none was installed for this episode — see "What was not verified" at the end.

## ⭐ Gotcha 1 — the generated Dockerfile ships the dev settings

`wagtail start` generates a `Dockerfile` whose server command is `gunicorn studio.wsgi` and which
never sets `DJANGO_SETTINGS_MODULE`. `studio/wsgi.py` defaults to dev. Loading it with no
variables set:

```
settings module : studio.settings.dev
DEBUG           : True
ALLOWED_HOSTS   : ['*']
SECRET_KEY      : django-insecure-kh2$(of6...
```

Deployed as generated, the live site would show full tracebacks — settings included — to anyone,
answer for any hostname, and sign sessions with a key that is committed to git.

Fixed twice over:
- `wsgi.py` now defaults to **production**, which refuses to start without a secret:
  `ImproperlyConfigured: Set the DJANGO_SECRET_KEY environment variable.` Fail closed.
- The Dockerfile sets `DJANGO_SETTINGS_MODULE=studio.settings.production` explicitly.

`manage.py` still defaults to dev, so `runserver` on a laptop is unchanged (checked: all pages 200).

## ⭐ Gotcha 2 — forget collectstatic and the whole site is a 500

With production settings and no `collectstatic`:

```
/                 500
/about/           500
/admin/login/     500
/no-such-page/    500
ValueError: Missing staticfiles manifest entry for 'css/studio.css'
```

**Every** page, including the admin login and the 404 page — so you can't even log in to find
out why. The manifest storage refuses to render `{% static %}` for a file it hasn't seen.

After `collectstatic` (217 files copied, 633 post-processed): all 200, and `/no-such-page/` is a
real **404** using our `404.html` — episode 4's promise, kept.

## ⭐ Gotcha 3 — pointing DATABASE_URL at Postgres fails before connecting

`DATABASE_URL=postgres://…` and `migrate --check`:

```
wagtailsearch.IndexEntry.body: (postgres.E005) 'django.contrib.postgres' must be in
INSTALLED_APPS in order to use SearchVectorField.
```

On Postgres, Wagtail's database search backend uses Postgres full-text search, which needs
`django.contrib.postgres`. Added conditionally. After that the checks pass and it reaches the
connection.

## Gotcha 4 — a wrong DATABASE_URL hangs

Nothing listening on 5432: `OperationalError: connection timeout expired` — after **more than two
minutes**. Added `connect_timeout = 10`: the same failure in **12 seconds**.

## The rest, measured

| Test | Result |
|---|---|
| Nothing set | `Set the DJANGO_SECRET_KEY environment variable.` |
| Secret, no hosts | `Set DJANGO_ALLOWED_HOSTS, e.g. 'studio.example'.` |
| `check --deploy`, generated settings | 6 issues |
| `check --deploy`, new settings | 2 — W005, W021 (HSTS subdomains / preload), left on purpose |
| `http://studio.example/` | **301** → `https://studio.example/` |
| same, with `X-Forwarded-Proto: https` | 200 |
| `Host: evil.example` | **400** |
| HSTS header | `max-age=3600` |
| Stylesheet URL | `/static/css/studio.32463efc1907.css` |
| …with WhiteNoise | 200, `Cache-Control: max-age=315360000, public, immutable`, gzip |
| …without WhiteNoise | **404** |
| An image under `/media/` | **404** |

The hashed filename is worth a sentence on screen: the browser can cache CSS for ten years,
because a change produces a new filename. That is the permanent fix for episode 4's
"I changed the CSS and nothing happened".

## Media is not static

With `DEBUG = False`, Django stops serving `/media/`, and WhiteNoise deliberately doesn't serve
uploads. The production screenshot shows the hero as a broken image with its alt text — which,
incidentally, proves episode 6's alt text. Serving media depends on the host (a volume behind
the web server, or object storage), so it's decided in episode 14.

## Requirements

- Added `whitenoise==6.12.0`, `dj-database-url==3.1.2`, `psycopg[binary]==3.3.6`.
- `site/requirements.txt` — the file the Dockerfile installs — said `Django>=6,<6.1` as generated,
  while the project runs 6.1.1. A production image would have had a different Django than every
  episode was tested on. Both files now pin identical versions. `pip install --dry-run` and
  `pip check`: clean.

## HSTS, deliberately short

`SECURE_HSTS_SECONDS = 3600` by default, no subdomains, no preload. HSTS is a promise browsers
keep: set a year, then break HTTPS, and visitors can't reach the site until it expires. Raise it
once HTTPS on the real domain is proven — episode 14.

## Housekeeping

- `collectstatic` writes to `site/static/`, which **wasn't gitignored**. Added an anchored
  `/site/static/` rule; `site/studio/static/` (the real CSS) is still tracked — checked.

## What was not verified

- **A live Postgres connection.** No server here; installing one (or starting Docker Desktop and
  pulling an image) is a system change I didn't make unasked. What *was* verified: the URL
  parses to `django.db.backends.postgresql`, psycopg 3.3.6 loads with libpq 18, system checks
  pass with the Postgres URL, and an unreachable server fails in 12s. The first real connection
  happens against the host's database in episode 14.
- **Building the Docker image.** Docker Desktop isn't running. The changed `collectstatic` step
  was run locally with the same throwaway values and worked (217 files).
