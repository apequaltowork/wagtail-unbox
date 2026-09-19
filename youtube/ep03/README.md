# Ep 3 — The Page Model & the Tree

| | |
|---|---|
| **Video file** | `youtube/ep03/out/ep03.mp4` |
| **Subtitles** | `youtube/ep03/out/ep03.srt` |
| **Thumbnail** | `youtube/ep03/assets/thumb.png` |
| **Runtime** | 5:08 |
| **Git tag** | `ep03-end` — **push it before publishing** |
| **Category** | Education |

---

## Title

```
Wagtail Page Model Explained: Custom Page Types | Wagtail Tutorial #3
```

Target search: `wagtail page model`. Front-loaded, 69 characters.

**Alternatives:**

```
How to Create a Custom Page Type in Wagtail | Wagtail Tutorial #3
Wagtail Page Tree Explained: How Pages Are Stored | Wagtail Tutorial #3
```

---

## Description

```
We finally change code: two fields on the homepage, a second page type, and the one
migration line that explains how every Wagtail page is stored.

Last episode predicted that a page one level under Home would get the tree path
"000100010001". This episode we build that page and check it in the database.

WHAT YOU'LL LEARN
• Adding fields to a Wagtail page — and why they don't appear in the admin without content_panels
• Creating a second page type (StandardPage) and why it needs its own template
• Multi-table inheritance: every page lives in TWO tables, joined by page_ptr
• Reading the page tree from the shell — and the prediction checking out
• Why url_path says /home/about/ but the page is served at /about/
• The .specific gotcha: why Page.objects hands you a page with your fields missing

📋 Every command, with real output and a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep03/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep03-end

Starting from the previous episode? git checkout ep02-end

CHAPTERS
0:00 Last episode's prediction
0:19 Where we left HomePage
0:38 Adding intro and body fields
0:56 A field is not a form field: content_panels
1:17 A second page type: StandardPage
1:31 Every page type needs a template
1:54 makemigrations and migrate
2:02 The page_ptr line
2:15 Every page lives in two tables
2:45 Editing the homepage in the admin
2:56 Adding a child page
3:08 Printing the tree
3:14 The prediction checks out
3:31 url_path is not the URL
3:59 Why is my field missing? .specific
4:20 What's still wrong
4:38 Commit and tag
4:46 Next episode

NEXT → Ep 4: Templates & Static Files — replacing the welcome page with real templates.

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
wagtail page model, wagtail tutorial, wagtail custom page type, wagtail page tree, wagtail content_panels, wagtail richtextfield, django multi-table inheritance, wagtail specific, wagtail cms, django cms, wagtail for beginners, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep03/assets/thumb.png`

The tree from the payoff slide — `0001` / `00010001` / `000100010001`, with the last `0001`
in amber. Overlay: **THE PAGE TREE**, small *Wagtail Unboxed 3*.

---

## Pinned comment

```
The one that trips everyone up, from 3:59:

    p = Page.objects.get(slug="about")
    p.intro              # AttributeError -- p is a plain Page
    p.specific.intro     # works -- p.specific is your StandardPage

Every page lives in two tables. Page.objects only reads the shared one (title, slug,
path...). .specific fetches the second table with your own fields.

You'll need this again in the menu episode and the search episode -- anything that
queries through Page.objects returns base Pages.

And from 3:31: in templates, link with page.url, never page.url_path. url_path includes
the site root, so it gives you /home/about/, which is a 404.
```

---

## Before publishing

```bash
git push origin ep03-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 4
- Link element → the repo
