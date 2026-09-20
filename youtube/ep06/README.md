# Ep 6 — Images & Documents

| | |
|---|---|
| **Video file** | `youtube/ep06/out/ep06.mp4` |
| **Subtitles** | `youtube/ep06/out/ep06.srt` |
| **Captions (upload these)** | `youtube/ep06/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep06/assets/thumb.png` |
| **Runtime** | 7:49 |
| **Git tag** | `ep06-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=YYxtwAx4a0w |

---

## Title

```
Wagtail Images and Documents: Renditions and Focal Points | Wagtail Tutorial #6
```

Target search: `wagtail images renditions`. Front-loaded, 78 characters.

**Alternatives:**

```
Wagtail Images Explained: Renditions, Focal Points and Alt Text | Wagtail #6
Why Your Wagtail Images Break After a Server Move | Wagtail Tutorial #6
```

---

## Description

```
Six episodes into a design studio's website and there is not one picture on it.
We fix that — and hit the image bug that only shows up after you deploy.

Renditions are database rows, not files. Wipe your media folder, restore a backup
onto a new server, and Wagtail will keep serving URLs for files that are gone.
There is a one-line fix and it ships with Wagtail.

WHAT YOU'LL LEARN
• Images and documents are already installed — nothing to add
• Why media/ is gitignored, and what that means for your deploys
• The image ForeignKey, and why on_delete=SET_NULL instead of CASCADE
• What the image tag actually does: renditions, cached as rows
• Filter specs: width, height, fill, max, min, format
• srcset_image — responsive images in one tag
• Focal points, with a real before and after at the same fill spec
• The rendition bug that survives a media restore, and the command that fixes it
• ImageBlock instead of ImageChooserBlock, and why alt text is content
• Documents, and why they are served by a view rather than as static files

Also: WAGTAILIMAGES_IMAGE_MODEL is a day-one decision. We say why, and don't do it.

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep06/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep06-end

Starting from the previous episode? git checkout ep05-end

The three sample images from the video are in the repo under site/sample_images/,
because uploads themselves are not in git.

CHAPTERS
0:00 A studio site with no pictures
0:19 Nothing to install
0:43 Why media/ is gitignored
1:03 The image ForeignKey
1:15 SET_NULL, never CASCADE
1:37 What the image tag actually does
2:01 Filter specs
2:19 Responsive images in one tag
2:44 Focal points, before and after
3:07 Two things to know about them
3:28 Renditions are rows, not files
3:45 Eleven rows, eleven 404s
4:15 The fix that ships with Wagtail
4:32 The default alt text is a filing label
4:54 ImageBlock, not ImageChooserBlock
5:17 Alt text is content
5:37 Documents
5:50 Why documents go through a view
6:10 A day-one decision, named not done
6:37 The finished hero
6:49 Further down the page
7:09 The About page
7:22 Commit and tag
7:29 Next episode

NEXT → Ep 7: Blog: Parent & Child Pages — an index and its posts, subpage_types, pagination.

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
wagtail images, wagtail renditions, wagtail focal point, wagtail imagechooserblock, wagtail imageblock, wagtail alt text, wagtail documents, wagtail srcset_image, wagtail responsive images, wagtail_update_image_renditions, wagtail media files, wagtail image model, django images, wagtail tutorial, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep06/assets/thumb.png`

Best candidate: the focal-point before/after side by side, subject sliced off on the left
and centred on the right. Overlay: **FOCAL POINTS**. Second choice is the rendition audit
line — **11 rows, 11 missing files** — which is the searchable pain.

---

## Pinned comment

```
The bug from 3:28, because it will find you in production and not before:

Renditions are DATABASE ROWS that point at generated files. get_rendition() looks for a
row and returns it — it never checks whether the file is still on disk.

So after a media restore, a move to a new server, or somebody clearing disk space:

    rows: 14 | missing files: 11

and the site keeps putting all eleven URLs into img tags. Every one is a 404, and nothing
in the logs tells you why.

    python manage.py wagtail_update_image_renditions --purge-only

They regenerate on the next request. Put it in your deployment notes.

And from 4:32: with no alt attribute, Wagtail falls back to the image TITLE. Ours came out
as alt="Studio hero" — a filing label, useless to a screen reader. In a StreamField use
ImageBlock (Wagtail 6.3+), which carries alt text and a decorative flag. On a plain
ForeignKey, add your own field.
```

---

## Before publishing

```bash
git push origin ep06-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 7
- Link element → the repo
