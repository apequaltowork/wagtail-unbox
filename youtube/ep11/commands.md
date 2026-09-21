# Ep 11 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 10's end state

```bash
git checkout ep10-end
```

The `search/` app, its URL and the database search backend have been there since
`wagtail start`. Try it: http://127.0.0.1:8000/search/?query=pricing

## 1. Tell Wagtail what to index

`blog/models.py`:

```python
from wagtail.search import index


class BlogPage(HeroMixin, Page):
    ...
    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.FilterField("date"),
    ]
```

`home/models.py`, on both `HomePage` and `StandardPage`:

```python
from wagtail.search import index

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]
```

No migration needed — `makemigrations` reports **No changes detected**.

## 2. Rebuild the index

Adding `search_fields` doesn't reindex pages that already exist:

```bash
python manage.py update_index
```

```
default: indexed 19 objects
```

From now on, saving or publishing a page updates its entry automatically.

## 3. Index text that lives in snippets — `home/blocks.py`

```python
class TestimonialBlock(blocks.StructBlock):
    testimonial = SnippetChooserBlock("home.Testimonial")

    def get_searchable_content(self, value):
        t = value.get("testimonial")
        return [t.quote, t.author, t.company] if t else []
    ...


class TeamBlock(blocks.StructBlock):
    ...
    def get_searchable_content(self, value):
        from home.models import TeamMember

        content = [value.get("heading", "")]
        for m in TeamMember.objects.all():
            content += [m.name, m.role]
        return content
```

Then `python manage.py update_index` again. If the team changes later, re-save About (or run
`update_index`) to refresh its entry.

## 4. The view — replace `search/views.py`

```python
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page

RESULTS_PER_PAGE = 10


def search(request):
    search_query = request.GET.get("query", "").strip()

    if search_query:
        search_results = Page.objects.live().public().specific().search(search_query)
    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, RESULTS_PER_PAGE)
    results_page = paginator.get_page(request.GET.get("page"))

    return TemplateResponse(request, "search/search.html", {
        "search_query": search_query,
        "search_results": results_page,
        "result_count": paginator.count,
    })
```

- **`.public()`** — without it, password-protected and login-only pages appear in results.
- **`.specific()`** — so the template can show each result's `intro`.

## 5. The template — `search/templates/search/search.html`

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block title %}{% if search_query %}Search: {{ search_query }}{% else %}Search{% endif %}{% endblock %}

{% block content %}
    <h1>Search</h1>

    <form class="search-form" action="{% url 'search' %}" method="get" role="search">
        <label for="search-query" class="visually-hidden">Search the site</label>
        <input id="search-query" type="search" name="query" value="{{ search_query }}" placeholder="Search the site">
        <button type="submit" class="button button--solid">Search</button>
    </form>

    {% if search_query %}
        <p class="result-count">{{ result_count }} result{{ result_count|pluralize }} for <strong>{{ search_query }}</strong></p>
        {% if search_results %}
            <ol class="post-list">
                {% for result in search_results %}
                    <li>
                        <p class="result-kind">{{ result.specific_class.get_verbose_name }}</p>
                        <h2><a href="{% pageurl result %}">{{ result.title }}</a></h2>
                        {% if result.intro %}<p>{{ result.intro|striptags|truncatewords:30 }}</p>{% endif %}
                    </li>
                {% endfor %}
            </ol>
            {# pagination: carry ?query= in every link #}
        {% endif %}
    {% endif %}
{% endblock %}
```

Full file, with pagination:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/search/templates/search/search.html

## 6. Search in the menu — `home/templates/home/includes/main_menu.html`

After the loop, inside the `<ul>`:

```django
<li><a href="{% url 'search' %}"{% if request.resolver_match.url_name == 'search' %} aria-current="page"{% endif %}>Search</a></li>
```

## 7. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 11"
git tag ep11-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Only titles match | `search_fields` not extended | Step 1 |
| Added `search_fields`, still no results | Existing pages not reindexed | `python manage.py update_index` |
| Text visible on the page isn't found | It comes from a snippet or chooser, not the page | `get_searchable_content` on the block — step 3 |
| Search finds old team names | Copied-in snippet text is stale | Re-save the page, or `update_index` |
| Private pages appear in results | View uses `.live()` only | `.live().public()` |
| Results show only titles | Plain `Page` objects | `.specific()` |
| Page 2 of results is a different search | Pagination link drops `query` | `?query={{ search_query|urlencode }}&page=…` |
| `update_index` is slow on a big site | It rebuilds everything | It's a deploy-time command, not a per-request one |
