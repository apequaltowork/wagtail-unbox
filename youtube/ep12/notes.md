# Ep 12 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- A client user, **casey**, in Wagtail's default **Editors** group, no password (created with
  `set_unusable_password`; logged in with `force_login` for tests).
- All admin checks below used Django's test client as that user.

## ⭐ Gotcha 1 — the client can't edit what we built for them

As casey, before any change:

| Admin URL | Status |
|---|---|
| `/admin/` | 200 |
| `/admin/pages/` | 200 |
| `/admin/snippets/home/teammember/` | **302 → /admin/** |
| `/admin/snippets/home/testimonial/` | **302 → /admin/** |
| `/admin/settings/home/studiosettings/` | **302 → /admin/** |
| `/admin/forms/` | 200 |

The **Studio** and **Settings** menu items don't appear at all. The default Editors group can
add and change pages, images and documents — nothing we defined. Episodes 8 and 9 built the
team, testimonials and footer for the client, and the client couldn't open any of them.

After migration `0009`: all 200 (settings redirects to its per-site URL, then 200).

## ⭐ Gotcha 2 — a permissions migration that silently does nothing

Permissions in a **migration**, not by clicking in Settings → Groups, so every copy of the
site gets them. The obvious version:

```python
Permission.objects.filter(content_type__app_label="home", codename__in=GRANTS)
```

Tested on a **fresh database**, with the `create_permissions` call removed:

```
Applying home.0009_editors_can_edit_studio_content... OK
WITHOUT create_permissions -> Editors home perms: []
...yet the permissions exist now: True
```

Django creates `Permission` rows in a `post_migrate` signal, **after** every migration. On a
fresh database they don't exist yet when `0009` runs, so the filter matches nothing, the
migration reports OK, and the permissions appear a moment later — so nothing looks wrong. On
my existing database it would have worked, which is exactly why it would have shipped. With
`create_permissions` called first, the fresh database gets all 7.

## ⭐ Gotcha 3 — the preview we broke in episode 10

Episode 10 turned `render_landing_page` into a redirect. Wagtail's form preview calls that same
method for its **Landing page** mode:

```
preview mode 'form'    -> 200
preview mode 'landing' -> 302 /contact/?sent=1
```

The preview redirected to the **live** thank-you page, so an editor changing the thank-you
text would preview the published version. `serve_preview` now renders the landing template
directly. Verified with a saved-but-unpublished revision: preview shows the draft text, the
live page is unchanged.

## The dashboard panel

`construct_homepage_panels` hook, a `Component` subclass. The hook is **homepage** panels —
the admin dashboard, not the site's homepage.

The query goes through `get_forms_for_user`, the same permission check as **Forms** in the
menu:

| User | Panel shown | Enquiries |
|---|---|---|
| superuser | yes | Alex Moreau, Sam Patel |
| casey (Editors) | yes | Alex Moreau, Sam Patel |
| admin access only | **no** | — |

Without that filter, the dashboard would show submissions to anyone who can log in.

## page_description

Added to every page type. It's shown when an editor **chooses between** page types. On this
site, that never happens any more: with Journal and Contact at their `max_count`, Home only
allows Standard page, so Wagtail **skips the chooser** and opens the Standard page form
directly — confirmed in the screenshot. Kept: it's free, and it matters the day a new type is
added.

## Small ones

- `WAGTAIL_SITE_NAME = "Studio"` (was `"studio"`, as generated).
- The admin shows every `help_text` we've written since episode 3, straight under each field.

## The screenshots

Real admin, logged in as casey. Captured from a **temporary** local server on port 8002 with a
throwaway settings module that auto-logged-in one user. It was never committed and was deleted
straight after — a middleware like that must never exist outside a scratch file.

## Not done, deliberately
- Custom admin CSS / branding the login screen — cosmetic.
- Workflows and moderation — a two-person studio publishes directly.
- Snippet drafts and revisions (`DraftStateMixin`) — worth it for bigger content teams.
