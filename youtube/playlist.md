# YouTube playlist metadata

Paste-ready. Links and handles are filled in from `video/brand.py`.

---

## Title

**Recommended:**

```
Wagtail Unboxed: Learning by Building (Wagtail 7 + Django Tutorial)
```

Why this one: the brand name comes first so the series is recognisable once people are
following it, and the parenthetical carries the words people actually type into search —
*wagtail*, *django*, *tutorial*. A playlist title is indexed, so a pure brand name like
"Wagtail Unboxed" alone would be found by nobody who doesn't already know it.

Keep it under ~60 characters of *visible* weight where you can; YouTube truncates playlist
titles in some surfaces around there. The version above runs long by design — the tail is the
disposable part, so if it gets cut, nothing important is lost.

**Alternatives:**

```
Wagtail Unboxed — Build a Real Wagtail CMS Site from Scratch
Wagtail CMS Tutorial for Django Developers | Wagtail Unboxed
Learn Wagtail by Building: A Complete Wagtail 7 Series
```

The second is the strongest if search discovery matters more to you than branding — it leads
with the exact phrase a Django developer would search — but it buries the series name.

---

## Description

First two lines are what shows before "show more", so the hook and the prerequisite warning
go at the top.

```
Build a real Wagtail site from an empty folder — and understand every file in it.

We open a brand new Wagtail project, read all 29 files it generates, then build a working
client site: pages, StreamField, images, a blog, snippets, navigation, a contact form,
search, and a live deployment.

⚠️ YOU NEED BASIC DJANGO
Models, migrations, templates, settings.py. Not deeply — but Wagtail IS Django, so this
series teaches Wagtail, not Django. New to Django? Do the official Django tutorial first
(about a weekend), then come back.
Full prerequisites: https://github.com/apequaltowork/wagtail-unbox/blob/main/docs/prerequisites.md

WHAT MAKES THIS DIFFERENT
Most tutorials tell you to ignore the files Wagtail generates. We read them — including the
data migration that quietly creates your homepage, and what "00010001" in your database
actually means. The goal is that you can modify this code, not just copy it.

📦 CODE — every episode ends on a git tag, so you can start anywhere:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep06-end    (exactly the code episode 7 begins with)

🔧 PINNED VERSIONS — the code on screen is the code you get:
Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows; macOS and Linux commands are in the repo for every episode.

THE SERIES
Act 1 — Unboxing (ep 1-3): install, create, and read every generated file
Act 2 — Building (ep 4-11): templates, StreamField, images, blog, snippets,
        navigation, forms, search
Act 3 — Shipping (ep 12-14): editor polish, production settings, deploy

NOT COVERED, on purpose: no React, no Tailwind, no Node, no Docker deep-dive. Plain CSS
written by hand, so the episodes stay about Wagtail.

New episodes every Tuesday.
Questions? Comment on any episode — I read them.

#wagtail #django #python #cms #webdevelopment
```

---

## Notes on setup

- **Playlist ordering:** set to **manual**, not "date added" or "date published". You'll
  re-upload or re-order episodes at some point, and a series playlist that shuffles itself is
  the fastest way to lose a viewer mid-series.
- **Visibility:** make it public before episode 0a goes up, so the first video already has a
  playlist to sit in.
- **Add every video to the playlist at upload time**, not later — playlist membership feeds
  YouTube's "next video" suggestions, which is most of how a series gets watched through.
- **Playlist thumbnail** comes from the first video, so ep 0a's thumbnail is doing double duty.
- Set the series as a **"show"/season** in YouTube Studio if the option is available on the
  account — it enables episode numbering in the UI.
- Description limit is 5000 characters; the above is well within it.
- **YouTube rejects `<` and `>` in titles and descriptions** with a generic "not valid input"
  error and does not say which character is at fault. Keep angle brackets out of anything
  pasted into Studio -- that includes placeholder markers like `<your name here>`.
- If links are rejected rather than the text, the account likely needs phone verification
  before it can put external URLs in descriptions.
