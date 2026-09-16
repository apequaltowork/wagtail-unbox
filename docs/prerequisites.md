# Prerequisites — Wagtail Unboxed

Every video description links here, so this is the one place these are maintained.

## Required skills

**You need these.** The series teaches *Wagtail*, not Python and not Django.

| Skill | How much |
|---|---|
| **Python** | Functions, classes, imports, `pip`. You should be comfortable *reading* a class definition. You do not need to be advanced. |
| **Django** | **The real prerequisite.** Models, migrations, views, templates, `settings.py`, basic ORM queries. Wagtail *is* Django — if `models.py` and `makemigrations` are unfamiliar, episode 3 will hurt. |
| **HTML / CSS** | Enough to open a template and change markup. No frameworks needed. |
| **Command line** | `cd`, listing files, running a command, reading an error. |

**Nice to have, not required:** git basics (the episode tags are explained as we go), a little JavaScript (never required).

**Explicitly NOT required:** any prior Wagtail, any prior CMS experience, React/Vue/Tailwind, Docker, Kubernetes.

### If you don't know Django yet

Do the [official Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) first — it's about a weekend. Then come back. You'll get far more out of this series, and you won't spend it copying code you can't modify.

## System requirements

| | |
|---|---|
| **OS** | Windows 10/11, macOS, or Linux. Recording is on **Windows 10 Pro**, so Windows/PowerShell commands are what's on screen. macOS/Linux equivalents are in every episode's `commands.md`. |
| **Python** | **3.12** (we record on 3.12.10). Wagtail 7.4 also runs on 3.10–3.13. |
| **Editor** | Any. VS Code + the Python extension is what's shown. |
| **git** | 2.x — needed to check out the episode tags. |
| **Terminal** | PowerShell on Windows; bash/zsh on macOS/Linux. |
| **Disk / RAM** | ~2 GB free, 8 GB RAM. |
| **Database** | **SQLite** for episodes 1–12. It ships with Python — nothing to install. |
| **Postgres** | **Not needed until episode 13.** Installing it is part of that episode. Don't install it now. |
| **Node.js** | **Not required at any point.** This series deliberately avoids a front-end build toolchain so the episodes stay about Wagtail. |

## Pinned versions

The series is pinned so it stays reproducible:

```
wagtail==7.4.3
Django==6.1.1
```

Wagtail 7.4 declares only `Django>=5.2` with no upper bound, so an unpinned install will quietly give you a different Django than the one on screen. Note that the `requirements.txt` that `wagtail start` generates says `Django>=6,<6.1`, which does **not** match what `pip install wagtail` actually resolves — we cover that in episode 2.

Wagtail 8.0 is out. We're on 7.4 on purpose: wider third-party package compatibility, and the series ages more slowly.
