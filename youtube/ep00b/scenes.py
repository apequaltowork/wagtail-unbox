"""Ep 0b — Setting Up Your Machine.

Scene spec for video/build.py. Keep narration sentences short; long clauses
expose the synthetic voice.

Deliberate choices:
- The failure modes get their own slides. Setup episodes lose people at the
  errors, not at the happy path.
- Experienced viewers are told to leave in the first scene. Respecting their
  time is worth more than the watch-time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "video"))
from build import Episode, Scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 0b'

EPISODE = Episode(
    key="ep00b",
    number="0b",
    title="Ep 0b - Setting Up Your Machine",
    badge=BADGE,
    intro_say="Setting up your machine.",
    outro_say="That is your starting line. Next episode, we install Wagtail.",
    scenes=[
        Scene(
            id="skip",
            body="""
            <h2>Already set up?</h2>
            <div class="quote">If you have <span class="hl">Python 3.12</span>,
            <span class="hl">git</span>, and you know what a virtualenv is &mdash;<br>
            skip this one. Go straight to episode 1.</div>
            """,
            say="Before anything else. If you already have Python three twelve, git, and you "
                "know what a virtual environment is, skip this episode. Go straight to episode "
                "one. I will see you there.",
        ),
        Scene(
            id="checklist",
            body="""
            <h2>Four things. That's it.</h2>
            <div class="checks">
              <div class="yes">Python 3.12</div>
              <div class="yes">An editor</div>
              <div class="yes">git</div>
              <div class="yes">A terminal you're comfortable in</div>
            </div>
            """,
            say="For everyone else, this is short. We are installing four things. Python three "
                "twelve, an editor, git, and we will get comfortable with a terminal.",
        ),
        Scene(
            id="not_installing",
            body="""
            <h2>What we are <i>not</i> installing</h2>
            <div class="checks">
              <div class="no"><b>Postgres</b> &mdash; episodes 1 to 12 use SQLite, which ships inside Python</div>
              <div class="no"><b>Node.js</b> &mdash; there is no front-end build step in this series</div>
            </div>
            <div class="sub" style="margin-top:44px">Postgres arrives in episode 13, and we install it there.</div>
            """,
            say="And just as importantly, what we are not installing. No database server. "
                "Episodes one to twelve use SQLite, which already ships inside Python. Postgres "
                "turns up in episode thirteen and we install it there. And no Node. There is no "
                "front end build step in this series, at any point.",
        ),
        Scene(
            id="python_install",
            body="""
            <div class="eyebrow">Step 1</div>
            <h2>Python 3.12</h2>
            <table>
              <tr><th>Platform</th><th>How</th></tr>
              <tr><td class="k">Windows</td><td class="v">python.org installer &mdash; <b style="color:var(--amber)">tick "Add python.exe to PATH"</b></td></tr>
              <tr><td class="k">macOS</td><td class="v">brew install python@3.12</td></tr>
              <tr><td class="k">Linux</td><td class="v">sudo apt install python3.12 python3.12-venv</td></tr>
            </table>
            """,
            say="Step one, Python three point twelve. On Windows, use the installer from "
                "python dot org. On Mac, homebrew. On Debian or Ubuntu, apt &mdash; and note that "
                "the venv package is separate there. If you miss it, creating a virtual "
                "environment fails later with a confusing error.",
        ),
        Scene(
            id="path_box",
            body="""
            <div class="eyebrow">The single most common failure</div>
            <h2>Tick the PATH box</h2>
            <div class="quote">On the <span class="hl">first installer screen</span>,
            tick<br>&ldquo;Add python.exe to PATH&rdquo;.<br><br>
            <span style="font-size:38px;color:var(--muted)">Missed it? Re-run the installer &rarr;
            Modify &rarr; tick it.</span></div>
            """,
            say="Windows users, this one box causes more failed setups than everything else "
                "combined. On the first screen of the installer, tick add python dot e x e to "
                "path. If you already installed without it, run the installer again, choose "
                "modify, and tick it then.",
        ),
        Scene(
            id="verify_python",
            body="""
            <h2>Check it worked</h2>
            <div class="term">
              <div class="bar">Windows &nbsp;&middot;&nbsp; PowerShell</div>
              <div class="body"><span class="p">PS&gt;</span> py --version
<span class="o">Python 3.12.10</span>

<span class="p">PS&gt;</span> git --version
<span class="o">git version 2.50.0.windows.1</span></div>
            </div>
            <div class="sub" style="margin-top:34px">macOS / Linux: <span style="font-family:var(--mono)">python3 --version</span></div>
            """,
            say="Check it worked. On Windows, p y space minus minus version. On Mac and Linux, "
                "python three minus minus version. You want three point twelve something. If it "
                "says command not found on Windows, that is the path box.",
        ),
        Scene(
            id="editor",
            body="""
            <div class="eyebrow">Step 2</div>
            <h2>An editor</h2>
            <ul class="bullets">
              <li><b>VS Code</b> &mdash; free, cross-platform. Install the <b>Python</b> extension.</li>
              <li><span class="dim">PyCharm, Neovim, Sublime all work fine. VS Code is just what's on my screen.</span></li>
            </ul>
            """,
            say="Step two, an editor. I use VS Code with the Python extension, and that is what "
                "you will see on screen. But any editor works. PyCharm, Neovim, Sublime. Do not "
                "spend an afternoon on themes. Install it and move on.",
        ),
        Scene(
            id="git",
            body="""
            <div class="eyebrow">Step 3</div>
            <h2>git</h2>
            <pre class="code"><span class="c"># tell git who you are, once</span>
