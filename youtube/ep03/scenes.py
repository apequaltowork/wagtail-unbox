"""Ep 3 — The Page Model & the Tree.

Scene spec for video/build.py. The first episode that changes code.

Every terminal output, column count and path string here was captured from a
real run on the recording machine -- see notes.md for the list. Nothing is
invented; if the pinned Wagtail version moves, re-capture before re-rendering.
"""

import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 03'
VENV = "(.venv) PS&gt;"


def _tree(highlight_about: bool) -> str:
    """The three-row tree, read from the real database."""
    rows = [
        ("0001", "", "Root", "depth 1", "/", 0),
        ("0001", "0001", "Home", "depth 2", "/home/", 1),
        ("00010001", "0001", "About", "depth 3", "/home/about/", 2),
    ]
    out = []
    for prefix, last, label, depth, url, indent in rows:
        is_about = label == "About"
        new_colour = "var(--amber)" if (is_about and highlight_about) else "var(--teal)"
        path = (f'<span style="color:var(--teal-dim)">{prefix}</span>'
                f'<span style="color:{new_colour}">{last}</span>') if last else \
               f'<span style="color:var(--teal)">{prefix}</span>'
        weight = "font-weight:700;" if is_about and highlight_about else ""
        out.append(
            f'<div class="node" style="margin-left:{indent * 60}px;{weight}">'
            f'<span class="path">{path}</span>'
            f'<span class="label">{label}</span>'
            f'<span class="meta">{depth} &nbsp;&middot;&nbsp; {url}</span></div>')
    return f'<div class="tree">{"".join(out)}</div>'


