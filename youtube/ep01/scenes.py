"""Ep 1 — What Wagtail Actually Is.

Scene spec for video/build.py.

The terminal scenes animate: commands type out, then their output appears.
**Every line of output here was captured from a real run** on the recording
machine. Inventing terminal output in a teaching video sends viewers chasing a
result that will never appear on their screen.
"""

import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parent.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 01'
PS = "PS&gt;"

EPISODE = Episode(
    key="ep01",
    number="01",
    title="Ep 1 - What Wagtail Actually Is",
    badge=BADGE,
    intro_say="What Wagtail actually is.",
    outro_say="Next episode, we open the box and read every file. Thanks for watching.",
    scenes=[
        # ---------------------------------------------------------- framing
        Scene(
            id="promise",
            body="""
            <h2>By the end of this episode</h2>
            <ul class="bullets">
              <li>Wagtail installed</li>
              <li>A project created</li>
              <li><b>Logged into a real CMS admin</b></li>
              <li class="off">Then we stop &mdash; and episode 2 reads every file it made</li>
            </ul>
            """,
            say="By the end of this episode you will have Wagtail installed, a project created, "
                "and you will be logged into a real content management system. And then we stop. "
                "Because episode two reads every single file it just generated.",
        ),
        Scene(
            id="vs",
            body="""
            <h2>Wagtail vs Django vs WordPress</h2>
            <div class="cols">
              <div class="col">
                <h3>Django</h3>
                <p>A web framework.</p>
                <p><b>No content editing at all.</b></p>
              </div>
              <div class="col hero">
                <h3>Wagtail</h3>
                <p>Django apps that add a page tree and a real editor.</p>
                <p><b>Non-developers edit comfortably.</b></p>
              </div>
              <div class="col">
                <h3>WordPress</h3>
                <p>A PHP CMS with its own everything.</p>
                <p><b>Plugins instead of code.</b></p>
              </div>
            </div>
            """,
            say="First, where Wagtail sits. Django is a web framework with no content editing at "
                "all. WordPress is a PHP C M S with its own everything. Wagtail is in between: "
                "Django apps that add a page tree and a genuinely good editor on top of a normal "
                "Django project.",
        ),
        Scene(
            id="not_django_admin",
            body="""
            <h2>But Django already has an admin?</h2>
            <div class="quote" style="font-size:52px">The Django admin is a
            <span class="hl">database table editor</span> for staff.<br><br>
            Wagtail's is a <span class="hl">publishing tool</span> &mdash; drafts, previews,
            workflow, a page hierarchy, image cropping.</div>
            """,
            say="A fair question: Django already has an admin. But the Django admin is a database "
                "table editor, built for staff. Wagtail's admin is a publishing tool. Drafts, "
                "previews, workflow, a page hierarchy, image cropping. You would not hand a client "
                "the Django admin. You would hand them this.",
        ),
        Scene(
            id="when",
            body="""
            <div class="quote">Wagtail is what you reach for when you'd write a
            <span class="hl">Django site anyway</span> &mdash;<br>
            but somebody who isn't you<br>needs to change the words on it.</div>
            """,
            say="So here is the one sentence version. Wagtail is what you reach for when you would "
                "write a Django site anyway, but somebody who is not you needs to change the words "
                "on it.",
        ),

        # ---------------------------------------------------------- terminal: setup
        terminal_scene(
            scene_id="venv",
            eyebrow="Step 1",
            title="A folder and a virtualenv",
            bar="Windows &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="mkdir wagtail-unboxed", prompt=PS),
                Cmd(text="cd wagtail-unboxed", prompt=PS),
                Cmd(text="py -m venv .venv", prompt=PS),
                Cmd(text=".venv\\Scripts\\activate", prompt=PS),
            ],
            say="Start with an empty folder and a virtual environment. If you watched episode "
                "zero b, this is exactly what we practised. Make it, then activate it. Watch for "
                "the dot venv prefix on the prompt. On Mac and Linux the activate line is source "
                "dot venv slash bin slash activate.",
        ),
        terminal_scene(
            scene_id="install",
            eyebrow="Step 2",
            title="Install Wagtail",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text='pip install "wagtail==7.4.3" "Django==6.1.1"',
                    prompt="(.venv) PS&gt;",
                    out="Successfully installed Django-6.1.1 Pillow-12.3.0 Willow-1.12.0\n"
                        "  anyascii-0.3.3 beautifulsoup4-4.15.0 django-modelcluster-6.5\n"
                        "  django-taggit-6.1.0 django-treebeard-5.3.1 djangorestframework-3.18.1\n"
                        "  laces-0.1.2 modelsearch-1.3.2 telepath-0.3.1 wagtail-7.4.3",
                    highlight=["django-treebeard", "Pillow"]),
            ],
            say="Now install Wagtail. Watch the dependency list. Two worth naming. Treebeard, "
                "which is what stores the page tree. And Pillow, which is image processing, so "
                "Wagtail can generate resized versions of whatever you upload.",
        ),
        Scene(
            id="why_pin",
            body="""
            <h2>Why pin Django too?</h2>
            <pre class="code"><span class="c"># Wagtail 7.4 asks only for:</span>
Django &gt;= 5.2   <span class="c">... with no upper limit</span>

<span class="c"># so an unpinned install gives you whatever</span>
<span class="c"># Django shipped most recently</span></pre>
            <div class="sub" style="margin-top:36px">Pin both, and your screen matches mine.</div>
            """,
            say="You might wonder why we pinned Django as well as Wagtail. Because Wagtail seven "
                "four only asks for Django five point two or newer, with no upper limit. Unpinned, "
                "you get whatever Django shipped most recently, and three episodes from now your "
                "screen stops matching mine. Pin both.",
        ),
        terminal_scene(
            scene_id="start",
            eyebrow="Step 3",
            title="Create the project",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="wagtail --version", prompt="(.venv) PS&gt;",
                    out="You are using Wagtail 7.4.3", highlight=["7.4.3"]),
                Cmd(text="wagtail start studio site", prompt="(.venv) PS&gt;",
                    out="Creating a Wagtail project called studio using the default Wagtail template\n"
                        "Success! studio has been created",
                    highlight=["Success!"]),
            ],
            say="Check the version, then create the project. One command.",
        ),
        Scene(
            id="two_args",
            body="""
            <h2>Those two arguments</h2>
            <pre class="code">wagtail start <span class="k">studio</span> <span class="s">site</span></pre>
            <ul class="bullets" style="margin-top:50px">
              <li><b style="color:var(--teal)">studio</b> &mdash; the Django <b>project package</b> name. Ours is a design studio.</li>
              <li><b style="color:var(--amber)">site</b> &mdash; the <b>folder</b> to create it in. Wagtail makes it for you.</li>
            </ul>
            """,
            say="Those two arguments trip people up constantly, so let us be precise. Studio is the "
                "name of the Django project package. Ours is a design studio site. And site is the "
                "folder to create it in. Wagtail creates that folder for you, so you do not need to "
                "make it first.",
        ),
        Scene(
            id="never_site",
            body="""
            <div class="eyebrow">Costs people an afternoon</div>
            <h2>Never name your project <span style="color:var(--red)">site</span></h2>
            <div class="quote" style="font-size:46px">Python already has a built-in module called
            <span class="hl">site</span>.<br>
            Shadowing it gives you import errors that make no sense.<br><br>
            <span style="font-size:36px;color:var(--muted)">Same for
            <b>test</b>, <b>json</b>, <b>email</b>.</span></div>
            """,
            say="And one warning that genuinely costs people an afternoon. Do not name your project "
                "site. Python already has a built in module called site, and shadowing it gives you "
                "import errors that make no sense at all. The same goes for test, json, and email. "
                "The folder can be called site. The package cannot.",
        ),

        # ---------------------------------------------------------- terminal: run it
        terminal_scene(
            scene_id="migrate",
            eyebrow="Step 4",
            title="Create the database",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="cd site", prompt="(.venv) PS&gt;"),
                Cmd(text="python manage.py migrate", prompt="(.venv) PS&gt;",
                    # Trimmed to fit the box; the app list really is this long.
                    out="Operations to perform:\n"
                        "  Apply all migrations: admin, auth, contenttypes, home, sessions,\n"
                        "    taggit, wagtailadmin, wagtailcore, wagtaildocs, ...\n"
                        "Running migrations:\n"
                        "  Applying contenttypes.0001_initial... OK\n"
                        "  Applying auth.0001_initial... OK\n"
                        "  Applying admin.0001_initial... OK\n"
                        "  ... 180 more ...\n"
                        "  Applying wagtailusers.0015_userprofile_keyboard_shortcuts... OK",
                    highlight=["180 more"]),
            ],
            say="Now build the database. And look at what goes past: a hundred and eighty four "
                "migrations, before you have written a single line of code. Those are Wagtail's "
                "own tables. Pages, images, documents, revisions, permissions.",
        ),
        Scene(
            id="no_db_server",
            body="""
            <h2>No database server</h2>
            <div class="quote" style="font-size:52px">That created
            <span class="hl">db.sqlite3</span>, right there in the folder.<br><br>
            <span style="font-size:38px;color:var(--muted)">SQLite ships inside Python. Nothing to
            install, nothing to configure. Postgres arrives in episode 13.</span></div>
            """,
            say="And notice what you did not have to do. There is no database server. That created "
                "a file called d b dot sqlite three, right there in the folder. SQLite ships inside "
                "Python. Postgres turns up in episode thirteen, and not before.",
        ),
        terminal_scene(
            scene_id="superuser",
            title="Create your login",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py createsuperuser", prompt="(.venv) PS&gt;",
                    out="Username: admin\n"
                        "Email address: you@example.com\n"
                        "Password:\n"
                        "Password (again):\n"
                        "Superuser created successfully.",
                    highlight=["Superuser created successfully."]),
            ],
            say="Create your login. One thing that worries people: the password is invisible while "
                "you type it. Your keyboard is fine. Keep typing and press enter.",
        ),
        terminal_scene(
            scene_id="runserver",
            eyebrow="Step 5",
            title="Run it",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py runserver", prompt="(.venv) PS&gt;",
                    out="Watching for file changes with StatReloader\n"
                        "Performing system checks...\n\n"
                        "System check identified no issues (0 silenced).\n"
                        "Django version 6.1.1, using settings 'studio.settings.dev'\n"
                        "Starting development server at http://127.0.0.1:8000/\n"
                        "Quit the server with CTRL-BREAK.",
                    highlight=["http://127.0.0.1:8000/"]),
            ],
            say="And run it. Your site is now live on port eight thousand.",
        ),
        Scene(
            id="two_urls",
            body="""
            <h2>Two addresses</h2>
            <table>
              <tr><th>URL</th><th>What's there</th></tr>
              <tr><td class="k">127.0.0.1:8000</td><td class="v">The site. Right now, Wagtail's welcome page &mdash; we delete it in episode 4.</td></tr>
              <tr><td class="k" style="color:var(--teal)">127.0.0.1:8000/admin/</td><td class="v">The CMS. Log in with the superuser you just made.</td></tr>
            </table>
            """,
            say="Two addresses matter. The site itself, which right now shows Wagtail's welcome "
                "page, and we delete that in episode four. And slash admin, which is the C M S. "
                "Log in there with the superuser you just created.",
        ),
        Scene(
            id="one_page",
            body="""
            <div class="eyebrow">Something to notice</div>
            <h2>One page already exists</h2>
            <div class="quote" style="font-size:48px">You didn't create it.<br>
            <span class="hl">A migration did.</span><br><br>
            <span style="font-size:36px;color:var(--muted)">That file is one of the more surprising
            things in the box &mdash; and we open it next episode.</span></div>
            """,
            say="Open the pages section and notice something. A page already exists. You did not "
                "create it, and it did not come from a fixture. A migration made it, the first time "
                "you ran migrate. That file is one of the more surprising things in the box, and we "
                "open it next episode.",
        ),

        # ---------------------------------------------------------- wrap
        terminal_scene(
            scene_id="commit",
            eyebrow="Step 6",
            title="Commit it untouched",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git init -b main", prompt="(.venv) PS&gt;"),
                Cmd(text="git add -A", prompt="(.venv) PS&gt;"),
                Cmd(text='git commit -m "episode 1"', prompt="(.venv) PS&gt;"),
                Cmd(text="git tag ep01-end", prompt="(.venv) PS&gt;"),
            ],
            say="Last thing. Put it in git, and tag it. Gitignore the virtual environment, the "
                "database and the media folder. Your content is yours; the code is what gets "
                "shared.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 2 &mdash; Every file, explained</h2>
            <div class="quote" style="font-size:44px">29 files. Most tutorials explain three.<br>
            <span class="hl">We read all of them.</span></div>
            """,
            say="We are leaving that generated project completely untouched, because next episode "
                "is a guided tour of exactly this tree. Twenty nine files. Most tutorials explain "
                "three of them. We read all of them, including the ones you are told to ignore.",
        ),
    ],
)
