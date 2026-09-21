"""Ep 13 — Production Settings.

Scene spec for video/build.py.

Every result here ran against studio.settings.production on this machine, with
DEBUG off. No Postgres server was available: the Postgres slides show only what
was verified without one (URL parsing, system checks, the timeout), and say so.
See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 13'
VENV = "(.venv) PS&gt;"
PY = "&gt;&gt;&gt;"

SHOT_404 = (HERE / "assets" / "shot-404.png").as_uri()
SHOT_BROKEN = (HERE / "assets" / "shot-broken-media.png").as_uri()

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
    key="ep13",
    number="13",
    title="Ep 13 - Production Settings",
    badge=BADGE,
    intro_say="Production settings.",
    outro_say="Next episode, we deploy it. Thanks for watching.",
    scenes=[
        Scene(
            id="what_we_got",
            body="""
            <div class="eyebrow">What wagtail start gave us</div>
            <pre class="code" style="font-size:32px"><span class="c"># studio/settings/production.py</span>
<span class="k">from</span> .base <span class="k">import</span> *
DEBUG = <span class="s">False</span>
STORAGES[&hellip;] = <span class="s">"&hellip;ManifestStaticFilesStorage"</span>
<span class="k">from</span> .local <span class="k">import</span> *   <span class="c"># if it exists</span></pre>
            <div class="sub" style="margin-top:30px"><b>check --deploy</b>: 6 issues. And no
            <b>SECRET_KEY</b> at all &mdash; it expects a <b>local.py</b> that doesn't exist.</div>
            """,
            say="Here is what wagtail start gave us for production. Debug off, one storage setting, "
                "and an import of a local settings file that does not exist. Django's deploy check "
                "finds six issues. And there is no secret key at all.",
        ),

        # ------------------------------------------------------- gotcha 1
        terminal_scene(
            scene_id="dockerfile_dev",
            eyebrow="The generated Dockerfile runs gunicorn studio.wsgi",
            title="",
            bar="studio.wsgi, loaded with no variables set",
            steps=[
                Cmd(text="settings.SETTINGS_MODULE", out="'studio.settings.dev'", prompt=PY, error=["dev"]),
                Cmd(text="settings.DEBUG", out="True", prompt=PY, error=["True"]),
                Cmd(text="settings.ALLOWED_HOSTS", out="['*']", prompt=PY, error=["*"]),
                Cmd(text="settings.SECRET_KEY[:16]", out="'django-insecure-'", prompt=PY, error=["insecure"]),
            ],
            say="And before any of that, the biggest one. The Dockerfile that wagtail start generates "
                "runs gunicorn on the W S G I file, and never says which settings to use. So I loaded "
                "it exactly the way gunicorn would. Development settings. Debug on. Any host. And the "
                "secret key that is committed to git.",
        ),
        Scene(
            id="fail_closed",
            body="""
            <h2>Fail closed</h2>
            <pre class="code" style="font-size:29px"><span class="c"># studio/wsgi.py</span>
os.environ.setdefault(<span class="s">"DJANGO_SETTINGS_MODULE"</span>, <span class="k">"studio.settings.production"</span>)

<span class="c"># site/Dockerfile</span>
ENV &hellip; DJANGO_SETTINGS_MODULE=studio.settings.production</pre>
            <div class="sub" style="margin-top:30px">Deployed as generated, visitors get full tracebacks
            &mdash; settings included. Now a missing variable stops the server instead:
            <b>Set the DJANGO_SECRET_KEY environment variable.</b></div>
            """,
            say="Deployed as generated, any error on the live site shows a full traceback, settings "
                "included, to anyone. So the W S G I file now defaults to production, and the "
                "Dockerfile says so explicitly. And production refuses to start without a secret. If "
                "something is missing, the server stops, with a message saying what. That is failing "
                "closed. Manage dot py still defaults to development, so nothing changes on your laptop.",
        ),

        # ------------------------------------------------------- env
        Scene(
            id="env",
            body="""
            <div class="filename">studio/settings/production.py</div>
            <pre class="code" style="font-size:27px"><span class="k">def</span> env(name, default=<span class="s">None</span>, required=<span class="s">False</span>):
    value = os.environ.get(name, default)
    <span class="k">if</span> required <span class="k">and not</span> value:
        <span class="k">raise</span> ImproperlyConfigured(<span class="s">f"Set the {name} environment variable."</span>)
    <span class="k">return</span> value

