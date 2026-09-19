# Ep 3 — Build notes & gotchas

## Verified on this machine

- `makemigrations` → `home/migrations/0003_standardpage_homepage_body_homepage_intro.py`,
  three operations: Create model StandardPage, Add field body, Add field intro.
- `migrate` → `Applying home.0003_standardpage_homepage_body_homepage_intro... OK`
- `manage.py check` → no issues.
- Tree after adding About under Home, read from the database:
  ```
  '0001'             1 /                Root     Page
  '00010001'         2 /home/           Home     HomePage
  '000100010001'     3 /home/about/     About    StandardPage
  ```
- `/about/` serves the page. `/home/about/` returns **404**. Checked in the browser.
- Table layout, read by introspection:
  - `home_standardpage` → `['page_ptr_id', 'intro', 'body']`
  - `home_homepage` → `['page_ptr_id', 'body', 'intro']`
  - `wagtailcore_page` → **29 columns**, including path, depth, title, slug, live,
    url_path, seo_title, content_type_id
- `Page.objects.get(slug="about")` → type `Page`, `hasattr(p, "intro")` is `False`.
  `.specific` → `StandardPage`, intro present.
- Admin, checked through Django's test client (logged in without typing a password):
  both edit forms return 200 and include `intro`, `body` and the help text. "Add child
  page" under Home offers both **Standard page** and **Home page**.

## Gotchas worth showing on camera

### `url_path` is not the URL
The most surprising thing in the episode. `url_path` is the path from the tree root, so
it includes `/home/`. The site's root page *is* Home, so the public URL drops it.
People copy `url_path` into links and get 404s. Use `page.url` in templates, which
resolves against the site.

### `.specific`
Anything that queries through `Page.objects` — menus, search results, `get_children()` —
returns base `Page` objects. Your custom fields aren't on them until you call
`.specific`. This will come back in ep 9 (menus) and ep 11 (search).

### Fields don't appear without panels
Adding a field to the model gives you a database column and nothing in the admin.
`content_panels` is what makes it editable. Easy to forget when adding a third field later.

### The template must exist
A page type with no template fails at "View live" with `TemplateDoesNotExist`, not at
creation. So the admin looks fine right up until you preview.

## Not done in this episode, deliberately
- No `subpage_types` — the admin will happily let you put a HomePage under a HomePage.
  Named on screen, fixed in ep 7.
- `body` is a plain `RichTextField`. StreamField replaces it in ep 5.
- The homepage template still includes the welcome egg. Ep 4.

## Local state note
The About page and the homepage Intro text exist only in the local `db.sqlite3`, which
is gitignored. Viewers create their own through the admin — that's steps 4.1–4.2 of
`commands.md`.
