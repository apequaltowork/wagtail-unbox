"""Ep 4 — Templates & Static Files.

Scene spec for video/build.py. The first episode with a visible before/after.

The payoff slides embed real screenshots of the running site, captured with
headless Chrome from localhost -- not mock-ups. See notes.md for what was
verified.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 04'
VENV = "(.venv) PS&gt;"

SHOT_HOME = (HERE / "assets" / "shot-home.png").as_uri()
SHOT_ABOUT = (HERE / "assets" / "shot-about.png").as_uri()

SHOT_CSS = """
<style>
.shot { border: 2px solid var(--line); border-radius: 14px; overflow: hidden;
        box-shadow: 0 30px 70px rgba(0,0,0,.45); }
.shot img { display: block; width: 100%; }
.shotbar { background: #161925; padding: 14px 22px; font-family: var(--mono);
           font-size: 24px; color: var(--muted); border-bottom: 2px solid var(--line); }
</style>
"""


def shot(url_label: str, src: str) -> str:
    return (SHOT_CSS +
            f'<div class="shot"><div class="shotbar">{url_label}</div>'
            f'<img src="{src}" alt=""></div>')


EPISODE = Episode(
    key="ep04",
    number="04",
    title="Ep 4 - Templates & Static Files",
    badge=BADGE,
    intro_say="Templates, and static files.",
    outro_say="Next episode, StreamField. Thanks for watching.",
    scenes=[
        Scene(
            id="the_egg",
            body="""
            <div class="eyebrow">Four episodes in</div>
            <h2>The site still shows this</h2>
            <div class="quote" style="font-size:48px">A teal egg, and
            <span class="hl">"Welcome to your new Wagtail site!"</span><br><br>
            <span style="font-size:36px;color:var(--muted)">Today it goes.</span></div>
            """,
            say="Four episodes in, and the front of our site still shows Wagtail's welcome page. "
                "A teal egg, and welcome to your new Wagtail site. Today, it goes.",
        ),
        Scene(
            id="where_egg",
            body="""
            <div class="filename">home/templates/home/home_page.html &nbsp;&middot;&nbsp; as generated</div>
            <pre class="code" style="font-size:32px"><span class="c">{% comment %}
Delete the line below if you're just getting
started and want to remove the welcome screen!
{% endcomment %}</span>
{% include <span class="s">'home/welcome_page.html'</span> %}</pre>
            <div class="sub" style="margin-top:36px">Wagtail tells you, in a comment, that this is
            disposable. Delete the include, the template, and its CSS.</div>
            """,
            say="It lives in an include, and Wagtail tells you in a comment that it is disposable. "
                "So we delete the include, the welcome template, and its stylesheet. Three files "
                "gone.",
        ),
        Scene(
            id="how_found",
            body="""
            <h2>How Wagtail finds a template</h2>
            <pre class="code">class <span class="k">HomePage</span>(Page)
        &darr;
home/templates/home/<span class="k">home_page</span>.html</pre>
            <div class="sub" style="margin-top:40px">Model name, lowercased, with underscores.
            You never wire it up.</div>
            """,
            say="Remember the rule from episode two. Model name, lowercased, with underscores. "
                "Home page becomes home underscore page dot html, and you never wire it up "
                "anywhere. Wagtail just looks for it.",
        ),
        Scene(
            id="two_places",
            body="""
            <h2>Two places templates live</h2>
            <table>
              <tr><th>Setting</th><th>Looks in</th><th>Use for</th></tr>
              <tr><td class="k">APP_DIRS: True</td><td class="v">home/templates/&hellip;</td><td class="v">page templates</td></tr>
              <tr><td class="k">DIRS: [PROJECT_DIR / "templates"]</td><td class="v">studio/templates/&hellip;</td><td class="v">base.html, 404, 500</td></tr>
            </table>
            <div class="sub" style="margin-top:40px">Page templates live with their app. Anything
            shared by every app lives in the project folder.</div>
            """,
            say="And there are two places templates can live, both switched on in settings. App "
                "dirs finds templates inside each app, which is where page templates go. And the "
                "dirs setting points at the project templates folder, which is where base dot html "
                "lives, because every app uses it.",
        ),

        # ---------------------------------------------------------- base.html
        Scene(
            id="base_keep",
            body="""
            <h2>base.html &mdash; keep the head</h2>
            <ul class="bullets">
              <li>SEO title with a fallback to <b>page.title</b></li>
              <li><b>{% wagtailuserbar %}</b> &mdash; the editor's floating admin bar</li>
              <li>The preview-panel <b>base target</b> fix</li>
            </ul>
            <div class="sub" style="margin-top:36px">All of that is already right. We only replace
            the <b>body</b>.</div>
            """,
            say="Open base dot html. The head that Wagtail generated is already good. An S E O "
                "title with a fallback, the user bar, and that preview panel fix we looked at in "
                "episode two. Keep all of it. We are only replacing the body.",
        ),
        Scene(
            id="base_body",
            body="""
            <div class="filename">studio/templates/base.html</div>
            <pre class="code" style="font-size:31px">&lt;header class=<span class="s">"site-header"</span>&gt;
  &lt;a class=<span class="s">"brand"</span> href=<span class="s">"</span>{% <span class="k">slugurl</span> <span class="s">'home'</span> %}<span class="s">"</span>&gt;Studio&lt;/a&gt;
