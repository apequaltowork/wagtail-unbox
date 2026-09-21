# Ep 7 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 6's end state

```bash
git checkout ep06-end
```

```powershell
.venv\Scripts\activate          # Windows
cd site
python manage.py runserver
```

## 1. A new app

```bash
python manage.py startapp blog
```

A Wagtail page app doesn't use Django's `admin.py` or `views.py`, so delete them:

```bash
rm blog/admin.py blog/views.py
```

PowerShell:
```powershell
Remove-Item blog\admin.py, blog\views.py
```

Register it in `studio/settings/base.py`:

```python
INSTALLED_APPS = [
    "home",
    "blog",
    ...
```

## 2. `blog/models.py`

```python
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from home.blocks import BodyBlock
from home.models import HeroMixin


class BlogIndexPage(Page):
    intro = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]
    max_count_per_parent = 1

    POSTS_PER_PAGE = 3

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = (
            BlogPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at")
        )
        paginator = Paginator(posts, self.POSTS_PER_PAGE)
        context["posts"] = paginator.get_page(request.GET.get("page"))
        return context


class BlogPage(HeroMixin, Page):
    date = models.DateField("Post date", default=timezone.localdate)
    intro = models.CharField(max_length=250)
    body = StreamField(BodyBlock(), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
    ] + HeroMixin.hero_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
```

Two things that are easy to get wrong:

- **`BlogPage.objects.child_of(self)`, not `self.get_children()`.** `get_children()` returns
  plain `Page` objects in tree order, and `order_by("-date")` on it raises
  `FieldError: Cannot resolve keyword 'date'`.
- **`paginator.get_page()`, not `paginator.page()`.** `page("abc")` raises
  `PageNotAnInteger`; `get_page("abc")` gives you page 1.

## 3. Lock down the home app too — `home/models.py`

Without this, an editor can create a second homepage inside the About page.

```python
class HomePage(HeroMixin, Page):
    ...
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["home.StandardPage", "blog.BlogIndexPage"]
    max_count = 1


class StandardPage(HeroMixin, Page):
    ...
    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = ["home.StandardPage"]
```

## 4. Migrate

```bash
python manage.py makemigrations blog
python manage.py migrate
```

```
Migrations for 'blog':
  blog\migrations\0001_initial.py
    + Create model BlogIndexPage
    + Create model BlogPage
```

The page-type rules from step 3 don't need a migration — they're Python only.

## 5. Templates

`blog/templates/blog/blog_index_page.html`:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-blogindexpage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    {% if page.intro %}
        <p class="intro">{{ page.intro }}</p>
    {% endif %}

    <ol class="post-list">
        {% for post in posts %}
            <li>
                <time datetime="{{ post.date|date:'Y-m-d' }}">{{ post.date|date:"j F Y" }}</time>
                <h2><a href="{% pageurl post %}">{{ post.title }}</a></h2>
                <p>{{ post.intro }}</p>
            </li>
        {% empty %}
            <li>No posts yet.</li>
        {% endfor %}
    </ol>

    {% if posts.paginator.num_pages > 1 %}
        <nav class="pagination" aria-label="Journal pages">
            <span class="prev">{% if posts.has_previous %}<a href="?page={{ posts.previous_page_number }}" rel="prev">&larr; Newer</a>{% endif %}</span>
            <span class="count">Page {{ posts.number }} of {{ posts.paginator.num_pages }}</span>
            <span class="next">{% if posts.has_next %}<a href="?page={{ posts.next_page_number }}" rel="next">Older &rarr;</a>{% endif %}</span>
        </nav>
    {% endif %}
{% endblock content %}
```

`blog/templates/blog/blog_page.html`:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-blogpage{% endblock %}

{% block content %}
    {% include "home/includes/hero.html" %}

    <p class="post-meta">
        <time datetime="{{ page.date|date:'Y-m-d' }}">{{ page.date|date:"j F Y" }}</time>
    </p>
    <h1>{{ page.title }}</h1>
    <p class="intro">{{ page.intro }}</p>

    {{ page.body }}

    <p><a class="back" href="{% pageurl page.get_parent %}">&larr; {{ page.get_parent.title }}</a></p>
{% endblock content %}
```

CSS for the post list and pagination is appended to `studio/static/css/studio.css`:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/studio/static/css/studio.css

## 6. Build the blog in the admin

http://127.0.0.1:8000/admin/ → Pages → Home → **Add child page** → Blog index page.
Title it "Journal". Then add a few Blog pages under it.

Try adding a Blog page under **About** — it isn't offered. That's step 3 working.

## 7. Check pagination

- http://127.0.0.1:8000/journal/
- http://127.0.0.1:8000/journal/?page=2
- http://127.0.0.1:8000/journal/?page=abc — page 1, not an error
- http://127.0.0.1:8000/journal/?page=999 — the last page, not an error

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 7"
git tag ep07-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FieldError: Cannot resolve keyword 'date' into field` | Ordering `get_children()`, which is a `Page` queryset | `BlogPage.objects.child_of(self)` |
| Posts come out oldest first | `get_children()` returns tree order | Same — query `BlogPage` and `order_by("-date")` |
| `?page=abc` gives a 404 or 500 | `paginator.page()` | `paginator.get_page()` |
| "Blog page" isn't offered under Journal | `subpage_types` misspelled | It's `"app_label.ModelName"` — `"blog.BlogPage"` |
| Can still add a homepage inside About | Home app types unrestricted | Step 3 |
| `makemigrations` says "No changes" after adding page-type rules | Expected | They're not stored in the database |
| `TemplateDoesNotExist: blog/blog_index_page.html` | Template in the wrong folder | `blog/templates/blog/…` — the app name twice |
| Post shows a hero error | `HeroMixin` not imported | `from home.models import HeroMixin` |
