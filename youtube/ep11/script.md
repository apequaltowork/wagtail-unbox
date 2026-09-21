# Ep 11 — Search

Start from `git checkout ep10-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — the app we unboxed and never used
Episode 2 toured `search/`: a view, a template, a URL. It has been there all series. Today it
works, and we find four ways it doesn't.

### It already runs
`/search/?query=pricing` → 1 result. The database backend, no Elasticsearch.

### ⭐ Only titles are searched
"fixed price" (in an intro) → 0. "integrations" (in a body) → 0. `Page.search_fields` is the
title and filters. Name your fields: `SearchField("intro")`, `SearchField("body")`.
No migration — `No changes detected`.

### ⭐ And still nothing
Fields added, still 0. The index is what was written at save time. `update_index` → 19
objects → now it finds them. After this, publishing reindexes automatically.

### ⭐ Visible, but not searchable
"Priya" is on the About page. Search: nothing. The team block fetches names at render time;
the testimonial stores an id. `get_searchable_content` on each block copies the words in.
Trade-off: they go stale until the page is saved or reindexed.

### ⭐ The generated view leaks private pages
Password-protect the pricing post: `.live().search()` still returns it. `.public()` doesn't.
The view `wagtail start` gives you shows private titles to anyone.

### The view, rewritten
`.live().public().specific()`, `get_page()`, a stripped query. `.specific()` so results can
show their intro.

### The template
A labelled search input, a result count, each result's kind and intro, pagination that
carries `query` — episode 8's lesson.

### Search in the menu
One extra `<li>`, `aria-current` from `request.resolver_match`.

### Before and after
"handover" → 9 results. "Priya" → About.

### Next
Ep 12: editor experience — making the admin pleasant for the client.
