# Ep 8 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- Two snippets in `home/models.py`: `TeamMember` (Orderable) and `Testimonial`.
  Registered in `home/wagtail_hooks.py` as a `SnippetViewSetGroup` called **Studio**.
- 3 team members, 2 testimonials, 7 posts tagged across 5 tags.
- About renders a `team` block listing all 3 members, in `sort_order`.
- Home renders a `testimonial` block: Alex Moreau, Moreau Architects.
- `?tag=editors` → 4 posts, "Page 1 of 2". `?tag=process` → 4 posts, "Page 1 of 2".
- The people are fictional and their avatars are generated shapes, not photos.

## ⭐ Gotcha 1 — pagination forgets the filter

Adding `?tag=` filtering and changing nothing else:

```
?tag=process   -> Page 1 of 2
'Older' link   -> ?page=2
following it   -> Page 2 of 3       # the tag is gone -- this is the unfiltered list
```

The pagination links from episode 7 were written as `?page=N`, so they replace the whole
query string. Page 2 silently shows the unfiltered journal. Fixed by passing the tag back
into the context and building links as `?tag=…&page=N`:

```
'Older' link   -> ?tag=process&page=2
following it   -> Page 2 of 2
```

Any time you add a second query parameter, every link that builds a query string has to
carry both.

## ⭐ Gotcha 2 — deleting a snippet a page uses

Tested inside a rolled-back transaction:

- **Before delete**, Wagtail's reference index already knows: usage count **1**, on `Home`.
  The admin shows this on the delete confirmation. Use it.
- **After delete**, the page still renders **200**. The block's value is **`None`**.
- Without a guard, the template renders an **empty styled quote box**. With
  `{% if t %}` it renders nothing.

Every template that reads a chooser block value should expect `None`.

## Gotcha 3 — circular import between blocks and models

`home/models.py` imports `home/blocks.py` to build `BodyBlock`. So `blocks.py` cannot import
`home.models` at the top:

- `SnippetChooserBlock("home.Testimonial")` — pass the model as a **string**.
- `TeamBlock.get_context` — import `TeamMember` **inside the method**.

## Fixed while building

- **Tag pills had borders above and below them.** `.post-list li` is a descendant selector,
  and the tag list inside each post is also a `<ul>`, so every pill got the post row's
  padding and border. Changed to `.post-list > li`.
- The measured link above came out as `?tag=process&amp;page=2` when read raw from HTML —
  that is correct HTML; a browser decodes `&amp;` to `&`.

## Design decisions

- **Testimonial is chosen per page, Team is not.** A page picks which testimonial it wants.
  The team block has nothing to choose — it fetches everyone in `get_context`, so adding a
  person updates every page that shows the team.
- **`Orderable` on TeamMember** gives drag-and-drop ordering in the snippet listing for free
  (the viewset auto-detects `sort_order`).
- **`ParentalKey` on the tag through-model**, not `ForeignKey`: tags are saved with the page
  revision, so a draft can change its tags without touching the live post.

## Not done, deliberately
- Snippet revisions, drafts and locking (`DraftStateMixin`, `RevisionMixin`) — ep 12.
- A tag cloud / tag index page — small, not worth the screen time.
