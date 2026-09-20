# Ep 6 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 5's end state

```bash
git checkout ep05-end
```

```powershell
.venv\Scripts\activate          # Windows
cd site
python manage.py runserver
```

## 0. Nothing to install

`wagtail.images` and `wagtail.documents` were in `INSTALLED_APPS` from the very first
`wagtail start`, and `studio/settings/base.py` already has:

```python
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
```

`studio/urls.py` already serves both — **only under `DEBUG = True`**:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Serving media in production is episode 13. `media/` is gitignored: uploads are content.

## 1. The hero field — `home/models.py`

```python
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HeroMixin(models.Model):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,     # never CASCADE
        related_name="+",
    )
    hero_alt = models.CharField(max_length=180, blank=True,
                                verbose_name="Hero alt text")
    hero_caption = models.CharField(max_length=180, blank=True)

    hero_panels = [
        MultiFieldPanel(
            [FieldPanel("hero_image"), FieldPanel("hero_alt"),
             FieldPanel("hero_caption")],
            heading="Hero",
        )
    ]

    class Meta:
        abstract = True
```

Then on both page types:

```python
class HomePage(HeroMixin, Page):
    ...
    content_panels = Page.content_panels + HeroMixin.hero_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
```

`on_delete=models.SET_NULL` is the important one. With `CASCADE`, deleting an image in the
admin would delete every page using it.

## 2. Image and document blocks — `home/blocks.py`

```python
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageBlock


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageBlock()                       # NOT ImageChooserBlock
    caption = blocks.CharBlock(required=False, max_length=180)
    width = blocks.ChoiceBlock(
        choices=[("text", "Text width"), ("wide", "Full width")],
        default="text",
    )

    class Meta:
        icon = "image"
        label = "Image"
        template = "home/blocks/image_block.html"


class DownloadBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    title = blocks.CharBlock(required=False, max_length=120)

    class Meta:
        icon = "doc-full"
        label = "Download"
        template = "home/blocks/download_block.html"
```

and add them to `BodyBlock`:

```python
    image = CaptionedImageBlock()
    download = DownloadBlock()
```

**`ImageBlock`, not `ImageChooserBlock`.** It is Wagtail 6.3+ and it carries alt text and a
"decorative" checkbox alongside the image, so accessibility is part of the content. It still
behaves as an Image everywhere an `ImageChooserBlock` value did.

## 3. Migrate

```bash
python manage.py makemigrations home
python manage.py migrate
```

No drama this time: the `body` column is already JSON and the existing blocks stay valid.
Adding block types to a StreamField does not need a data migration.

## 4. The hero template

`home/templates/home/includes/hero.html`:

```django
{% load wagtailimages_tags %}
{% if page.hero_image %}
    <figure class="hero">
        {% srcset_image page.hero_image fill-{800x350,1200x525,1600x700} sizes="(max-width: 46rem) 100vw, 46rem" alt=page.hero_alt %}
        {% if page.hero_caption %}
            <figcaption>{{ page.hero_caption }}</figcaption>
        {% endif %}
    </figure>
{% endif %}
```

and include it at the top of `{% block content %}` in both page templates:

```django
{% include "home/includes/hero.html" %}
```

## 5. Block templates

`home/templates/home/blocks/image_block.html`:

```django
{% load wagtailimages_tags %}
<figure class="img img--{{ value.width }}">
    {% if value.width == "wide" %}
        {% srcset_image value.image width-{1200,1800,2400} sizes="100vw" %}
    {% else %}
        {% srcset_image value.image width-{600,900,1200} sizes="(max-width: 46rem) 100vw, 46rem" %}
    {% endif %}
    {% if value.caption %}
        <figcaption>{{ value.caption }}</figcaption>
    {% endif %}
</figure>
```

No `alt` here — `ImageBlock` supplies it from the editor's own alt text.

`home/templates/home/blocks/download_block.html`:

```django
<p class="download">
    <a href="{{ value.document.url }}" download>
        {{ value.title|default:value.document.title }}
    </a>
    <span class="meta">{{ value.document.file_extension|upper }} · {{ value.document.file.size|filesizeformat }}</span>
</p>
```

## 6. Filter specs

| Spec | Does |
|---|---|
| `width-800` | scales to 800 wide, keeps ratio |
| `height-400` | scales to 400 tall |
| `fill-800x350` | **crops** to exactly that, honours the focal point |
| `max-1200x1200` | fits inside the box, never crops, never enlarges |
| `min-500x500` | covers the box |
| `format-webp` | changes the output format |

## 7. Upload some images

http://127.0.0.1:8000/admin/images/ → Add an image.

Three sample images are in the repo if you want the exact ones from the video:

```
site/sample_images/studio-hero.jpg
site/sample_images/process-banner.jpg
site/sample_images/team-portrait.jpg
```

## 8. Focal points

Images → pick one → **Set focal point**, drag a box over the subject, save.

The rendition filename changes, because the focal point is part of the cache key:

```
studio-hero.2e16d0ba.fill-700x700.jpg     before
studio-hero.49a095d8.fill-700x700.jpg     after
```

Focal points only affect **`fill-`**. `width-`, `height-` and `max-` ignore them — nothing
is being cropped, so there is nothing to choose.

## 9. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 6"
git tag ep06-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Images 404 after restoring a database or moving server | Rendition **rows** survived; the files did not. `get_rendition()` never checks the disk | `python manage.py wagtail_update_image_renditions --purge-only` |
| Images still broken after that | The browser cached the failures | Hard-reload: `Ctrl`+`F5`, or `Cmd`+`Shift`+`R` |
| `alt` comes out as the image's title | No `alt` given, so Wagtail falls back to the title | Pass `alt=...`, or use `ImageBlock` in a StreamField |
| Focal point makes no difference | The spec is `width-` or `max-` | Only `fill-` crops, so only `fill-` uses it |
| `Invalid filter spec` | Typo, or a space in the spec | `fill-800x350`, no spaces |
| Deleting an image deleted pages | `on_delete=CASCADE` on the ForeignKey | `on_delete=models.SET_NULL` with `null=True` |
| Images work locally, 404 in production | Media is only served by Django when `DEBUG = True` | Episode 13 |
| `AttributeError: 'Image' object has no attribute 'caption'` | Reading a caption off `ImageBlock`'s value | `ImageBlock` resolves to an Image; put the caption in the wrapping StructBlock |
