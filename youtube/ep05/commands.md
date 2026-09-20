# Ep 5 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 4's end state

```bash
git checkout ep04-end
```

```powershell
.venv\Scripts\activate          # Windows
cd site
python manage.py runserver
```

## 1. `home/blocks.py` — new file

Full file in the repo:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/home/blocks.py

The shape of it:

```python
from wagtail import blocks


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(rows=3)
    attribution = blocks.CharBlock(required=False, max_length=120)

    class Meta:
        icon = "openquote"
        label = "Pull quote"
        template = "home/blocks/quote_block.html"


class ServiceBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=80)
    description = blocks.TextBlock(rows=3)


class ServicesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=80, default="What we do")
    services = blocks.ListBlock(ServiceBlock(), min_num=1, max_num=6)

    class Meta:
        icon = "list-ul"
        label = "Services"
        template = "home/blocks/services_block.html"


class BodyBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(form_classname="title", icon="title",
                               template="home/blocks/heading_block.html")
    paragraph = blocks.RichTextBlock(
        icon="pilcrow",
        features=["bold", "italic", "link", "ol", "ul", "document-link"],
    )
    quote = QuoteBlock()
    services = ServicesBlock()
    cta = CTABlock()

    class Meta:
        block_counts = {"services": {"max_num": 1}}
```

`StructBlock` = these fields go together. `ListBlock` = there can be several.
`StreamBlock` = the editor picks from these, in any order.

Icon names come from Wagtail's own icon set: `openquote`, `list-ul`, `title`, `pilcrow`,
`link`. A name that isn't in the set silently renders nothing.

## 2. `home/models.py`

```python
from wagtail.fields import StreamField       # was: RichTextField
from home.blocks import BodyBlock

    body = StreamField(BodyBlock(), blank=True)   # was: RichTextField(blank=True)
```

Both `HomePage` and `StandardPage`. **Do not pass `use_json_field=True`** — pre-Wagtail-6
tutorials all do, and in 7.4 it is accepted and ignored.

## 3. Make the migration

```bash
python manage.py makemigrations home
python manage.py migrate
```

On any page that already has rich-text content, this fails:

```
django.db.utils.IntegrityError: CHECK constraint failed: (JSON_VALID("body") OR "body" IS NULL)
```

**Nothing is broken.** Django rolls the whole migration back — `python manage.py showmigrations home`
still shows `0004` unapplied, and your content is untouched. Postgres reports the same
problem as `invalid input syntax for type json`.

## 4. Fix it: a data migration in front of the AlterField

Open the generated `home/migrations/0004_alter_homepage_body_alter_standardpage_body.py`.
Leave the `AlterField` operations alone — add this above them:

```python
import json
import uuid

MODELS = ("HomePage", "StandardPage")


def html_to_stream(apps, schema_editor):
    """Rewrap each page's rich-text HTML as one 'paragraph' block."""
    for model_name in MODELS:
        Model = apps.get_model("home", model_name)
        for page in Model.objects.all():
            html = (page.body or "").strip()
            if html.startswith("["):
                continue  # already StreamField JSON
            blocks = (
                [{"type": "paragraph", "value": html, "id": str(uuid.uuid4())}]
                if html
                else []
            )
            Model.objects.filter(pk=page.pk).update(body=json.dumps(blocks))


def stream_to_html(apps, schema_editor):
    """Reverse: flatten paragraph blocks back to a single HTML string."""
    for model_name in MODELS:
        Model = apps.get_model("home", model_name)
        for page in Model.objects.all():
            try:
                blocks = json.loads(page.body or "[]")
            except (TypeError, ValueError):
                continue
            html = "".join(
                b.get("value", "") for b in blocks if b.get("type") == "paragraph"
            )
            Model.objects.filter(pk=page.pk).update(body=html)
```

and put it first in `operations`:

```python
    operations = [
        migrations.RunPython(html_to_stream, stream_to_html),
        migrations.AlterField(
            ...
```

Order matters: the RunPython runs while the column is still plain text.

```bash
python manage.py migrate
```

```
Applying home.0004_alter_homepage_body_alter_standardpage_body... OK
```

## 5. Templates

`home/templates/home/home_page.html` and `standard_page.html` — one line each:

```django
{{ page.body }}          {# was: {{ page.body|richtext }} #}
```

Then the block templates, in `home/templates/home/blocks/`:

```bash
mkdir home/templates/home/blocks
```

PowerShell:
```powershell
New-Item -ItemType Directory home\templates\home\blocks
```

`heading_block.html`
```django
<h2>{{ value }}</h2>
```

`quote_block.html`
```django
<blockquote>
    <p>{{ value.quote }}</p>
    {% if value.attribution %}
        <cite>{{ value.attribution }}</cite>
    {% endif %}
</blockquote>
```

`services_block.html`
```django
<h2>{{ value.heading }}</h2>
<ul class="service-grid">
    {% for service in value.services %}
        <li>
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
        </li>
    {% endfor %}
</ul>
```

`cta_block.html`
```django
{% load wagtailcore_tags %}
<p>{{ value.text }}</p>
{% if value.page %}
    <a class="button" href="{% pageurl value.page %}">{{ value.button_text }}</a>
{% elif value.external_url %}
    <a class="button" href="{{ value.external_url }}">{{ value.button_text }}</a>
{% endif %}
```

Notice what is **not** in any of them: a wrapper `div` with a class. Wagtail 7 already emits
`<div class="w-block-NAME block-NAME">` around every block. Add your own `block-cta` and you
get the styling twice — a teal box inside a teal box.

## 6. CSS

Appended to `studio/static/css/studio.css`, targeting Wagtail's wrappers:

```css
.block-heading h2    { ... }
.block-quote blockquote { border-left: 3px solid var(--accent); ... }
.service-grid        { display: grid; grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr)); }
.block-cta           { background: var(--accent); color: #fff; text-align: center; }
```

Full file:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/studio/static/css/studio.css

## 7. Build a page out of blocks

http://127.0.0.1:8000/admin/ → Home → edit. The Body field now has a "+" menu with
Heading, Paragraph, Pull quote, Services and Call to action. Add a few, drag to reorder,
publish.

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 5"
git tag ep05-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `IntegrityError: CHECK constraint failed: (JSON_VALID("body")...)` | A page already has rich-text content and the column is becoming JSON | Step 4 — RunPython before AlterField |
| `invalid input syntax for type json` | Same thing, on Postgres | Same fix |
| Block renders inside a duplicate coloured box | Your template adds a class Wagtail already adds | Drop the wrapper class — step 5 |
| `TypeError: __init__() got an unexpected keyword argument` on a block | A `Meta` option passed as a constructor argument, or vice versa | `icon`/`label`/`template` go in `Meta`; `required`/`max_length` are constructor arguments |
| Block menu shows an empty icon | Icon name isn't in Wagtail's set | Use one of `title`, `pilcrow`, `openquote`, `list-ul`, `link`, `image`, `code`… |
| `ListBlock` won't save with zero items | `min_num=1` | Remove `min_num`, or add an item |
| Editors can't leave the body empty | `blank=True` missing on the field | `StreamField(BodyBlock(), blank=True)` |
| Old content vanished after migrating | Migrated without the data step, on a database that had no check constraint | Restore, then migrate with step 4 |
