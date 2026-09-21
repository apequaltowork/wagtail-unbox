from django import forms
from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from home.blocks import BodyBlock


class HeroMixin(models.Model):
    """A hero image and its caption, shared by every page type that has one.

    The ForeignKey is written the way Wagtail's own docs write it, and every
    part of it matters:

      null=True, blank=True  - a page without a hero is normal, not an error
      on_delete=SET_NULL     - deleting an image must never delete pages
      related_name="+"       - we never ask an image for its pages, so don't
                               pay for the reverse accessor
    """

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Shown full width above the page title. Landscape works best.",
    )
    hero_alt = models.CharField(
        max_length=180,
        blank=True,
        verbose_name="Hero alt text",
        help_text="What the image shows, for screen readers. Leave blank only "
                  "if the image is purely decorative.",
    )
    hero_caption = models.CharField(max_length=180, blank=True)

    hero_panels = [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_alt"),
                FieldPanel("hero_caption"),
            ],
            heading="Hero",
        )
    ]

    class Meta:
        abstract = True


class HomePage(HeroMixin, Page):
    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text="One or two sentences shown under the page title.",
    )
    body = StreamField(BodyBlock(), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + HeroMixin.hero_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    # The homepage sits directly under the root, and there is only one of it.
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["home.StandardPage", "blog.BlogIndexPage", "home.ContactPage"]
    max_count = 1


class StandardPage(HeroMixin, Page):
    """A plain content page: About, Services, anything that is mostly words."""

    page_description = "A general page: About, Services -- anything that is mostly words."

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text="One or two sentences shown under the page title.",
    )
    body = StreamField(BodyBlock(), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + HeroMixin.hero_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = ["home.StandardPage"]

    # New pages of this type start with "Show in menus" ticked. Pages that
    # already exist keep whatever they have -- this is only a default.
    show_in_menus_default = True


# ---------------------------------------------------------------- snippets
# Snippets are content that is not a page: it has no URL and no place in the
# tree. Written once in the admin, used on as many pages as you like.
# They are registered with the admin in home/wagtail_hooks.py.


class TeamMember(Orderable):
    """One person at the studio. Orderable gives the admin drag-and-drop order."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    bio = models.TextField(blank=True, max_length=400)

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("photo"),
        FieldPanel("bio"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "team member"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Something a client said. Chosen per page, so each page picks its own."""

    quote = models.TextField(max_length=400)
    author = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True)

    panels = [
        FieldPanel("quote"),
        FieldPanel("author"),
        FieldPanel("company"),
    ]

    def __str__(self):
        return f"{self.author}: {self.quote[:40]}"


# ---------------------------------------------------------------- settings


@register_setting(icon="cog")
class StudioSettings(BaseSiteSetting):
    """Studio-wide details the client edits once: Settings -> Studio settings.

    BaseSiteSetting, not BaseGenericSetting: one row per Site, so a second
    site on the same install can have its own phone number.
    """

    studio_name = models.CharField(max_length=80, default="Studio")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True, max_length=300)
    linkedin_url = models.URLField("LinkedIn URL", blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True)

    panels = [
        FieldPanel("studio_name"),
        MultiFieldPanel(
            [FieldPanel("email"), FieldPanel("phone"), FieldPanel("address")],
            heading="Contact",
        ),
        MultiFieldPanel(
            [FieldPanel("linkedin_url"), FieldPanel("instagram_url")],
            heading="Social",
        ),
    ]

    class Meta:
        verbose_name = "Studio settings"


# ---------------------------------------------------------------- contact form


class FormField(AbstractFormField):
    """One field on the contact form, defined by the editor in the admin."""

    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class StudioFormBuilder(FormBuilder):
    """Give optional dropdowns a blank first choice.

    Wagtail builds a dropdown from the editor's choices and nothing else, so an
    optional one has no empty option. The browser submits whatever is showing
    -- the first choice -- and every enquiry quietly says "Under 5k".
    """

    def create_dropdown_field(self, field, options):
        form_field = super().create_dropdown_field(field, options)
        if not field.required:
            form_field.choices = [("", "Choose one (optional)")] + list(form_field.choices)
        return form_field


class ContactPage(AbstractEmailForm):
    """A form the editor builds field by field. Each submission is stored, and
    emailed to `to_address` if one is set.

    Two changes from the stock form page:

    * A honeypot field. Bots fill in every input; people never see this one.
      A filled honeypot gets the normal thank-you page, but nothing is stored
      and nothing is emailed -- telling a bot it failed only teaches it.
    * Post/Redirect/Get. Wagtail renders the thank-you page as the response
      to the POST, so refreshing it resubmits the form. We redirect instead.
    """

    HONEYPOT = "website"
    form_builder = StudioFormBuilder
    page_description = "The contact form. Only one is allowed, directly under the homepage."

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
            return None
        return super().process_form_submission(form)

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
        # The stock "Landing page" preview calls render_landing_page -- which
        # we turned into a redirect to the *live* page, so an editor previewing
        # a new thank-you message would see the published one. Render the draft.
        if mode_name == "landing":
            return self.landing_response(request)
        return super().serve_preview(request, mode_name)
