# Ep 4 — Commands

Mostly editing files rather than running commands. Everything below was run and checked
on the recording machine.

## Start from episode 3's end state

```bash
git checkout ep03-end
```

```powershell
.venv\Scripts\activate          # Windows
cd site
python manage.py runserver
```

## 1. Delete the welcome page

```bash
rm home/templates/home/welcome_page.html
rm home/static/css/welcome_page.css
```

PowerShell:
```powershell
Remove-Item home\templates\home\welcome_page.html
Remove-Item home\static\css\welcome_page.css
```

The `home/static/` folder is now empty and can go too. Nothing else references either file
once step 3 is done.

## 2. A real `base.html`

`studio/templates/base.html` — keep everything Wagtail generated in `<head>`, and replace
the `<body>` with:

```django
<body class="{% block body_class %}{% endblock %}">
    {% wagtailuserbar %}

    <header class="site-header">
        <div class="wrap">
            <a class="brand" href="{% slugurl 'home' %}">Studio</a>
        </div>
    </header>

    <main class="wrap">
        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        <div class="wrap">
            <p>&copy; {% now "Y" %} Studio. Built with Wagtail.</p>
        </div>
    </footer>

    <script type="text/javascript" src="{% static 'js/studio.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
```

`{% slugurl 'home' %}` looks a page up by slug, so the link survives Home being renamed.

## 3. `home/templates/home/home_page.html`

Replace the whole file:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    {% if page.intro %}
        <p class="intro">{{ page.intro }}</p>
    {% endif %}

    {{ page.body|richtext }}

    {% if page.get_children.live %}
        <ul class="page-list">
            {% for child in page.get_children.live %}
                <li><a href="{% pageurl child %}">{{ child.title }}</a></li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock content %}
```

## 4. `home/templates/home/standard_page.html`

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-standardpage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    {% if page.intro %}
        <p class="intro">{{ page.intro }}</p>
    {% endif %}

    {{ page.body|richtext }}

    <p><a class="back" href="{% pageurl page.get_parent %}">&larr; {{ page.get_parent.title }}</a></p>
{% endblock content %}
```

## 5. The CSS

`studio/static/css/studio.css` is **0 bytes** out of the box — Wagtail wires up an empty
placeholder. Fill it in; the full file is in the repo:

https://github.com/apequaltowork/wagtail-unbox/blob/main/site/studio/static/css/studio.css

No build step, no framework. Plain CSS, served straight from `studio/static/`.

## 6. Look at it

- http://127.0.0.1:8000/ — the welcome egg is gone
- http://127.0.0.1:8000/about/ — and a back-link to Home

**If the page still looks unstyled, it's your browser cache**, not your code. `studio.css`
was 0 bytes when the page first loaded, and the browser kept that empty copy. Hard-reload:

| | |
|---|---|
| Windows / Linux | `Ctrl` + `F5`, or `Ctrl` + `Shift` + `R` |
| macOS | `Cmd` + `Shift` + `R` |

## 7. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 4"
git tag ep04-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Page renders but has no styling | Browser cached the empty `studio.css` | Hard-reload — step 6 |
| `TemplateSyntaxError: Invalid block tag 'pageurl'` | Missing load tag | `{% load wagtailcore_tags %}` at the top |
| `richtext` filter not found | Same | It also comes from `wagtailcore_tags` |
| CSS edits don't show up | Same cache | Hard-reload. Dev server picks up the file immediately |
| The 404 page still looks like Django's | `DEBUG = True` | Expected. `404.html` is only used when `DEBUG = False` — episode 13 |
| Child links missing on the homepage | Children are drafts | `get_children.live` only lists published pages |
