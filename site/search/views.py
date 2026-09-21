from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page

RESULTS_PER_PAGE = 10


def search(request):
    """Site search.

    Three changes from the view `wagtail start` generates:

    * .public() -- without it, the titles of password-protected and
      login-only pages show up in results for anyone.
    * .specific() -- results come back as plain Page objects otherwise, and
      only Page's fields (title, search_description) are available to show.
    * paginator.get_page() -- same reason as the journal in episode 7.
    """
    search_query = request.GET.get("query", "").strip()

    if search_query:
        search_results = Page.objects.live().public().specific().search(search_query)
    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, RESULTS_PER_PAGE)
    results_page = paginator.get_page(request.GET.get("page"))

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": results_page,
            "result_count": paginator.count,
        },
    )
