# Ep 9 — Navigation & Site Settings

Start from `git checkout ep08-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — a site you can't get around
There's an About page and a Journal, and the only way to reach them is the homepage list.
And the footer says "Studio" because it's typed into a template.

### The menu comes from the tree
No menu model. The site's root page's children, live, **in menu**. An editor controls the
menu by ticking "Show in menus" on the Promote tab.

### An inclusion tag
`home/templatetags/navigation_tags.py`: `{% main_menu %}` finds the Site for the request,
takes its root page's children, and marks the active item.

### ⭐ The server doesn't know the tag exists
`TemplateSyntaxError: 'navigation_tags' is not a registered tag library.` The code is fine.
The autoreloader only watches modules already imported. Restart `runserver`.

### ⭐ The menu is empty
Every page has `show_in_menus = False`. That's the default. Tick the box on Promote.
`show_in_menus_default = True` fixes it for **new** pages only.

### The active item
`current.url_path.startswith(item.url_path)` — a post under the journal keeps Journal lit.
`url_path` ends in `/`, so About can't match About-us. `aria-current="page"` carries it; the
CSS styles the attribute.

### One query
Measured: the menu costs one query. No caching needed yet.

### Site settings
`wagtail.contrib.settings` in `INSTALLED_APPS`, plus its context processor. `StudioSettings`
is a `BaseSiteSetting` — one row per site. `@register_setting` puts it under Settings.

### The row creates itself
Zero rows, one request, one row. Defaults matter — the header shows `studio_name` before
anyone opens the settings screen.

### Using it
`{{ settings.home.StudioSettings.email }}` — app label, model name, field. The brand, the
footer, `mailto:`, and a `tel:` link with the spaces cut out.

### Before and after
The header with Journal highlighted on a post. The footer from settings.

### Next
Ep 10: a contact form that emails the studio and stores every submission.
