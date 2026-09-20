# Ep 4 — Templates & Static Files

| | |
|---|---|
| **Video file** | `youtube/ep04/out/ep04.mp4` |
| **Subtitles** | `youtube/ep04/out/ep04.srt` |
| **Captions (upload these)** | `youtube/ep04/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep04/assets/thumb.png` |
| **Runtime** | 5:38 |
| **Git tag** | `ep04-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=e-FeE6O9AhM |

---

## Title

```
Wagtail Templates and Static Files Explained | Wagtail Tutorial #4
```

Target search: `wagtail templates`. Front-loaded, 66 characters.

**Alternatives:**

```
How to Remove the Wagtail Welcome Page and Add Your Own Templates | #4
Wagtail Template Tags: pageurl, slugurl and richtext | Wagtail Tutorial #4
```

---

## Description

```
The teal egg finally goes. We delete Wagtail's welcome page, write a real base template,
list child pages from the page tree, and style the site with plain CSS.

Plus the ten-minute trap nobody warns you about: you write your CSS, reload, and the page
is still completely unstyled — and there's nothing wrong with your code.

WHAT YOU'LL LEARN
• Where the welcome page lives and how to delete it properly
• How Wagtail finds a template from the model name, and the two places templates can live
• A real base.html: header, main, footer — and which generated bits to keep
• pageurl, slugurl and the richtext filter
• Listing child pages with get_children.live, straight from the page tree
• Why studio.css ships at 0 bytes, and how {% static %} resolves it
• The browser-cache trap, with proof of what's actually happening

No build step, no framework, no Node. Plain CSS, hand-written — for the whole series.

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep04/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep04-end

Starting from the previous episode? git checkout ep03-end

CHAPTERS
0:00 Four episodes in, still an egg
0:16 Where the welcome page lives
0:30 How Wagtail finds a template
0:46 Two places templates live
1:06 base.html — keep the head
1:23 Header, main, footer
1:35 pageurl, slugurl, richtext
1:58 Never build links from url_path
2:14 Listing child pages from the tree
2:32 The stylesheet that ships empty
2:56 static and STATICFILES_DIRS
3:14 You write the CSS. Nothing changes.
3:30 What's actually happening
3:52 Hard-reload
4:09 The result
4:22 The About page
4:36 One media query
4:50 Why the 404 page hasn't changed
5:09 Commit and tag
5:12 Next episode

NEXT → Ep 5: StreamField, Properly — replacing the rich-text blob with real content blocks.

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
wagtail templates, wagtail static files, wagtail pageurl, wagtail slugurl, wagtail richtext, wagtail base template, django templates, wagtail tutorial, wagtail cms, remove wagtail welcome page, wagtail get_children, django static files, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep04/assets/thumb.png`

Best candidate for a before/after split: the teal welcome egg on the left, the finished
studio homepage on the right. Overlay: **DELETE THE EGG**.

---

## Pinned comment

```
The trap from 3:14 — it will get you at least once:

You write your CSS, reload the page, and nothing changes. Your code is fine.

studio.css ships at 0 BYTES in a new Wagtail project, so your browser cached an empty
file the first time you loaded the site. An ordinary reload re-uses it.

    Windows/Linux: Ctrl+F5   (or Ctrl+Shift+R)
    macOS:         Cmd+Shift+R

Proof, from the live page before hard-reloading:
    document.styleSheets[0].cssRules.length   // 0
    fetch(href, {cache:'no-store'})           // 200, 2065 bytes of CSS

Server fine, browser stale.

Also from 1:58: link with {% pageurl page %}, never page.url_path — url_path includes the
site root and gives you a 404.
```

---

## Before publishing

```bash
git push origin ep04-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 5
- Link element → the repo
