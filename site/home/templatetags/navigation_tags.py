"""The site menu, built from the page tree.

    {% load navigation_tags %}
    {% main_menu %}

The menu is the live, in-menu children of the site's root page -- so an editor
adds a page to the menu by ticking "Show in menus" on its Promote tab. No menu
model, no hard-coded links.
"""

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
            # A post at /home/journal/some-post/ keeps "Journal" highlighted.
            # url_path always ends in "/", so /home/about/ can't match
            # /home/about-us/ by accident.
            active = bool(current) and current.url_path.startswith(item.url_path)
            items.append({"page": item, "active": active})
    return {"items": items, "request": request}
