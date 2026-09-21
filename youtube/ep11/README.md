# Ep 11 — Search

| | |
|---|---|
| **Video file** | `youtube/ep11/out/ep11.mp4` |
| **Subtitles** | `youtube/ep11/out/ep11.srt` |
| **Captions (upload these)** | `youtube/ep11/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep11/assets/thumb.png` |
| **Runtime** | 3:50 |
| **Git tag** | `ep11-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Ready to upload |
| **URL** | — |

---

## Title

```
Wagtail Search Tutorial: search_fields, update_index and Private Pages | Wagtail #11
```

Target search: `wagtail search`. 83 characters.

**Alternatives:**

```
Wagtail Search Not Finding Your Content? Here's Why | Wagtail Tutorial #11
Wagtail Search Tutorial: Index Pages and Search | Wagtail Tutorial #11
```

---

## Description

```
The search app we unboxed in episode 2 finally does something. It works out of the box,
and this episode finds four ways it doesn't work well, every one measured.

Only titles are searched. Adding fields changes nothing until you rebuild the index.
Text that comes from snippets is visible on the page but can't be found. And the view
Wagtail generates shows the titles of password-protected pages to anyone.

WHAT YOU'LL LEARN
• What Wagtail indexes by default: the title, and nothing else you wrote
• search_fields: SearchField and FilterField
• Why adding search_fields changes nothing, and update_index
• get_searchable_content: indexing text that lives in snippets
• The private-page leak in the generated view, and .public()
• .specific() so results can show their intro
• A search results template with a count, page types and pagination
• Putting search in the menu

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep11/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep11-end

Starting from the previous episode? git checkout ep10-end

CHAPTERS
0:00 The app we unboxed in episode 2
0:21 Only titles are searched
0:33 search_fields
0:50 Still nothing
0:56 update_index
1:16 Visible, but not searchable
1:39 get_searchable_content
2:07 Password-protect a page, then search
2:20 The generated view leaks private pages
2:43 The view, rewritten
2:57 The results template
3:11 Search in the menu
3:20 A name from a snippet
3:27 Commit and tag
3:30 Next: Act 3

NEXT → Ep 12: Editor Experience Polish — making the admin pleasant for the client.

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
wagtail search, wagtail search tutorial, wagtail search_fields, wagtail update_index, wagtail searchfield, wagtail get_searchable_content, wagtail search not working, wagtail private pages search, wagtail public, wagtail database search backend, wagtail search view, wagtail streamfield search, wagtail tutorial, wagtail cms, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep11/assets/thumb.png`

Best hook: `search('fixed price')` with a red **0 results**. Overlay: **WHY SEARCH FINDS NOTHING**.

---

## Pinned comment

```
The four from this episode:

1) Only the title is indexed by default. Name every other field:
    search_fields = Page.search_fields + [index.SearchField("intro"), index.SearchField("body")]

2) Adding search_fields doesn't reindex existing pages:
    python manage.py update_index

3) Text from snippets (a team list, a chosen testimonial) is on the page but not in the
index. Override get_searchable_content on the block — and re-save the page when the
snippet changes.

4) At 2:07 — the search view that wagtail start generates uses .live(), which means
published, not visible. Titles of password-protected pages appear in results.
Use Page.objects.live().public().specific().search(q)
```

---

## Before publishing

```bash
git push origin ep11-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 12
- Link element → the repo
