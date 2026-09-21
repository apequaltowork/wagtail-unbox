# Ep 8 — Commands

Everything below was run and checked on the recording machine.

## Start from episode 7's end state

```bash
git checkout ep07-end
```

## 1. Snippet models — append to `home/models.py`

```python
from wagtail.models import Orderable, Page


class TeamMember(Orderable):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    bio = models.TextField(blank=True, max_length=400)

    panels = [FieldPanel("name"), FieldPanel("role"), FieldPanel("photo"), FieldPanel("bio")]

    class Meta(Orderable.Meta):
        verbose_name = "team member"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    quote = models.TextField(max_length=400)
    author = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True)

    panels = [FieldPanel("quote"), FieldPanel("author"), FieldPanel("company")]

    def __str__(self):
        return f"{self.author}: {self.quote[:40]}"
```

Snippets use `panels`, not `content_panels` — they aren't pages.

## 2. Register them — new file `home/wagtail_hooks.py`

```python
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
```

## 3. Blocks — `home/blocks.py`

```python
from wagtail.snippets.blocks import SnippetChooserBlock


class TestimonialBlock(blocks.StructBlock):
    testimonial = SnippetChooserBlock("home.Testimonial")   # a string: avoids a circular import

    class Meta:
        icon = "openquote"
        label = "Testimonial"
        template = "home/blocks/testimonial_block.html"


class TeamBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=80, default="The team")

    def get_context(self, value, parent_context=None):
        from home.models import TeamMember      # inside the method: circular otherwise
        context = super().get_context(value, parent_context=parent_context)
        context["members"] = TeamMember.objects.select_related("photo")
        return context

    class Meta:
        icon = "group"
        label = "Team"
        template = "home/blocks/team_block.html"
```

Add both to `BodyBlock`, and cap the team at one per page:

```python
    testimonial = TestimonialBlock()
    team = TeamBlock()
    ...
    class Meta:
        block_counts = {"services": {"max_num": 1}, "team": {"max_num": 1}}
```

`home/templates/home/blocks/testimonial_block.html` — note the guard:

```django
{% with t=value.testimonial %}
    {% if t %}
        <blockquote>
            <p>{{ t.quote }}</p>
            <cite>{{ t.author }}{% if t.company %}, {{ t.company }}{% endif %}</cite>
        </blockquote>
    {% endif %}
{% endwith %}
```

`home/templates/home/blocks/team_block.html`:

```django
{% load wagtailimages_tags %}
<h2>{{ value.heading }}</h2>
<ul class="team-grid">
    {% for member in members %}
        <li>
            {% if member.photo %}{% image member.photo fill-240x240 alt="" %}{% endif %}
            <h3>{{ member.name }}</h3>
            <p class="role">{{ member.role }}</p>
            {% if member.bio %}<p>{{ member.bio }}</p>{% endif %}
        </li>
    {% endfor %}
</ul>
```

The photo's `alt=""` is deliberate: the name is right underneath it, so the image is
decorative.

## 4. Tags — `blog/models.py`

```python
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogPage(HeroMixin, Page):
    ...
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("tags"),
    ] + ...
```

And filter in `BlogIndexPage.get_context`, **passing the tag back to the template**:

```python
        tag = request.GET.get("tag")
        if tag:
            posts = posts.filter(tags__slug=tag)
        context["tag"] = tag
```

## 5. Migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Carry the tag through pagination — `blog_index_page.html`

Episode 7's links were `?page=N`, which throws the tag away. Build both parameters:

```django
<a href="?{% if tag %}tag={{ tag|urlencode }}&amp;{% endif %}page={{ posts.next_page_number }}" rel="next">Older &rarr;</a>
```

(same for the previous link), and show the filter and each post's tags:

```django
{% if tag %}
    <p class="filter">Posts tagged <strong>{{ tag }}</strong> · <a href="{% pageurl page %}">show all</a></p>
{% endif %}
...
{% for t in post.tags.all %}
    <li><a href="{% pageurl page %}?tag={{ t.slug }}">{{ t.name }}</a></li>
{% endfor %}
```

## 7. In the admin

- **Studio → Team** — add people; drag rows to reorder.
- **Studio → Testimonials** — add a couple.
- About → add a **Team** block. Home → add a **Testimonial** block and choose one.
- Journal posts → add tags.

## 8. Commit and tag

```bash
cd ..
git add -A
git commit -m "episode 8"
git tag ep08-end
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ImportError` / circular import on startup | `blocks.py` imports `home.models` at the top | Use `"home.Testimonial"` as a string; import inside `get_context` |
| Page 2 of a tag filter shows every post | Pagination link is `?page=N` | `?tag=…&page=N` — step 6 |
| Empty quote box on a page | Its testimonial was deleted; the block value is `None` | `{% if t %}` guard |
| Snippet doesn't appear in the admin | `wagtail_hooks.py` not in an installed app, or `register_snippet` missing | It lives in `home/`, which is installed |
| Tags don't save on a draft | `ForeignKey` instead of `ParentalKey` on the through model | `ParentalKey` |
| Every tag pill has a border | `.post-list li` matches nested lists | `.post-list > li` |
| No drag handles in the Team listing | Model isn't `Orderable` | `class TeamMember(Orderable)` |
