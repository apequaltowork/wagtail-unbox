from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

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