&lt;/header&gt;

&lt;main class=<span class="s">"wrap"</span>&gt;
  {% <span class="k">block</span> content %}{% <span class="k">endblock</span> %}
&lt;/main&gt;

&lt;footer class=<span class="s">"site-footer"</span>&gt;
  &lt;p&gt;&amp;copy; {% <span class="k">now</span> <span class="s">"Y"</span> %} Studio.&lt;/p&gt;
&lt;/footer&gt;</pre>
            """,
            say="A header, a main, and a footer, wrapped around the content block. That is the "
                "whole layout. Every page in the series inherits it from here.",
        ),
        Scene(
            id="three_tags",
            body="""
            <h2>Three tags do the linking</h2>
            <table>
              <tr><th>Tag</th><th>What it does</th></tr>
              <tr><td class="k">{% pageurl child %}</td><td class="v">link to a page object</td></tr>
              <tr><td class="k">{% slugurl 'home' %}</td><td class="v">link by slug &mdash; survives renaming</td></tr>
              <tr><td class="k">{{ page.body|richtext }}</td><td class="v">render a RichTextField as HTML</td></tr>
            </table>
            <div class="sub" style="margin-top:36px">All three come from
            <b>{% load wagtailcore_tags %}</b>.</div>
            """,
            say="Three tags do all the linking. Page url takes a page object and gives you its "
                "address. Slug url looks a page up by slug, which is why the brand link keeps "
                "working even if somebody renames the home page. And the rich text filter turns a "
                "rich text field into H T M L. All three need the wagtail core tags load at the top.",
        ),
        Scene(
            id="never_url_path",
            body="""
            <div class="eyebrow">Callback to episode 3</div>
            <h2>Never build links from url_path</h2>
            <table>
              <tr><td class="k" style="color:var(--red)">page.url_path</td><td class="v">/home/about/ &mdash; a 404</td></tr>
              <tr><td class="k" style="color:var(--teal)">{% pageurl page %}</td><td class="v">/about/ &mdash; correct</td></tr>
            </table>
            """,
            say="And this is where last episode's warning pays off. Never build a link out of url "
                "path. It gives you slash home slash about, which is a four oh four. Page url gives "
                "you the real address.",
        ),
        Scene(
            id="children",
            body="""
            <div class="filename">home_page.html</div>
            <pre class="code" style="font-size:34px">{% <span class="k">for</span> child <span class="k">in</span> page.get_children.<span class="k">live</span> %}
  &lt;li&gt;&lt;a href=<span class="s">"</span>{% pageurl child %}<span class="s">"</span>&gt;{{ child.title }}&lt;/a&gt;&lt;/li&gt;
{% <span class="k">endfor</span> %}</pre>
            <div class="sub" style="margin-top:40px"><b>.live</b> means published only &mdash;
            drafts stay hidden.<br>The homepage doesn't know About exists. It just asks the tree
            for its children.</div>
            """,
            say="And here is the page tree finally doing something useful. The home page lists its "
                "own children. It does not know that an About page exists. It just asks the tree. "
                "Dot live means published pages only, so drafts stay hidden from visitors.",
        ),

        # ---------------------------------------------------------- static
        Scene(
            id="empty_css",
            body="""
            <h2>The file that ships empty</h2>
            <div class="term">
              <div class="bar">a fresh Wagtail project</div>
              <div class="body"><span class="p">PS&gt;</span> <span class="o">studio/static/css/studio.css</span>
<span class="hl-out">0 bytes</span></div>
            </div>
            <div class="sub" style="margin-top:36px">Wagtail links it in base.html and leaves it
            for you. Plain CSS &mdash; no build step, no framework, all series.</div>
            """,
            say="Now the styling. Wagtail generates a stylesheet at studio slash static slash c s s "
                "slash studio dot c s s, links it in base dot html, and leaves it completely empty. "
                "Zero bytes. We fill it in with plain C S S. No build step, no framework, not in "
                "this episode and not in any of them.",
        ),
        Scene(
            id="static_tag",
            body="""
            <h2>{% static %} and STATICFILES_DIRS</h2>
            <pre class="code" style="font-size:32px"><span class="c"># base.py</span>
STATICFILES_DIRS = [ PROJECT_DIR / <span class="s">"static"</span> ]

<span class="c"># base.html</span>
&lt;link href=<span class="s">"</span>{% <span class="k">static</span> <span class="s">'css/studio.css'</span> %}<span class="s">"</span>&gt;
        &darr;
