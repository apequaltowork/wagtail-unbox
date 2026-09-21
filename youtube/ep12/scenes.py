"""Ep 12 — Editor Experience Polish.

Scene spec for video/build.py.

The admin screenshots are the real admin, logged in as a user in the default
Editors group. The access table, the fresh-database permissions result and
the preview redirect are from real runs. See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 12'
VENV = "(.venv) PS&gt;"
PY = "&gt;&gt;&gt;"

SHOT_DASH = (HERE / "assets" / "shot-dashboard-crop.png").as_uri()
SHOT_ADD = (HERE / "assets" / "shot-addpage-crop.png").as_uri()

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
    key="ep12",
    number="12",
    title="Ep 12 - Editor Experience Polish",
    badge=BADGE,
    intro_say="The editor experience.",
    outro_say="Next episode, production settings. Thanks for watching.",
    scenes=[
        Scene(
            id="as_client",
            body="""
            <div class="eyebrow">Act 3 &mdash; shipping</div>
            <h2>Log in as the client</h2>
            <div class="sub" style="margin-top:36px">Every episode so far, we've been a
            <b>superuser</b>. The client won't be.<br><br>
            A user called <b>casey</b>, in Wagtail's default <b>Editors</b> group. Then look.</div>
            """,
            say="Every episode so far, we have been logged in as a superuser. The client will not be. "
                "So this episode starts by creating a user called Casey, putting them in Wagtail's "
                "default editors group, and looking at the admin through their eyes.",
        ),
        Scene(
            id="locked_out",
            body="""
            <div class="eyebrow">As casey, in the Editors group</div>
            <table>
              <tr><td class="k">/admin/pages/</td><td class="v" style="color:var(--teal)">200</td></tr>
              <tr><td class="k">Studio &rarr; Team</td><td class="v" style="color:var(--red)">302 &rarr; /admin/</td></tr>
              <tr><td class="k">Studio &rarr; Testimonials</td><td class="v" style="color:var(--red)">302 &rarr; /admin/</td></tr>
              <tr><td class="k">Settings &rarr; Studio settings</td><td class="v" style="color:var(--red)">302 &rarr; /admin/</td></tr>
            </table>
            <div class="sub" style="margin-top:30px">The menu items aren't even there. We built the
            team, the testimonials and the footer <b>for the client</b> &mdash; and the client
            can't open any of them.</div>
            """,
            say="Pages work. But the team, the testimonials and the studio settings all bounce straight "
                "back to the dashboard, and the menu items are not even there. We spent two episodes "
                "building those things for the client, and the client can not open any of them. The "
                "default editors group can edit pages, images and documents, and nothing we defined.",
        ),
        Scene(
            id="migration_why",
            body="""
            <h2>Permissions belong in a migration</h2>
            <div class="sub" style="margin-top:32px">Clicking in <b>Settings &rarr; Groups</b> fixes
            one database. A <b>data migration</b> fixes every copy &mdash; a colleague's laptop,
            staging, production.</div>
            <pre class="code" style="font-size:29px;margin-top:34px">GRANTS = [<span class="s">"change_teammember"</span>, <span class="s">"change_testimonial"</span>,
          <span class="s">"change_studiosettings"</span>, &hellip;]
