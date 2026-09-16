"""Ep 0a — What This Series Is (and Who It's For).

Scene spec for video/build.py. Narration text here is what gets spoken; keep it
conversational and keep sentences short -- long clauses expose the synth voice.

The cold-open beat (finished site footage) is a CARD here, because that footage
does not exist until episode 14. Replace scene `cold_open` with the real capture
before publishing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import Episode, Scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 0a'

EPISODE = Episode(
    key="ep00a",
    number="0a",
    title="Ep 0a - What This Series Is (and Who It's For)",
    badge=BADGE,
    intro_say="Wagtail Unboxed. Learning by building.",
    outro_say="Thanks for watching. Everything is linked below. Let us open the box.",
    scenes=[
        Scene(
            id="cold_open",
            body="""
            <div class="eyebrow">Cold open</div>
            <h2>The site we're building</h2>
            <div class="sub">
            <b style="color:var(--amber)">PLACEHOLDER.</b> Replace with the finished
            studio site capture from episode 14: scroll the live site, then cut to the
            admin and edit a heading live.
            </div>
            """,
            say="That is a real website. And that is somebody editing it, without touching "
                "any code. By the end of this series you will have built it, from an empty "
                "folder, and you will understand every file in it.",
        ),
        Scene(
            id="what_is",
            body="""
            <h2>What Wagtail actually is</h2>
            <div class="quote">Wagtail is a content management system
            <span class="hl">built on Django</span>.</div>
            """,
            say="So, what is Wagtail? It is a content management system built on Django.",
        ),
        Scene(
            id="not_a_fork",
            body="""
            <h2>Not a fork. Not a rival.</h2>
            <ul class="bullets">
              <li>It is a set of <b>Django apps</b> you pip install</li>
              <li>Models are models. Templates are templates. <span class="dim">Your Django knowledge transfers directly.</span></li>
              <li>What it adds: a <b>page tree</b>, a genuinely good editor, images with renditions, and StreamField</li>
            </ul>
            """,
            say="It is not a fork of Django, and it is not a competitor to it. It is a set of "
                "Django apps that you pip install. Models are still models. Templates are still "
                "templates. What Wagtail adds is a page tree, a genuinely good editing interface, "
                "an image system, and a content block system called StreamField.",
        ),
        Scene(
            id="seventy_percent",
            body="""
            <div class="quote">If you already write Django,<br>
            you already know <span class="hl">seventy percent</span> of Wagtail.<br><br>
            <span style="font-size:44px;color:var(--muted)">This series is about the other thirty.</span></div>
            """,
            say="If you already write Django, you already know about seventy percent of Wagtail. "
                "This series is about the other thirty.",
        ),
        Scene(
            id="who_for",
            body="""
            <h2>Who this is for</h2>
            <div class="cols">
              <div class="col">
                <h3>Django developers</h3>
                <p>who keep getting asked <b>"can the client edit this?"</b></p>
              </div>
              <div class="col">
                <h3>Agency &amp; freelance devs</h3>
                <p>building sites for people who are <b>not developers</b></p>
              </div>
              <div class="col">
                <h3>People leaving WordPress</h3>
                <p>who want the editor without the <b>PHP plugin ecosystem</b></p>
              </div>
            </div>
            """,
            say="Who is this for? Three groups. Django developers who keep getting asked, can the "
                "client edit this. Agency and freelance developers, building sites for people who "
                "are not developers. And people leaving WordPress, who want that editing experience "
                "without the PHP plugin ecosystem.",
        ),
        Scene(
            id="prereq_header",
            body="""
            <div class="eyebrow">Read this part</div>
            <h2>What you need to know first</h2>
            <div class="sub">The honest version.</div>
            """,
            say="Now the part I am not going to soften.",
        ),
        Scene(
            id="prereq_table",
            body="""
            <h2 style="font-size:52px">Prerequisites</h2>
            <table>
              <tr><th>Skill</th><th>How much</th></tr>
              <tr><td class="k">Python</td><td class="v">Functions, classes, imports, pip. Comfortable <i>reading</i> a class.</td></tr>
              <tr><td class="k" style="color:var(--teal)">Django</td><td class="v">Models, migrations, templates, settings.py, basic ORM. <b style="color:var(--fg)">The real prerequisite.</b></td></tr>
              <tr><td class="k">HTML &amp; CSS</td><td class="v">Enough to open a template and change markup.</td></tr>
              <tr><td class="k">Command line</td><td class="v">cd, list files, run a command, read an error.</td></tr>
            </table>
            """,
            say="You need basic Python. Functions, classes, imports, pip. And you need Django. "
                "Models, migrations, templates, settings dot pie. That is the real prerequisite, "
                "because Wagtail is Django. Plus enough HTML and CSS to edit a template, and enough "
                "command line to run a command and read an error.",
        ),
        Scene(
            id="go_learn_django",
            body="""
            <div class="quote">If <span class="hl">models.py</span> and
            <span class="hl">makemigrations</span><br>are not familiar yet
            &mdash; pause here.<br><br>
            <span style="font-size:40px;color:var(--muted)">Do the official Django tutorial first.
            It is about a weekend. Then come back.</span></div>
            """,
            say="If models dot pie and make migrations are not familiar yet, pause this video and go "
                "do the official Django tutorial. It is about a weekend of work. Then come back. You "
                "will get far more out of this, and you will not spend fourteen episodes copying code "
                "you cannot change.",
        ),
        Scene(
            id="not_required",
            body="""
            <h2>Not required</h2>
            <div class="checks">
              <div class="no">Any prior Wagtail</div>
              <div class="no">Any prior CMS experience</div>
              <div class="no">React, Vue, or Tailwind</div>
              <div class="no">Docker or Kubernetes</div>
            </div>
            <div class="sub" style="margin-top:44px">Wagtail itself is taught from zero.</div>
            """,
            say="What you do not need: any prior Wagtail, any prior CMS experience, no front end "
                "frameworks, and no Docker. Wagtail itself is taught from zero.",
        ),
        Scene(
            id="windows",
            body="""
            <h2>One practical note</h2>
            <ul class="bullets">
              <li>I record on <b>Windows</b>, so Windows commands are what you'll see</li>
              <li>Every episode ships a <b>commands.md</b> with macOS and Linux equivalents</li>
              <li><span class="dim">Nothing in this series is Windows-only.</span></li>
            </ul>
            """,
            say="One practical note. I record on Windows, so Windows commands are what you will see "
                "on screen. Every episode ships a commands file in the repo with the mac and Linux "
                "equivalents. Nothing in this series is Windows only.",
        ),
        Scene(
            id="roadmap_header",
            body="""
            <div class="eyebrow">The plan</div>
            <h2>Fourteen episodes, three acts</h2>
            <div class="sub">One concept each. Fifteen to twenty-five minutes.
            Nothing gets hand-waved.</div>
            """,
            say="Here is the plan. Fourteen episodes, in three acts. One concept per episode, "
                "fifteen to twenty five minutes each, and nothing gets hand waved.",
        ),
        Scene(
            id="act1",
            body="""
            <div class="eyebrow">Act one &nbsp;&middot;&nbsp; episodes 1&ndash;3</div>
            <h2>Unboxing</h2>
            <ul class="bullets">
              <li><b>1.</b> What Wagtail actually is <span class="dim">&mdash; install, create, run</span></li>
              <li><b>2.</b> Every generated file explained <span class="dim">&mdash; all twenty-nine of them</span></li>
              <li><b>3.</b> The Page model and the tree</li>
            </ul>
            """,
            say="Act one, episodes one to three. Unboxing. We create the project, and then we read "
                "every single file Wagtail generated. All twenty nine of them. Most tutorials skip "
                "that, and it is exactly why people stay confused.",
        ),
        Scene(
            id="act2",
            body="""
            <div class="eyebrow">Act two &nbsp;&middot;&nbsp; episodes 4&ndash;11</div>
            <h2>Building the site</h2>
            <ul class="bullets">
              <li>Templates &amp; static files &nbsp;&middot;&nbsp; <b>StreamField</b> &nbsp;&middot;&nbsp; images &amp; documents</li>
              <li>A blog with parent and child pages &nbsp;&middot;&nbsp; snippets</li>
              <li>Navigation &amp; site settings &nbsp;&middot;&nbsp; forms &nbsp;&middot;&nbsp; search</li>
            </ul>
            """,
            say="Act two, episodes four to eleven. We build. Templates and static files, StreamField, "
                "images and documents, a blog, reusable snippets, navigation, a working contact form, "
                "and search.",
        ),
        Scene(
            id="act3",
            body="""
            <div class="eyebrow">Act three &nbsp;&middot;&nbsp; episodes 12&ndash;14</div>
            <h2>Shipping it</h2>
            <ul class="bullets">
              <li><b>12.</b> Editor experience polish <span class="dim">&mdash; making it pleasant for the client</span></li>
              <li><b>13.</b> Production settings <span class="dim">&mdash; Postgres, env vars, security</span></li>
              <li><b>14.</b> Deploy to a real domain</li>
            </ul>
            """,
            say="And act three, episodes twelve to fourteen. Shipping. Polishing the editor experience "
                "for the client, real production settings, and deploying to an actual domain.",
        ),
        Scene(
            id="repo",
            body="""
            <h2>How to follow along</h2>
            <div class="term">
              <div class="bar">every episode ends on a git tag</div>
              <div class="body"><span class="p">$</span> git clone github.com/apequaltowork/wagtail-unbox
