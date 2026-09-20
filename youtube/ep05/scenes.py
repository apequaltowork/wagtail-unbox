"""Ep 5 — StreamField, Properly.

Scene spec for video/build.py.

The two gotchas in here are both real and both were hit while building this
episode: the JSON_VALID migration failure, and Wagtail's automatic per-block
wrapper class. See notes.md for the measurements behind the proof slides.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 05'
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
    key="ep05",
    number="05",
    title="Ep 5 - StreamField, Properly",
    badge=BADGE,
    intro_say="StreamField, properly.",
    outro_say="Next episode, images and documents. Thanks for watching.",
    scenes=[
        # ------------------------------------------------------- the problem
        Scene(
            id="one_blob",
            body="""
            <div class="eyebrow">Where we are</div>
            <h2>One field. One blob.</h2>
            <pre class="code" style="font-size:36px">body = <span class="k">RichTextField</span>(blank=True)</pre>
            <div class="sub" style="margin-top:40px">One box. The editor can put anything in it,
            and you have no say in what comes out the other end.</div>
            """,
            say="Right now the body of every page is a single rich text field. One box. The editor "
                "can put anything they like in it, and you, the person who designed the site, have "
                "no say at all in what comes out the other end.",
        ),
        Scene(
            id="what_it_is",
            body="""
            <h2>What StreamField actually is</h2>
            <div class="quote" style="font-size:44px">A <span class="hl">JSON column</span> holding an
            <span class="hl">ordered list of typed blocks</span>.</div>
            <div class="sub" style="margin-top:40px">Not a rich text editor with extras.
            Remember the JSON part &mdash; it explains the error we hit in four minutes.</div>
            """,
            say="So what is StreamField. It is not a fancier rich text editor. It is a JSON column "
                "holding an ordered list of typed blocks. Hold on to the JSON part of that "
                "sentence, because it explains an error we are going to hit in about four minutes.",
        ),
        Scene(
            id="hierarchy",
            body="""
            <h2>Four kinds of block</h2>
            <table>
              <tr><th>Block</th><th>What it is</th></tr>
              <tr><td class="k">CharBlock, RichTextBlock&hellip;</td><td class="v">primitives &mdash; one value</td></tr>
              <tr><td class="k">StructBlock</td><td class="v">a <b>record</b> &mdash; these fields go together</td></tr>
              <tr><td class="k">ListBlock</td><td class="v">a <b>repeat</b> &mdash; several of the same thing</td></tr>
              <tr><td class="k">StreamBlock</td><td class="v">a <b>choice</b> &mdash; pick any, in any order</td></tr>
            </table>
            """,
            say="There are four kinds of block and they nest inside each other. Primitives hold one "
                "value. A struct block is a record: these fields belong together. A list block is a "
                "repeat: several of the same thing. And a stream block is a choice: pick any of "
                "these, in any order. That last one is the body field itself.",
        ),
        Scene(
            id="struct_vs_list",
            body="""
            <div class="eyebrow">The two people mix up</div>
            <h2>Struct is a record. List is a repeat.</h2>
            <pre class="code" style="font-size:33px"><span class="k">class</span> ServiceBlock(blocks.<span class="k">StructBlock</span>):
    name = blocks.CharBlock(max_length=<span class="s">80</span>)
    description = blocks.TextBlock(rows=<span class="s">3</span>)

