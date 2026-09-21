# Ep 7 — Blog: Parent & Child Pages

Start from `git checkout ep06-end`.

Everything quoted here was run on the recording machine — see `notes.md`.

## Beats

### Cold open — a studio that never says anything
The site has a homepage and an About page. A studio that wants clients needs a journal:
an index, posts under it, newest first, a few at a time.

### A second app
`python manage.py startapp blog`. Delete `admin.py` and `views.py` — a Wagtail page app uses
neither. Add `"blog"` to `INSTALLED_APPS`.

Why a separate app: the blog has its own templates and rules, and will grow tags. `home`
stays the site shell. The blog still **imports** `HeroMixin` and `BodyBlock` from `home` —
one hero, one set of blocks, everywhere.

### Two models, one relationship
- `BlogIndexPage` — the `/journal/` page. Just an intro.
- `BlogPage` — one post: `date`, `intro`, a hero, a StreamField body.

`date` is its own field, not `first_published_at` — editors backdate posts, and a republish
must not reorder the blog.

### ⭐ With no rules, anything goes anywhere
Print what each page type allows before adding any rules:

```
HomePage      children: ['BlogIndexPage', 'HomePage', 'Page', 'StandardPage']
StandardPage  children: ['HomePage', 'Page', 'StandardPage']
```

A second homepage inside About. A bare `Page` with no template. Wagtail defaults to
anything, anywhere.

### Two lists fix it
```python
parent_page_types = ["blog.BlogIndexPage"]
subpage_types = []
```
Every page type says where it may live and what may live under it. Plus `max_count = 1` on
the homepage and `max_count_per_parent = 1` on the journal.

Checked with `can_create_at()`: BlogPage under About → False. Second homepage → False.

Python-only: `makemigrations` says **No changes detected**.

### ⭐ get_children() lies to you
The obvious query:
```python
self.get_children().live().order_by("-date")
# FieldError: Cannot resolve keyword 'date'
```
`get_children()` queries the **Page** table. It returns `Page` objects, in tree order, and
`Page` has no `date`. Query the model you mean:
```python
BlogPage.objects.child_of(self).live().order_by("-date")
```

### get_context
The index page puts its posts into the template context. That's the hook: override
`get_context`, call `super()`, add what the template needs.

### Pagination — get_page, not page
```
page('abc')      -> PageNotAnInteger
get_page('abc')  -> page 1
page('999')      -> EmptyPage
get_page('999')  -> page 3
```
The query string is user input. `get_page()` clamps it.

### Templates
`blog_index_page.html` loops over `posts` and renders prev/next. `blog_page.html` reuses the
hero include from episode 6 and the back-link pattern from episode 4.

Fixed on the way: the page counter jumped sideways between page 1 and page 3. Three fixed
slots now.

### Before and after
The journal, page 1. Page 3 with only a "Newer" link. A post.

### Next
Ep 8: snippets — team members and testimonials, reusable across pages. And tags for the blog.

## Do NOT do in this episode
- Tags and categories — ep 8.
- RSS — later.
- Blog search — ep 11.
