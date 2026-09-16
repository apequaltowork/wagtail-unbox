# Ep 0b — Setting Up Your Machine

| | |
|---|---|
| **Video file** | `youtube/ep00b/out/ep00b.mp4` |
| **Subtitles** | `youtube/ep00b/out/ep00b.srt` |
| **Thumbnail** | `youtube/ep00b/assets/thumb.png` |
| **Runtime** | 4:48 |
| **Git tag** | — (no code in this episode) |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=7AtlyySq4l4 |

## Title

```
Wagtail Setup: Install Python, Git and Virtualenv | Wagtail Tutorial #0b
```

Target search: `wagtail setup / python virtualenv`. Front-loaded, 72 characters.

Previous (brand-first) version, kept for reference:
`Wagtail Unboxed #0b: Set Up Your Machine (Python, git, virtualenvs)`

**Alternatives:**

```
Python Setup Done Right — Before We Touch Wagtail | Wagtail Unboxed #0b
Python, git and virtualenvs: the setup that stops breaking later
```

---

## Description

```
Setup episode. Short, skippable, and it shows the failure modes — not just the happy path.

Already have Python 3.12, git, and a virtualenv habit? Skip straight to Episode 1.

We install Python 3.12, git and an editor on Windows, macOS and Linux, then spend real time
on virtual environments — what they actually are, why they matter, and the mistake that
breaks people three episodes later: forgetting to activate in a new terminal.

WHAT WE ARE NOT INSTALLING
✗ Postgres — episodes 1 to 12 use SQLite, which ships inside Python. Postgres arrives in ep 13.
✗ Node.js — there is no front-end build step in this series, at any point.

📋 Every command for all three platforms, plus a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep00b/commands.md

CHAPTERS
0:00 Already set up? Skip this one
0:18 Four things, that's it
0:30 What we are NOT installing
0:53 Python 3.12 — Windows, macOS, Linux
1:15 The "Add to PATH" mistake
1:34 Check it worked
1:53 An editor
2:11 git
2:30 What a virtualenv actually is
2:54 Making one
3:05 The (.venv) prefix
3:16 The trap: new terminal, activate again
3:37 Windows: "running scripts is disabled"
3:55 Verify your starting line
4:07 No Wagtail yet — on purpose
4:28 Next episode

NEXT → Ep 1: What Wagtail Actually Is — first install, first project, first admin login.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#python #django #wagtail #virtualenv #webdevelopment
```

---

## Tags

```
python setup, python 3.12 install, virtualenv, python venv tutorial, install python windows, git install, vs code python, wagtail, wagtail tutorial, django, python for beginners, development environment setup, powershell execution policy, python path windows
```

---

## Thumbnail

`youtube/ep00b/assets/thumb.png`

A dark terminal showing the `(.venv)` prompt prefix, circled in teal.
Overlay: **SET UP ONCE** with a small *Wagtail Unboxed 0b*.

---

## Pinned comment

```
Stuck? Reply with your OS and the exact error text and I'll help.

The three that catch almost everyone:

1. Windows: "'py' is not recognized" → you missed the "Add python.exe to PATH" tick box.
   Re-run the installer, choose Modify, tick it.
2. Windows: "running scripts is disabled" →
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
3. Ubuntu/Debian: "No module named venv" → sudo apt install python3.12-venv

Full troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep00b/commands.md
```

---

## End screen

- Subscribe element
- "Next video" → Ep 1
- Link element → the repo
