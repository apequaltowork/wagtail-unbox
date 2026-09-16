# Wagtail Unboxed: Learning by Building

Companion repo for the YouTube series **[Wagtail Unboxed](https://www.youtube.com/@apequaltowork)**.

We open a fresh `wagtail start` project, tour **every** file it generates, and then build one
real site — a small design-studio site with pages, StreamField, a blog, snippets, navigation,
a contact form, search, and a deploy — one episode at a time.

**Pinned:** Wagtail 7.4.3 · Django 6.1.1 · Python 3.12

Read [docs/prerequisites.md](docs/prerequisites.md) before episode 1.

## Jump in at any episode

Every episode ends on a tagged commit. To start from where an episode began, check out the
*previous* episode's tag:

```bash
git clone https://github.com/apequaltowork/wagtail-unbox.git
cd wagtail-unbox
git checkout ep03-end      # the state at the END of episode 3
```

Then set up and run:

```bash
py -m venv .venv                      # Windows
.venv\Scripts\activate
pip install -r requirements.txt
cd site
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

macOS/Linux: `python3 -m venv .venv` and `source .venv/bin/activate`.

Site: http://127.0.0.1:8000 · Admin: http://127.0.0.1:8000/admin/

`db.sqlite3` and `media/` are **not** committed — you create your own content as you follow along.

## Episodes

| # | Title | Tag |
|---|---|---|
| 0a | [What This Series Is (and Who It's For)](https://www.youtube.com/watch?v=ck4T3lnkhqs) | — |
| 0b | Setting Up Your Machine | — |
| 01 | What Wagtail Actually Is | `ep01-end` |
| 02 | Opening the Box: Every File Explained | `ep02-end` |
| 03 | The Page Model & the Tree | `ep03-end` |
| 04 | Templates & Static Files | `ep04-end` |
| 05 | StreamField, Properly | `ep05-end` |
| 06 | Images & Documents | `ep06-end` |
| 07 | Blog: Parent & Child Pages | `ep07-end` |
| 08 | Snippets & Reusable Content | `ep08-end` |
| 09 | Navigation & Site Settings | `ep09-end` |
| 10 | Forms That Work | `ep10-end` |
| 11 | Search | `ep11-end` |
| 12 | Editor Experience Polish | `ep12-end` |
| 13 | Production Settings | `ep13-end` |
| 14 | Deploy It | `ep14-end` |

Titles after the last released episode may still shift.

## Repo layout

```
site/          the Wagtail project (Django package: studio)
docs/          prerequisites and reference notes
youtube/       one folder per episode: script, commands, scene spec,
               assets, render output, and publishing details
video/         the shared render engine and branding
```

Each `youtube/epNN/` holds everything for that episode:

- `README.md` — title, description, tags, chapters, pinned comment
- `script.md` — beats, talking points, on-screen actions, timings
- `commands.md` — every command in order, Windows + macOS/Linux
- `notes.md` — gotchas found while rehearsing
- `scenes.py` — the video's scene spec (slides + narration)
- `assets/` — intro poster, end card, thumbnail
- `out/` — rendered MP4, subtitles, narration script (not committed)

**The full plan for the series is in [PLAN.md](PLAN.md).**
