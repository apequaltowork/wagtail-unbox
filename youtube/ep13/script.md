# Ep 13 — Production Settings

Start from `git checkout ep12-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — what `wagtail start` gave us for production
A `production.py` that sets `DEBUG = False` and nothing else. `check --deploy`: 6 issues. And no
`SECRET_KEY` at all — it expects a `local.py` that doesn't exist.

### ⭐ The Dockerfile runs the dev settings
`gunicorn studio.wsgi`, no `DJANGO_SETTINGS_MODULE`, and `wsgi.py` defaults to dev: DEBUG on, any
host, the SECRET_KEY that's in git. Deployed as generated, the world gets tracebacks. Default WSGI
to production — it refuses to start without a secret. Fail closed. Set it in the Dockerfile too.

### Everything from the environment
`DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` required, with messages that say which variable.
No hosts would otherwise mean every request is a 400.

### One variable for the database
`DATABASE_URL`, via dj-database-url. Unset → the local SQLite file, so production settings run on
a laptop.

### ⭐ Postgres fails before it connects
Point it at Postgres: `postgres.E005 'django.contrib.postgres' must be in INSTALLED_APPS`.
Wagtail's search switches to Postgres full-text search. Add it when the engine is Postgres.

### A wrong URL hangs
No server listening: over two minutes to fail. `connect_timeout = 10`: 12 seconds.

### ⭐ Forget collectstatic, lose the whole site
Every page 500 — admin login included. `Missing staticfiles manifest entry`. Run `collectstatic`.

### WhiteNoise
Without it, the CSS is a 404 once DEBUG is off. With it: 200, gzip, and a hashed filename cached
for ten years. That's the permanent fix for episode 4's cache trap.

### Media is not static
Images 404 under DEBUG=False. The screenshot: a broken hero showing its alt text. Media depends on
the host — episode 14.

### HTTPS behind a proxy
`SECURE_PROXY_SSL_HEADER`, then redirect, secure cookies, HSTS. http → 301; wrong Host → 400.
HSTS starts at an hour — it's a promise browsers keep.

### check --deploy
6 → 2, and the 2 are deliberate.

### The requirements file the Dockerfile uses
Generated with `Django<6.1`; we run 6.1.1. Pinned identically.

### What isn't verified yet
No Postgres server here. The URL, the driver, the checks and the timeout are verified; the first
real connection is episode 14.

### Next
Ep 14: deploy it.