EPISODE = Episode(
    key="ep03",
    number="03",
    title="Ep 3 - The Page Model & the Tree",
    badge=BADGE,
    intro_say="The page model, and the tree.",
    outro_say="Next episode, we replace the welcome page with real templates. Thanks for watching.",
    scenes=[
        # ---------------------------------------------------------- the promise
        Scene(
            id="promise",
            body="""
            <div class="eyebrow">Last episode, a prediction</div>
            <h2>A page under Home gets this path</h2>
            <pre class="code" style="font-size:64px;text-align:center">000100010001</pre>
            <div class="sub" style="margin-top:40px">Today we build that page &mdash; and check.</div>
            """,
            say="Last episode we made a prediction. A page one level under Home would get the path "
                "zero zero zero one, zero zero zero one, zero zero zero one. Today we build that "
                "page, and we check.",
        ),
        Scene(
            id="six_lines",
            body="""
            <div class="filename">home/models.py &nbsp;&middot;&nbsp; where we left it</div>
            <pre class="code"><span class="k">class</span> HomePage(Page):
    <span class="k">pass</span></pre>
            <div class="sub" style="margin-top:40px">Already a working page type. <b>Page</b> brings
            title, slug, SEO fields, publishing, revisions and permissions.<br>
            What it doesn't have is anything of <i>ours</i>.</div>
            """,
            say="Here is where we left the home page. Two lines, and already a working page type, "
                "because Page brings title, slug, S E O fields, publishing, revisions and "
                "permissions. What it does not have is anything of ours. So let us add some.",
        ),

        # ---------------------------------------------------------- the code
        Scene(
            id="fields",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:34px"><span class="k">class</span> HomePage(Page):
    intro = models.CharField(
        max_length=250, blank=<span class="k">True</span>,
        help_text=<span class="s">"One or two sentences shown under the page title."</span>,
    )
    body = RichTextField(blank=<span class="k">True</span>)

<span class="hl">    content_panels = Page.content_panels + [
        FieldPanel(<span class="s">"intro"</span>),
        FieldPanel(<span class="s">"body"</span>),
    ]</span></pre>
            """,
            say="Two fields. Intro is an ordinary Django char field, and the help text is what the "
                "editor sees under the box, so write it for them. Body is a rich text field, "
                "Wagtail's editor. And then the part people forget: content panels.",
        ),
        Scene(
            id="panels",
            body="""
            <h2>A field is not a form field</h2>
            <div class="quote" style="font-size:50px">Adding a field to the model gives you
            <span class="hl">a database column</span>.<br><br>
            It only appears in the admin once it has a
            <span class="hl">FieldPanel</span>.</div>
            <div class="sub" style="margin-top:40px"><b>Page.content_panels +</b> keeps the title
            field Wagtail already gives you.</div>
            """,
            say="A field on the model is not the same as a field in the admin. Adding it gives you "
                "a database column, and nothing else. It only becomes editable once it has a field "
                "panel. And we add to page dot content panels, rather than replacing it, so we keep "
                "the title field that Wagtail already provides.",
        ),
        Scene(
            id="standard_page",
            body="""
            <div class="filename">home/models.py &nbsp;&middot;&nbsp; a second page type</div>
            <pre class="code" style="font-size:36px"><span class="k">class</span> StandardPage(Page):
    <span class="c"># About, Services -- anything that is mostly words</span>
    intro = models.CharField(max_length=250, blank=<span class="k">True</span>, ...)
    body = RichTextField(blank=<span class="k">True</span>)

    content_panels = Page.content_panels + [
        FieldPanel(<span class="s">"intro"</span>), FieldPanel(<span class="s">"body"</span>),
    ]</pre>
            """,
            say="And a second page type. Standard page, for About, Services, anything that is "
                "mostly words. Same two fields. Having two page types is what lets us build an "
                "actual tree.",
        ),
        Scene(
            id="template_needed",
            body="""
            <h2>Every page type needs a template</h2>
            <pre class="code">class <span class="k">StandardPage</span>(Page)
        &darr;
home/templates/home/<span class="k">standard_page</span>.html</pre>
            <div class="sub" style="margin-top:40px">Without it, <b>View live</b> fails with
            <b style="color:var(--red)">TemplateDoesNotExist</b> &mdash; and the admin looks fine
            right up until you preview.<br>We keep it bare. Styling is episode 4.</div>
            """,
            say="Every page type needs a template, named by the rule from last episode: standard "
                "underscore page dot html. Leave it out and you get template does not exist, but "
                "only when you hit view live, so the admin looks perfectly fine right up until you "
                "preview. We keep this template bare. Styling is episode four.",
        ),

        # ---------------------------------------------------------- migration
        terminal_scene(
            scene_id="makemigrations",
            eyebrow="Make the migration",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py makemigrations", prompt=VENV,
                    out="Migrations for 'home':\n"
                        "  home\\migrations\\0003_standardpage_homepage_body_homepage_intro.py\n"
                        "    + Create model StandardPage\n"
                        "    + Add field body to homepage\n"
                        "    + Add field intro to homepage",
                    highlight=["+ Create model StandardPage"]),
                Cmd(text="python manage.py migrate", prompt=VENV,
                    out="Running migrations:\n"
                        "  Applying home.0003_standardpage_homepage_body_homepage_intro... OK",
                    highlight=["OK"]),
            ],
            say="Make the migration. One new model, two new fields. Then apply it.",
        ),
        Scene(
            id="page_ptr",
            body="""
            <div class="filename">0003_standardpage_homepage_body_homepage_intro.py</div>
            <pre class="code" style="font-size:32px">migrations.CreateModel(
    name=<span class="s">'StandardPage'</span>,
    fields=[
<span class="hl">        (<span class="s">'page_ptr'</span>, models.OneToOneField(
            parent_link=<span class="k">True</span>, primary_key=<span class="k">True</span>,
            to=<span class="s">'wagtailcore.page'</span>)),</span>
        (<span class="s">'intro'</span>, models.CharField(...)),
        (<span class="s">'body'</span>, wagtail.fields.RichTextField(blank=<span class="k">True</span>)),
    ],
)</pre>
            """,
            say="Now open that migration, because one line in it explains how every Wagtail page "
                "is stored. Page pointer. A one to one field, pointing at wagtail core page.",
        ),
        Scene(
            id="two_tables",
            body="""
            <div class="eyebrow">The mental model</div>
            <h2 style="font-size:54px;margin-bottom:34px">Every page lives in two tables</h2>
            <div class="cols">
              <div class="col hero">
                <h3 style="font-family:var(--mono);font-size:34px">wagtailcore_page</h3>
                <p><b>29 columns</b>, shared by every page on the site</p>
                <p style="font-family:var(--mono);font-size:26px">title &middot; slug &middot; path &middot;
                depth &middot; url_path &middot; live &middot; seo_title &middot; content_type_id &hellip;</p>
              </div>
              <div class="col">
                <h3 style="font-family:var(--mono);font-size:34px">home_standardpage</h3>
                <p><b>3 columns</b>, only what's unique to this type</p>
                <p style="font-family:var(--mono);font-size:26px">page_ptr_id &middot; intro &middot; body</p>
              </div>
            </div>
            <div class="sub" style="margin-top:36px"><b>page_ptr_id</b> joins them. It's Django
            multi-table inheritance.</div>
            """,
            say="That is Django multi table inheritance, and it is the mental model for the rest "
                "of this series. Every page lives in two tables. The shared page table has twenty "
                "nine columns: title, slug, path, depth, and the content type from last episode. "
                "Our standard page table has three. Page pointer, intro, and body. Only what is "
                "unique to this page type. Page pointer is what joins them.",
        ),

        # ---------------------------------------------------------- admin
        Scene(
            id="admin_edit",
            body="""
            <div class="eyebrow">In the admin</div>
            <h2>Edit Home</h2>
            <ul class="bullets">
              <li><b>Intro</b> and <b>Body</b> are there now</li>
              <li>With the help text underneath, written for the editor</li>
              <li>Fill in Intro, then <b>Publish</b></li>
            </ul>
            """,
            say="Over to the admin. Edit the home page, and there are the two new fields, with our "
                "help text underneath. Fill in the intro and publish.",
        ),
        Scene(
            id="admin_child",
            body="""
            <h2>Add a child page</h2>
            <ul class="bullets">
              <li>On Home: <b>Add child page</b> &rarr; <b>Standard page</b></li>
              <li>Title: <b>About</b>, fill in Intro and Body</li>
              <li><b>Publish</b></li>
            </ul>
            """,
            say="Now on Home, add a child page. Choose standard page, call it About, fill it in, "
                "and publish. That is our first page that we made ourselves.",
        ),

        # ---------------------------------------------------------- the payoff
        terminal_scene(
            scene_id="shell_tree",
            eyebrow="Checking the prediction",
            title="",
            bar="python manage.py shell",
            steps=[
                Cmd(text='for p in Page.objects.all().order_by("path"):', prompt="&gt;&gt;&gt;"),
                Cmd(text='    print(repr(p.path), p.depth, p.url_path, p.title)', prompt="...",
                    out="'0001'             1 /                Root\n"
                        "'00010001'         2 /home/           Home\n"
                        "'000100010001'     3 /home/about/     About",
                    highlight=["'000100010001'"]),
            ],
            say="Now the moment of truth. Open the shell and print the tree.",
        ),
        Scene(
            id="tree_payoff",
            body=f"""
            <div class="eyebrow">Exactly as predicted</div>
            <h2 style="font-size:56px;margin-bottom:40px">Four characters per level</h2>
            {_tree(highlight_about=True)}
            <div class="sub" style="margin-top:44px">About = Home's path + <b style="color:var(--amber)">0001</b>.</div>
            """,
            say="There it is. About sits at zero zero zero one, zero zero zero one, zero zero zero "
                "one. Exactly what the animation predicted last episode. It is Home's path, plus "
                "four more characters.",
        ),
        Scene(
            id="url_surprise",
            body="""
            <div class="eyebrow">But look at the URL</div>
            <h2>url_path is not the URL</h2>
            <table>
              <tr><th>Address</th><th>Result</th></tr>
              <tr><td class="k">/home/about/</td><td class="v"><b style="color:var(--red)">404</b> &mdash; that's the url_path</td></tr>
              <tr><td class="k" style="color:var(--teal)">/about/</td><td class="v"><b style="color:var(--teal)">200</b> &mdash; the real URL</td></tr>
            </table>
            <div class="sub" style="margin-top:40px">url_path includes the site root. Home <i>is</i>
            the root, so it drops out. In templates, use <b>page.url</b>.</div>
            """,
            say="But look closely at that url path. It says slash home slash about. Visit that and "
                "you get a four oh four. The page is actually at slash about. The url path is the "
                "route from the root of the tree, so it includes home. But home is the root of the "
                "site, so it drops out of the real address. If you ever build links, use page dot "
                "url, not url path.",
        ),
        terminal_scene(
            scene_id="specific",
            eyebrow="The most common question",
            title="Why is my field missing?",
            bar="python manage.py shell",
            steps=[
                Cmd(text='p = Page.objects.get(slug="about")', prompt="&gt;&gt;&gt;"),
                Cmd(text='type(p).__name__, hasattr(p, "intro")', prompt="&gt;&gt;&gt;",
                    out="('Page', False)", highlight=["False"]),
                Cmd(text='type(p.specific).__name__, p.specific.intro', prompt="&gt;&gt;&gt;",
                    out="('StandardPage', 'Who we are and how we work.')",
                    highlight=["StandardPage"]),
            ],
            say="And one more thing that catches everyone. Ask page dot objects for About, and you "
                "get a plain Page, with no intro field. Call dot specific, and you get the real "
                "standard page, with everything on it. That is the two tables again. Page dot "
                "objects only reads the shared one.",
        ),

        # ---------------------------------------------------------- wrap
        Scene(
            id="still_wrong",
            body="""
            <div class="eyebrow">Something is still wrong</div>
            <h2>Add a child under Home and you're offered&hellip;</h2>
            <div class="checks">
              <div class="yes">Standard page</div>
              <div class="no" style="color:var(--fg)"><b>Home page</b> &mdash; a homepage inside a homepage</div>
            </div>
            <div class="sub" style="margin-top:40px">Nothing stops it yet.
            <b>subpage_types</b> fixes it in episode 7.</div>
            """,
            say="Before we finish, something is still wrong. When you add a child under Home, "
                "Wagtail offers you Home page as well. Nothing stops you putting a home page inside "
                "a home page. We fix that with sub page types, in episode seven.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 3"', prompt=VENV),
                Cmd(text="git tag ep03-end", prompt=VENV),
            ],
            say="Commit it, and tag it. E p zero three end is our first checkpoint with real code "
                "changes in it.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 4 &mdash; Templates &amp; Static Files</h2>
            <div class="quote" style="font-size:46px">The site still shows Wagtail's welcome egg.<br>
            <span class="hl">Time to replace it.</span></div>
            """,
            say="Our pages have content now, but the home page still shows Wagtail's welcome egg. "
                "Next episode, we replace it with real templates.",
        ),
    ],
)
