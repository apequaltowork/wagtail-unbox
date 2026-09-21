# Ep 9 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 8's end state

```bash
git checkout ep08-end
```

## 1. Turn on the settings app — `studio/settings/base.py`

```python
INSTALLED_APPS = [
    ...
    "wagtail.contrib.forms",
    "wagtail.contrib.settings",
    ...
]

TEMPLATES = [{
    ...
    "OPTIONS": {
        "context_processors": [
            ...
            "wagtail.contrib.settings.context_processors.settings",
        ],
    },
}]
```

## 2. A settings model — append to `home/models.py`

```python
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="cog")
class StudioSettings(BaseSiteSetting):
    studio_name = models.CharField(max_length=80, default="Studio")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True, max_length=300)
    linkedin_url = models.URLField("LinkedIn URL", blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True)

    panels = [
        FieldPanel("studio_name"),
        MultiFieldPanel([FieldPanel("email"), FieldPanel("phone"), FieldPanel("address")],
                        heading="Contact"),
        MultiFieldPanel([FieldPanel("linkedin_url"), FieldPanel("instagram_url")],
                        heading="Social"),
    ]

    class Meta:
        verbose_name = "Studio settings"
```

`default="Studio"` matters: the row is created automatically on the first request, with
these defaults.

## 3. New pages start in the menu

On `StandardPage` (in `home/models.py`) and `BlogIndexPage` (in `blog/models.py`):

```python
    show_in_menus_default = True
```

This only affects pages created from now on.

## 4. Migrate

```bash
python manage.py makemigrations home
python manage.py migrate
```

## 5. The menu tag — new package `home/templatetags/`

```bash
mkdir home/templatetags
```

Create an empty `home/templatetags/__init__.py`, then `home/templatetags/navigation_tags.py`:

```python
from django import template

from wagtail.models import Site

register = template.Library()


@register.inclusion_tag("home/includes/main_menu.html", takes_context=True)
def main_menu(context):
    request = context["request"]
    site = Site.find_for_request(request)
    current = context.get("page")

    items = []
    if site:
        for item in site.root_page.get_children().live().in_menu():
            active = bool(current) and current.url_path.startswith(item.url_path)
            items.append({"page": item, "active": active})
    return {"items": items, "request": request}
```

`home/templates/home/includes/main_menu.html`:

```django
{% load wagtailcore_tags %}
{% if items %}
    <nav class="main-menu" aria-label="Main">
        <ul>
            {% for item in items %}
                <li>
                    <a href="{% pageurl item.page %}"{% if item.active %} aria-current="page"{% endif %}>{{ item.page.title }}</a>
                </li>
            {% endfor %}
        </ul>
    </nav>
{% endif %}
```

**Restart `runserver` now.** A new template tag module isn't picked up by the autoreloader.

## 6. `studio/templates/base.html`

```django
{% load static wagtailcore_tags wagtailuserbar navigation_tags %}
...
<header class="site-header">
    <div class="wrap">
        <a class="brand" href="{% slugurl 'home' %}">{{ settings.home.StudioSettings.studio_name }}</a>
        {% main_menu %}
    </div>
</header>
...
<footer class="site-footer">
    <div class="wrap">
        {% with s=settings.home.StudioSettings %}
            <div class="footer-grid">
                <p>&copy; {% now "Y" %} {{ s.studio_name }}. Built with Wagtail.</p>
                {% if s.email or s.phone %}
                    <p>
                        {% if s.email %}<a href="mailto:{{ s.email }}">{{ s.email }}</a>{% endif %}
                        {% if s.email and s.phone %}<br>{% endif %}
                        {% if s.phone %}<a href="tel:{{ s.phone|cut:' ' }}">{{ s.phone }}</a>{% endif %}
                    </p>
                {% endif %}
                {% if s.address %}<p>{{ s.address|linebreaksbr }}</p>{% endif %}
                ...
            </div>
        {% endwith %}
    </div>
</footer>
```

CSS for the menu and footer grid is in `studio/static/css/studio.css`:
https://github.com/apequaltowork/wagtail-unbox/blob/main/site/studio/static/css/studio.css

## 7. In the admin

- **Pages → About → Promote → Show in menus** — tick, publish. Same for Journal.
- **Settings → Studio settings** — fill in the email, phone and address.

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 9"
git tag ep09-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `'navigation_tags' is not a registered tag library` | Dev server started before the module existed | Restart `runserver` |
| Same error after restarting | Missing `__init__.py`, or the app isn't installed | `home/templatetags/__init__.py` |
| Menu renders nothing | No page has "Show in menus" ticked | Promote tab → Show in menus |
| New pages still not in the menu | `show_in_menus_default` only affects new pages of that type | Tick existing pages by hand |
| `settings` is empty in templates | Context processor missing | Step 1 |
| `{{ settings.StudioSettings.email }}` is blank | Missing app label | `settings.home.StudioSettings.email` |
| Phone link doesn't dial | Spaces in the `tel:` href | `{{ s.phone|cut:' ' }}` |
| Journal isn't highlighted on a post | Comparing `url`s or ids instead of `url_path` prefixes | `current.url_path.startswith(item.url_path)` |
