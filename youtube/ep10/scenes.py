"""Ep 10 — Forms That Work.

Scene spec for video/build.py.

Every number here is from a real run with the locmem email backend: the
500-after-saving, the refresh that resubmits, the redirect fix, the honeypot
and the CSRF 403. See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 10'
VENV = "(.venv) PS&gt;"

SHOT_CONTACT = (HERE / "assets" / "shot-contact.png").as_uri()
SHOT_SENT = (HERE / "assets" / "shot-sent.png").as_uri()

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
    key="ep10",
    number="10",
    title="Ep 10 - Forms That Work",
    badge=BADGE,
    intro_say="Forms that work.",
    outro_say="Next episode, search. Thanks for watching.",
    scenes=[
        Scene(
            id="no_contact",
            body="""
            <div class="eyebrow">Where we are</div>
            <h2>A studio you can't contact</h2>
            <div class="sub" style="margin-top:36px">A menu, a journal, a team &mdash; and no way to
            get in touch. Today: a contact form that <b>works</b>, which turns out to mean four
            separate things.</div>
            """,
            say="The site has a menu, a journal and a team, and no way to get in touch. Today we add a "
                "contact form. And a form that actually works turns out to mean four separate "
                "things, three of which the defaults get wrong.",
        ),
        Scene(
            id="models",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> FormField(AbstractFormField):
    page = ParentalKey(<span class="s">"ContactPage"</span>, on_delete=models.CASCADE,
                       related_name=<span class="s">"form_fields"</span>)

<span class="k">class</span> ContactPage(<span class="k">AbstractEmailForm</span>):
    intro = RichTextField(blank=<span class="s">True</span>)
    thank_you_text = RichTextField(blank=<span class="s">True</span>)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(), &hellip;,
        InlinePanel(<span class="s">"form_fields"</span>), &hellip; ]</pre>
            <div class="sub" style="margin-top:26px">The <b>editor</b> builds the form field by field.
            Every submission is stored, and emailed if a To address is set.</div>
            """,
            say="Two models. A form field, tied to the page with a parental key, and the contact page "
                "itself, which is an abstract email form. The editor builds the form in the admin, "
                "field by field. Every submission is stored in the database, and emailed if the "
                "page has a to address.",
        ),
        Scene(
            id="template",
            body="""
            <div class="filename">home/templates/home/contact_page.html</div>
            <pre class="code" style="font-size:28px">&lt;form action=<span class="s">"</span>{% pageurl page %}<span class="s">"</span> method=<span class="s">"post"</span>&gt;
  {% <span class="k">csrf_token</span> %}
  {% <span class="k">for</span> field <span class="k">in</span> form %}
    {{ field.label_tag }} {{ field }}
    {% <span class="k">for</span> error <span class="k">in</span> field.errors %}&hellip;{% <span class="k">endfor</span> %}
  {% <span class="k">endfor</span> %}
  &lt;button type=<span class="s">"submit"</span>&gt;Send&lt;/button&gt;
&lt;/form&gt;</pre>
            <div class="sub" style="margin-top:26px">Forget <b>csrf_token</b> and every submission is a
            <b>403</b>. That's the first thing, and the easy one.</div>
            """,
            say="The template loops over the form and prints each field with its errors. Leave out the "
                "C S R F token and every single submission is a four oh three forbidden. That is the "
                "first of the four things, and the easy one.",
        ),

        # ------------------------------------------------------- gotcha 1
        terminal_scene(
            scene_id="the_500",
            eyebrow="Submit it, before writing a thank-you page",
            title="",
            bar="measured with the locmem email backend",
            steps=[
                Cmd(text="POST /contact/",
                    out="500  TemplateDoesNotExist: home/contact_page_landing.html",
                    prompt="$", error=["500"]),
                Cmd(text="# and yet",
                    out="submissions saved: 1  |  emails sent: 1",
                    prompt="$", highlight=["saved"]),
            ],
            say="Second thing. Submit the form before you have written a thank you page. Five hundred. "
                "Template does not exist. And yet. The submission was saved, and the email was sent.",
        ),
        Scene(
            id="the_500_why",
            body="""
            <h2>An error page for a form that worked</h2>
            <div class="sub" style="margin-top:28px">The visitor sees a server error, assumes nothing
            happened, and sends it again. The studio gets <b>two</b> enquiries.</div>
            <pre class="code" style="font-size:30px;margin-top:32px">contact_page.html
contact_page<span class="k">_landing</span>.html   <span class="c"># same folder, same name + _landing</span></pre>
            """,
            say="Think about what the visitor sees. A server error. So they assume nothing happened, "
                "and they send it again, and the studio gets two enquiries. The thank you template is "
                "the page template's name plus underscore landing, in the same folder. Write it first.",
        ),

        # ------------------------------------------------------- gotcha 2
        terminal_scene(
            scene_id="refresh",
            eyebrow="Now refresh the thank-you page",
            title="",
            bar="measured with the locmem email backend",
            steps=[
                Cmd(text="POST /contact/", out="200   (not a redirect)", prompt="$", error=["200"]),
                Cmd(text="# refresh -- the browser POSTs again",
                    out="submissions: 2  |  emails: 2", prompt="$", error=["2"]),
            ],
            say="Third thing. Refresh the thank you page. Wagtail renders it as the direct response to "
                "the post, so refreshing makes the browser send the post again. Two submissions, two "
                "emails. Every refresh, another one.",
        ),
        Scene(
            id="prg",
            body="""
            <div class="eyebrow">Post / Redirect / Get</div>
            <pre class="code" style="font-size:27px"><span class="k">def</span> render_landing_page(self, request, form_submission=<span class="s">None</span>, *a, **kw):
    <span class="k">return</span> redirect(self.url + <span class="s">"?sent=1"</span>)

<span class="k">def</span> serve(self, request, *args, **kwargs):
    <span class="k">if</span> request.method == <span class="s">"GET"</span> <span class="k">and</span> request.GET.get(<span class="s">"sent"</span>):
        <span class="k">return</span> TemplateResponse(request,
            self.get_landing_page_template(request), self.get_context(request))
    <span class="k">return</span> <span class="k">super</span>().serve(request, *args, **kwargs)</pre>
            <div class="sub" style="margin-top:26px">Now: <b>302</b> &rarr; /contact/?sent=1. Refresh it
            twice &mdash; still <b>1</b> submission.</div>
            """,
            say="The fix is the oldest pattern on the web. Post, redirect, get. After a good "
                "submission, redirect to the contact page with sent equals one, and render the thank "
                "you template for that. Now the post answers with a three oh two, and I refreshed the "
                "thank you page twice. Still one submission.",
        ),

        # ------------------------------------------------------- gotcha 3
        Scene(
            id="dropdown",
            body="""
            <div class="eyebrow">The dropdown that lies</div>
            <h2>An optional dropdown has no blank choice</h2>
            <div class="sub" style="margin-top:28px">Wagtail builds it from the editor's choices and
            nothing else. So <b>Under &pound;5k</b> is selected, and the browser sends it.<br><br>
            Every enquiry records a budget nobody chose.</div>
            """,
            say="Fourth thing. The budget question is optional. But Wagtail builds a dropdown from the "
                "editor's choices and nothing else, so there is no blank option. Under five thousand "
                "is selected by default, and the browser sends it. Every single enquiry records a "
                "budget that the person never picked.",
        ),
        Scene(
            id="form_builder",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> StudioFormBuilder(FormBuilder):
    <span class="k">def</span> create_dropdown_field(self, field, options):
        form_field = <span class="k">super</span>().create_dropdown_field(field, options)
        <span class="k">if not</span> field.required:
            form_field.choices = [(<span class="s">""</span>, <span class="s">"Choose one (optional)"</span>)] \\
                                 + list(form_field.choices)
        <span class="k">return</span> form_field

<span class="k">class</span> ContactPage(AbstractEmailForm):
    form_builder = StudioFormBuilder</pre>
            """,
            say="A small custom form builder fixes it. If a dropdown is optional, put a blank choice "
                "in front of the editor's list. Tell the page to use it, and a budget left blank is "
                "now stored as blank.",
        ),

        # ------------------------------------------------------- spam
        Scene(
            id="honeypot",
            body="""
            <h2>A honeypot for spam</h2>
            <table>
              <tr><td class="k">what</td><td class="v">an ordinary text input, moved off-screen with CSS</td></tr>
              <tr><td class="k">people</td><td class="v">never see it &mdash; <b>tabindex -1</b>, aria-hidden</td></tr>
              <tr><td class="k">bots</td><td class="v">fill in every input they find</td></tr>
              <tr><td class="k">filled in</td><td class="v"><b>302</b>, same thank-you page, <b>0</b> stored, <b>0</b> emailed</td></tr>
            </table>
            <div class="sub" style="margin-top:28px">Not <b>type="hidden"</b> &mdash; bots skip those.
            And don't tell the bot it failed.</div>
            """,
            say="And spam. A honeypot is an ordinary text input, pushed off screen with C S S. People "
                "never see it, and keyboard users can not tab into it. Bots fill in every input they "
                "find. If it comes back filled in, the bot gets exactly the same thank you page, and "
                "nothing is stored or sent. Do not make it a hidden input, because bots skip those. "
                "And never tell the bot that it failed.",
        ),
        Scene(
            id="email_dev",
            body="""
            <div class="eyebrow">Where the email goes in development</div>
            <pre class="code" style="font-size:30px"><span class="c"># studio/settings/dev.py -- already there</span>
EMAIL_BACKEND = <span class="s">"django.core.mail.backends.console.EmailBackend"</span></pre>
            <pre class="code" style="font-size:28px;margin-top:26px">Your name: Sam
Email: sam@example.com
Budget: &pound;5k&ndash;&pound;15k
About the project: A new site.</pre>
            <div class="sub" style="margin-top:22px">It prints in the runserver terminal. Real sending
            is episode 13.</div>
            """,
            say="In development, the email does not go anywhere. The development settings already use "
                "the console backend, so it prints in the terminal running the server. That is the "
                "whole email. Real sending is episode thirteen.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="after_form",
            body=f"""
            <div class="eyebrow">In the menu by itself &mdash; episode 9's default</div>
            {shot("localhost:8000/contact/", SHOT_CONTACT, "58%")}
            """,
            say="And here is the form. Notice contact appeared in the menu on its own, because of the "
                "show in menus default from last episode.",
        ),
        Scene(
            id="after_sent",
            body=f"""
            <div class="eyebrow">/contact/?sent=1 &mdash; refresh it all you like</div>
            {shot("localhost:8000/contact/?sent=1", SHOT_SENT, "66%")}
            """,
            say="And the thank you page, at its own address. Refresh it as often as you like.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 10"', prompt=VENV),
                Cmd(text="git tag ep10-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 11 &mdash; Search</h2>
            <div class="sub" style="margin-top:36px">The <b>search/</b> app we unboxed in episode 2,
            finally doing something.</div>
            """,
            say="Next episode, search. The search app we unboxed in episode two, finally doing "
                "something.",
        ),
    ],
)