SECRET_KEY = env(<span class="s">"DJANGO_SECRET_KEY"</span>, required=<span class="s">True</span>)
ALLOWED_HOSTS = env_list(<span class="s">"DJANGO_ALLOWED_HOSTS"</span>)
<span class="k">if not</span> ALLOWED_HOSTS:
    <span class="k">raise</span> ImproperlyConfigured(<span class="s">"Set DJANGO_ALLOWED_HOSTS, e.g. 'studio.example'."</span>)</pre>
            <div class="sub" style="margin-top:22px">Empty hosts would start fine &mdash; and answer every
            request with <b>400</b>.</div>
            """,
            say="Everything secret or host specific now comes from environment variables, so nothing "
                "sensitive is in git and the same code runs on any host. Two are required. The secret "
                "key, and the allowed hosts. An empty hosts list would start perfectly happily and then "
                "answer every single request with a four hundred, so we refuse to start instead.",
        ),
        Scene(
            id="database_url",
            body="""
            <h2>One variable for the database</h2>
            <pre class="code" style="font-size:28px">DATABASES = {<span class="s">"default"</span>: dj_database_url.config(
    default=<span class="s">f"sqlite:///{BASE_DIR / 'db.sqlite3'}"</span>,
    conn_max_age=<span class="s">600</span>, conn_health_checks=<span class="s">True</span>)}

<span class="c"># DATABASE_URL=postgres://studio:&hellip;@db.internal:5432/studio</span>
<span class="c">#   -&gt; django.db.backends.postgresql</span></pre>
            <div class="sub" style="margin-top:26px">Unset means the local SQLite file &mdash; so
            production settings run on a laptop before any server exists.</div>
            """,
            say="The database is one variable. Database U R L. Set it to a Postgres address and it "
                "parses to Django's Postgres backend. Leave it unset and you get the local SQLite file, "
                "which means you can try these production settings on a laptop before any server exists.",
        ),
        Scene(
            id="postgres_e005",
            body="""
            <div class="eyebrow">Point it at Postgres &mdash; before it even connects</div>
            <pre class="code" style="font-size:25px"><span class="bad">wagtailsearch.IndexEntry.body: (postgres.E005)
