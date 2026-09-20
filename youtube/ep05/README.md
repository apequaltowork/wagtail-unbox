# Ep 5 — StreamField, Properly

| | |
|---|---|
| **Video file** | `youtube/ep05/out/ep05.mp4` |
| **Subtitles** | `youtube/ep05/out/ep05.srt` |
| **Captions (upload these)** | `youtube/ep05/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep05/assets/thumb.png` |
| **Runtime** | 7:56 |
| **Git tag** | `ep05-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=8_wrJLU57Qw |

---

## Title

```
Wagtail StreamField Tutorial: Blocks and StructBlock | Wagtail Tutorial #5
```

Target search: `wagtail streamfield tutorial`. Front-loaded, 73 characters.

**Alternatives:**

```
Wagtail StreamField Explained: StructBlock vs ListBlock | Wagtail Tutorial #5
How to Convert a RichTextField to StreamField Without Losing Data | Wagtail #5
```

---

## Description

```
The episode everyone came for. We replace the rich-text blob with real content
blocks — and hit the migration error that stops most people on their first try.

If you have ever seen "CHECK constraint failed: JSON_VALID" and had no idea why,
that is in here, with the fix and the reason.

WHAT YOU'LL LEARN
• What StreamField actually is: a JSON column holding an ordered list of typed blocks
• The four kinds of block, and when to reach for each
• StructBlock vs ListBlock — record vs repeat, the one people mix up
• Meta: icon, label and template, and what the editor sees
• Why the migration fails on any page that already has content, and how to fix it
• Writing a data migration that runs before the column changes type
• The one-line template change, and how tiny a block template really is
• block_counts on a StreamBlock vs max_num on a ListBlock

Two gotchas, both hit while building this episode. The migration failure, and the
reason my call to action rendered as a teal box inside a teal box.

Also: stop passing use_json_field=True. Wagtail 7.4 accepts it and ignores it.

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep05/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep05-end

Starting from the previous episode? git checkout ep04-end

CHAPTERS
0:00 One field, one blob
0:20 What StreamField actually is
0:38 The four kinds of block
1:01 StructBlock vs ListBlock
1:21 Writing a StructBlock
1:40 A struct containing a list
1:57 The top-level StreamBlock
2:14 The model change
2:27 use_json_field is dead
2:48 The migration blows up
3:01 What that error actually means
3:24 Nothing is broken
3:47 The fix: convert the data first
4:07 Writing the data migration
4:33 It applies
4:42 That unreadable block_lookup
5:04 One line in the page template
5:17 Inside a block template
5:33 A teal box inside a teal box
5:47 Wagtail already wrapped your block
6:06 Style the wrapper instead
6:19 What the client sees
6:41 Two ways to say "max"
7:01 The finished home page
7:17 The migrated About page
7:31 Commit and tag
7:34 Next episode

NEXT → Ep 6: Images & Documents — renditions, focal points, and ImageChooserBlock.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#wagtail #django #python #cms #streamfield #webdev
```

---

## Tags

```
wagtail streamfield, wagtail streamfield tutorial, wagtail structblock, wagtail listblock, wagtail blocks, wagtail streamblock, richtextfield to streamfield, wagtail data migration, json_valid error, wagtail custom blocks, wagtail block template, django wagtail tutorial, wagtail cms, wagtail 7.4, use_json_field, wagtail unboxed
```

---

## Thumbnail

`youtube/ep05/assets/thumb.png`

Strongest overlay for this one: **JSON_VALID?!** over the error, with the finished
services grid behind it. The error is the hook — it is what people paste into search.

---

## Pinned comment

```
The error from 2:48, because it is what brought most of you here:

    IntegrityError: CHECK constraint failed: (JSON_VALID("body") OR "body" IS NULL)
    (on Postgres: invalid input syntax for type json)

StreamField's column is JSON. Your old rich-text content is HTML. The AlterField
alone cannot convert one to the other, so it refuses.

Nothing is broken — Django runs migrations in a transaction and rolled it back.
Check with: python manage.py showmigrations home

The fix is a RunPython placed BEFORE the AlterField, so it runs while the column is
still plain text. Full code in youtube/ep05/commands.md, step 4.

And from 5:47: Wagtail 7 already wraps every block in a div carrying the classes
w-block-NAME and block-NAME. Don't add that class yourself — style Wagtail's
wrapper instead, or you get everything twice.
```

---

## Before publishing

```bash
git push origin ep05-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 6
- Link element → the repo
