# Ep 8 — Snippets & Reusable Content

| | |
|---|---|
| **Video file** | `youtube/ep08/out/ep08.mp4` |
| **Subtitles** | `youtube/ep08/out/ep08.srt` |
| **Captions (upload these)** | `youtube/ep08/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep08/assets/thumb.png` |
| **Runtime** | 4:37 |
| **Git tag** | `ep08-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=L9A5RAPO5uI |

---

## Title

```
Wagtail Snippets Tutorial: Reusable Content and Tags | Wagtail Tutorial #8
```

Target search: `wagtail snippets`. Front-loaded, 74 characters.

**Alternatives:**

```
Wagtail SnippetViewSet and SnippetChooserBlock Explained | Wagtail Tutorial #8
Add Tags to a Wagtail Blog (and Keep Them in Pagination) | Wagtail Tutorial #8
```

---

## Description

```
Content that isn't a page: a team member, a testimonial. No URL, no place in the tree,
but they belong on several pages. That is a snippet. Plus tags for the journal.

And the bug that tag filtering introduces: click "Older" on a filtered list and page 2
quietly shows every post, because the pagination link forgot the tag.

WHAT YOU'LL LEARN
• What a snippet is, and when content should be one instead of a page
• TeamMember with Orderable — drag-and-drop ordering for free
• SnippetViewSet and SnippetViewSetGroup: the Wagtail 7 way to register snippets
• Two ways to use a snippet: chosen per page, or fetched by the block
• get_context on a block
• The circular import between blocks.py and models.py, and the two ways around it
• What happens when you delete a snippet a page is using
• Tags with ClusterTaggableManager, and why the through model needs a ParentalKey
• Filtering by tag, and keeping the filter through pagination

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep08/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep08-end

Starting from the previous episode? git checkout ep07-end

CHAPTERS
0:00 Content that isn't a page
0:23 Two snippet models
0:39 SnippetViewSet
1:01 Two ways to use a snippet
1:24 get_context on a block
1:36 The circular import
1:57 Deleting a snippet a page uses
2:29 Tags, and why ParentalKey
2:49 Filtering by tag
3:00 Pagination forgets the filter
3:17 Carry every parameter
3:36 Fixed on the way
3:51 The team
3:59 A testimonial
4:06 The journal, filtered
4:13 Commit and tag
4:17 Next episode

NEXT → Ep 9: Navigation & Site Settings — a menu from the page tree, and editable contact details.

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
wagtail snippets, wagtail snippet tutorial, wagtail snippetviewset, wagtail snippetchooserblock, wagtail orderable, wagtail tags, wagtail clustertaggablemanager, wagtail parentalkey, wagtail blog tags, wagtail block get_context, django pagination query string, wagtail reusable content, wagtail tutorial, wagtail cms, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep08/assets/thumb.png`

Best hook: the team grid, overlay **WRITE ONCE, USE ANYWHERE**.

---

## Pinned comment

```
The bug from 3:00 — it'll hit you the first time you add any filter to a paginated list:

    ?tag=process        → Page 1 of 2
    'Older' link        → ?page=2
    following it        → Page 2 of 3   (the tag is gone)

Pagination links written as ?page=N replace the whole query string. Pass the tag back
into the template context and carry it in every link:

    ?tag=process&page=2  → Page 2 of 2

And from 1:57: if a page uses a snippet and someone deletes that snippet, the page still
loads but the block's value becomes None. Guard every chooser value in the template:
{% if t %} ... {% endif %}
```

---

## Before publishing

```bash
git push origin ep08-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 9
- Link element → the repo
