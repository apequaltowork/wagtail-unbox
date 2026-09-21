# Ep 12 — Editor Experience Polish

| | |
|---|---|
| **Video file** | `youtube/ep12/out/ep12.mp4` |
| **Subtitles** | `youtube/ep12/out/ep12.srt` |
| **Captions (upload these)** | `youtube/ep12/captions.srt` |
| **Transcript** | [`transcript.md`](transcript.md) |
| **Thumbnail** | `youtube/ep12/assets/thumb.png` |
| **Runtime** | 4:26 |
| **Git tag** | `ep12-end` — **push it before publishing** |
| **Category** | Education |
| **Status** | Ready to upload |
| **URL** | — |

---

## Title

```
Customize the Wagtail Admin for Editors: Permissions, Hooks, Previews | Wagtail #12
```

Target search: `wagtail hooks` / `customize wagtail admin` / `wagtail permissions`. 82 characters.

**Alternatives:**

```
Why Your Wagtail Editors Can't See Snippets or Settings | Wagtail Tutorial #12
Wagtail Admin Dashboard Panel with construct_homepage_panels | Wagtail Tutorial #12
```

---

## Description

```
Act 3 starts by logging in as the client. Every episode so far we've been a superuser.
The client isn't — and in Wagtail's default Editors group, they can't open the team,
the testimonials or the footer settings we built for them.

Then a permissions migration that says OK, grants nothing, and would only have failed
in production. And a preview bug we wrote ourselves two episodes ago.

WHAT YOU'LL LEARN
• What the default Editors group can and can't do
• Granting permissions in a data migration, so every copy of the site matches
• Why that migration silently grants nothing on a fresh database, and create_permissions
• The landing-page preview that showed the live page instead of the draft
• A custom dashboard panel with construct_homepage_panels
• Filtering it with get_forms_for_user, so it can't leak enquiries
• page_description, and why Wagtail sometimes skips the page-type chooser
• WAGTAIL_SITE_NAME

📋 Every command and file, with a troubleshooting table:
https://github.com/apequaltowork/wagtail-unbox/blob/main/youtube/ep12/commands.md

📦 CODE — the state at the end of this episode:
https://github.com/apequaltowork/wagtail-unbox

    git checkout ep12-end

Starting from the previous episode? git checkout ep11-end

CHAPTERS
0:00 Log in as the client
0:21 Locked out of their own content
0:45 Permissions belong in a migration
1:06 It says OK and grants nothing
1:17 Permissions are created after every migration
1:48 Fixed, on a fresh database
1:58 The preview bug from episode 10
2:10 The preview showed the live page
2:37 A dashboard panel
2:54 Don't leak enquiries
3:19 The client's dashboard
3:28 The chooser that disappeared
3:53 Every help_text, where it belongs
4:04 Commit and tag
4:07 Next episode

NEXT → Ep 13: Production Settings — Postgres, environment variables, DEBUG off, and Django's checklist.

📦 Code: https://github.com/apequaltowork/wagtail-unbox
🌐 Site: https://apequaltowork.github.io/ashish-pitroda/
💼 LinkedIn: https://www.linkedin.com/in/ashish-pitroda/
✉️ apequaltowork@gmail.com

🔧 Wagtail 7.4.3 · Django 6.1.1 · Python 3.12
Recorded on Windows. macOS and Linux commands are in the repo for every episode.

#wagtail #django #python #cms #webdev
```

---

## Tags

```
wagtail admin, customize wagtail admin, wagtail hooks, wagtail permissions, wagtail editors group, wagtail snippet permissions, wagtail settings permissions, django data migration permissions, create_permissions post_migrate, wagtail construct_homepage_panels, wagtail dashboard panel, wagtail preview, wagtail page_description, wagtail tutorial, wagtail 7.4, wagtail unboxed
```

---

## Thumbnail

`youtube/ep12/assets/thumb.png`

Best hook: the access table with three red **302**s. Overlay: **YOUR CLIENT CAN'T SEE THIS**.

---

## Pinned comment

```
The one to remember from this episode (1:06):

A data migration that adds permissions to a group will say "OK" and grant NOTHING on a
fresh database. Django creates Permission rows in a post_migrate signal, after every
migration has run — so they don't exist yet. It works on your existing database, which
is exactly why it ships broken. Call create_permissions first:

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

Also: the default Editors group can't open your snippets or settings. And if you
overrode render_landing_page to redirect (episode 10), override serve_preview too —
otherwise the Landing page preview shows the live page, not the draft.
```

---

## Before publishing

```bash
git push origin ep12-end
```

---

## End screen

- Subscribe element
- "Next video" → Ep 13
- Link element → the repo
