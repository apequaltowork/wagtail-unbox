"""Ep 8 — Snippets & Reusable Content.

Scene spec for video/build.py.

The pagination-forgets-the-filter output and the deleted-snippet results are
from real runs (the delete ran inside a rolled-back transaction). See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 08'
VENV = "(.venv) PS&gt;"
PY = "&gt;&gt;&gt;"

SHOT_TEAM = (HERE / "assets" / "shot-team.png").as_uri()
SHOT_TESTIMONIAL = (HERE / "assets" / "shot-testimonial.png").as_uri()
SHOT_TAG = (HERE / "assets" / "shot-tag.png").as_uri()

SHOT_CSS = """
<style>
.shot { border: 2px solid var(--line); border-radius: 14px; overflow: hidden;
        box-shadow: 0 30px 70px rgba(0,0,0,.45); margin: 0 auto; }
.shot img { display: block; width: 100%; }
.shotbar { background: #161925; padding: 14px 22px; font-family: var(--mono);
           font-size: 24px; color: var(--muted); border-bottom: 2px solid var(--line); }
</style>
"""


def shot(url_label: str, src: str, width: str) -> str:
    return (SHOT_CSS +
            f'<div class="shot" style="width:{width}"><div class="shotbar">{url_label}</div>'
            f'<img src="{src}" alt=""></div>')


EPISODE = Episode(
    key="ep08",
    number="08",
    title="Ep 8 - Snippets & Reusable Content",
    badge=BADGE,
    intro_say="Snippets, and reusable content.",
    outro_say="Next episode, navigation and site settings. Thanks for watching.",
    scenes=[
        Scene(
            id="not_a_page",
            body="""
            <div class="eyebrow">Content that isn't a page</div>
            <h2>No URL. No place in the tree.</h2>
            <div class="sub" style="margin-top:36px">A team member. A testimonial. They belong on
            pages &mdash; often on several &mdash; but they aren't pages themselves.<br><br>
            That is a <b>snippet</b>: a plain Django model that the admin can edit.</div>
            """,
            say="A team member does not have a U R L. A testimonial does not have a place in the "
                "page tree. But both belong on pages, and usually on more than one page. That is "
                "what a snippet is. A plain Django model, that editors can manage in the admin.",
        ),
        Scene(
            id="models",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> TeamMember(<span class="k">Orderable</span>):
    name = models.CharField(max_length=<span class="s">120</span>)
    role = models.CharField(max_length=<span class="s">120</span>)
    photo = models.ForeignKey(<span class="s">"wagtailimages.Image"</span>, &hellip;)
    bio = models.TextField(blank=<span class="s">True</span>)

<span class="k">class</span> Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=<span class="s">120</span>)
    company = models.CharField(max_length=<span class="s">120</span>, blank=<span class="s">True</span>)</pre>
            <div class="sub" style="margin-top:28px"><b>Orderable</b> adds a sort order &mdash; and
            with it, drag-and-drop in the admin.</div>
            """,
            say="Two models. A team member, and a testimonial. Neither one inherits from Page. The "
                "team member inherits from Orderable, which adds a sort order column, and that alone "
                "gives the admin drag and drop reordering.",
        ),
        Scene(
            id="viewset",
            body="""
            <div class="filename">home/wagtail_hooks.py</div>
            <pre class="code" style="font-size:27px"><span class="k">class</span> TeamMemberViewSet(SnippetViewSet):
    model = TeamMember
    icon = <span class="s">"user"</span>
    menu_label = <span class="s">"Team"</span>
    list_display = [<span class="s">"name"</span>, <span class="s">"role"</span>]
    search_fields = [<span class="s">"name"</span>, <span class="s">"role"</span>]

<span class="k">class</span> StudioGroup(SnippetViewSetGroup):
    items = (TeamMemberViewSet, TestimonialViewSet)
    menu_label = <span class="s">"Studio"</span>

register_snippet(StudioGroup)</pre>
            """,
            say="And you register them with a snippet view set, which is the Wagtail seven way. One "
                "class per model sets the icon, the menu label, the listing columns and what is "
                "searchable. A view set group puts both of them under a single Studio item in the "
                "admin menu, instead of burying them in a generic snippets list.",
        ),
        Scene(
            id="two_ways",
            body="""
            <h2>Two ways to put a snippet on a page</h2>
            <table>
              <tr><td class="k">Chosen per page</td><td class="v">TestimonialBlock &rarr; <b>SnippetChooserBlock</b></td></tr>
              <tr><td class="k">Fetched by the block</td><td class="v">TeamBlock &rarr; <b>get_context</b> loads everyone</td></tr>
            </table>
            <div class="sub" style="margin-top:36px">Add a person to the team and every page showing
            the team updates. Nobody re-edits a page.</div>
            """,
            say="There are two ways to put a snippet on a page. Either the editor chooses one, which "
                "is what the testimonial block does with a snippet chooser. Or the block fetches "
                "them itself. The team block has nothing to choose. It loads every team member, so "
                "when somebody joins the studio, every page showing the team updates on its own.",
        ),
        Scene(
            id="team_block",
            body="""
            <div class="filename">home/blocks.py</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> TeamBlock(blocks.StructBlock):
    heading = blocks.CharBlock(default=<span class="s">"The team"</span>)

    <span class="k">def</span> get_context(self, value, parent_context=<span class="s">None</span>):
        <span class="k">from</span> home.models <span class="k">import</span> TeamMember   <span class="c"># not at the top</span>
        context = <span class="k">super</span>().get_context(value, parent_context)
        context[<span class="s">"members"</span>] = TeamMember.objects.select_related(<span class="s">"photo"</span>)
        <span class="k">return</span> context</pre>
            <div class="sub" style="margin-top:28px">Blocks have <b>get_context</b> too &mdash; the
            same idea as a page's, from last episode.</div>
            """,
            say="Blocks have a get context method as well, exactly like pages did last episode. And "
                "notice the import is inside the method, not at the top of the file.",
        ),
        Scene(
            id="circular",
            body="""
            <div class="eyebrow">Why the import is inside the method</div>
            <h2>models.py imports blocks.py</h2>
            <pre class="code" style="font-size:30px"><span class="c"># models.py</span>   from home.blocks import BodyBlock
<span class="c"># blocks.py</span>   from home.models import TeamMember   <span class="bad">&larr; circular</span></pre>
            <div class="sub" style="margin-top:36px">So <b>SnippetChooserBlock("home.Testimonial")</b>
            names its model as a <b>string</b>, and TeamBlock imports late.</div>
            """,
            say="Because the models file imports the blocks file, to build the body field. If the "
                "blocks file imported the models file back, that is a circular import and Django will "
                "not start. So the snippet chooser names its model as a string, and the team block "
                "imports its model only when it actually runs.",
        ),
        Scene(
            id="deleted_snippet",
            body="""
            <div class="eyebrow">Delete a testimonial that a page is using</div>
            <table>
              <tr><td class="k">before delete</td><td class="v">reference index: <b>used 1 time</b>, on Home</td></tr>
              <tr><td class="k">page after delete</td><td class="v">still <b>200</b></td></tr>
              <tr><td class="k">block value</td><td class="v" style="color:var(--red)">None</td></tr>
              <tr><td class="k">without a guard</td><td class="v">an <b>empty styled quote box</b></td></tr>
            </table>
            <div class="sub" style="margin-top:30px">Every chooser value can become None. Template it:
            <b>{% if t %}</b></div>
            """,
            say="Now, what happens when somebody deletes a testimonial that a page is using. Before "
                "the delete, Wagtail already knows. Its reference index says used one time, on the "
                "home page, and the admin shows that on the confirmation screen. After the delete, "
                "the page still loads. But the block's value is now None, and without a guard in "
                "the template you ship an empty, styled quote box. Every chooser value can become "
                "None. Write the template for it.",
        ),

        # ------------------------------------------------------- tags
        Scene(
            id="tags",
            body="""
            <div class="filename">blog/models.py</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> BlogPageTag(TaggedItemBase):
    content_object = <span class="k">ParentalKey</span>(<span class="s">"blog.BlogPage"</span>,
                                 on_delete=models.CASCADE,
                                 related_name=<span class="s">"tagged_items"</span>)

<span class="k">class</span> BlogPage(HeroMixin, Page):
    &hellip;
    tags = <span class="k">ClusterTaggableManager</span>(through=BlogPageTag, blank=<span class="s">True</span>)</pre>
            <div class="sub" style="margin-top:28px"><b>ParentalKey</b>, not ForeignKey: tags are
            saved with the <b>revision</b>, so a draft can change them without touching the live post.</div>
            """,
            say="Now tags for the journal. A small through model, and a taggable manager on the post. "
                "The detail that matters is parental key instead of foreign key. It means the tags "
                "are saved as part of the page's revision, so an editor can change the tags on a "
                "draft without touching the live post.",
        ),
        Scene(
            id="filter",
            body="""
            <div class="filename">BlogIndexPage.get_context</div>
            <pre class="code" style="font-size:31px">tag = request.GET.get(<span class="s">"tag"</span>)
<span class="k">if</span> tag:
    posts = posts.filter(tags__slug=tag)
context[<span class="s">"tag"</span>] = tag</pre>
            <div class="sub" style="margin-top:36px">Four lines. And the last one matters more than it
            looks.</div>
            """,
            say="Filtering by tag is four lines in get context. And the last of those four lines "
                "matters a lot more than it looks. Here is why.",
        ),
        terminal_scene(
            scene_id="lost_filter",
            eyebrow="Before passing the tag back",
            title="",
            bar="measured against the running site",
            steps=[
                Cmd(text="GET /journal/?tag=process", out="Page 1 of 2", prompt="$", highlight=["Page"]),
                Cmd(text="# the 'Older' link", out="?page=2", prompt="$", error=["?page=2"]),
                Cmd(text="GET /journal/?page=2", out="Page 2 of 3    # the tag is gone",
                    prompt="$", error=["Page 2 of 3"]),
            ],
            say="Filter by the process tag. Page one of two. Click older. The link is question mark "
                "page equals two, and it lands on page two of three. That is the unfiltered journal. "
                "The tag just vanished.",
        ),
        Scene(
            id="lost_filter_fix",
            body="""
            <h2>Every link has to carry every parameter</h2>
            <pre class="code" style="font-size:27px"><span class="bad">href="?page={{ posts.next_page_number }}"</span>

<span class="k">href="?{% if tag %}tag={{ tag|urlencode }}&amp;amp;{% endif %}page={{ posts.next_page_number }}"</span></pre>
            <div class="sub" style="margin-top:32px">Now <b>Older</b> goes to
            <b>?tag=process&amp;page=2</b> &rarr; <b>Page 2 of 2</b>.</div>
            """,
            say="Last episode's pagination links replace the entire query string. The moment you add "
                "a second parameter, every link that builds a query string has to carry both of them. "
                "Pass the tag back to the template, put it in the link, and older now goes to page "
                "two of two.",
        ),
        Scene(
            id="css_fix",
            body="""
            <div class="eyebrow">Fixed while building</div>
            <h2>Every tag pill had a border</h2>
            <pre class="code" style="font-size:30px"><span class="bad">.post-list li</span>   <span class="c">{ border-top: &hellip; }   /* matches the tag list too */</span>
<span class="k">.post-list &gt; li</span> <span class="c">{ border-top: &hellip; }   /* only the posts */</span></pre>
            """,
            say="And one small fix on the way. The tag list inside each post is a list as well, so "
                "the post row's border and padding landed on every tag pill. One child selector "
                "instead of a descendant selector.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="after_team",
            body=f"""
            <div class="eyebrow">The team block, on About</div>
            {shot("localhost:8000/about/", SHOT_TEAM, "70%")}
            """,
            say="And here it is. The team, on the About page, in the order set by dragging rows in "
                "the admin.",
        ),
        Scene(
            id="after_testimonial",
            body=f"""
            <div class="eyebrow">A chosen testimonial, on Home</div>
            {shot("localhost:8000", SHOT_TESTIMONIAL, "66%")}
            """,
            say="A testimonial on the home page, chosen by the editor from the snippet list.",
        ),
        Scene(
            id="after_tag",
            body=f"""
            <div class="eyebrow">?tag=editors</div>
            {shot("localhost:8000/journal/?tag=editors", SHOT_TAG, "52%")}
            """,
            say="And the journal, filtered by tag, with every post showing its own tags as links.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 8"', prompt=VENV),
                Cmd(text="git tag ep08-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 9 &mdash; Navigation &amp; Site Settings</h2>
            <div class="sub" style="margin-top:36px">A menu built from the page tree, and contact
            details the client can edit.</div>
            """,
            say="Next episode, navigation. A menu built from the page tree, and footer and contact "
                "details the client can edit themselves.",
        ),
    ],
)