<span class="p">$</span> cd wagtail-unbox
<span class="p">$</span> git checkout ep06-end

<span class="o"># exactly the code episode 7 starts from</span></div>
            </div>
            """,
            say="Everything is in a public repo. Every episode ends on a git tag. So if you want to "
                "start at episode seven, you check out the tag from episode six, and you have exactly "
                "the code that episode begins with.",
        ),
        Scene(
            id="no_db",
            body="""
            <h2>The database is not committed</h2>
            <div class="quote">You make your own content.<br>
            <span style="font-size:42px;color:var(--muted)">That is deliberate. Making content is how
            the admin stops being abstract.</span></div>
            """,
            say="The database is not in the repo. You make your own content as you follow along. "
                "That is deliberate. Actually making content is how the admin stops being abstract.",
        ),
        Scene(
            id="not_this",
            body="""
            <h2>What this series is <i>not</i></h2>
            <div class="checks">
              <div class="no">A Django tutorial</div>
              <div class="no">A front-end course &mdash; no React, no Tailwind, no Node</div>
              <div class="no">A headless / API series</div>
              <div class="no">"Clone the repo and you're done"</div>
            </div>
            """,
            say="And what this series is not. It is not a Django tutorial. It is not a front end "
                "course. There is no React, no Tailwind, and no Node, at any point. We write plain "
                "CSS by hand so the episodes stay about Wagtail. It is not a headless or API series. "
                "And it is not a clone the repo and you are done series. You will type the code.",
        ),
        Scene(
            id="versions",
            body="""
            <h2>Pinned versions</h2>
            <pre class="code"><span class="c"># the code on screen is the code you get</span>
wagtail==<span class="s">7.4.3</span>
Django==<span class="s">6.1.1</span>
<span class="c"># Python 3.12</span></pre>
            <div class="sub" style="margin-top:36px">Wagtail 8.0 exists. We're on 7.4 on purpose &mdash;
            wider package compatibility, and it ages slower.</div>
            """,
            say="Versions are pinned, so the code on screen is the code you get. Wagtail seven point "
                "four point three, Django six point one point one, Python three point twelve. Wagtail "
                "eight is out. We are on seven point four on purpose: wider package compatibility, and "
                "it ages more slowly.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 0b &mdash; Setting up your machine</h2>
            <div class="quote" style="font-size:48px">Already have Python, virtualenvs and git?<br>
            <span class="hl">Skip straight to episode 1.</span></div>
            """,
            say="Next episode, we set up your machine. Python, git, and virtual environments. But if "
                "you already have Python, a virtualenv habit, and git, then skip it and go straight to "
                "episode one. I will see you there.",
        ),
    ],
)
