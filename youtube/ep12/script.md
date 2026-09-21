# Ep 12 — Editor Experience Polish

Start from `git checkout ep11-end`. Everything quoted here was run — see `notes.md`.

## Beats

### Cold open — log in as the client
Every episode so far, we've been a superuser. The client won't be. Create **casey**, put them
in Wagtail's default Editors group, and look.

### ⭐ The client can't open what we built for them
Team, Testimonials, Studio settings: all **302 → /admin/**. The menu items aren't there.
Episodes 8 and 9 built them for the client, and the client can't get in.

### Permissions belong in a migration
Clicking in Settings → Groups works on one machine. A data migration works on every copy —
a colleague's laptop, staging, production.

### ⭐ The migration that says OK and does nothing
On a fresh database: "Applying … OK", Editors get **zero** permissions, and a second later the
permissions exist. Django creates them in `post_migrate`, after every migration. Call
`create_permissions` first. It would have worked on my database — that's why it would have
shipped.

### After
All 200. Studio and Settings in casey's menu.

### ⭐ The preview we broke in episode 10
The "Landing page" preview mode calls `render_landing_page` — which we made a redirect. So it
showed the **live** thank-you page, never the draft. Override `serve_preview`. Verified with an
unpublished revision.

### A panel on the dashboard
`construct_homepage_panels` — the admin's homepage. "Recent enquiries", filtered by
`get_forms_for_user`, so it can't show submissions to anyone Forms wouldn't. Admin-access-only
user: no panel.

### The chooser that disappeared
`page_description` on every type. But under Home, only one type is allowed now, so Wagtail skips
the chooser and opens the form. That's `max_count` doing its job.

### Small things
`WAGTAIL_SITE_NAME = "Studio"`. Every `help_text` since episode 3, under its field.

### What the client sees
casey's dashboard: Studio, Settings, Recent enquiries. A new page: hero help text, alt-text
guidance.

### Next
Ep 13: production settings.
