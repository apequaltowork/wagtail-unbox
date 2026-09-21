# Ep 9 — Navigation & Site Settings

| | |
|---|---|
| **Video file** | `youtube/ep09/out/ep09.mp4` |
| **Subtitles** | `youtube/ep09/out/ep09.srt` |
| **Captions (upload these)** | `youtube/ep09/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep09/assets/thumb.png` |
| **Runtime** | 4:17 |
| **Git tag** | `ep09-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Ready to upload |
| **URL** | — |

---

## Title

```
Wagtail Navigation Menus and Site Settings | Wagtail Tutorial #9
```

Target search: `wagtail menu` / `wagtail site settings`. 64 characters.

**Alternatives:**

```
Build a Wagtail Menu from the Page Tree (show_in_menus) | Wagtail Tutorial #9
Wagtail BaseSiteSetting: Editable Footer and Contact Details | Wagtail Tutorial #9
```

---

## Description

```
The studio site gets a real menu and a footer the client can edit. No menu model, no
hard-coded links: the menu is built from the page tree, and the contact details come
from Wagtail's site settings.

And two reasons your first menu will be empty, or won't render at all.

WHAT YOU'LL LEARN
• Building a menu from the page tree with in_menu()
• A custom inclusion tag, and why the dev server says it doesn't exist
• Why the menu is empty: show_in_menus, and what show_in_menus_default really does
• Keeping the right item highlighted on child pages
• Measuring the menu's cost: one query
• wagtail.contrib.settings and its context processor
• BaseSiteSetting vs BaseGenericSetting
• The settings row that creates itself, and why defaults matter
• settings.app_label.ModelName in templates, mailto and tel links

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep09/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep09-end

Starting from the previous episode? git checkout ep08-end

CHAPTERS
0:00 A site you can't get around
0:22 The menu comes from the tree
0:39 An inclusion tag
0:53 Not a registered tag library
1:04 Restart runserver
1:24 The menu is empty
1:43 show_in_menus_default
1:59 Which item is active
2:18 One query
2:34 Site settings
2:44 A settings model
3:00 The row that creates itself
3:21 Using settings in templates
3:36 The menu on a post
3:43 The footer
3:57 Commit and tag
4:01 Next episode

NEXT → Ep 10: Forms That Work — a contact page that emails the studio and keeps every submission.

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
wagtail menu, wagtail navigation, wagtail site settings, wagtail basesitesetting, wagtail show_in_menus, wagtail in_menu, wagtail inclusion tag, django custom template tag, wagtail contrib settings, wagtail footer, wagtail register_setting, not a registered tag library, wagtail tutorial, wagtail cms, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep09/assets/thumb.png`

Best hook: the header with **Journal** underlined on a post page. Overlay: **MENU FROM THE TREE**.

---

## Pinned comment

```
Two reasons your first Wagtail menu won't show up:

1) At 0:53 — "'navigation_tags' is not a registered tag library", with code that's fine.
The dev server's autoreloader only watches modules it has already imported. A brand-new
templatetags module isn't one. Stop runserver and start it again.

2) At 1:24 — the menu renders nothing. Every page has show_in_menus = False by default.
Tick "Show in menus" on each page's Promote tab.

show_in_menus_default = True on a page class only affects NEW pages of that type —
existing pages keep what they have.

Settings in templates: settings.home.StudioSettings.email
(app label, then model name, then field).
```

---

## Before publishing

```bash
git push origin ep09-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 10
- Link element → the repo
