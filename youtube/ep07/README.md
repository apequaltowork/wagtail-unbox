# Ep 7 — Blog: Parent & Child Pages

| | |
|---|---|
| **Video file** | `youtube/ep07/out/ep07.mp4` |
| **Subtitles** | `youtube/ep07/out/ep07.srt` |
| **Captions (upload these)** | `youtube/ep07/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep07/assets/thumb.png` |
| **Runtime** | 5:25 |
| **Git tag** | `ep07-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Published |
| **URL** | https://www.youtube.com/watch?v=lvWFyLOHSBo |

---

## Title

```
Build a Blog in Wagtail: Parent and Child Pages | Wagtail Tutorial #7
```

Target search: `wagtail blog tutorial`. Front-loaded, 69 characters.

**Alternatives:**

```
Wagtail subpage_types and parent_page_types Explained | Wagtail Tutorial #7
Wagtail Blog with Pagination: get_children vs child_of | Wagtail Tutorial #7
```

---

## Description

```
The studio site gets a journal: an index page, posts under it, newest first, three at
a time. Our first app of our own.

And two things that go wrong for nearly everyone. With no rules, Wagtail lets an editor
put a second homepage inside your About page. And the obvious query for "newest posts
first" throws a FieldError.

WHAT YOU'LL LEARN
• Adding a second app, and why a page app needs no admin.py or views.py
• BlogIndexPage and BlogPage — and why date is its own field
• What happens with no page-type rules at all (it's worse than you think)
• parent_page_types, subpage_types, max_count and max_count_per_parent
• Why get_children() returns Page, not BlogPage — and the FieldError it causes
• BlogPage.objects.child_of(self): querying the model you actually mean
• get_context: handing extra data to a page's template
• Pagination, and why get_page() beats page()

Every rule and query in the video was checked against the running site.

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep07/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep07-end

Starting from the previous episode? git checkout ep06-end

CHAPTERS
0:00 A studio that never says anything
0:20 A second app
0:38 Why a separate app
0:59 Two models
1:23 With no rules, anything goes anywhere
1:45 Two lists fix it
2:03 Checked, and no migration needed
2:25 The query everybody writes first
2:39 FieldError, and Page objects
2:52 Why get_children() lies to you
3:16 get_context
3:36 page() vs get_page()
3:54 The index template
4:09 The counter that jumped sideways
4:26 The journal
4:34 Page 3, and page 999
4:49 A post
5:00 Commit and tag
5:03 Next episode

NEXT → Ep 8: Snippets & Reusable Content — team members, testimonials, and tags.

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
wagtail blog, wagtail blog tutorial, wagtail subpage_types, wagtail parent_page_types, wagtail get_children, wagtail child_of, wagtail pagination, wagtail get_context, wagtail max_count, wagtail page types, django pagination, wagtail index page, wagtail tutorial, wagtail cms, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep07/assets/thumb.png`

Best hook: the "anything goes anywhere" listing with **'HomePage'** highlighted red under
StandardPage. Overlay: **A HOMEPAGE INSIDE ABOUT?** It's the surprise nobody expects.

---

## Pinned comment

```
The two from this episode that catch nearly everyone:

1) At 1:23 — with no page-type rules, Wagtail lets an editor create a second homepage
INSIDE your About page, or a bare Page with no template. Every page type needs:

    parent_page_types = [...]
    subpage_types = [...]

No migration needed — they're Python only.

2) At 2:39 — this looks right and isn't:

    self.get_children().live().order_by("-date")
    # FieldError: Cannot resolve keyword 'date' into field.

get_children() queries the shared Page table, so you get Page objects in tree order,
and Page has no date. Query the model you mean:

    BlogPage.objects.child_of(self).live().order_by("-date")

And for pagination, use paginator.get_page(), not paginator.page() — the page number
comes from the URL, so ?page=abc must not crash your site.
```

---

## Before publishing

```bash
git push origin ep07-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 8
- Link element → the repo