git config --global user.name <span class="s">"Your Name"</span>
git config --global user.email <span class="s">"you@example.com"</span></pre>
            <div class="sub" style="margin-top:36px">You need git to check out the episode tags.</div>
            """,
            say="Step three, git. Windows, use the installer from git dash s c m dot com and "
                "accept the defaults. Mac and Linux, one command. Then tell git who you are. "
                "You need git because every episode of this series ends on a tag you can check "
                "out.",
        ),
        Scene(
            id="venv_what",
            body="""
            <div class="eyebrow">Step 4 &mdash; the important one</div>
            <h2>What a virtualenv actually is</h2>
            <div class="quote" style="font-size:52px">A folder holding
            <span class="hl">one project's packages</span>.<br><br>
            <span style="font-size:36px;color:var(--muted)">Without it, every Python project on your
            machine shares one set of libraries &mdash; and two projects needing different Wagtail
            versions will fight.</span></div>
            """,
            say="Step four, and this is the one that matters. A virtual environment is just a "
                "folder that holds one project's packages. Without it, every Python project on "
                "your machine shares one set of libraries. Two projects that need different "
                "versions of Wagtail will fight, and you will lose an evening to it. With one, "
                "they never meet.",
        ),
        Scene(
            id="venv_make",
            body="""
            <h2>Make one</h2>
            <div class="term">
              <div class="bar">Windows</div>
              <div class="body"><span class="p">PS&gt;</span> py -m venv .venv
<span class="p">PS&gt;</span> .venv\\Scripts\\activate
<span class="p">(.venv) PS&gt;</span> <span class="cur"> </span></div>
            </div>
            <div class="sub" style="margin-top:34px">macOS / Linux:
            <span style="font-family:var(--mono)">python3 -m venv .venv</span> then
            <span style="font-family:var(--mono)">source .venv/bin/activate</span></div>
            """,
            say="Two commands. Make it, then activate it. On Mac and Linux the activate command "
                "is slightly different, and it is on screen now.",
        ),
        Scene(
            id="the_prefix",
            body="""
            <div class="quote">See that <span class="hl">(.venv)</span> in front of your prompt?<br><br>
            <span style="font-size:42px;color:var(--muted)">That prefix is the whole lesson.
            It means you are inside.</span></div>
            """,
            say="Look at your prompt. It now starts with dot venv in brackets. That prefix is "
                "the whole lesson. It means you are inside the environment.",
        ),
        Scene(
            id="the_trap",
            body="""
            <div class="eyebrow">The trap</div>
            <h2>A new terminal starts deactivated</h2>
            <div class="quote" style="font-size:50px">Every new window,<br>
            <span class="hl">activate again</span>.<br><br>
            <span style="font-size:36px;color:var(--muted)">This is the number one reason a command
            &ldquo;suddenly&rdquo; cannot find Wagtail three episodes from now.</span></div>
            """,
            say="Here is the trap. Opening a new terminal window starts you outside the "
                "environment again. You have to activate every single time. This is the number "
                "one reason that, three episodes from now, a command suddenly cannot find "
                "Wagtail. Nothing broke. You are just outside the venv.",
        ),
        Scene(
            id="exec_policy",
            body="""
            <div class="eyebrow">Windows only</div>
            <h2>&ldquo;running scripts is disabled&rdquo;</h2>
            <pre class="code">Set-ExecutionPolicy -Scope CurrentUser <span class="k">`</span>
                  -ExecutionPolicy RemoteSigned</pre>
            <div class="sub" style="margin-top:36px">Answer <b>Y</b>, then activate again.
            Affects your user account only.</div>
            """,
            say="One more Windows thing. If activate fails saying running scripts is disabled on "
                "this system, that is PowerShell's execution policy. Run the command on screen, "
                "answer yes, and try again. It only affects your own user account.",
        ),
        Scene(
            id="verify",
            body="""
            <h2>Your starting line</h2>
            <div class="term">
              <div class="bar">all three should succeed</div>
              <div class="body"><span class="p">PS&gt;</span> py --version
<span class="p">PS&gt;</span> git --version
<span class="p">PS&gt;</span> py -m venv --help</div>
            </div>
            <div class="sub" style="margin-top:34px">All three work? You're ready for episode 1.</div>
            """,
            say="Let us check everyone is in the same place. Three commands. Python, git, and "
                "venv support. If all three run without an error, you are ready.",
        ),
        Scene(
            id="cleanup",
            body="""
            <h2>Nothing Wagtail yet</h2>
            <ul class="bullets">
              <li>We have installed <b>no Wagtail</b> &mdash; that's episode 1's first command</li>
              <li>Delete the practice folder. The real project starts fresh.</li>
              <li><span class="dim">Something failed? Comment with your OS and the exact error.</span></li>
            </ul>
            """,
            say="Notice we have not installed Wagtail at all. That is deliberate. It is the first "
                "command of episode one. Delete the practice folder, because the real project "
                "starts from an empty directory. And if anything failed, leave a comment with "
                "your operating system and the exact error text.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 1 &mdash; What Wagtail Actually Is</h2>
            <div class="sub">Install it, create a project, and log into a real CMS admin.<br>
            Then we stop, and read every file it generated.</div>
            """,
            say="Next episode, we install Wagtail, create a project, and log into a real C M S "
                "admin. And then we stop, and read every single file it generated.",
        ),
    ],
)
