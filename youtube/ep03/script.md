# Ep 3 — The Page Model & the Tree

The first episode that changes code. Start from `git checkout ep02-end`.

Every value and output quoted here was captured from a real run. See `notes.md` for what
was verified and how.

## Beats

### Cold open — the promise
Ep 2 predicted that a page one level under Home would get the path `000100010001`.
This episode we create that page and check it.

### Recap: six lines
`HomePage(Page): pass` is already a working page type, because `Page` brings title, slug,
SEO fields, publishing, revisions and permissions with it.

### Adding fields
- `intro` — a `CharField`, with `help_text` the editor actually sees
- `body` — a `RichTextField`, Wagtail's rich-text editor field
- **`content_panels`** — a field on the model is *not* automatically editable. It only
  appears in the admin once it has a `FieldPanel`. `Page.content_panels + [...]` keeps the
  title field Wagtail already provides.

### A second page type
`StandardPage` for About, Services and anything that is mostly words. Same two fields.
It needs `home/standard_page.html` — the template-naming rule from ep 2 in action —
or "View live" fails with `TemplateDoesNotExist`. The template is bare on purpose.

### The migration
Real output: `0003_standardpage_homepage_body_homepage_intro` — one new model, two new
fields. Open the file and look at one line:

```python
('page_ptr', models.OneToOneField(..., parent_link=True, primary_key=True,
                                  to='wagtailcore.page'))
```

### ⭐ The mental model: two tables
This is Django **multi-table inheritance**:

- `wagtailcore_page` — **29 columns**, shared by every page on the site: title, slug,
  path, depth, url_path, live, seo_title, content_type…
- `home_standardpage` — **3 columns**: `page_ptr_id`, `intro`, `body`. Only what's unique
  to this page type.

`page_ptr_id` joins them. Callback to ep 2: `content_type_id` on the shared row is how
Wagtail knows which second table to look in.

### In the admin
Edit Home: Intro and Body are there, with the help text. Publish.
Add a child page under Home → Standard page → "About". Publish.

### ⭐ The payoff: the tree
Shell, real output:

```
'0001'             1 /                Root
'00010001'         2 /home/           Home
'000100010001'     3 /home/about/     About
```

Exactly as predicted. Four characters per level.

### The URL surprise
`url_path` says `/home/about/`, but the page is served at **`/about/`**. `/home/about/`
is a 404. The `url_path` includes the site root; the public URL doesn't. Home *is* the
root, so it drops out.

### The `.specific` gotcha
`Page.objects.get(slug="about")` returns a plain `Page` — no `intro`. `.specific` returns
the `StandardPage`. The single most common "why is my field missing?" question.

### What's still wrong — teaser for ep 7
When adding a child under Home, the admin offers **Home page** as well as Standard page.
Nothing stops you nesting a homepage inside a homepage. `subpage_types` and
`parent_page_types` fix that, in episode 7.

### Next
Ep 4: the site still shows Wagtail's welcome egg. We replace it with real templates.

## Do NOT do in this episode
- Style anything. Ep 4.
- StreamField. `body` is a plain `RichTextField` on purpose; ep 5 replaces it.
- `subpage_types`. Name the problem, defer the fix to ep 7.