editors.permissions.add(*Permission.objects.filter(codename__in=GRANTS))</pre>
            """,
            say="You could fix it by clicking in the groups screen. That fixes one database. Put it in a "
                "data migration and it fixes every copy of the site. A colleague's laptop, staging, and "
                "production. The obvious version looks like this. Find the permissions, add them to the "
                "group.",
        ),
        terminal_scene(
            scene_id="silent_fail",
            eyebrow="On a fresh database",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py migrate",
                    out="Applying home.0009_editors_can_edit_studio_content... OK",
                    prompt=VENV, highlight=["OK"]),
                Cmd(text="# Editors' home permissions", out="[]", prompt=VENV, error=["[]"]),
                Cmd(text="# ...and do the permissions exist?", out="True", prompt=VENV),
            ],
            say="Run it on a fresh database. Okay. The editors group got nothing. And yet, ask whether "
                "the permissions exist, and they do.",
        ),
        Scene(
            id="post_migrate",
            body="""
            <h2>Permissions are created after every migration</h2>
            <div class="sub" style="margin-top:28px">Django makes Permission rows in a
            <b>post_migrate</b> signal. On a fresh database they don't exist yet when your migration
            runs &mdash; so the filter matches nothing, it says OK, and a second later they appear.</div>
            <pre class="code" style="font-size:29px;margin-top:30px"><span class="k">for</span> app_config <span class="k">in</span> apps.get_app_configs():
    app_config.models_module = <span class="s">True</span>
    <span class="k">create_permissions</span>(app_config, apps=apps, verbosity=<span class="s">0</span>)
    app_config.models_module = <span class="s">None</span></pre>
            """,
            say="Django creates permission rows in a signal that runs after every migration has "
                "finished. On a fresh database they do not exist yet when our migration runs. So the "
                "filter finds nothing, the migration says okay, and a moment later the permissions "
                "appear, so nothing looks wrong. Create them first. And the nasty part. On my existing "
                "database, the broken version worked. It would only have failed in production.",
        ),
        Scene(
            id="after_perms",
            body="""
            <div class="eyebrow">After the migration, as casey</div>
            <table>
              <tr><td class="k">Studio &rarr; Team</td><td class="v" style="color:var(--teal)">200</td></tr>
              <tr><td class="k">Studio &rarr; Testimonials</td><td class="v" style="color:var(--teal)">200</td></tr>
              <tr><td class="k">Settings &rarr; Studio settings</td><td class="v" style="color:var(--teal)">200</td></tr>
            </table>
            <div class="sub" style="margin-top:30px">Tested on a fresh database: all seven permissions.</div>
            """,
            say="Fixed, and tested on a fresh database this time. All seven permissions, and Casey can "
                "open everything we built.",
        ),

        # ------------------------------------------------------- preview
        terminal_scene(
            scene_id="preview_broken",
            eyebrow="The bug we wrote in episode 10",
            title="",
            bar="ContactPage.serve_preview(request, mode)",
            steps=[
                Cmd(text="serve_preview(request, 'form')", out="200", prompt=PY, highlight=["200"]),
                Cmd(text="serve_preview(request, 'landing')", out="302 /contact/?sent=1",
                    prompt=PY, error=["302"]),
            ],
            say="Now a bug we wrote ourselves. The contact page has two preview modes. The form previews "
                "fine. The landing page preview redirects.",
        ),
        Scene(
            id="preview_fix",
            body="""
            <h2>The preview showed the live page</h2>
            <div class="sub" style="margin-top:26px">Wagtail's landing preview calls
            <b>render_landing_page</b> &mdash; which episode 10 turned into a redirect. An editor
            rewriting the thank-you text would preview the <b>published</b> one.</div>
            <pre class="code" style="font-size:28px;margin-top:30px"><span class="k">def</span> serve_preview(self, request, mode_name):
    <span class="k">if</span> mode_name == <span class="s">"landing"</span>:
        <span class="k">return</span> self.landing_response(request)   <span class="c"># the draft</span>
    <span class="k">return</span> <span class="k">super</span>().serve_preview(request, mode_name)</pre>
            """,
            say="In episode ten, we turned render landing page into a redirect, to fix the refresh "
                "problem. Wagtail's preview calls that same method. So the preview jumped to the live "
                "thank you page, and an editor rewriting the thank you message would only ever see the "
                "published version. Render the template directly for previews. I checked it against an "
                "unpublished draft, and the draft text now shows.",
        ),

        # ------------------------------------------------------- dashboard
        Scene(
            id="dashboard_hook",
            body="""
            <div class="filename">home/wagtail_hooks.py</div>
            <pre class="code" style="font-size:26px"><span class="k">class</span> RecentEnquiriesPanel(Component):
    template_name = <span class="s">"home/admin/recent_enquiries.html"</span>
    order = <span class="s">50</span>

    <span class="k">def</span> get_context_data(self, parent_context):
        context = <span class="k">super</span>().get_context_data(parent_context)
        forms = <span class="k">get_forms_for_user</span>(self.request.user)
        context[<span class="s">"submissions"</span>] = FormSubmission.objects.filter(
            page__in=forms).order_by(<span class="s">"-submit_time"</span>)[:<span class="s">5</span>]
        <span class="k">return</span> context

