# Ep 13 — Production Settings

| | |
|---|---|
| **Video file** | `youtube/ep13/out/ep13.mp4` |
| **Subtitles** | `youtube/ep13/out/ep13.srt` |
| **Captions (upload these)** | `youtube/ep13/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep13/assets/thumb.png` |
| **Runtime** | 6:06 |
| **Git tag** | `ep13-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Ready to upload |
| **URL** | — |

---

## Title

```
Wagtail Production Settings: DEBUG, Static Files, Postgres and Security | Wagtail #13
```

Target search: `wagtail production` / `wagtail deploy settings`. 84 characters.

**Alternatives:**

```
Your Wagtail Dockerfile Ships DEBUG=True (Here's the Fix) | Wagtail Tutorial #13
Missing staticfiles manifest entry: Why Your Whole Wagtail Site Is a 500 | #13
```

---

## Description

```
Getting the studio site ready for production, and five things the generated project
gets wrong, every one measured with DEBUG off.

The Dockerfile that wagtail start creates runs the DEVELOPMENT settings: DEBUG on, any
host, and the secret key committed to git. Forget collectstatic and every page, even
the admin login, is a 500. Point DATABASE_URL at Postgres and it fails before
connecting. And uploaded images stop working entirely.

WHAT YOU'LL LEARN
• What the generated production.py does and doesn't do (it has no SECRET_KEY)
• Why the generated Dockerfile runs dev settings, and failing closed
• Secrets and hosts from environment variables
• DATABASE_URL with dj-database-url, and SQLite as the local default
• The postgres.E005 error, and a 10-second connect timeout
• "Missing staticfiles manifest entry" — the 500 on every page
• WhiteNoise, hashed filenames and ten-year caching
• Why media stops working with DEBUG off
• HTTPS behind a proxy, secure cookies and a deliberately short HSTS
• check --deploy: from 6 issues to 2
• The requirements file the Dockerfile really installs

Said plainly: there is no Postgres server on the recording machine, so a live Postgres
connection isn't shown here. It happens against the real host in episode 14.

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep13/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep13-end

Starting from the previous episode? git checkout ep12-end

CHAPTERS
0:00 What wagtail start gave us
0:21 The Dockerfile runs dev settings
0:45 Fail closed
1:17 Everything from the environment
1:41 One variable for the database
2:01 Postgres fails before connecting
2:29 No collectstatic: every page 500
2:47 collectstatic
3:11 The 404 page, finally
3:23 WhiteNoise and hashed filenames
3:51 Media is not static
4:15 HTTPS behind a proxy
4:48 check --deploy
5:01 The requirements the Dockerfile installs
5:25 What isn't verified yet
5:46 Commit and tag
5:49 Next: deploy it

NEXT → Ep 14: Deploy It — a real host, a real database, media that works, and the first live edit.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#wagtail #django #python #cms #webdev
```

---

## Tags

```
wagtail production, wagtail production settings, wagtail deploy, django production settings, django debug false, missing staticfiles manifest entry, wagtail whitenoise, django collectstatic, dj-database-url, wagtail postgres, postgres.E005, django check --deploy, wagtail dockerfile, django secret key environment variable, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep13/assets/thumb.png`

Best hook: the red `DEBUG  True` / `'django-insecure-'` terminal. Overlay: **YOUR DOCKERFILE SHIPS DEBUG=TRUE**.

---

## Pinned comment

```
The five from this episode, all measured with DEBUG off:

1) At 0:21 — the Dockerfile wagtail start generates runs gunicorn studio.wsgi and never
sets DJANGO_SETTINGS_MODULE. wsgi.py defaults to dev: DEBUG=True, ALLOWED_HOSTS=['*'],
and the SECRET_KEY in git. Default wsgi.py to production and set it in the Dockerfile.

2) At 2:29 — "ValueError: Missing staticfiles manifest entry" on EVERY page, admin login
included. Run: python manage.py collectstatic --noinput

3) At 2:01 — DATABASE_URL pointing at Postgres fails with postgres.E005 before it
connects. Add "django.contrib.postgres" to INSTALLED_APPS when the engine is Postgres.

4) With DEBUG off, uploaded images (media) are not served by Django or WhiteNoise.
That's a hosting decision — episode 14.

5) site/requirements.txt (what the Dockerfile installs) was generated capping Django below 6.1
while the project runs 6.1.1. Pin them the same.
```

---

## Before publishing

```bash
git push origin ep13-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 14 (add once it exists; until then, the playlist)
- Link element → the repo
