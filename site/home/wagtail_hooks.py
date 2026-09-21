"""Admin registration for the studio's snippets.

A SnippetViewSet is the Wagtail 7 way to register a snippet: it controls the
listing, search and menu entry in one place. Grouping them puts "Team" and
"Testimonials" under one "Studio" menu item instead of burying them in Snippets.
"""

from wagtail import hooks
from wagtail.admin.ui.components import Component
from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.utils import get_forms_for_user
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


# ---------------------------------------------------------------- dashboard


class RecentEnquiriesPanel(Component):
    """The five newest contact-form submissions, on the admin dashboard.

    Only for form pages the user may already see submissions for --
    get_forms_for_user applies the same page permissions as Forms in the menu,
    so the dashboard can't show enquiries to someone the Forms screen wouldn't.
    """

    name = "recent_enquiries"
    template_name = "home/admin/recent_enquiries.html"
    order = 50  # above Wagtail's own panels, which start at 100

    def __init__(self, request):
        self.request = request

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        forms = get_forms_for_user(self.request.user)
        context["submissions"] = (
            FormSubmission.objects.filter(page__in=forms)
            .select_related("page")
            .order_by("-submit_time")[:5]
        )
        return context


@hooks.register("construct_homepage_panels")
def add_recent_enquiries(request, panels):
    panels.append(RecentEnquiriesPanel(request))