'django.contrib.postgres' must be in INSTALLED_APPS
in order to use SearchVectorField.</span></pre>
            <pre class="code" style="font-size:27px;margin-top:22px"><span class="k">if</span> DATABASES[<span class="s">"default"</span>][<span class="s">"ENGINE"</span>] == <span class="s">"django.db.backends.postgresql"</span>:
    INSTALLED_APPS = [*INSTALLED_APPS, <span class="s">"django.contrib.postgres"</span>]
    DATABASES[<span class="s">"default"</span>][<span class="s">"OPTIONS"</span>][<span class="s">"connect_timeout"</span>] = <span class="s">10</span></pre>
            <div class="sub" style="margin-top:20px">On Postgres, Wagtail's search uses Postgres full-text
            search. And a wrong URL took <b>over two minutes</b> to fail &mdash; now <b>12 seconds</b>.</div>
            """,
            say="Point it at Postgres, and it fails before it even tries to connect. On Postgres, "
                "Wagtail's search switches to Postgres full text search, and that needs Django's "
                "Postgres app installed. So add it when the engine is Postgres. And while testing with "
                "no server listening, a wrong address took more than two minutes to fail. A ten second "
                "connect timeout, and the same mistake shows up in twelve seconds.",
        ),

        # ------------------------------------------------------- static
        terminal_scene(
            scene_id="all_500",
            eyebrow="DEBUG off, no collectstatic",
            title="",
            bar="studio.settings.production",
            steps=[
                Cmd(text="GET /", out="500", prompt="$", error=["500"]),
                Cmd(text="GET /admin/login/", out="500", prompt="$", error=["500"]),
                Cmd(text="GET /no-such-page/",
                    out="500\nValueError: Missing staticfiles manifest entry for 'css/studio.css'",
                    prompt="$", error=["500", "ValueError"]),
            ],
            say="Now run the site with production settings, before collecting static files. The home "
                "page, five hundred. The admin login, five hundred. Even the four oh four page is a "
                "five hundred. Missing static files manifest entry.",
        ),
        Scene(
            id="collectstatic",
            body="""
            <h2>Forget collectstatic, lose the whole site</h2>
            <div class="sub" style="margin-top:26px">The manifest storage refuses to render
            <b>{% static %}</b> for a file it hasn't seen &mdash; on every page, including the one you'd
            use to log in and find out why.</div>
            <pre class="code" style="font-size:30px;margin-top:30px">python manage.py collectstatic --noinput
<span class="o">217 static files copied, 633 post-processed.</span></pre>
            <div class="sub" style="margin-top:22px">Then every page is 200 &mdash; and a missing page is a
            real <b>404</b>.</div>
            """,
            say="The manifest storage will not render a static tag for any file it has not seen. So "
                "without collect static, every page on the site breaks, including the admin login you "
                "would use to investigate. Collect static. Two hundred and seventeen files. And now "
                "everything is two hundred, and a missing page is a real four oh four.",
        ),
        Scene(
            id="after_404",
            body=f"""
            <div class="eyebrow">Episode 4's promise &mdash; the 404 template, finally used</div>
            {shot("127.0.0.1:8003/no-such-page/ -- production settings", SHOT_404, "62%")}
            """,
            say="Which means, back in episode four, I promised this. The four oh four template that "
                "extends our base, finally showing up, because debug is off.",
        ),
        Scene(
            id="whitenoise",
            body="""
            <div class="eyebrow">Measured, DEBUG off</div>
            <h2>WhiteNoise serves the CSS</h2>
            <table>
              <tr><td class="k">stylesheet URL</td><td class="v">/static/css/studio.<b>32463efc1907</b>.css</td></tr>
              <tr><td class="k">without WhiteNoise</td><td class="v" style="color:var(--red)">404</td></tr>
              <tr><td class="k">with WhiteNoise</td><td class="v" style="color:var(--teal)">200 &middot; gzip &middot; <b>immutable</b>, 10 years</td></tr>
            </table>
            <div class="sub" style="margin-top:26px">A change makes a new filename, so the browser can
            cache for a decade. That's the <b>permanent fix</b> for episode 4's cache trap.</div>
            """,
            say="With debug off, Django stops serving static files, so without help the stylesheet is a "
                "four oh four. White noise serves it from the app itself, compressed. And look at the "
                "file name. It has a hash in it, so the browser is told to cache it for ten years. "
                "Change the C S S and the hash changes. That is the permanent fix for the cache trap "
                "that cost us ten minutes in episode four.",
        ),
        Scene(
            id="media",
            body=f"""
            <div class="eyebrow">Media is not static &mdash; every upload is a 404</div>
            {shot("127.0.0.1:8003 -- production settings", SHOT_BROKEN, "54%")}
            """,
            say="But look at the hero. Broken. Uploaded images are media, not static files, and with "
                "debug off nothing serves them. White noise deliberately does not. You can see the alt "
                "text from episode six doing its job, at least. How media is served depends on the "
                "host, so that is decided in the next episode.",
        ),

        # ------------------------------------------------------- https
        Scene(
            id="https",
            body="""
            <h2>HTTPS behind a proxy</h2>
            <table>
              <tr><td class="k">SECURE_PROXY_SSL_HEADER</td><td class="v">trust the host's <b>X-Forwarded-Proto</b></td></tr>
              <tr><td class="k">http://studio.example/</td><td class="v"><b>301</b> &rarr; https://studio.example/</td></tr>
              <tr><td class="k">Host: evil.example</td><td class="v"><b>400</b></td></tr>
              <tr><td class="k">cookies</td><td class="v">session and CSRF: secure only</td></tr>
              <tr><td class="k">HSTS</td><td class="v">max-age=<b>3600</b> &mdash; start short</td></tr>
            </table>
            """,
            say="And H T T P S. The host terminates the encryption and forwards plain requests with a "
                "header, so Django is told to trust it. Plain H T T P now redirects. A request for "
                "somebody else's hostname is refused. Cookies are secure only. And H S T S starts at "
                "one hour. It is a promise browsers keep. Set a year, then break your certificate, and "
                "nobody can reach the site until the year is up. Raise it once H T T P S is proven.",
        ),
        terminal_scene(
            scene_id="check_deploy",
            eyebrow="Django's own checklist",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py check --deploy",
                    out="(security.W005) SECURE_HSTS_INCLUDE_SUBDOMAINS ...\n"
                        "(security.W021) SECURE_HSTS_PRELOAD ...\n"
                        "System check identified 2 issues (0 silenced).",
                    prompt=VENV, highlight=["2 issues"]),
            ],
            say="Django's deploy check. Six issues down to two, and both of those are about committing "
                "harder to H S T S, which we are not doing until the real domain exists.",
        ),
        Scene(
            id="requirements",
            body="""
            <div class="eyebrow">One more from wagtail start</div>
            <h2>The requirements the Dockerfile installs</h2>
            <pre class="code" style="font-size:30px"><span class="c"># site/requirements.txt, as generated</span>
