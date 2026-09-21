"""Ep 9 — Navigation & Site Settings.

Scene spec for video/build.py.

The show_in_menus listing, the "not a registered tag library" error, the
settings row count and the one-query measurement are all from real runs.
See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 09'
VENV = "(.venv) PS&gt;"
PY = "&gt;&gt;&gt;"

SHOT_MENU = (HERE / "assets" / "shot-menu.png").as_uri()
SHOT_FOOTER = (HERE / "assets" / "shot-footer.png").as_uri()

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
    key="ep09",
    number="09",
    title="Ep 9 - Navigation & Site Settings",
    badge=BADGE,
    intro_say="Navigation, and site settings.",
    outro_say="Next episode, forms. Thanks for watching.",
    scenes=[
        Scene(
            id="no_way_around",
            body="""
            <div class="eyebrow">Where we are</div>
            <h2>A site you can't get around</h2>
            <div class="sub" style="margin-top:36px">The only way to reach About or the Journal is
            the list on the homepage. And the footer says <b>Studio</b> because somebody typed it into
            a template.</div>
            """,
            say="There is an About page and a journal, and the only way to reach either of them is "
                "the list at the bottom of the homepage. And the footer says Studio, because somebody "
                "typed that word into a template. Today, a real menu, and details the client can edit.",
        ),
        Scene(
            id="from_the_tree",
            body="""
            <h2>The menu comes from the tree</h2>
            <pre class="code" style="font-size:31px">site.root_page.get_children().live().<span class="k">in_menu</span>()</pre>
            <div class="sub" style="margin-top:36px">No menu model, no hard-coded links. An editor
            adds a page to the menu by ticking <b>Show in menus</b> on its Promote tab.</div>
            """,
            say="There is no menu model here, and no hard coded links. The menu is simply the "
                "children of the site's root page that are live and marked as in menu. So an editor "
                "adds a page to the menu by ticking one checkbox, on that page's Promote tab.",
        ),
        Scene(
            id="tag",
            body="""
            <div class="filename">home/templatetags/navigation_tags.py</div>
            <pre class="code" style="font-size:26px">@register.inclusion_tag(<span class="s">"home/includes/main_menu.html"</span>, takes_context=<span class="s">True</span>)
<span class="k">def</span> main_menu(context):
    request = context[<span class="s">"request"</span>]
    site = Site.find_for_request(request)
    current = context.get(<span class="s">"page"</span>)
    items = []
    <span class="k">for</span> item <span class="k">in</span> site.root_page.get_children().live().in_menu():
        active = bool(current) <span class="k">and</span> current.url_path.startswith(item.url_path)
        items.append({<span class="s">"page"</span>: item, <span class="s">"active"</span>: active})
    <span class="k">return</span> {<span class="s">"items"</span>: items, <span class="s">"request"</span>: request}</pre>
            """,
            say="It is an inclusion tag. It finds the site for this request, takes the root page's "
                "children, and works out which one is active. Then base dot html just says main menu.",
        ),
        terminal_scene(
            scene_id="not_registered",
            eyebrow="Reload the page, and",
            title="",
            bar="runserver, already running",
            steps=[
                Cmd(text="GET /journal/",
                    out="TemplateSyntaxError: 'navigation_tags' is not a\nregistered tag library.",
                    prompt="$", error=["TemplateSyntaxError", "registered"]),
            ],
            say="Reload the page, and. Template syntax error. Navigation tags is not a registered tag "
                "library. And the code is correct.",
        ),
        Scene(
            id="restart",
            body="""
            <div class="eyebrow">The code is fine</div>
            <h2>Restart runserver</h2>
            <div class="sub" style="margin-top:32px">The autoreloader had already restarted for the
            <b>models.py</b> edit. But it only watches modules that are <b>already imported</b> &mdash;
            and a brand-new tag library isn't one.<br><br>New <b>templatetags</b> module? Stop the
            server and start it again.</div>
            """,
            say="The development server had already reloaded itself for the models change a minute "
                "earlier. But the reloader only watches files that are already imported, and a brand "
                "new tag library is not one of them. So any time you add a new template tags module, "
                "stop the server and start it again.",
        ),
        Scene(
            id="empty_menu",
            body="""
            <div class="eyebrow">Restarted. And the menu is empty.</div>
            <pre class="code" style="font-size:28px">HomePage       show_in_menus=<span class="bad">False</span>   /home/
StandardPage   show_in_menus=<span class="bad">False</span>   /home/about/
BlogIndexPage  show_in_menus=<span class="bad">False</span>   /home/journal/

Page.show_in_menus_default = <span class="bad">False</span></pre>
            <div class="sub" style="margin-top:30px">Every page starts out of the menu. Tick
            <b>Show in menus</b> on About and Journal, and it appears.</div>
            """,
            say="Restarted, and now the menu is empty. Nothing there at all. Because every page on "
                "this site has show in menus set to false. That is the default for every page type. "
                "Tick the box on About and on the journal, publish, and the menu appears.",
        ),
        Scene(
            id="default",
            body="""
            <h2>show_in_menus_default</h2>
            <pre class="code" style="font-size:31px"><span class="k">class</span> StandardPage(HeroMixin, Page):
    &hellip;
    show_in_menus_default = <span class="s">True</span></pre>
            <div class="sub" style="margin-top:36px">New pages of this type start ticked.<br>
            Pages that <b>already exist</b> keep whatever they have.</div>
            """,
            say="And to stop that happening next time, set show in menus default to true on the page "
                "types that belong in a menu. But be clear what it does. New pages start with the box "
                "ticked. Pages that already exist are not touched.",
        ),
        Scene(
            id="active",
            body="""
            <h2>Which item is active</h2>
            <pre class="code" style="font-size:29px">current.url_path.startswith(item.url_path)

