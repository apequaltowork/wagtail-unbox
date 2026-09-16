# Ep 1 — What Wagtail Actually Is

| | |
|---|---|
| **Video file** | `youtube/ep01/out/ep01.mp4` |
| **Subtitles** | `youtube/ep01/out/ep01.srt` |
| **Thumbnail** | `youtube/ep01/assets/thumb.png` |
| **Runtime** | 5:19 |
| **Git tag** | `ep01-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=X7FgE9j1XLY |

## Title

```
How to Install Wagtail and Create Your First Project | Wagtail Tutorial #1
```

Target search: `how to install wagtail`. Front-loaded, 74 characters.

Previous (brand-first) version, kept for reference:
`Wagtail Unboxed #1: What Wagtail Actually Is (First Project, Start to Admin)`

**Alternatives:**

```
Your First Wagtail Project — Explained Properly | Wagtail Unboxed #1
Wagtail CMS Tutorial #1: Install, Create, Run
```

---

## Description

```
We install Wagtail, create a project, and get a real CMS admin running — then stop, because
episode 2 opens up every single file it generated.

First, the question nobody answers clearly: what IS Wagtail? It's not an alternative to
Django — it runs on Django. We compare it to plain Django, to the Django admin, and to
WordPress, and say where each one actually wins.

Also covered: why you should never name a Django project "site" (Python already has a module
with that name), and why we pin BOTH Wagtail and Django — Wagtail 7.4 declares a minimum of
Django 5.2 with no upper limit, so an unpinned install won't match what's on screen.

No database to install. SQLite ships inside Python. Postgres arrives in episode 13.

📋 Every command, Windows + macOS + Linux, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep01/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep01-end

CHAPTERS
0:00 What you'll have by the end
0:20 Wagtail vs Django vs WordPress
0:40 But Django already has an admin?
1:02 The one-sentence version
1:14 A folder and a virtualenv
1:35 Installing Wagtail
1:53 Why pin Django too?
2:14 Creating the project
2:20 Those two arguments
2:41 Never name your project "site"
3:04 migrate — 184 migrations before you write any code
3:21 No database server
3:40 createsuperuser
3:52 Running it
3:59 The two addresses
4:15 One page already exists
4:36 git and the episode tag
4:50 Next episode

NEXT → Ep 2: Opening the Box — every generated file explained, including the migration that
quietly created your homepage.

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
wagtail tutorial, wagtail cms, wagtail start, install wagtail, django cms, wagtail 7.4, python cms, django tutorial, wagtail for beginners, wagtail admin, wordpress alternative python, build cms with django, wagtail project setup, wagtail unboxed
```

---

## Thumbnail

`youtube/ep01/assets/thumb.png`

The Wagtail welcome egg on the left, the admin dashboard on the right, an arrow between.
Overlay: **INSTALL → RUNNING CMS**, small *Wagtail Unboxed 1*.

---

## Pinned comment

```
Two things from this episode worth repeating:

1. Don't name your Django project "site" — Python has a built-in module called `site` and
   shadowing it produces import errors that make no sense. Same for "test", "json", "email".

2. Pin Django, not just Wagtail. Wagtail 7.4 declares a minimum of Django 5.2 with no upper
   limit, so `pip install wagtail` alone gives you whatever Django shipped most recently.
   We use:
       wagtail==7.4.3
       Django==6.1.1

Commands for all three platforms:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep01/commands.md

Stuck? Reply with your OS and the exact error.
```

---

## Before publishing

```bash
git push origin ep01-end
```

The description links to this tag. If it isn't pushed, the link fails and it reads as the
series being broken.

---

## End screen

- Subscribe element
- "Next video" → Ep 2
- Link element → the repo