<span class="bad">Django&gt;=6,&lt;6.1</span>

<span class="c"># what every episode ran on</span>
<span class="k">Django==6.1.1</span></pre>
            <div class="sub" style="margin-top:28px">A production image would have run a different Django
            than we ever tested. Both requirements files now pin the same versions.</div>
            """,
            say="And one more from the generated files. The requirements file that the Dockerfile "
                "installs still caps Django below six point one. Every episode has run on six point one "
                "point one. So a production image would have been a different Django from anything we "
                "ever tested. Both requirements files now pin exactly the same versions.",
        ),
        Scene(
            id="not_verified",
            body="""
            <div class="eyebrow">Said plainly</div>
            <h2>What isn't verified yet</h2>
            <table>
              <tr><td class="k" style="color:var(--teal)">verified</td><td class="v">the URL, the driver, the system checks, the 10s timeout</td></tr>
              <tr><td class="k" style="color:var(--red)">not yet</td><td class="v">a live Postgres connection &mdash; no server on this machine</td></tr>
              <tr><td class="k" style="color:var(--red)">not yet</td><td class="v">building the Docker image</td></tr>
            </table>
            <div class="sub" style="margin-top:28px">Both happen against the real host, in episode 14.</div>
            """,
            say="And to be straight about it. The Postgres address, the driver, the system checks and "
                "the timeout are all verified. A live Postgres connection is not, because there is no "
                "database server on this machine, and neither is building the Docker image. Both happen "
                "against the real host, next episode.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 13"', prompt=VENV),
                Cmd(text="git tag ep13-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next &mdash; the last one</div>
            <h2>Ep 14 &mdash; Deploy It</h2>
            <div class="sub" style="margin-top:36px">A real host, a real database, media that works,
            and the first live edit.</div>
            """,
            say="Next episode, the last one. A real host, a real database, media that works, and the "
                "first live edit.",
        ),
    ],
)
