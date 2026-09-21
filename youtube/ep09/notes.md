# Ep 9 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- `wagtail.contrib.settings` added to `INSTALLED_APPS`, plus its context processor.
- `StudioSettings(BaseSiteSetting)` in `home/models.py`; **Settings → Studio settings**.
- `{% main_menu %}` inclusion tag in `home/templatetags/navigation_tags.py`.
- Menu, read from the rendered HTML (title, active):

  | URL | Menu |
  |---|---|
  | `/` | About · Journal — neither active |
  | `/about/` | **About** active |
  | `/journal/` | **Journal** active |
  | `/journal/pricing-a-website-honestly/` | **Journal** active — a post keeps its section lit |

- The menu costs **1 query** per page (measured by rendering the tag alone, Site cache warm).
- Footer links: `mailto:hello@studio.example`, `tel:+442079460000`.
- At 375px wide: `scrollWidth === innerWidth`, menu fits beside the brand.
- Contact details are placeholders (`.example` domain, an Ofcom drama number range).

## ⭐ Gotcha 1 — the menu is empty

With the tag written and the template wired up, the menu rendered **nothing**. Every existing
page had `show_in_menus = False`:

```
2 HomePage       show_in_menus=False  /home/
3 StandardPage   show_in_menus=False  /home/about/
3 BlogIndexPage  show_in_menus=False  /home/journal/
Page.show_in_menus_default = False
```

`.in_menu()` filters on that flag. It's the **"Show in menus"** checkbox on each page's
**Promote** tab. Ticked About and Journal and the menu appeared.

`show_in_menus_default = True` on `StandardPage` and `BlogIndexPage` makes *new* pages start
ticked. It does **not** change pages that already exist.

## ⭐ Gotcha 2 — a new templatetags module needs a server restart

After creating `home/templatetags/navigation_tags.py`, the running dev server returned:

```
TemplateSyntaxError: 'navigation_tags' is not a registered tag library.
```

The code was fine — a fresh process (the test client) rendered it. `runserver`'s autoreloader
had restarted for the `base.py` and `models.py` edits, but it only watches modules that are
already imported; a brand-new tag module isn't one, so nothing triggered a reload. Stop and
start `runserver`.

## Gotcha 3 — the settings row appears by itself

```
settings rows before first request: 0
settings rows after first request:  1
```

`StudioSettings.for_request()` creates the row with field defaults the first time any page
renders. So `studio_name` must have a sensible `default` — it's what the header shows before
anyone opens Settings.

In templates the path is `settings.APP_LABEL.ModelName.field`:
`{{ settings.home.StudioSettings.email }}`.

## Small, but worth doing

- **`tel:` links with spaces** — `+44 20 7946 0000` is shown as typed, but the `href` uses
  `|cut:' '` so it becomes `tel:+442079460000`.
- **Active state is a prefix match on `url_path`.** Because `url_path` always ends in `/`,
  `/home/about/` can't accidentally match `/home/about-us/`.
- **`aria-current="page"`** marks the active item, and the CSS styles that attribute rather
  than a separate `.active` class — one source of truth.
- `BaseSiteSetting` rather than `BaseGenericSetting`: one row per Site, so a second site on
  the same install gets its own contact details.

## Not done, deliberately
- Nested / dropdown menus — the site has one level. `get_children().live().in_menu()` on each
  item would do it, at one query per item.
- Caching the menu fragment — one query doesn't need it. Worth it once menus nest.