<span class="o">/static/css/studio.css</span></pre>
            <div class="sub" style="margin-top:36px">In production this becomes
            <b>collectstatic</b>. Episode 13.</div>
            """,
            say="The static tag turns a path inside your static folder into a U R L, using the "
                "static files dirs setting we read in episode two. In development the server just "
                "serves it. In production there is a collect static step, and that is episode "
                "thirteen.",
        ),

        # ---------------------------------------------------------- the gotcha
        Scene(
            id="gotcha",
            body="""
            <div class="eyebrow">This will cost you ten minutes</div>
            <h2>You write the CSS. Nothing changes.</h2>
            <div class="quote" style="font-size:46px">The page is still unstyled &mdash;<br>
            and <span class="hl">nothing is wrong with your code</span>.</div>
            """,
            say="And now the thing that will cost you ten minutes, because it cost me ten minutes. "
                "You write the C S S. You reload. And the page is still completely unstyled. "
                "Nothing is wrong with your code.",
        ),
        Scene(
            id="gotcha_proof",
            body="""
            <div class="filename">measured in the live page</div>
            <pre class="code" style="font-size:30px">document.styleSheets.length             <span class="c">// 1  -- attached</span>
document.styleSheets[0].cssRules.length <span class="bad">// 0  -- parsed as empty</span>

fetch(href, {cache: <span class="s">'no-store'</span>})       <span class="c">// 200, 2065 bytes, text/css</span></pre>
            <div class="sub" style="margin-top:36px">The server is serving it fine. The browser
            cached the file <b>while it was 0 bytes</b>.</div>
            """,
            say="Here is the proof. The stylesheet is attached to the page, but it has zero rules "
                "in it. Meanwhile fetching the same U R L returns two thousand bytes of perfectly "
                "good C S S. The server is fine. Your browser cached that file back when it was "
                "zero bytes, and it is still using the empty copy.",
        ),
        Scene(
            id="hard_reload",
            body="""
            <h2>Hard-reload</h2>
            <table>
              <tr><td class="k">Windows / Linux</td><td class="v">Ctrl + F5 &nbsp;&nbsp;or&nbsp;&nbsp; Ctrl + Shift + R</td></tr>
              <tr><td class="k">macOS</td><td class="v">Cmd + Shift + R</td></tr>
            </table>
            <div class="sub" style="margin-top:40px">Every viewer will hit this, because the file
            ships empty and you loaded the site before writing any CSS.</div>
            """,
            say="The fix is a hard reload. Control F five on Windows, or command shift R on a Mac. "
                "Every single person following along will hit this, because the file ships empty "
                "and you loaded the site before you wrote anything into it.",
        ),

        # ---------------------------------------------------------- payoff
        Scene(
            id="after_home",
            body=f"""
            <div class="eyebrow">After</div>
            {shot("localhost:8000", SHOT_HOME)}
            """,
            say="And there it is. A header, a title, the intro from episode three, a list of child "
                "pages generated from the tree, and a footer. That is our studio site.",
        ),
        Scene(
            id="after_about",
            body=f"""
            <div class="eyebrow">And the About page</div>
            {shot("localhost:8000/about/", SHOT_ABOUT)}
            """,
            say="The About page gets the same layout for free, because it extends the same base "
                "template. And that back link is built from page dot get parent, so it always "
                "points at wherever the page actually sits in the tree.",
        ),
        Scene(
            id="mobile",
            body="""
            <h2>One media query</h2>
            <pre class="code" style="font-size:34px"><span class="k">@media</span> (max-width: 34rem) {
    h1 { font-size: 2rem; }
}</pre>
            <div class="sub" style="margin-top:40px">At 375px wide the heading drops from 2.6rem to
            <b>2rem</b>. Checked in the browser.</div>
            """,
            say="And one media query makes it work on a phone. At three hundred and seventy five "
                "pixels the heading drops from two point six rem to two rem. That is the entire "
                "responsive story for this site.",
        ),
        Scene(
            id="still_django_404",
            body="""
            <div class="eyebrow">One thing that didn't change</div>
            <h2>The 404 page</h2>
            <div class="sub"><b>studio/templates/404.html</b> exists and extends base.html &mdash;
            but Django only uses it when <b>DEBUG = False</b>.<br><br>
            Under runserver you still get Django's technical 404. That's expected.
            Episode 13.</div>
            """,
            say="One last thing. If you try a bad U R L you still get Django's yellow debug page. "
                "The four oh four template exists and extends our base, but Django only uses it "
                "when debug is switched off. That is episode thirteen, not a bug.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 4"', prompt=VENV),
                Cmd(text="git tag ep04-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 5 &mdash; StreamField, Properly</h2>
            <div class="quote" style="font-size:46px">Right now <b>body</b> is one rich-text blob.<br>
            <span class="hl">StreamField turns it into real content blocks.</span></div>
            """,
            say="Our pages look like a site now, but the body field is still one big blob of rich "
                "text. Next episode, StreamField replaces it with real content blocks. That is the "
                "episode most people come to Wagtail for.",
        ),
    ],
)
