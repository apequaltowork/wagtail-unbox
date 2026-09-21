# Ep 7 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- New `blog` app: `BlogIndexPage` at `/journal/`, 7 `BlogPage` posts under it.
- Pagination, read out of the rendered HTML, 3 posts per page:

  | URL | Status | Counter | First post |
  |---|---|---|---|
  | `/journal/` | 200 | Page 1 of 3 | Pricing a website honestly |
  | `?page=2` | 200 | Page 2 of 3 | Three pages we build on every site |
  | `?page=3` | 200 | Page 3 of 3 | Why we stopped using page builders |
  | `?page=abc` | 200 | Page 1 of 3 | — |
  | `?page=999` | 200 | Page 3 of 3 | — |
  | `?page=0` | 200 | Page 3 of 3 | — |

- Post back-link → `/journal/`. Homepage child list now shows About and Journal.
- Page-type rules, checked with `can_create_at()`:
  - second HomePage under root → **False**
  - second Journal under Home → **False**
  - BlogPage under About → **False**
  - BlogPage under Journal → True
  - StandardPage under About → True

## ⭐ Gotcha 1 — with no rules, anything goes anywhere

Before adding `parent_page_types` / `subpage_types` to the home app, printed what each type
allowed:

```
HomePage      children: ['BlogIndexPage', 'HomePage', 'Page', 'StandardPage']
StandardPage  children: ['HomePage', 'Page', 'StandardPage']
```

An editor could create a **second homepage inside the About page**, or a bare `Page` with no
template that errors the moment anyone visits it. Wagtail's default is "anything, anywhere",
and every page type you leave unrestricted is a way for the tree to go wrong.

Also worth saying: these rules are Python-only. `makemigrations` after adding them reports
**No changes detected**.

## ⭐ Gotcha 2 — get_children() returns Page, not BlogPage

The obvious query fails:

```python
index.get_children().live().order_by("-date")
# FieldError: Cannot resolve keyword 'date' into field.
```

and without the `order_by` it silently returns plain `Page` objects in **tree order** —
oldest first here, because posts were added chronologically:

```
Page | Why we stopped using page builders
Page | A content model is a conversation
```

`get_children()` queries the `Page` table, which has no `date`. Query the specific model:

```python
BlogPage.objects.child_of(self).live().order_by("-date")
```

returns `BlogPage` instances, newest first. `.specific()` would fix the types but not the
ordering, because the ORDER BY still runs against `Page`.

## Gotcha 3 — Paginator.page() vs get_page()

```
page('abc')      -> PageNotAnInteger
get_page('abc')  -> page 1
page('999')      -> EmptyPage
get_page('999')  -> page 3
```

`page()` raises on anything a visitor can type into the URL. `get_page()` clamps it. Use
`get_page()` for anything driven by a query string.

## Fixed while building

- **The pagination counter jumped sideways.** With `justify-content: space-between`, page 1
  put "Page 1 of 3" on the left and page 3 put it on the right, because the missing link
  removed a flex item. Now three fixed grid slots with empty spans; the counter stays put.
- `startapp` generates `admin.py` and `views.py`. A Wagtail page app uses neither — deleted.

## Design decisions

- **A separate `blog` app**, not more models in `home/`. The blog has its own templates,
  its own rules, and will grow tags and categories. `home` stays the site shell.
- **`BlogPage` reuses `HeroMixin` and `BodyBlock`** from `home`. One definition of a hero,
  one set of content blocks, across every page type.
- **`max_count = 1` on HomePage, `max_count_per_parent = 1` on BlogIndexPage.** One homepage
  per site, one journal per homepage.
- **`date` defaults to `timezone.localdate`**, and is a separate field from
  `first_published_at` — editors backdate posts, and a republish must not reorder the blog.
- Ordering tiebreak is `-first_published_at`, so two posts on the same day are stable.

## Not done in this episode, deliberately

- Tags and categories — they need `ClusterTaggableManager` and snippets. Ep 8.
- RSS feed — small, but it's a routing lesson. Could fold into ep 9.
- Blog search — ep 11.
