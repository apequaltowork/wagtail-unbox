# Ep 10 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 9's end state

```bash
git checkout ep09-end
```

`wagtail.contrib.forms` is already in `INSTALLED_APPS` — it has been since `wagtail start`.

## 1. The form page — append to `home/models.py`

```python
from django import forms
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField


class FormField(AbstractFormField):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class StudioFormBuilder(FormBuilder):
    """Optional dropdowns get a blank first choice."""

    def create_dropdown_field(self, field, options):
        form_field = super().create_dropdown_field(field, options)
        if not field.required:
            form_field.choices = [("", "Choose one (optional)")] + list(form_field.choices)
        return form_field


class ContactPage(AbstractEmailForm):
    HONEYPOT = "website"
    form_builder = StudioFormBuilder

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
                FieldPanel("subject"),
            ],
            heading="Email",
        ),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1
    show_in_menus_default = True

    # --- honeypot: bots fill every input; people never see this one
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields[self.HONEYPOT] = forms.CharField(
            required=False,
            label="Leave this field empty",
            widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
        )
        return form

    def process_form_submission(self, form):
        if form.cleaned_data.pop(self.HONEYPOT, ""):
            return None                      # a bot: store nothing, send nothing
        return super().process_form_submission(form)

    # --- Post/Redirect/Get: refreshing the thank-you page must not resubmit
    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        return redirect(self.url + "?sent=1")

    def serve(self, request, *args, **kwargs):
        if request.method == "GET" and request.GET.get("sent"):
            return TemplateResponse(
                request, self.get_landing_page_template(request), self.get_context(request)
            )
        return super().serve(request, *args, **kwargs)
```

And let the homepage accept it:

```python
class HomePage(HeroMixin, Page):
    ...
    subpage_types = ["home.StandardPage", "blog.BlogIndexPage", "home.ContactPage"]
```

## 2. Migrate

```bash
python manage.py makemigrations home
python manage.py migrate
```

## 3. The form template — `home/templates/home/contact_page.html`

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
    <h1>{{ page.title }}</h1>
    {{ page.intro|richtext }}

    <form class="contact-form" action="{% pageurl page %}" method="post" novalidate>
        {% csrf_token %}
        {% for field in form %}
            {% if field.name == page.HONEYPOT %}
                <div class="hp" aria-hidden="true">{{ field.label_tag }} {{ field }}</div>
            {% else %}
                <div class="field{% if field.errors %} has-error{% endif %}">
                    {{ field.label_tag }}
                    {{ field }}
                    {% if field.help_text %}<p class="help">{{ field.help_text }}</p>{% endif %}
                    {% for error in field.errors %}<p class="error">{{ error }}</p>{% endfor %}
                </div>
            {% endif %}
        {% endfor %}
        <button type="submit" class="button button--solid">Send</button>
    </form>
{% endblock content %}
```

## 4. The thank-you template — `home/templates/home/contact_page_landing.html`

**Write this before anyone submits the form.** Without it, the POST returns a 500 *after*
saving the submission and sending the email.

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
    <h1>Message sent</h1>
    {{ page.thank_you_text|richtext }}
    <p><a class="back" href="{% slugurl 'home' %}">&larr; Back to the homepage</a></p>
{% endblock content %}
```

The name is the page template's name plus `_landing`, in the same folder.

## 5. CSS

The honeypot must be off-screen, not `display: none` and not `type="hidden"`:

```css
.hp { position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden; }
```

The rest of the form styling is in `studio/static/css/studio.css`.

## 6. Build it in the admin

Home → Add child page → **Contact page**. Add fields:

| Label | Type | Required |
|---|---|---|
| Your name | Single line text | ✓ |
| Email | Email | ✓ |
| Budget | Drop down — choices one per line | |
| About the project | Multi-line text | ✓ |

Fill in **To address** and **Subject** under Email, and publish.

## 7. Try it

Submit the form. In development the email prints in the `runserver` terminal —
`dev.py` sets `EMAIL_BACKEND` to the console backend.

Then: refresh the thank-you page. Admin → Forms → Contact — still one submission.

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 10"
git tag ep10-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 500 `TemplateDoesNotExist: …_landing.html` after submitting | No landing template — but it **was** saved and emailed | Step 4 |
| Refreshing the thank-you page creates another submission | Stock form renders the landing page as the POST response | `render_landing_page` → redirect |
| Every submission has the same budget | Optional dropdown has no blank choice | `StudioFormBuilder` |
| 403 Forbidden on submit | `{% csrf_token %}` missing | Put it inside the `<form>` |
| No email arrives in development | Console backend | Look in the `runserver` output |
| No email at all, even in the console | `to_address` blank | Fill in To address on the page |
| Honeypot visible on the page | Its CSS didn't load | Hard-reload; check `.hp` exists |
| "Contact page" not offered under Home | Not in `HomePage.subpage_types` | Step 1 |
