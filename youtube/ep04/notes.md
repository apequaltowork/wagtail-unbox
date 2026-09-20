# Ep 4 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues after the template rewrite.
- Homepage renders: header, `<h1>Home</h1>`, intro paragraph, a child list containing
  About, footer. The welcome egg is gone — checked `'welcome' not in html`.
- Link rendering, read out of the response HTML:
  - brand → `/` (from `{% slugurl 'home' %}`)
  - About → `/about/` (from `{% pageurl child %}`)
  - stylesheet → `/static/css/studio.css`
- `/about/` renders with the `← Home` back-link built from `page.get_parent`.
- Mobile at 375px: `h1` computes to **32px** (the 2rem media query), down from 2.6rem.
- No server errors in the dev log.

## ⭐ The browser-cache gotcha — worth the screen time

After writing the CSS the page still rendered completely unstyled. The code was fine.
Measured in the live page:

```js
document.styleSheets.length            // 1   -- the sheet IS attached
document.styleSheets[0].cssRules.length // 0  -- but it parsed as empty
fetch(href, {cache:'no-store'})         // 200, 2065 bytes, text/css
```

So the file was being served correctly, while Chrome kept using the **0-byte copy it
cached on the first page load**. `location.reload(true)` does not help — modern Chrome
ignores the flag. Bypassing the cache produced **20 rules** and the styled page.

This will hit every viewer, because `studio.css` ships at 0 bytes and they will have
loaded the site at least once before writing any CSS. Show it on camera rather than
letting them think they typed something wrong.

## Expected, not broken

- **The 404 page still looks like Django's.** `studio/templates/404.html` exists and
  extends `base.html`, but Django only uses it when `DEBUG = False`. Under `runserver`
  with debug on you get the technical 404. Episode 13.
- **`home/static/` disappears.** Deleting `welcome_page.css` empties it; the folder can go.
  Project-wide CSS lives in `studio/static/`.

## Deviation from the original plan

The plan sheet for this episode listed `{% image %}`. Dropped: there is no image field on
any page until ep 6, so demonstrating it would mean adding a model field that belongs to
that episode. Templates, static files and page linking fill the episode on their own.

## Not done in this episode, deliberately
- Navigation is one hard-coded brand link. Menus built from the page tree are ep 9.
- `body` is still a single `RichTextField`. StreamField replaces it in ep 5.
- No `collectstatic` — named only, deferred to ep 13.

## Local state note
The About page and the homepage intro text live only in the local gitignored
`db.sqlite3`. Viewers created their own in episode 3.
