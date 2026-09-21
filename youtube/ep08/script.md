# Ep 8 — Snippets & Reusable Content

Start from `git checkout ep07-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — content that isn't a page
A team member has no URL. A testimonial has no place in the tree. But both belong on pages,
and on more than one. That is a **snippet**: a plain Django model the admin can edit.

### Two models
`TeamMember(Orderable)` — name, role, photo, bio. `Testimonial(models.Model)` — quote,
author, company. `Orderable` adds `sort_order` and, with it, drag-and-drop ordering.

### Register them: SnippetViewSet
`home/wagtail_hooks.py`. One viewset per model sets the icon, menu label, listing columns and
search. A `SnippetViewSetGroup` puts both under one **Studio** menu item.

### Two ways to use a snippet
- **Chosen per page:** `TestimonialBlock` wraps a `SnippetChooserBlock("home.Testimonial")`.
- **Fetched by the block:** `TeamBlock` has nothing to choose — `get_context` loads every
  member. Add a person and every page showing the team updates.

### The circular import
`models.py` imports `blocks.py`. So `blocks.py` names the model as a string, and imports
`TeamMember` inside `get_context`.

### ⭐ Deleting a snippet that a page uses
Wagtail's reference index already knows: "used 1 time, on Home". After deleting, the page
still returns 200 and the block value is `None`. Guard it: `{% if t %}`.

### Tags for the journal
`BlogPageTag(TaggedItemBase)` with a **ParentalKey**, and `ClusterTaggableManager` on the
post. ParentalKey so tags live in the revision — a draft can change tags without touching the
live post. Filter with `?tag=`.

### ⭐ Pagination forgets the filter
`?tag=process` → Page 1 of 2. Click Older → `?page=2` → **Page 2 of 3**. The tag is gone.
Episode 7's links replace the whole query string. Carry the tag: `?tag=…&page=N`.

### Fixed on the way
Tag pills had borders — `.post-list li` matched the tag list too. `.post-list > li`.

### Before and after
The team on About. A testimonial on Home. The journal filtered by tag.

### Next
Ep 9: navigation from the page tree, and site settings the client can edit.
