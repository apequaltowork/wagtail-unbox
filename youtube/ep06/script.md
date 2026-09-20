# Ep 6 — Images & Documents

Start from `git checkout ep05-end`.

Everything quoted here was run on the recording machine — see `notes.md`.

## Beats

### Cold open — the site has no pictures
Five episodes of a design studio's website with not one image on it. Today that changes,
and it is the first episode where something we make does **not** live in the repo.

### Already unboxed, already wired
Nothing to install. From episode 2's tour:
- `wagtail.images` and `wagtail.documents` are in `INSTALLED_APPS`
- `MEDIA_ROOT` and `MEDIA_URL` are already set
- `urls.py` already serves media, **but only when `DEBUG = True`** — production is ep 13
- `media/` is in `.gitignore`, because uploads are content, not code

### The hero field
```python
hero_image = models.ForeignKey(
    "wagtailimages.Image", null=True, blank=True,
    on_delete=models.SET_NULL, related_name="+",
)
```
Three things, all deliberate:
- `null/blank` — a page without a hero is normal
- **`SET_NULL`, never `CASCADE`** — deleting an image must not delete pages
- `related_name="+"` — we never ask an image for its pages

### Renditions: what `{% image %}` actually does
It does not resize on every request. It generates a copy, writes it to
`media/images/`, and records a **row** in the rendition table. Next time, the row wins.
The original in `original_images/` is never touched.

Filter specs worth knowing: `width-800`, `height-400`, `fill-800x350`, `max-1200x1200`,
`format-webp`. `fill` crops; `max` does not.

### Responsive images for free
```django
{% srcset_image page.hero_image fill-{800x350,1200x525,1600x700}
   sizes="(max-width: 46rem) 100vw, 46rem" alt=page.hero_alt %}
```
One tag, three renditions, a `srcset` and a `sizes`. Verified at 375px wide: the browser
downloads the **800w** file, not the 1600w one.

### ⭐ Focal points
Show the before and after crop side by side. Same image, same `fill-700x700`, and in the
first one the subject is sliced off at the edge.

Two details worth the screen time:
- Focal points only change **`fill-`** crops. `width-` and `max-` ignore them.
- The filename changes: `studio-hero.2e16d0ba.fill-700x700.jpg` →
  `studio-hero.49a095d8.fill-700x700.jpg`. The focal point is part of the cache key, so a
  stale crop cannot be served.

### ⭐ The gotcha: renditions are rows, not files
Clear out `media/images/` and audit:

```
rows: 14 | missing files: 11
```

`get_rendition()` looks for a database row and returns it. It never checks the disk. So the
site keeps emitting those URLs and every one is a 404 — after a media restore, a new
server, or someone tidying up disk space.

```bash
python manage.py wagtail_update_image_renditions --purge-only
```

### ⭐ Alt text is content, not decoration
Default `{% image %}` with no `alt` falls back to the **image title**. Ours rendered as
`alt="Studio hero"` — a filing label, useless to a screen reader.

In a StreamField the answer is `ImageBlock`, not `ImageChooserBlock`. It carries alt text
and a "decorative" flag alongside the image, so the person writing the page supplies it.
On a plain ForeignKey there is nothing to inherit, so we added our own `hero_alt` field.

This is the episode's opinion: if your CMS makes alt text optional and invisible, you will
ship a site without it.

### Documents
`DocumentChooserBlock`, and a download block that reads `file_extension` and `file.size`
straight off the document. Note the URL: `/documents/1/rate-card.txt` — served by a
**view**, not as a static file. That is what makes private documents possible later.

### One warning, not a task
`WAGTAILIMAGES_IMAGE_MODEL` swaps in your own image model. Decide it on day one or not at
all — retrofitting means migrating every image ForeignKey in the project. Named, not done.

### Before and after
Home with a hero, a full-width image block, and a download. About with a portrait that is
cropped correctly because of its focal point.

### Next
Ep 7: the blog. Parent and child pages, `subpage_types`, and pagination.

## Do NOT do in this episode
- Collections and image permissions — ep 12.
- `format-webp` and optimisation — ep 13, with production.
- Image search indexing — ep 11.
