# Ep 11 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues. Backend: `wagtail.search.backends.database` (generated
  default, uses the SQLite database — no Elasticsearch).
- `update_index` → `indexed 19 objects`.
- Search results, from the rendered `/search/` page:

  | Query | Results |
  |---|---|
  | `fixed price` | 2 — Home page, Blog page |
  | `Priya` | 1 — About (Standard page) |
  | `handover` | 9 |
  | `zzzz` | 0 |
  | *(empty)* | no count shown |

- Search appears in the menu and is marked `aria-current` on `/search/`.
- The seeded posts share one body, so body-text queries match several posts at once.

## ⭐ Gotcha 1 — only the title is searched

Out of the box, `BlogPage.search_fields` is just `Page.search_fields` — title plus a set of
filter fields. Before adding anything:

```
'pricing'       -> 1 result   (it's in a title)
'fixed price'   -> 0          (it's in the intro)
'integrations'  -> 0          (it's in the body)
'handover'      -> 0
```

Every custom field has to be named:

```python
search_fields = Page.search_fields + [
    index.SearchField("intro"),
    index.SearchField("body"),
    index.FilterField("date"),
]
```

`makemigrations` → **No changes detected**. Search config isn't a schema change.

## ⭐ Gotcha 2 — adding fields doesn't reindex anything

With `search_fields` added and nothing else: **still 0 results** for all three. The index
holds what was written when each page was last saved. Existing pages need:

```bash
python manage.py update_index
```

After that: `fixed price` → 1, `integrations` → 7, `handover` → 8. From here, saving or
publishing a page reindexes it automatically.

## ⭐ Gotcha 3 — text on the page, not in the index

```
'Priya'   visible on /about/  True | search finds: []
'Moreau'  visible on /        True | search finds: []
```

The team block fetches names at render time; the testimonial block stores only an id. Neither
text is part of the page when it's indexed. Fixed with `get_searchable_content` on both
blocks. After `update_index`: `Priya` → About, `Moreau` → Home.

Trade-off, said out loud: those names are copied into the page's index entry. If the team
changes, About's entry is stale until About is saved again or `update_index` runs.

## ⭐ Gotcha 4 — the generated view shows private pages

Inside a rolled-back transaction, a password restriction on the pricing post:

```
.live().search("pricing")          -> ['Pricing a website honestly']
.live().public().search("pricing") -> []
```

The view `wagtail start` generates uses `.live()` only, so the **titles of private pages**
appear in results for anyone. Added `.public()`.

## Also changed in the view

- `.specific()` so results are real `BlogPage`/`StandardPage` objects and the template can
  show `intro`, not just `search_description` (which nobody fills in).
- `paginator.get_page()` instead of the try/except around `page()` — episode 7's lesson.
- `query` is stripped; an empty query shows the form and no count.

## Not done, deliberately
- `wagtail.contrib.search_promotions` (editor-picked "best bets") — ep 12 territory.
- Autocomplete / `AutocompleteField` — needs a different query method and front-end JS.
- Elasticsearch / OpenSearch — the database backend is right for a site this size.