<span class="c"># and then, several of them:</span>
services = blocks.<span class="k">ListBlock</span>(ServiceBlock())</pre>
            """,
            say="These two are the ones everybody confuses. A service has a name and a description, "
                "and those two always travel together, so that is a struct block. A studio offers "
                "several services, so we wrap it in a list block. Struct, then list. Record, then "
                "repeat.",
        ),

        # ------------------------------------------------------- blocks.py
        Scene(
            id="quote_block",
            body="""
            <div class="filename">home/blocks.py</div>
            <pre class="code" style="font-size:32px"><span class="k">class</span> QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(rows=<span class="s">3</span>)
    attribution = blocks.CharBlock(required=<span class="s">False</span>)

    <span class="k">class</span> Meta:
        icon = <span class="s">"openquote"</span>
        label = <span class="s">"Pull quote"</span>
        template = <span class="s">"home/blocks/quote_block.html"</span></pre>
            <div class="sub" style="margin-top:36px"><b>Meta</b> is what the editor sees:
            the icon in the menu, the label, and the template it renders through.</div>
            """,
            say="Here is the first real block. A quote, and an optional attribution. The fields are "
                "constructor arguments. Everything in Meta is about presentation: the icon that "
                "shows in the block menu, the label the editor reads, and the template it renders "
                "through on the front end.",
        ),
        Scene(
            id="services_block",
            body="""
            <div class="filename">home/blocks.py</div>
            <pre class="code" style="font-size:31px"><span class="k">class</span> ServicesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(default=<span class="s">"What we do"</span>)
    services = blocks.<span class="k">ListBlock</span>(ServiceBlock(),
                                min_num=<span class="s">1</span>, max_num=<span class="s">6</span>)

    <span class="k">class</span> Meta:
        icon = <span class="s">"list-ul"</span>
        label = <span class="s">"Services"</span>
        template = <span class="s">"home/blocks/services_block.html"</span></pre>
            <div class="sub" style="margin-top:36px">A struct <b>containing</b> a list. This is the
            pattern worth remembering.</div>
            """,
            say="And this is the pattern worth remembering. A struct block containing a list block. "
                "A heading that appears once, and then between one and six services under it. Min "
                "num and max num are the guard rails you hand the client.",
        ),
        Scene(
            id="body_block",
            body="""
            <div class="filename">home/blocks.py &nbsp;&middot;&nbsp; the top-level block</div>
            <pre class="code" style="font-size:31px"><span class="k">class</span> BodyBlock(blocks.<span class="k">StreamBlock</span>):
    heading   = blocks.CharBlock(icon=<span class="s">"title"</span>, &hellip;)
    paragraph = blocks.RichTextBlock(icon=<span class="s">"pilcrow"</span>, &hellip;)
    quote     = QuoteBlock()
    services  = ServicesBlock()
    cta       = CTABlock()

    <span class="k">class</span> Meta:
        block_counts = {<span class="s">"services"</span>: {<span class="s">"max_num"</span>: <span class="s">1</span>}}</pre>
            <div class="sub" style="margin-top:32px">Five things an editor may add. Rich text is
            still here &mdash; it is now <b>one block among several</b>, not the whole field.</div>
            """,
            say="And the top level block collects them. Five things an editor is allowed to add to a "
                "page. Notice rich text has not gone away. It is still here, it is just one block "
                "among several now instead of being the entire field.",
        ),
        Scene(
            id="model_change",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:34px"><span class="bad">- body = RichTextField(blank=True)</span>
<span class="k">+ body = StreamField(BodyBlock(), blank=True)</span></pre>
            <div class="sub" style="margin-top:40px">Two lines, on both <b>HomePage</b> and
            <b>StandardPage</b>. The panel doesn't change at all.</div>
            """,
            say="The model change is two lines, on both page types. And the content panel underneath "
                "does not change one character. It is still just a field panel pointing at body.",
        ),
        Scene(
            id="no_use_json",
            body="""
            <div class="eyebrow">Don't copy this from older tutorials</div>
            <h2>use_json_field is dead</h2>
            <pre class="code" style="font-size:32px">body = StreamField(BodyBlock(), <span class="bad">use_json_field=True</span>)

<span class="c"># wagtail/fields.py, 7.4:
# "Ignored, but retained for compatibility
#  with historical migrations."</span></pre>
            """,
            say="One warning before we migrate. Nearly every StreamField tutorial you will find tells "
                "you to pass use json field equals true. That was needed before Wagtail six. In "
                "seven point four the parameter is still accepted and, in Wagtail's own words, "
                "ignored. Don't type it into new code.",
        ),

        # ------------------------------------------------------- the failure
        terminal_scene(
            scene_id="migrate_fail",
            eyebrow="And now it breaks",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py makemigrations home",
                    out="Migrations for 'home':\n"
                        "  home\\migrations\\0004_alter_homepage_body_alter_standardpage_body.py\n"
                        "    ~ Alter field body on homepage\n"
                        "    ~ Alter field body on standardpage",
                    prompt=VENV),
                Cmd(text="python manage.py migrate",
                    out="django.db.utils.IntegrityError: CHECK constraint failed:\n"
                        "(JSON_VALID(\"body\") OR \"body\" IS NULL)",
                    prompt=VENV,
                    error=["IntegrityError", "JSON_VALID"]),
            ],
            say="So. Make migrations, migrate, and it blows up. Integrity error. Check constraint "
                "failed. J SON valid body.",
        ),
        Scene(
            id="why_fail",
            body="""
            <h2>Nothing in that message says StreamField</h2>
            <pre class="code" style="font-size:32px"><span class="c"># the About page, written in episode 3:</span>
body = <span class="s">'&lt;p&gt;We are a small studio.&lt;/p&gt;'</span>

<span class="c"># the new column:</span>
<span class="k">JSON</span>  &mdash; and that string is <span class="bad">not JSON</span></pre>
            <div class="sub" style="margin-top:36px">Every viewer following along will hit this,
            because you wrote content into that field two episodes ago.</div>
            """,
            say="And nothing in that message says the word StreamField. Here is what it means. Back "
                "in episode three you typed some text into the About page, so that column holds a "
                "paragraph of H T M L. The new column is JSON, and a paragraph of H T M L is not "
                "JSON. Every single person following along will hit this.",
        ),
        Scene(
            id="nothing_broken",
            body="""
            <div class="eyebrow">Before you panic</div>
            <h2>Nothing is broken</h2>
            <div class="term">
              <div class="bar">(.venv) &middot; PowerShell</div>
              <div class="body"><span class="p">PS&gt;</span> python manage.py showmigrations home
 [X] 0003_standardpage_homepage_body_homepage_intro
 <span class="hl-out">[ ] 0004_alter_homepage_body_alter_standardpage_body</span></div>
            </div>
            <div class="sub" style="margin-top:36px">Django runs migrations in a transaction. It
            rolled the whole thing back. Your data is untouched.</div>
            """,
            say="And before you panic: nothing is broken. Django runs a migration inside a "
                "transaction, so when it failed it rolled the whole thing back. Show migrations "
                "still lists oh oh oh four as not applied, and your content is exactly where it "
                "was. On Postgres you get a different message for the same cause, and the same fix.",
        ),

        # ------------------------------------------------------- the fix
        Scene(
            id="the_fix",
            body="""
            <h2>The fix: convert the data <span class="hl">first</span></h2>
            <pre class="code" style="font-size:33px">operations = [
    migrations.<span class="k">RunPython</span>(html_to_stream, stream_to_html),
    migrations.AlterField(&hellip;),   <span class="c"># homepage</span>
    migrations.AlterField(&hellip;),   <span class="c"># standardpage</span>
]</pre>
            <div class="sub" style="margin-top:40px">Order is the whole trick. The RunPython runs
            <b>while the column is still plain text</b>.</div>
            """,
            say="The fix is to hand edit the migration Django just generated, and convert the data "
                "before the column changes type. The order is the entire trick. That run python "
                "runs while the column is still plain text, so it can read the H T M L out and "
                "write valid JSON back in.",
        ),
        Scene(
            id="run_python",
            body="""
            <div class="filename">home/migrations/0004_&hellip;.py</div>
            <pre class="code" style="font-size:29px"><span class="k">def</span> html_to_stream(apps, schema_editor):
    <span class="k">for</span> model_name <span class="k">in</span> (<span class="s">"HomePage"</span>, <span class="s">"StandardPage"</span>):
        Model = apps.get_model(<span class="s">"home"</span>, model_name)
        <span class="k">for</span> page <span class="k">in</span> Model.objects.all():
            html = (page.body <span class="k">or</span> <span class="s">""</span>).strip()
            blocks = [{<span class="s">"type"</span>: <span class="s">"paragraph"</span>,
                       <span class="s">"value"</span>: html,
                       <span class="s">"id"</span>: str(uuid.uuid4())}] <span class="k">if</span> html <span class="k">else</span> []
            Model.objects.filter(pk=page.pk).update(
                body=json.dumps(blocks))</pre>
            <div class="sub" style="margin-top:28px">Each page's HTML becomes one
            <b>paragraph</b> block. Every block needs a <b>type</b>, a <b>value</b> and a unique
            <b>id</b>.</div>
            """,
            say="And this is it. Take whatever H T M L is in the field, wrap it as a single "
                "paragraph block, and write it back as JSON. Note the shape of a block: a type, a "
                "value, and a unique id. That id matters, it is how Wagtail tracks a block across "
                "revisions. Write the reverse function too. It is six more lines and it means you "
                "can undo this.",
        ),
        terminal_scene(
            scene_id="migrate_ok",
            eyebrow="Again",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py migrate",
                    out="Applying home.0004_alter_homepage_body_alter_standardpage_body... OK",
                    prompt=VENV, highlight=["OK"]),
            ],
            say="Run it again, and it applies. And the About page's paragraph is still there, now "
                "living inside a block.",
        ),
        Scene(
            id="block_lookup",
            body="""
            <div class="eyebrow">Don't be alarmed by the rest of the file</div>
            <h2>block_lookup</h2>
            <pre class="code" style="font-size:26px">field=wagtail.fields.StreamField(
    [(<span class="s">'heading'</span>, 0), (<span class="s">'paragraph'</span>, 1), (<span class="s">'quote'</span>, 4), &hellip;],
    block_lookup={0: (<span class="s">'wagtail.blocks.CharBlock'</span>, (), {&hellip;}),
                  1: (<span class="s">'wagtail.blocks.RichTextBlock'</span>, (), {&hellip;}), &hellip;})</pre>
            <div class="sub" style="margin-top:36px">Wagtail 7's compact migration format &mdash;
            each block defined once, then referenced by number. Unreadable, and that's fine.
            Nobody hand-edits this half.</div>
            """,
            say="While we are in there, the rest of that file looks horrifying. That is Wagtail "
                "seven's compact migration format. Every block definition is written once and then "
                "referred to by number. It is unreadable and it is meant to be. Nobody hand edits "
                "that half. We only touched the top.",
        ),

        # ------------------------------------------------------- templates
        Scene(
            id="template_line",
            body="""
            <div class="filename">home_page.html &nbsp;and&nbsp; standard_page.html</div>
            <pre class="code" style="font-size:36px"><span class="bad">- {{ page.body|richtext }}</span>
<span class="k">+ {{ page.body }}</span></pre>
            <div class="sub" style="margin-top:40px">StreamField renders every block through its own
            template. There is nothing left to filter.</div>
            """,
            say="The page templates get one line shorter. The rich text filter goes, because "
                "StreamField renders every block through that block's own template. There is "
                "nothing left for a filter to do.",
        ),
        Scene(
            id="block_templates",
            body="""
            <div class="filename">home/templates/home/blocks/quote_block.html</div>
            <pre class="code" style="font-size:33px">&lt;blockquote&gt;
  &lt;p&gt;{{ value.quote }}&lt;/p&gt;
  {% <span class="k">if</span> value.attribution %}
    &lt;cite&gt;{{ value.attribution }}&lt;/cite&gt;
  {% <span class="k">endif</span> %}
&lt;/blockquote&gt;</pre>
            <div class="sub" style="margin-top:36px">Inside a block template the block is called
            <b>value</b>. A StructBlock's fields hang off it by name.</div>
            """,
            say="And a block template is tiny. Inside one, the block is always called value, and a "
                "struct block's fields hang off it by name. Value dot quote, value dot attribution. "
                "That is the whole API.",
        ),

        # ------------------------------------------------------- gotcha 2
        Scene(
            id="gotcha2",
            body="""
            <div class="eyebrow">This cost me ten minutes</div>
            <h2>A teal box inside a teal box</h2>
            <div class="quote" style="font-size:44px">My call-to-action rendered
            <span class="hl">twice the height</span> it should have &mdash;<br>
            and the CSS was right.</div>
            """,
            say="And here is this episode's ten minute lesson. My call to action rendered as a teal "
                "box inside another teal box, twice the height it should have been. And the C S S "
                "was correct.",
        ),
        Scene(
            id="gotcha2_proof",
            body="""
            <div class="filename">measured in the live page</div>
            <pre class="code" style="font-size:28px">[...document.querySelectorAll(<span class="s">'.block-cta'</span>)]
    .map(e =&gt; e.tagName + <span class="s">'.'</span> + e.className)

<span class="bad">// ["DIV.w-block-cta block-cta",
//  "ASIDE.block-cta"]</span></pre>
            <div class="sub" style="margin-top:36px">Wagtail 7 already wraps every block in
            <b>&lt;div class="w-block-NAME <span class="hl">block-NAME</span>"&gt;</b>.
            My template added the same class again.</div>
            """,
            say="Two elements matched. Wagtail seven already wraps every block in a div, and that "
                "div already carries a class named after the block. Block dash c t a. My template "
                "added a class with exactly the same name, so the styling landed twice.",
        ),
        Scene(
            id="gotcha2_fix",
            body="""
            <h2>Style the wrapper Wagtail gives you</h2>
            <pre class="code" style="font-size:32px"><span class="c">/* not this */</span>
<span class="bad">&lt;aside class="block-cta"&gt;&hellip;</span>

<span class="c">/* this */</span>
<span class="k">.block-quote blockquote</span> { border-left: 3px solid &hellip; }
<span class="k">.block-cta p</span>           { margin: 0 0 1rem; }</pre>
            <div class="sub" style="margin-top:36px">Fewer lines &mdash; and every block you add
            later gets a wrapper class for free.</div>
            """,
            say="So delete the wrapper class from your templates and style Wagtail's instead. It is "
                "fewer lines, and every block you add later gets a wrapper class for free without "
                "you doing anything.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="admin_payoff",
            body="""
            <div class="eyebrow">What the client sees</div>
            <h2>One "+", five choices</h2>
            <table>
              <tr><td class="k">Heading</td><td class="v">one line of text</td></tr>
              <tr><td class="k">Paragraph</td><td class="v">rich text, restricted features</td></tr>
              <tr><td class="k">Pull quote</td><td class="v">quote + attribution</td></tr>
              <tr><td class="k">Services</td><td class="v">heading + 1&ndash;6 services</td></tr>
              <tr><td class="k">Call to action</td><td class="v">text, button, page chooser</td></tr>
            </table>
            <div class="sub" style="margin-top:32px">Drag to reorder. This is why StreamField
            exists.</div>
            """,
            say="And this is the payoff, in the admin. One plus button opens a menu of exactly five "
                "things, with the icons and labels we set in Meta. Add them, drag them into any "
                "order you like. The editor gets freedom, you keep control of what the page can "
                "contain. That is the whole reason StreamField exists.",
        ),
        Scene(
            id="counts",
            body="""
            <h2>Two ways to say "max"</h2>
            <table>
              <tr><td class="k">block_counts on StreamBlock</td><td class="v">caps a block <b>type</b> across the whole stream</td></tr>
              <tr><td class="k">max_num on ListBlock</td><td class="v">caps items <b>inside</b> one list</td></tr>
            </table>
            <div class="sub" style="margin-top:40px">One services section per page.
            Up to six services in it.</div>
            """,
            say="Two settings, same word, different jobs. Block counts on the stream block limits how "
                "many of a block type the whole page may have. Max num on the list block limits how "
                "many items go inside one list. One services section per page. Up to six services "
                "in it.",
        ),
        Scene(
            id="after_home",
            body=f"""
            <div class="eyebrow">Four blocks, four templates</div>
            {shot("localhost:8000", SHOT_HOME)}
            """,
            say="And here is the home page. A paragraph, a services grid, a pull quote, and a call to "
                "action whose button link came out of the page chooser. Four blocks, four templates, "
                "all ordered by the editor.",
        ),
        Scene(
            id="after_about",
            body=f"""
            <div class="eyebrow">And the migrated content</div>
            {shot("localhost:8000/about/", SHOT_ABOUT)}
            """,
            say="And the About page. That first paragraph is the one we wrote in episode three, "
                "carried across by the data migration, with a new heading block underneath it. "
                "Nothing was lost.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 5"', prompt=VENV),
                Cmd(text="git tag ep05-end", prompt=VENV),
            ],
            say="Commit, and tag.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 6 &mdash; Images &amp; Documents</h2>
            <div class="sub" style="margin-top:36px">Renditions, focal points, and
            <b>ImageChooserBlock</b> &mdash; the block everybody wanted today.</div>
            """,
            say="Next episode, images and documents. Renditions, focal points, and the image chooser "
                "block, which is the block everybody wanted today.",
        ),
    ],
)
