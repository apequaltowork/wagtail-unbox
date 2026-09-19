# Ep 3 — Commands

The first episode that changes code. Every command and every output below was run on
the recording machine.

## Start from episode 2's end state

```bash
git checkout ep02-end
```

Activate your venv, then move into the project:

```powershell
.venv\Scripts\activate          # Windows
cd site
```
```bash
source .venv/bin/activate       # macOS / Linux
cd site
```

## 1. Edit `home/models.py`

Replace the whole file with:

```python
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text="One or two sentences shown under the page title.",
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


class StandardPage(Page):
    """A plain content page: About, Services, anything that is mostly words."""

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text="One or two sentences shown under the page title.",
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
```

## 2. Add a template for the new page type

Create `home/templates/home/standard_page.html`:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-standardpage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    {% if page.intro %}
        <p>{{ page.intro }}</p>
    {% endif %}

    {{ page.body|richtext }}
{% endblock content %}
```

Without this file, "View live" on a Standard page fails with `TemplateDoesNotExist`.
It's deliberately bare; styling is episode 4.

## 3. Make and apply the migration

```bash
python manage.py makemigrations
```

```
Migrations for 'home':
  home\migrations\0003_standardpage_homepage_body_homepage_intro.py
    + Create model StandardPage
    + Add field body to homepage
    + Add field intro to homepage
```

```bash
python manage.py migrate
```

```
Running migrations:
  Applying home.0003_standardpage_homepage_body_homepage_intro... OK
```

The migration's name and the timestamp inside it will differ slightly on your machine.
That's fine.

## 4. In the admin

```bash
python manage.py runserver
```

1. Go to http://127.0.0.1:8000/admin/ → **Pages** → **Home** → **Edit**.
   The new **Intro** and **Body** fields are there. Fill in Intro and **Publish**.
2. Back on Home, click **Add child page** → **Standard page**.
   Title: `About`, fill in Intro and Body, **Publish**.
3. Visit http://127.0.0.1:8000/about/

## 5. Look at the tree

```bash
python manage.py shell
```

```python
from wagtail.models import Page

for p in Page.objects.all().order_by("path"):
    print(repr(p.path).ljust(18), p.depth, p.url_path.ljust(16), p.title)
```

```
'0001'             1 /                Root
'00010001'         2 /home/           Home
'000100010001'     3 /home/about/     About
```

About sits at `000100010001` — exactly what the episode 2 animation predicted.

## 6. The `.specific` gotcha

Still in the shell:

```python
p = Page.objects.get(slug="about")
type(p)                  # <class 'wagtail.models.Page'>
hasattr(p, "intro")      # False

type(p.specific)         # <class 'home.models.StandardPage'>
p.specific.intro         # 'Who we are and how we work.'
```

`Page.objects` gives you the base `Page`. `.specific` gives you the real page type.

Exit with `exit()`.

## 7. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 3"
git tag ep03-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TemplateDoesNotExist: home/standard_page.html` | Template missing or misnamed | Step 2. The name must be `standard_page.html` — the model name, lowercased with an underscore |
| `/home/about/` gives a 404 | That's the `url_path`, not the public URL | The site root is Home, so the page is served at `/about/` |
| `AttributeError: 'Page' object has no attribute 'intro'` | You got the base `Page` from `Page.objects` | Use `.specific` — step 6 |
| New fields don't appear in the admin | Missing from `content_panels` | Every field you want editable needs a `FieldPanel` |
| `makemigrations` says "No changes detected" | The app isn't saved, or you're in the wrong folder | Save `models.py`; run from `site/`, next to `manage.py` |