@hooks.register(<span class="s">"construct_homepage_panels"</span>)
<span class="k">def</span> add_recent_enquiries(request, panels):
    panels.append(RecentEnquiriesPanel(request))</pre>
            """,
            say="Now something for the client. The newest enquiries, right on the admin dashboard. A "
                "small component, registered with the construct homepage panels hook. Homepage here "
                "means the admin's own front page, not the website's.",
        ),
        Scene(
            id="dashboard_perms",
            body="""
            <div class="eyebrow">get_forms_for_user &mdash; the same rule as Forms</div>
            <table>
              <tr><td class="k">superuser</td><td class="v">panel shown &mdash; 2 enquiries</td></tr>
              <tr><td class="k">casey (Editors)</td><td class="v">panel shown &mdash; 2 enquiries</td></tr>
              <tr><td class="k">admin access only</td><td class="v" style="color:var(--red)">no panel</td></tr>
            </table>
            <div class="sub" style="margin-top:30px">Query every FormSubmission instead, and the
            dashboard shows enquiries to anyone who can log in.</div>
            """,
            say="The important line is get forms for user. It applies exactly the same permission rule "
                "as the forms screen. I checked three users. The superuser and Casey see the panel. A "
                "user who can only log in sees nothing. If you queried every submission instead, the "
                "dashboard would show enquiries, names and email addresses, to anyone with a login.",
        ),
        Scene(
            id="after_dashboard",
            body=f"""
            <div class="eyebrow">casey's dashboard &mdash; Studio and Settings are back</div>
            {shot("localhost:8000/admin/", SHOT_DASH, "86%")}
            """,
            say="And here is Casey's dashboard. Studio and Settings in the menu, and recent enquiries "
                "at the top.",
        ),

        # ------------------------------------------------------- small ones
        Scene(
            id="chooser_skipped",
            body="""
            <h2>The chooser that disappeared</h2>
            <div class="sub" style="margin-top:28px">Every page type now has a
            <b>page_description</b>, shown when an editor chooses between types.<br><br>
            But under Home, Journal and Contact are at their <b>max_count</b>. Only Standard page is
            allowed &mdash; so Wagtail <b>skips the chooser</b> and opens the form.</div>
            """,
            say="Every page type now has a page description, which Wagtail shows when an editor chooses "
                "between page types. And then I went to add a page under Home, and the chooser never "
                "appeared. The journal and the contact page are both at their max count, so only one "
                "type is allowed, and Wagtail skips straight to the form. That is episode seven's rules "
                "doing their job.",
        ),
        Scene(
            id="after_add",
            body=f"""
            <div class="eyebrow">Straight to the form &mdash; with every help_text we wrote</div>
            {shot("localhost:8000/admin/pages/3/add_subpage/", SHOT_ADD, "80%")}
            """,
            say="And every piece of help text we have written since episode three is right there, under "
                "its field. Including the alt text guidance from episode six.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 12"', prompt=VENV),
                Cmd(text="git tag ep12-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 13 &mdash; Production Settings</h2>
            <div class="sub" style="margin-top:36px">Postgres, environment variables, DEBUG off,
            static and media files &mdash; and the checklist Django already ships.</div>
            """,
            say="Next episode, production settings. Postgres, environment variables, debug off, and the "
                "checklist Django already ships with.",
        ),
    ],
)
