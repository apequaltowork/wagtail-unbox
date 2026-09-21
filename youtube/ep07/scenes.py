"""Ep 7 — Blog: Parent & Child Pages.

Scene spec for video/build.py.

Every terminal output here was captured from a real run: the allowed-page-type
listing before the rules were added, the FieldError from ordering
get_children(), and Paginator.page() against get_page(). See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 07'
VENV = "(.venv) PS&gt;"
PY = "&gt;&gt;&gt;"

SHOT_JOURNAL = (HERE / "assets" / "shot-journal-crop.png").as_uri()
SHOT_JOURNAL_P3 = (HERE / "assets" / "shot-journal-p3-crop.png").as_uri()
SHOT_POST = (HERE / "assets" / "shot-post-crop.png").as_uri()

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
    """Text-heavy pages are cropped to the content column, so each shot gets its
    own width -- whatever keeps it inside the slide's height."""
    return (SHOT_CSS +
            f'<div class="shot" style="width:{width}"><div class="shotbar">{url_label}</div>'
            f'<img src="{src}" alt=""></div>')


EPISODE = Episode(
    key="ep07",
    number="07",
    title="Ep 7 - Blog: Parent & Child Pages",
    badge=BADGE,
    intro_say="The blog. Parent and child pages.",
    outro_say="Next episode, snippets. Thanks for watching.",
    scenes=[
        # ------------------------------------------------------- setup
        Scene(
            id="cold_open",
            body="""
            <div class="eyebrow">Where we are</div>
            <h2>A studio that never says anything</h2>
            <div class="sub" style="margin-top:40px">A homepage and an About page. Today: a
            <b>journal</b> &mdash; an index, posts under it, newest first, a few at a time.</div>
            """,
            say="Right now the studio's site is a homepage and an About page. A studio that wants "
                "clients needs to say something, so today we build a journal. An index page, posts "
                "underneath it, newest first, three at a time.",
        ),
        terminal_scene(
            scene_id="startapp",
            eyebrow="A second app",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py startapp blog", prompt=VENV),
                Cmd(text="Remove-Item blog\\admin.py, blog\\views.py", prompt=VENV),
            ],
            say="This is the first time we have added an app of our own. Start app blog, and then "
                "delete two of the files it made. A Wagtail page app does not use Django's admin "
                "dot py or views dot py. Add blog to installed apps, and we are ready.",
        ),
        Scene(
            id="why_app",
            body="""
            <h2>Why a separate app</h2>
            <table>
              <tr><td class="k">home/</td><td class="v">the site shell &mdash; HeroMixin, BodyBlock, templates</td></tr>
              <tr><td class="k">blog/</td><td class="v">its own models, rules and templates &mdash; and it will grow tags</td></tr>
            </table>
            <div class="sub" style="margin-top:36px">The blog still <b>imports</b> HeroMixin and
            BodyBlock from home. One hero, one set of blocks, on every page type.</div>
            """,
            say="Why a separate app rather than two more models in home. The blog has its own "
                "templates and its own rules, and next episode it grows tags. Home stays the site "
                "shell. But the blog still imports the hero and the content blocks from home, so "
                "there is one definition of each, used everywhere.",
        ),

        # ------------------------------------------------------- models
        Scene(
            id="two_models",
            body="""
            <div class="filename">blog/models.py</div>
            <pre class="code" style="font-size:29px"><span class="k">class</span> BlogIndexPage(Page):
    intro = models.CharField(max_length=<span class="s">250</span>, blank=<span class="s">True</span>)


<span class="k">class</span> BlogPage(HeroMixin, Page):
    date = models.DateField(default=timezone.localdate)
    intro = models.CharField(max_length=<span class="s">250</span>)
    body = StreamField(BodyBlock(), blank=<span class="s">True</span>)</pre>
            <div class="sub" style="margin-top:30px"><b>date</b> is its own field, not
            <b>first_published_at</b> &mdash; editors backdate posts, and a republish must not
            reorder the blog.</div>
            """,
            say="Two models. The index is just a page with an intro. A post has a date, an intro, "
                "the hero from last episode, and the same StreamField body as every other page. "
                "The date is deliberately its own field and not the publish date, because editors "
                "backdate posts, and fixing a typo must not move a post to the top of the blog.",
        ),

        # ------------------------------------------------------- gotcha 1
        Scene(
            id="anything_anywhere",
            body="""
            <div class="eyebrow">Before adding any rules</div>
            <h2>With no rules, anything goes anywhere</h2>
            <pre class="code" style="font-size:27px">HomePage      children: [<span class="s">'BlogIndexPage'</span>, <span class="bad">'HomePage'</span>, <span class="bad">'Page'</span>, <span class="s">'StandardPage'</span>]
StandardPage  children: [<span class="bad">'HomePage'</span>, <span class="bad">'Page'</span>, <span class="s">'StandardPage'</span>]</pre>
            <div class="sub" style="margin-top:36px">A <b>second homepage inside About</b>. A bare
            <b>Page</b> with no template, which errors the moment anybody visits it.</div>
            """,
            say="Before writing any rules, I printed what each existing page type allows underneath "
                "it. Look at the About page. It will happily accept a second homepage. And a bare "
                "Page, which has no template, and throws an error the moment anybody visits it. "
                "Wagtail's default is anything, anywhere.",
        ),
        Scene(
            id="rules",
            body="""
            <h2>Two lists fix it</h2>
            <pre class="code" style="font-size:30px"><span class="k">class</span> BlogPage(HeroMixin, Page):
    &hellip;
    parent_page_types = [<span class="s">"blog.BlogIndexPage"</span>]
    subpage_types = []

<span class="k">class</span> HomePage(HeroMixin, Page):
    &hellip;
    parent_page_types = [<span class="s">"wagtailcore.Page"</span>]
    subpage_types = [<span class="s">"home.StandardPage"</span>, <span class="s">"blog.BlogIndexPage"</span>]
    max_count = <span class="s">1</span></pre>
            """,
            say="Two lists fix it. Every page type says where it may live, and what may live under "
                "it. A post may only sit under the journal, and nothing may sit under a post. The "
                "homepage lives at the root, and max count one means there can only ever be one.",
        ),
        Scene(
            id="rules_proof",
            body="""
            <div class="eyebrow">Checked with can_create_at()</div>
            <table>
              <tr><td class="k">second HomePage under root</td><td class="v" style="color:var(--red)">False</td></tr>
              <tr><td class="k">second Journal under Home</td><td class="v" style="color:var(--red)">False</td></tr>
              <tr><td class="k">BlogPage under About</td><td class="v" style="color:var(--red)">False</td></tr>
              <tr><td class="k">BlogPage under Journal</td><td class="v" style="color:var(--teal)">True</td></tr>
            </table>
            <div class="sub" style="margin-top:36px">Python only. <b>makemigrations</b> says
            <b>No changes detected</b>.</div>
            """,
            say="And checked. A second homepage, no. A second journal, no. A blog post under About, "
                "no. A post under the journal, yes. And these rules live entirely in Python. Make "
                "migrations says no changes detected, because nothing about the database changed.",
        ),

        # ------------------------------------------------------- gotcha 2
        Scene(
            id="get_children_naive",
            body="""
            <div class="eyebrow">The query everybody writes first</div>
            <h2>Newest posts first&hellip;</h2>
            <pre class="code" style="font-size:32px">self.get_children().live().order_by(<span class="s">"-date"</span>)</pre>
            <div class="sub" style="margin-top:36px">Looks right. Isn't.</div>
            """,
            say="Now the index page needs its posts, newest first. And here is the query everybody "
                "writes first. Get children, live ones, ordered by date descending. It looks right.",
        ),
        terminal_scene(
            scene_id="field_error",
            eyebrow="What actually happens",
            title="",
            bar="python manage.py shell",
            steps=[
                Cmd(text="index.get_children().live().order_by('-date')",
                    out="FieldError: Cannot resolve keyword 'date' into field.",
                    prompt=PY, error=["FieldError"]),
                Cmd(text="[type(p).__name__ for p in index.get_children()][:2]",
                    out="['Page', 'Page']",
                    prompt=PY, highlight=["Page"]),
            ],
            say="Field error. Cannot resolve keyword date. And take the order by off, and look at "
                "what comes back. Not blog pages. Plain Page objects.",
        ),
        Scene(
            id="why_page",
            body="""
            <h2>get_children() queries the Page table</h2>
            <div class="sub" style="margin-top:8px">It returns <b>Page</b> objects, in
            <b>tree order</b>. Page has no <b>date</b>.</div>
            <pre class="code" style="font-size:31px;margin-top:36px"><span class="bad">self.get_children().live().order_by("-date")</span>

<span class="k">BlogPage.objects.child_of(self).live().order_by("-date")</span></pre>
            <div class="sub" style="margin-top:30px">Query the model you mean.</div>
            """,
            say="Here is why. Get children queries the page table, the one every page type shares. "
                "It gives you page objects, in the order they sit in the tree, and the page table "
                "has no date column. So ask the blog page model directly, for children of this "
                "page. Now you get real blog pages, and you can order them by date.",
        ),

        # ------------------------------------------------------- get_context + pagination
        Scene(
            id="get_context",
            body="""
            <div class="filename">blog/models.py &nbsp;&middot;&nbsp; BlogIndexPage</div>
            <pre class="code" style="font-size:28px"><span class="k">def</span> get_context(self, request, *args, **kwargs):
    context = <span class="k">super</span>().get_context(request, *args, **kwargs)
    posts = (BlogPage.objects.child_of(self).live()
             .order_by(<span class="s">"-date"</span>, <span class="s">"-first_published_at"</span>))
    paginator = Paginator(posts, self.POSTS_PER_PAGE)
    context[<span class="s">"posts"</span>] = paginator.<span class="k">get_page</span>(request.GET.get(<span class="s">"page"</span>))
    <span class="k">return</span> context</pre>
            <div class="sub" style="margin-top:30px"><b>get_context</b> is how a page hands extra
            data to its template. Call super, add what you need.</div>
            """,
            say="And get context is where it goes. This is how any Wagtail page hands extra data to "
                "its template. Call super, add what you need, return it. Here that is the posts, "
                "newest first, with the first published date as a tie breaker, and wrapped in "
                "Django's paginator.",
        ),
        terminal_scene(
            scene_id="get_page",
            eyebrow="page() or get_page()",
            title="",
            bar="python manage.py shell",
            steps=[
                Cmd(text="paginator.page('abc')",
                    out="PageNotAnInteger: That page number is not an integer",
                    prompt=PY, error=["PageNotAnInteger"]),
                Cmd(text="paginator.get_page('abc').number",
                    out="1", prompt=PY, highlight=["1"]),
                Cmd(text="paginator.page('999')",
                    out="EmptyPage: That page contains no results",
                    prompt=PY, error=["EmptyPage"]),
                Cmd(text="paginator.get_page('999').number",
                    out="3", prompt=PY, highlight=["3"]),
            ],
            say="And use get page, not page. The page number comes from the U R L, which means "
                "anybody can type anything into it. Page raises an exception for rubbish, or for a "
                "page that does not exist. Get page just clamps it to something sensible.",
        ),

        # ------------------------------------------------------- templates
        Scene(
            id="index_template",
            body="""
            <div class="filename">blog/templates/blog/blog_index_page.html</div>
            <pre class="code" style="font-size:28px">{% <span class="k">for</span> post <span class="k">in</span> posts %}
  &lt;time&gt;{{ post.date|date:<span class="s">"j F Y"</span> }}&lt;/time&gt;
  &lt;h2&gt;&lt;a href=<span class="s">"</span>{% pageurl post %}<span class="s">"</span>&gt;{{ post.title }}&lt;/a&gt;&lt;/h2&gt;
  &lt;p&gt;{{ post.intro }}&lt;/p&gt;
{% <span class="k">empty</span> %}
  &lt;li&gt;No posts yet.&lt;/li&gt;
{% <span class="k">endfor</span> %}</pre>
            <div class="sub" style="margin-top:30px"><b>posts</b> is a paginator page &mdash; it
            iterates like a list, and knows <b>has_next</b> and <b>has_previous</b>.</div>
            """,
            say="The index template loops over posts. That is a paginator page, which iterates "
                "like a list, and also knows whether there is a next or previous page, which is "
                "all the prev and next links need.",
        ),
        Scene(
            id="counter_fix",
            body="""
            <div class="eyebrow">Fixed while building</div>
            <h2>The page counter jumped sideways</h2>
            <div class="sub" style="margin-top:28px">With <b>space-between</b>, page 1 put
            &ldquo;Page 1 of 3&rdquo; on the <b>left</b> and page 3 put it on the <b>right</b>
            &mdash; a missing link removes a flex item.</div>
            <pre class="code" style="font-size:30px;margin-top:32px"><span class="c">/* three fixed slots, empty or not */</span>
grid-template-columns: <span class="k">1fr auto 1fr</span>;</pre>
            """,
            say="A small thing I fixed on the way. The page counter jumped from one side of the "
                "screen to the other between page one and page three, because a missing link took "
                "an item out of the flex row. Three fixed grid slots, empty or not, and it stays "
                "in the middle.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="after_journal",
            body=f"""
            <div class="eyebrow">Page 1 of 3</div>
            {shot("localhost:8000/journal/", SHOT_JOURNAL, "46%")}
            """,
            say="And here is the journal. Newest first, three posts, and an older link.",
        ),
        Scene(
            id="after_p3",
            body=f"""
            <div class="eyebrow">?page=3 &mdash; and ?page=999 lands here too</div>
            {shot("localhost:8000/journal/?page=3", SHOT_JOURNAL_P3, "60%")}
            """,
            say="Page three. The oldest post, a newer link, and the counter still in the middle. "
                "Type page nine hundred and ninety nine into the address bar and you land here "
                "too, instead of on an error page.",
        ),
        Scene(
            id="after_post",
            body=f"""
            <div class="eyebrow">A post</div>
            {shot("localhost:8000/journal/pricing-a-website-honestly/", SHOT_POST, "56%")}
            """,
            say="And a post. The date, the title, the intro, the same StreamField blocks as every "
                "other page, and a back link to the journal built from the tree.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 7"', prompt=VENV),
                Cmd(text="git tag ep07-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 8 &mdash; Snippets &amp; Reusable Content</h2>
            <div class="sub" style="margin-top:36px">Team members and testimonials, written once
            and used anywhere &mdash; and tags for the journal.</div>
            """,
            say="Next episode, snippets. Team members and testimonials, written once and used on "
                "any page. And tags for the journal.",
        ),
    ],
)
