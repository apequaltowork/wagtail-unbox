from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

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

    content_panels = Page.content_panels + HeroMixin.hero_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    # The homepage sits directly under the root, and there is only one of it.
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["home.StandardPage", "blog.BlogIndexPage"]
    max_count = 1


class StandardPage(HeroMixin, Page):
    """A plain content page: About, Services, anything that is mostly words."""

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text="One or two sentences shown under the page title.",
    )
    body = StreamField(BodyBlock(), blank=True)

    content_panels = Page.content_panels + HeroMixin.hero_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = ["home.StandardPage"]


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
