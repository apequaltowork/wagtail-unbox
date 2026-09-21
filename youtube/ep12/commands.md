# Ep 12 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 11's end state

```bash
git checkout ep11-end
```

## 1. Look at the admin as the client

Admin → **Settings → Users → Add a user**. Put them in the **Editors** group only. Log in as
them in a private window. Try **Studio → Team**, and **Settings**: neither is there.

## 2. Grant the Editors group what the client edits — a data migration

```bash
python manage.py makemigrations home --empty -n editors_can_edit_studio_content
```

Replace the generated file's contents with:

```python
from django.contrib.auth.management import create_permissions
from django.db import migrations

GRANTS = [
    "add_teammember", "change_teammember", "delete_teammember",
    "add_testimonial", "change_testimonial", "delete_testimonial",
    "change_studiosettings",
]


def grant(apps, schema_editor):
    # Permissions are normally created AFTER all migrations (post_migrate).
    # On a fresh database they don't exist yet -- create them now.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    editors = Group.objects.filter(name="Editors").first()
    if editors is None:
        return
    editors.permissions.add(
        *Permission.objects.filter(content_type__app_label="home", codename__in=GRANTS)
    )


def revoke(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    editors = Group.objects.filter(name="Editors").first()
    if editors:
        editors.permissions.remove(
            *Permission.objects.filter(content_type__app_label="home", codename__in=GRANTS)
        )


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_contactpage_formfield"),
        ("wagtailcore", "0002_initial_data"),      # creates the Editors group
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [migrations.RunPython(grant, revoke)]
```

```bash
python manage.py migrate
```

**Test it on a fresh database**, because that's the case that breaks. Point a copy of the
settings at a new SQLite file, run `migrate`, and check the group:

```python
from django.contrib.auth.models import Group
sorted(p.codename for p in Group.objects.get(name="Editors").permissions.all())
```

## 3. Fix the landing-page preview — `home/models.py`, in `ContactPage`

```python
    def landing_response(self, request):
        return TemplateResponse(
            request, self.get_landing_page_template(request), self.get_context(request)
        )

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        return redirect(self.url + "?sent=1")

    def serve(self, request, *args, **kwargs):
        if request.method == "GET" and request.GET.get("sent"):
            return self.landing_response(request)
        return super().serve(request, *args, **kwargs)

    def serve_preview(self, request, mode_name):
        if mode_name == "landing":
            return self.landing_response(request)      # the draft, not the live page
        return super().serve_preview(request, mode_name)
```

## 4. A dashboard panel — append to `home/wagtail_hooks.py`

```python
from wagtail import hooks
from wagtail.admin.ui.components import Component
from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.utils import get_forms_for_user


class RecentEnquiriesPanel(Component):
    name = "recent_enquiries"
    template_name = "home/admin/recent_enquiries.html"
    order = 50

    def __init__(self, request):
        self.request = request

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        forms = get_forms_for_user(self.request.user)          # same rule as Forms
        context["submissions"] = (
            FormSubmission.objects.filter(page__in=forms)
            .select_related("page")
            .order_by("-submit_time")[:5]
        )
        return context


@hooks.register("construct_homepage_panels")
def add_recent_enquiries(request, panels):
    panels.append(RecentEnquiriesPanel(request))
```

`home/templates/home/admin/recent_enquiries.html`:

```django
{% load wagtailadmin_tags %}
{% if submissions %}
    {% panel id="recent-enquiries" heading="Recent enquiries" classname="w-panel--dashboard" %}
        <table class="listing listing--dashboard">
            <tbody>
                {% for s in submissions %}
                    <tr>
                        <td class="title"><a href="{% url 'wagtailforms:list_submissions' s.page_id %}">{{ s.form_data.your_name|default:"(no name)" }}</a></td>
                        <td>{{ s.form_data.about_the_project|truncatechars:70 }}</td>
                        <td>{% timesince_last_update s.submit_time %}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endpanel %}
{% endif %}
```

`your_name` and `about_the_project` are the `clean_name`s of the fields built in episode 10.

## 5. page_description — on each page type

```python
class StandardPage(HeroMixin, Page):
    page_description = "A general page: About, Services -- anything that is mostly words."
```

and similarly on `BlogIndexPage`, `BlogPage` and `ContactPage`. Shown when an editor chooses
between page types.

## 6. The admin's name — `studio/settings/base.py`

```python
WAGTAIL_SITE_NAME = "Studio"
```

## 7. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 12"
git tag ep12-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Editors don't see Studio or Settings | Default Editors group has no snippet or settings permissions | Step 2 |
| Permissions migration "OK" but group has nothing (fresh DB only) | Permissions don't exist until `post_migrate` | `create_permissions` first |
| `Group matching query does not exist` in the migration | Missing dependency on `wagtailcore 0002_initial_data` | Add it |
| Landing-page preview shows old text | `render_landing_page` redirects to the live page | `serve_preview` — step 3 |
| Dashboard panel doesn't appear | Hook name | `construct_homepage_panels` |
| Dashboard shows enquiries to the wrong people | Querying every `FormSubmission` | `get_forms_for_user(request.user)` |
| No "choose page type" screen | Only one type allowed there | Expected — Wagtail skips it |
