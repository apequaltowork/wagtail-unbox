# Wagtail Unboxed — the whole plan

Everything about how this series is built: what it is, what's decided, how the machinery
works, what's done, and what's next.

**Repo:** https://github.com/apequaltowork/wagtail-unbox
**Channel:** https://www.youtube.com/@apequaltowork

---

## 1. What this is

**Wagtail Unboxed: Learning by Building** — a 16-episode YouTube series.

The format is *unbox-then-build*. After two short intro episodes, we open a fresh
`wagtail start` project and tour **every one of the 29 files** it generates, then build a
single real site — a small design-studio site — growing it episode by episode until it
deploys.

The core bet: most Wagtail tutorials tell you to ignore the generated files, and that's
exactly why people stay confused. We read them. The goal is that a viewer can *modify* the
code, not just copy it.

---

## 2. Decisions already made

| Decision | Value | Why |
|---|---|---|
| **Spine** | Unbox, then build one cumulative site | Payoff builds; each episode has a reason to exist |
| **The site** | Small business / design studio | Hits every core Wagtail feature naturally; it's what people build for clients |
| **Wagtail** | 7.4.3 (pinned) | 8.0 exists; 7.4 has wider package compatibility and ages slower |
| **Django** | 6.1.1 (pinned) | Wagtail 7.4 declares only a minimum of 5.2 with no upper limit, so unpinned installs drift |
| **Python** | 3.12.10 | What's on the recording machine |
| **Episode length** | 15–25 min, one concept each | Best retention for tutorial content |
| **Database** | SQLite through ep 12, Postgres at ep 13 | Nothing to install = nobody quits at setup |
| **Front-end** | Plain CSS, by hand. No Node, React or Tailwind | Keeps episodes about Wagtail, not a toolchain |
| **Narration** | `en-US-SteffanNeural` via edge-tts | Chosen from a 15-voice audition |
| **Recording OS** | Windows 10 Pro | macOS/Linux equivalents ship in every `commands.md` |
| **Project package** | `studio` | **Never** name it `site` — shadows Python's stdlib `site` module |

### Prerequisites stated to viewers

Required: basic Python, **basic Django** (the real one), enough HTML/CSS to edit a
template, basic command line. Not required: any prior Wagtail or CMS experience, front-end
frameworks, Docker.

Saying the Django requirement plainly in ep 0a costs a few viewers and saves the comment
section. Full text in [docs/prerequisites.md](docs/prerequisites.md).

---

## 3. The episode arc

