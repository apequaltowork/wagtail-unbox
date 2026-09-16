# Ep 1 — Rehearsal notes & gotchas

## Verified on this machine
- Windows 10 Pro, Python 3.12.10, git 2.50.0
- `pip install "wagtail==7.4.3" "Django==6.1.1"` → clean
- `wagtail start studio site` → **creates the `site` folder itself**. No `mkdir` first. (Checked: mkdir-ing first also works, so don't worry if a viewer does.)
- `manage.py migrate` → clean, creates `site/db.sqlite3`
- `manage.py check` → "System check identified no issues (0 silenced)."
- Whole command list replayed from scratch in a temp dir → **identical file tree**.

## Gotchas to hit deliberately on camera

### The Django version mismatch (also ep 2 material)
`pip install wagtail` pulls **Django 6.1.1**, because Wagtail 7.4.3 declares `Django>=5.2`
with no upper bound. But the `requirements.txt` that `wagtail start` *generates* says:
```
Django>=6,<6.1
wagtail>=7.4,<7.5
```
Those disagree. The generated file would give you 6.0.x; pip gave us 6.1.1. Nothing breaks,
but it's exactly the kind of thing that makes a viewer's screen differ from mine. This is why
the repo root pins exact versions. **Mention in ep 1, dig into it in ep 2.**

### Naming the project `site`
Shadows Python's stdlib `site` module. Worth 20 seconds on camera — it's a real beginner
trap and the error messages are useless.

### Port already in use
Very likely if the viewer has another Django project running:
`python manage.py runserver 8001`

### `createsuperuser` password invisibility
People genuinely think their keyboard stopped working. Say it out loud.

## Counted, not estimated

`manage.py migrate` on a fresh database applies **184** migrations, not the "~70" an
earlier draft of the script claimed. Verified by counting the `Applying` lines on a
clean run. The on-screen output is trimmed to fit the frame, but the number is real.

## Recording notes
- Let the `pip install` output scroll. Don't cut it — naming treebeard and Pillow as they go
  past is a cheap, memorable explanation of how the page tree and images work.
- The admin tour must stay under 90 seconds. Every instinct will say to keep clicking. Don't —
  eps 2 and 3 need the material.
- Clear the terminal before `wagtail start` so the generated tree is readable on screen.

## Open
- Decide whether to show `py -m pip install --upgrade pip` on camera or cut it. Leaning cut —
  it adds nothing and the output is noisy.
