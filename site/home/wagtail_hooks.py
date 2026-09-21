"""Admin registration for the studio's snippets.

A SnippetViewSet is the Wagtail 7 way to register a snippet: it controls the
listing, search and menu entry in one place. Grouping them puts "Team" and
"Testimonials" under one "Studio" menu item instead of burying them in Snippets.
"""

from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from home.models import TeamMember, Testimonial


class TeamMemberViewSet(SnippetViewSet):
    model = TeamMember
    icon = "user"
    menu_label = "Team"
    list_display = ["name", "role"]
    search_fields = ["name", "role"]


class TestimonialViewSet(SnippetViewSet):
    model = Testimonial
    icon = "openquote"
    menu_label = "Testimonials"
    list_display = ["author", "company"]
    search_fields = ["quote", "author", "company"]


class StudioGroup(SnippetViewSetGroup):
    items = (TeamMemberViewSet, TestimonialViewSet)
    menu_icon = "group"
    menu_label = "Studio"
    menu_name = "studio"


register_snippet(StudioGroup)