<span class="c">/home/journal/pricing-a-website-honestly/</span>
<span class="k">/home/journal/</span>   &rarr; Journal stays lit</pre>
            <div class="sub" style="margin-top:30px"><b>url_path</b> always ends in a slash, so
            <b>/home/about/</b> can't match <b>/home/about-us/</b>.</div>
            """,
            say="The active item is a prefix match on the U R L path. So when you are reading a post, "
                "which lives under the journal, the journal stays highlighted. And because a U R L "
                "path always ends in a slash, About can never accidentally match a page called About us.",
        ),
        Scene(
            id="one_query",
            body="""
            <div class="eyebrow">Measured</div>
            <h2>The menu costs one query</h2>
            <div class="sub" style="margin-top:32px">Rendering <b>{% main_menu %}</b> on its own,
            with the Site cached: <b>1</b> query.<br><br>
            No caching needed. That changes once menus have a second level.</div>
            """,
            say="And it is cheap. I rendered the menu tag on its own and counted. One database query. "
                "No caching needed. That changes once you build dropdowns, because each level is "
                "another query per item.",
        ),

        # ------------------------------------------------------- settings
        Scene(
            id="settings_setup",
            body="""
            <h2>Site settings</h2>
            <pre class="code" style="font-size:28px"><span class="c"># studio/settings/base.py</span>
INSTALLED_APPS += [<span class="s">"wagtail.contrib.settings"</span>]
<span class="c"># TEMPLATES &rarr; context_processors</span>
<span class="s">"wagtail.contrib.settings.context_processors.settings"</span></pre>
            <div class="sub" style="margin-top:32px">One app, one context processor. Then any
            template can read the settings.</div>
            """,
            say="Now the footer. Wagtail's settings app, plus its context processor, and every template "
                "on the site can read the studio's details.",
        ),
        Scene(
            id="settings_model",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:28px">@register_setting(icon=<span class="s">"cog"</span>)
<span class="k">class</span> StudioSettings(<span class="k">BaseSiteSetting</span>):
    studio_name = models.CharField(max_length=<span class="s">80</span>, default=<span class="s">"Studio"</span>)
    email = models.EmailField(blank=<span class="s">True</span>)
    phone = models.CharField(max_length=<span class="s">40</span>, blank=<span class="s">True</span>)
    address = models.TextField(blank=<span class="s">True</span>)
    linkedin_url = models.URLField(blank=<span class="s">True</span>)</pre>
            <div class="sub" style="margin-top:28px"><b>BaseSiteSetting</b>: one row per Site. A second
            site on the same install gets its own details.</div>
            """,
            say="A settings model is a normal Django model with one decorator. Site setting, rather "
                "than generic setting, means one row per site, so if this install ever runs a second "
                "site, it gets its own phone number.",
        ),
        terminal_scene(
            scene_id="row_appears",
            eyebrow="Nobody created it",
            title="",
            bar="python manage.py shell",
            steps=[
                Cmd(text="StudioSettings.objects.count()   # before any request",
                    out="0", prompt=PY),
                Cmd(text="StudioSettings.objects.count()   # after one page load",
                    out="1", prompt=PY, highlight=["1"]),
            ],
            say="And watch this. No rows before any request. Load one page, and there is a row. "
                "Wagtail creates it the first time something reads it, using your defaults. Which is "
                "why the studio name needs a sensible default. It is what the header shows before "
                "anyone has opened the settings screen.",
        ),
        Scene(
            id="use_settings",
            body="""
            <div class="filename">studio/templates/base.html</div>
            <pre class="code" style="font-size:26px">{{ settings.<span class="k">home</span>.<span class="k">StudioSettings</span>.studio_name }}

{% <span class="k">with</span> s=settings.home.StudioSettings %}
  &lt;a href=<span class="s">"mailto:</span>{{ s.email }}<span class="s">"</span>&gt;{{ s.email }}&lt;/a&gt;
  &lt;a href=<span class="s">"tel:</span>{{ s.phone|<span class="k">cut</span>:<span class="s">' '</span> }}<span class="s">"</span>&gt;{{ s.phone }}&lt;/a&gt;
{% <span class="k">endwith</span> %}</pre>
            <div class="sub" style="margin-top:26px">App label, model name, field. And cut the
            spaces out of a <b>tel:</b> link.</div>
            """,
            say="In a template it is settings, then the app label, then the model name, then the "
                "field. The brand, the email as a mail to link, and the phone as a tel link, with the "
                "spaces cut out so it actually dials.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="after_menu",
            body=f"""
            <div class="eyebrow">Reading a post &mdash; Journal stays lit</div>
            {shot("localhost:8000/journal/pricing-a-website-honestly/", SHOT_MENU, "80%")}
            """,
            say="And here it is. Reading a post, and the journal is still highlighted in the menu.",
        ),
        Scene(
            id="after_footer",
            body=f"""
            <div class="eyebrow">Every line of this comes from Settings</div>
            {shot("localhost:8000", SHOT_FOOTER, "80%")}
            """,
            say="And the footer. The name, the email, the phone number, the address and the social "
                "link. All of it comes from the settings screen, and the client can change any of it "
                "without calling you.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 9"', prompt=VENV),
                Cmd(text="git tag ep09-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 10 &mdash; Forms That Work</h2>
            <div class="sub" style="margin-top:36px">A contact page that emails the studio and keeps
            every submission in the admin.</div>
            """,
            say="Next episode, forms. A contact page that emails the studio, and keeps every "
                "submission in the admin.",
        ),
    ],
)