### Act 0 — Before we open the box
| # | Title | Status |
|---|---|---|
| 0a | What This Series Is (and Who It's For) | ✅ **Published** |
| 0b | Setting Up Your Machine | Script + metadata written |

### Act 1 — Unboxing
| # | Title | Tag | Status |
|---|---|---|---|
| 01 | What Wagtail Actually Is | `ep01-end` | Code built, script written |
| 02 | Opening the Box: Every File Explained | `ep02-end` | Code built, script written |
| 03 | The Page Model & the Tree | `ep03-end` | Not started |

### Act 2 — Building the studio site
| # | Title | Covers |
|---|---|---|
| 04 | Templates & Static Files | Template resolution, `{% image %}`, base template, CSS |
| 05 | StreamField, Properly | Block types, `StructBlock`, `ListBlock`, block templates |
| 06 | Images & Documents | Renditions, focal points, `ImageChooserBlock` |
| 07 | Blog: Parent & Child Pages | `BlogIndexPage`, `subpage_types`, pagination |
| 08 | Snippets & Reusable Content | `register_snippet`, `SnippetChooserBlock` |
| 09 | Navigation & Site Settings | Menus from the tree, `BaseSiteSetting` |
| 10 | Forms That Work | `AbstractEmailForm`, contact page, submissions |
| 11 | Search | `search_fields`, indexing, the `search/` app finally doing something |

### Act 3 — Shipping
| # | Title | Covers |
|---|---|---|
| 12 | Editor Experience Polish | `wagtail_hooks.py`, panels, help text, previews |
| 13 | Production Settings | Postgres, env vars, static/media, security checklist |
| 14 | Deploy It | Target TBD (Fly.io / Railway / VPS), domain, media storage |

Titles after the last published episode may still shift. If ep 5 needs to split, it splits.

---

## 4. Repo layout

```
site/            the Wagtail project (Django package: studio)
docs/            prerequisites, reference notes
youtube/         ONE FOLDER PER EPISODE — everything for that episode
  README.md      upload checklist + settings shared by every episode
  channel.md     channel-level details, standard footer, tag base
  playlist.md    playlist title + description
  ep00a/
    README.md    title, description, tags, chapters, pinned comment
    script.md    beats, talking points, on-screen actions, timings
    commands.md  every command in order, Windows + macOS/Linux
    notes.md     gotchas found while rehearsing
    scenes.py    the video's scene spec (narration + slides)
    assets/      intro.png, end.png, thumb.png
    out/         rendered mp4, srt, narration.txt  (gitignored)
video/           the render engine, shared across episodes
  build.py       scene spec -> mp4
  cards.py       intro / end / thumbnail cards
  brand.py       SINGLE SOURCE OF TRUTH for all branding + URLs
  voices.py      voice audition
  theme.css      slide design system
```

**To work on an episode, only its folder name is needed** — `youtube/ep03/` holds the
script, the commands, the scene spec, the assets and the render.

### Episode checkpoints

Every code episode ends on a git tag: `ep01-end`, `ep02-end`, … A viewer runs
`git checkout ep06-end` to get exactly the code episode 7 begins with.

**Tags must be pushed before the episode publishes.** The description links to them; an
unpushed tag reads as the series being broken.

---

## 5. How the video is made

No camera, no screen recording, no editor. Each episode renders from a Python scene spec:

```
youtube/epNN/scenes.py
    -> HTML slide (video/theme.css)
    -> PNG 1920x1080 (headless Chrome)
    -> narration audio (edge-tts, en-US-SteffanNeural)
    -> per-scene MP4 segment (ffmpeg: still + audio + fades)
    -> concatenated episode MP4 + SRT + timecoded narration script
```

```bash
python video/build.py ep00a                 # full render
python video/build.py ep00a --stills-only   # check the design fast
python video/build.py ep00a --silent        # for recording your own voice
python video/cards.py --ep 03               # just that episode's cards
python video/voices.py                      # re-audition voices
```

**Scene durations are measured from the narration audio, not guessed** — so re-recording
the voice keeps the cuts aligned.

Every episode automatically opens on its intro card and closes on the end card, both driven
by `video/brand.py`. Change a URL there and every card in the series updates on re-render.

### Requirements for the render machine

ffmpeg, Chrome (or Edge), Python 3.12, `pip install -r requirements-video.txt`. edge-tts
sends narration text to Microsoft to synthesise, so it needs a network connection;
`--engine sapi` is a fully offline fallback but sounds robotic.

---

## 6. Working loop per episode

1. **Build the code** in `site/`, verified running
2. **Write `commands.md`** by replaying exactly what was typed
3. **Write `script.md`** — beats keyed to on-screen actions, timings summing to 15–25 min
4. **Write `scenes.py`** — the slides and narration
5. **Render** — `python video/build.py epNN`
6. **Write `README.md`** — title, description, tags, chapters *from the real render*
7. **Commit, tag `epNN-end`, push the tag**
8. **Upload** using the checklist in `youtube/README.md`

Never batch-write scripts for unbuilt episodes. A script has to describe code that actually
ran, or it will lie on camera.

---

## 7. Where things stand

**Done**
- Repo live, 14+ commits, tags `ep01-end` and `ep02-end` pushed
- Wagtail 7.4.3 project built and verified; admin login confirmed
- Ep 0a **published**: https://www.youtube.com/watch?v=ck4T3lnkhqs
- Scripts, commands and publishing metadata for 0a, 0b, 01, 02
- Render pipeline working end to end
- Branding: intro/end/thumbnail cards for all 16 episodes
- Playlist and channel metadata written

**Next**
1. Ep 0b scene spec and render (mostly slides — same shape as 0a)
2. Ep 1 — the real test, needs a terminal on screen. Either animate the terminal from the
   real captured output, or leave marked gaps for a screencast
3. Ep 3 onward — code first, then script

**Open questions**
- Deploy target for ep 14 — decide during ep 13
- Ep 0a's cold open is still the amber placeholder card; needs ep 14 footage, or a trim
- Whether the end card's five contact rows should drop to four

---

## 8. Things learned the hard way

Each of these cost real time and is worth not rediscovering.

- **YouTube rejects `<` and `>`** in titles and descriptions, with a generic "not valid
  input" that names no character. It bit the playlist description and two episode
  descriptions.
- **Never name a Django project `site`** — shadows Python's stdlib `site` module, and the
  resulting errors make no sense.
- **Wagtail's generated `requirements.txt` disagrees with what pip installs.** It caps
  Django below 6.1; pip resolves 6.1.1, because Wagtail's own metadata sets no upper bound.
  This is why the repo pins both.
- **`wagtail start studio site` creates the folder itself** — no `mkdir` first.
- **A Wagtail site has two pages, not one**, after `migrate`: an invisible Root above the
  homepage. And `root_page_id` is 3, not 1, because migration 0002 deletes and recreates.
- **Windows Credential Manager can cache the wrong GitHub account** and cause a 403 on
  push. SSH was the way through.
- **PowerShell variables are case-insensitive** — `$S` and `$s` are the same variable.
- **Chrome headless needs Windows-style absolute paths** for `--screenshot`.
