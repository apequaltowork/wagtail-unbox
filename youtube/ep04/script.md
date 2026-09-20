# Ep 4 — Templates & Static Files

The first episode with a visible before/after. Start from `git checkout ep03-end`.

Everything quoted here was verified against the running site — see `notes.md`.

## Beats

### Cold open — the egg has to go
Three episodes in, the site still shows Wagtail's welcome page. Today it goes, and the
studio site starts looking like a site.

### Where the welcome page actually lives
`home_page.html` includes `home/welcome_page.html` and pulls in `welcome_page.css`. Both
are Wagtail's, both are disposable, and the generated comment says so:
*"Delete the line below if you're just getting started."* Delete both files.

### How Wagtail finds a template
Recap from ep 2, now used for real:

```
class HomePage(Page)  ->  home/templates/home/home_page.html
```

Model name, lowercased, underscored. Two places templates can live:
- `APP_DIRS: True` → `home/templates/…` (per app)
- `DIRS: [PROJECT_DIR / "templates"]` → `studio/templates/…` (project-wide)

`base.html` is project-wide because every app uses it. Page templates sit with their app.

### base.html: the parts worth keeping
The generated `<head>` is already good — SEO title with fallback, `{% wagtailuserbar %}`,
the preview-panel `<base target="_blank">`. Keep all of it. Replace only the `<body>`,
adding a header, `<main>`, and a footer around `{% block content %}`.

### Three tags that do the linking
| Tag | Use |
|---|---|
| `{% pageurl child %}` | link to a page object |
| `{% slugurl 'home' %}` | link to a page by slug — survives renaming |
| `{{ page.body\|richtext }}` | render a RichTextField as HTML |

Callback to ep 3: never build links from `url_path`. `/home/about/` is a 404; `pageurl`
gives `/about/`.

### Listing children
```django
{% for child in page.get_children.live %}
```
`.live` means published only — drafts stay hidden. This is the page tree from ep 2 doing
something useful: the homepage doesn't know About exists, it just asks for its children.

### The static file that ships empty
`studio/static/css/studio.css` is **0 bytes**. Wagtail links it in `base.html` and leaves
it for you. `{% static %}` resolves it via `STATICFILES_DIRS`. Write plain CSS — no build
step, no framework, all series long.

### ⭐ The gotcha that will cost you ten minutes
Write the CSS, reload, and the page is **still unstyled**. Nothing is wrong with the code.
The browser cached `studio.css` while it was 0 bytes, and an ordinary reload re-uses it.
Hard-reload — `Ctrl+F5`, or `Cmd+Shift+R`. Verified live: the stylesheet was attached with
**0 rules** until the cache was bypassed, then 20.

### Before and after
Side by side: the egg, then the studio site. Then About, with its back-link built from
`page.get_parent`. Then the mobile width — `h1` drops from 2.6rem to 2rem at the media
query.

### One thing that hasn't changed
The 404 page still looks like Django's. `404.html` exists but is only used when
`DEBUG = False`. Episode 13.

### Next
Ep 5: `body` is one rich-text blob. StreamField replaces it with real content blocks.

## Do NOT do in this episode
- `{% image %}` — there's no image field until ep 6.
- Navigation menus. The header has one hard-coded link; menus from the tree are ep 9.
- `collectstatic`. Mention it exists, defer to ep 13.
