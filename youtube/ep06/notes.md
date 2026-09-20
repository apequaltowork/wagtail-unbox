# Ep 6 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- Three images uploaded through Wagtail's own API, one document (a 144-byte rate card).
- Home renders hero + 6 blocks: paragraph, services, image, quote, download, cta.
- Read out of the response HTML:
  - hero → `studio-hero.49a095d8.fill-800x350.jpg`, `sizes="(max-width: 46rem) 100vw, 46rem"`
  - block image → `process-banner.width-1200.jpg`, `sizes="100vw"`
  - download → `/documents/1/rate-card.txt`, rendered as `TXT · 144 bytes`
- Alt text, read off the live `<img>` elements:
  - hero → `"A dark teal studio wall with a bright disc of light"` (our own field)
  - block → `"Three columns of coloured bars, our process"` (ImageBlock's alt text)
- Measured in the browser at 1100px: the wide image is **1012px** against a 736px text
  column, and `scrollWidth === clientWidth` — no sideways scroll.
- At 375px the browser picks the **800w** hero rendition, not the 1600w one. srcset works.
- Rendition audit after regenerating: 9 rows, 9 files, 0 missing.

## ⭐ Gotcha 1 — deleting media/ does not clear the rendition table

The big one. Renditions are **database rows** that point at generated files.
`Image.get_rendition()` looks for a row and returns it — it never checks whether the file
is still on disk. Source, `wagtail/images/models.py`:

```python
try:
    rendition = self.find_existing_rendition(filter)
except Rendition.DoesNotExist:
    rendition = self.create_rendition(filter)
```

Deleted the contents of `media/images/` and audited:

```
rows: 14 | missing files: 11
```

Eleven rows still pointing at files that no longer exist, and the site cheerfully puts
those URLs in `<img src>`. Every one is a 404. Nothing in the logs says why.

This is not a contrived scenario — it is what happens when someone clears out `media/` to
save space, restores a database backup onto a fresh server, or deploys to a new host with
an empty media volume.

The fix, and it ships with Wagtail:

```bash
python manage.py wagtail_update_image_renditions --purge-only
```

Purged 14 rows, regenerated on next request, audit back to 0 missing.

## ⭐ Gotcha 2 — the default alt text is a filing label

With a plain `{% image %}` and no `alt`, Wagtail falls back to the **image title**. Ours
came out as `alt="Studio hero"`, which tells a screen-reader user nothing. The title is
how the image is filed in the CMS, not a description of it.

Two fixes, and the episode shows both:
- In a StreamField, use `ImageBlock` (Wagtail 6.3+) instead of `ImageChooserBlock`. It
  carries `alt_text` and a `decorative` flag next to the image, so alt text is content.
- On a plain ForeignKey there is no such thing, so add your own field. We added `hero_alt`.

## Gotcha 3 — the browser will cache a broken image

While the rendition files were missing, the browser cached the failures. After purging and
regenerating, the server returned a valid 12,493-byte JPEG (`fetch(url, {cache:'no-store'})`)
while the page still showed `naturalWidth: 0`. Same family as episode 4's CSS trap.
Hard-reload, or use a throwaway profile when screenshotting.

## Worth pointing at on screen

- **The hash in the filename** — `studio-hero.2e16d0ba.fill-700x700.jpg` becomes
  `studio-hero.49a095d8.fill-700x700.jpg` once a focal point is set. The focal point is
  part of the cache key, so changing it cannot serve a stale crop.
- **Focal points only affect crops.** `fill-` honours them; `width-`, `height-` and `max-`
  do not, because nothing is being cropped away.
- **`original_images/` is never touched.** Every rendition is a copy.
- **Documents are served by a view**, at `/documents/<id>/<filename>`, not as static files.
  That is what makes private collections possible — ep 12 territory.
- Adding block types to a StreamField produced an `AlterField` with **no data problem this
  time**: the column is already JSON and the existing blocks stay valid. A good contrast
  with episode 5.

## Custom image model — say it, don't do it

`WAGTAILIMAGES_IMAGE_MODEL` lets you swap in your own image model with extra fields. It has
to be done **before the first migration that references images**; retrofitting it later
means migrating every ForeignKey in the project. Worth knowing on day one, not worth doing
to a site that already has content. Named in the episode, deliberately not done.

## Not done in this episode, deliberately
- Image collections and permissions — ep 12, with the editor-experience pass.
- `format-webp` / AVIF output and image optimisation — belongs with production, ep 13.
- Image search indexing — ep 11.
- A team-members snippet using images — ep 8.

## Local state note

The uploaded images and the document live in the gitignored `media/`. The three source
JPEGs are committed under `site/sample_images/` so viewers can upload the same ones, or
use their own.
