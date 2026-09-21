from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from home.blocks import BodyBlock
from home.models import HeroMixin


class BlogIndexPage(Page):
    """The /blog/ page: lists its posts, newest first, a few at a time."""

    intro = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    # Where this page may live, and what may live under it.
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]
    max_count_per_parent = 1

    POSTS_PER_PAGE = 3

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # BlogPage.objects, not self.get_children(): get_children() returns plain
        # Page objects, and Page has no `date` field to order by.
        posts = (
            BlogPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at")
        )

        # get_page(), not page(): it turns ?page=abc and ?page=999 into a
        # sensible page instead of raising a 404.
        paginator = Paginator(posts, self.POSTS_PER_PAGE)
        context["posts"] = paginator.get_page(request.GET.get("page"))
        return context


class BlogPage(HeroMixin, Page):
    """One post."""

    date = models.DateField("Post date", default=timezone.localdate)
    intro = models.CharField(
        max_length=250,
        help_text="One or two sentences. Shown on the blog index and under the title.",
    )
    body = StreamField(BodyBlock(), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
    ] + HeroMixin.hero_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
