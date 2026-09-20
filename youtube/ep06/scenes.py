"""Ep 6 — Images & Documents.

Scene spec for video/build.py.

The focal-point slide uses two real renditions of the same image at the same
fill- spec, generated before and after setting a focal point. The rendition
audit numbers are from an actual run. See notes.md.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent.parent / "video"
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>UNBOXED</b> &nbsp;&middot;&nbsp; 06'
VENV = "(.venv) PS&gt;"

SHOT_HOME_TOP = (HERE / "assets" / "shot-home-top.png").as_uri()
SHOT_HOME_BOTTOM = (HERE / "assets" / "shot-home-bottom.png").as_uri()
SHOT_ABOUT = (HERE / "assets" / "shot-about-crop.png").as_uri()
FOCAL_BEFORE = (HERE / "assets" / "focal-before.jpg").as_uri()
FOCAL_AFTER = (HERE / "assets" / "focal-after.jpg").as_uri()

SHOT_CSS = """
<style>
.shot { border: 2px solid var(--line); border-radius: 14px; overflow: hidden;
        box-shadow: 0 30px 70px rgba(0,0,0,.45);
        /* These crops are taller than episode 4's, so hold them back from the
           full slide width or the bottom of the picture falls off the slide. */
        width: 78%; margin: 0 auto; }
.shot img { display: block; width: 100%; }
.shotbar { background: #161925; padding: 14px 22px; font-family: var(--mono);
           font-size: 24px; color: var(--muted); border-bottom: 2px solid var(--line); }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 56px;
        width: 82%; margin: 24px auto 0; }
.pair figure { margin: 0; }
.pair img { display: block; width: 100%; border-radius: 12px;
            box-shadow: 0 20px 50px rgba(0,0,0,.45); }
.pair figcaption { margin-top: 18px; font-family: var(--mono); font-size: 26px;
                   color: var(--muted); text-align: center; }
.pair .good { color: var(--teal); }
.pair .bad2 { color: var(--red); }
</style>
"""


def shot(url_label: str, src: str) -> str:
    return (SHOT_CSS +
            f'<div class="shot"><div class="shotbar">{url_label}</div>'
            f'<img src="{src}" alt=""></div>')


EPISODE = Episode(
    key="ep06",
    number="06",
    title="Ep 6 - Images & Documents",
    badge=BADGE,
    intro_say="Images, and documents.",
    outro_say="Next episode, the blog. Thanks for watching.",
    scenes=[
        # ------------------------------------------------------- the setup
        Scene(
            id="no_pictures",
            body="""
            <div class="eyebrow">Six episodes in</div>
            <h2>A design studio's site<br>with no pictures on it</h2>
            <div class="sub" style="margin-top:40px">Today that changes &mdash; and it is the
            first thing we make that <b>does not live in the repo</b>.</div>
            """,
            say="Six episodes into building a design studio's website, and there is not one image "
                "on it. Today we fix that. And this is the first episode where the thing we make "
                "does not live in the repository at all.",
        ),
        Scene(
            id="already_there",
            body="""
            <h2>Nothing to install</h2>
            <table>
              <tr><td class="k">wagtail.images</td><td class="v">in INSTALLED_APPS since episode 1</td></tr>
              <tr><td class="k">wagtail.documents</td><td class="v">same</td></tr>
              <tr><td class="k">MEDIA_ROOT / MEDIA_URL</td><td class="v">already in base.py</td></tr>
              <tr><td class="k">urls.py</td><td class="v">already serves media &mdash; <b>if DEBUG</b></td></tr>
              <tr><td class="k">media/</td><td class="v">gitignored &mdash; uploads are content</td></tr>
            </table>
            """,
            say="And there is nothing to install. We toured all of this back in episode two. The "
                "images app and the documents app have been sitting in installed apps since the "
                "first minute. Media root and media U R L are already in settings. The U R L "
                "config already serves uploaded files, but only when debug is on. Production is "
                "episode thirteen.",
        ),
        Scene(
            id="media_not_code",
            body="""
            <div class="eyebrow">Why media/ is gitignored</div>
            <h2>Uploads are content, not code</h2>
            <div class="quote" style="font-size:44px">Your repo holds the <span class="hl">site</span>.<br>
            The database and <b>media/</b> hold <span class="hl">what is in it</span>.</div>
            """,
            say="And this is worth being clear about. Your repository holds the site. The database "
                "and the media folder hold what is in it. Uploading an image is not a code change, "
                "which is why media is in git ignore, and why the images in this episode will not "
                "arrive when you check out the tag.",
        ),

        # ------------------------------------------------------- the field
        Scene(
            id="hero_field",
            body="""
            <div class="filename">home/models.py</div>
            <pre class="code" style="font-size:31px">hero_image = models.ForeignKey(
    <span class="s">"wagtailimages.Image"</span>,
    null=<span class="s">True</span>, blank=<span class="s">True</span>,
    on_delete=models.<span class="k">SET_NULL</span>,
    related_name=<span class="s">"+"</span>,
)</pre>
            <div class="sub" style="margin-top:36px">An image is a normal Django ForeignKey.
            Three arguments, all deliberate.</div>
            """,
            say="An image on a page is just a Django foreign key. There is no special image field. "
                "But three of these arguments matter, and people get them wrong.",
        ),
        Scene(
            id="set_null",
            body="""
            <div class="eyebrow">Get this one wrong and it hurts</div>
            <h2>SET_NULL, never CASCADE</h2>
            <table>
              <tr><td class="k" style="color:var(--red)">on_delete=CASCADE</td><td class="v">delete an image &rarr; <b>delete every page using it</b></td></tr>
              <tr><td class="k" style="color:var(--teal)">on_delete=SET_NULL</td><td class="v">delete an image &rarr; the page loses its hero</td></tr>
            </table>
            <div class="sub" style="margin-top:36px"><b>related_name="+"</b> because we never ask an
            image which pages use it.</div>
            """,
            say="Cascade would mean that deleting an image in the admin deletes every page that "
                "used it. An editor tidying up the image library could take out half the site. Set "
                "null means the page just loses its hero, which is what anybody would expect. And "
                "related name plus, because we never ask an image which pages are using it.",
        ),

        # ------------------------------------------------------- renditions
        Scene(
            id="renditions",
            body="""
            <h2>What {% image %} actually does</h2>
            <div class="sub" style="margin-bottom:28px">It does <b>not</b> resize on every request.</div>
            <pre class="code" style="font-size:30px"><span class="c"># first time</span>
generate a copy  &rarr;  media/images/&hellip;fill-800x350.jpg
record a <span class="k">row</span>      &rarr;  the rendition table

<span class="c"># every time after</span>
the row wins.

<span class="c"># and the original</span>
media/original_images/&hellip;  <span class="o">never touched</span></pre>
            """,
            say="So what does the image tag actually do. It does not resize anything on each "
                "request. The first time, it generates a copy, writes it into the media folder, and "
                "records a row in the rendition table. Every time after that, the row wins. And "
                "your original upload is never touched. Every rendition is a copy.",
        ),
        Scene(
            id="specs",
            body="""
            <h2>Filter specs</h2>
            <table>
              <tr><td class="k">width-800</td><td class="v">scale to 800 wide</td></tr>
              <tr><td class="k">fill-800x350</td><td class="v"><b>crops</b> &mdash; uses the focal point</td></tr>
              <tr><td class="k">max-1200x1200</td><td class="v">fit inside, never crop, never enlarge</td></tr>
              <tr><td class="k">min-500x500</td><td class="v">cover the box</td></tr>
              <tr><td class="k">format-webp</td><td class="v">change the output format</td></tr>
            </table>
            <div class="sub" style="margin-top:32px"><b>fill</b> crops. <b>max</b> does not.
            That is the whole distinction.</div>
            """,
            say="There are a handful of filter specs. Width scales. Fill crops to exactly the size "
                "you asked for. Max fits the image inside a box without cropping and without "
                "enlarging it. The one to remember is that fill crops and max does not.",
        ),
        Scene(
            id="srcset",
            body="""
            <div class="filename">home/includes/hero.html</div>
            <pre class="code" style="font-size:27px">{% <span class="k">srcset_image</span> page.hero_image
   fill-{800x350,1200x525,1600x700}
   sizes=<span class="s">"(max-width: 46rem) 100vw, 46rem"</span>
   alt=page.hero_alt %}</pre>
            <div class="sub" style="margin-top:36px">One tag, three renditions, a full srcset.
            Checked at 375px wide: the browser downloads the <b>800</b>, not the 1600.</div>
            """,
            say="And responsive images are one tag. Srcset image takes a list of specs, generates "
                "all three, and writes out a proper srcset and sizes attribute. I checked it at "
                "three hundred and seventy five pixels wide, and the browser downloads the eight "
                "hundred pixel file, not the sixteen hundred. Your phone visitors stop paying for "
                "desktop images.",
        ),

        # ------------------------------------------------------- focal points
        Scene(
            id="focal_problem",
            body=f"""
            <div class="eyebrow">Same image. Same fill-700x700.</div>
            {SHOT_CSS}
            <div class="pair">
              <figure><img src="{FOCAL_BEFORE}" alt="">
                <figcaption class="bad2">no focal point</figcaption></figure>
              <figure><img src="{FOCAL_AFTER}" alt="">
                <figcaption class="good">focal point set</figcaption></figure>
            </div>
            """,
            say="Now, cropping. These are two renditions of exactly the same image, at exactly the "
                "same fill spec. On the left, Wagtail crops from the centre and slices the subject "
                "off at the edge. On the right, the same crop, with a focal point set. That is the "
                "whole feature, and you set it by dragging a box in the admin.",
        ),
        Scene(
            id="focal_detail",
            body="""
            <h2>Two things to know about focal points</h2>
            <pre class="code" style="font-size:28px"><span class="c"># 1. the filename changes</span>
studio-hero.<span class="bad">2e16d0ba</span>.fill-700x700.jpg   <span class="c">before</span>
studio-hero.<span class="k">49a095d8</span>.fill-700x700.jpg   <span class="c">after</span></pre>
            <div class="sub" style="margin-top:32px">The focal point is part of the cache key, so a
            stale crop <b>cannot</b> be served.<br><br>
            <b>2.</b> Focal points only affect <b>fill-</b>. Nothing is cropped by
            <b>width-</b> or <b>max-</b>, so there is nothing to choose.</div>
            """,
            say="Two details. First, the filename changes when you set a focal point. That hash is "
                "part of the cache key, so a stale crop can never be served. And second, focal "
                "points only affect fill. Width and max do not crop anything, so there is nothing "
                "for a focal point to decide.",
        ),

        # ------------------------------------------------------- the gotcha
        Scene(
            id="gotcha",
            body="""
            <div class="eyebrow">The one that will catch you in production</div>
            <h2>Renditions are rows, not files</h2>
            <pre class="code" style="font-size:30px"><span class="c"># wagtail/images/models.py</span>
<span class="k">try</span>:
    rendition = self.find_existing_rendition(filter)
<span class="k">except</span> Rendition.DoesNotExist:
    rendition = self.create_rendition(filter)</pre>
            <div class="sub" style="margin-top:36px">It looks for a <b>database row</b>.
            It never checks whether the file is still on disk.</div>
            """,
            say="And here is the one that will catch you in production. Look at what get rendition "
                "actually does. It looks for a database row. If it finds one, it returns it. It "
                "never checks whether the file that row points at still exists.",
        ),
        Scene(
            id="gotcha_proof",
            body="""
            <div class="filename">after clearing media/images/</div>
            <pre class="code" style="font-size:32px">rows: 14 &nbsp;|&nbsp; <span class="bad">missing files: 11</span></pre>
            <div class="sub" style="margin-top:36px">Eleven rows pointing at files that are gone.
            The site puts every one of those URLs into <b>img src</b>, and every one is a
            <b>404</b>. Nothing in the logs says why.<br><br>
            A media restore, a new server, or somebody clearing disk space does this.</div>
            """,
            say="So I cleared out the rendition files and audited it. Fourteen rows, eleven of them "
                "pointing at files that no longer exist. And the site cheerfully puts all eleven "
                "U R Ls into image tags, and every single one is a four oh four. Nothing in the "
                "logs tells you why. This is not contrived. It is what happens after a media "
                "restore, or a move to a new server, or somebody clearing out disk space.",
        ),
        terminal_scene(
            scene_id="fix_renditions",
            eyebrow="The fix ships with Wagtail",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="python manage.py wagtail_update_image_renditions --purge-only",
                    out="Purging 14 rendition(s)\n"
                        "Successfully processed 14 rendition(s)",
                    prompt=VENV, highlight=["Successfully"]),
            ],
            say="And the fix ships with Wagtail. Purge the rendition rows, and they regenerate on "
                "the next request. After that the audit came back clean: nine rows, nine files, "
                "nothing missing. Put this one in your deployment notes.",
        ),

        # ------------------------------------------------------- alt text
        Scene(
            id="alt_default",
            body="""
            <div class="eyebrow">Read off the live page</div>
            <h2>The default alt text is a filing label</h2>
            <pre class="code" style="font-size:32px">{% image page.hero_image fill-800x350 %}
        &darr;
&lt;img alt=<span class="bad">"Studio hero"</span>&gt;</pre>
            <div class="sub" style="margin-top:36px">With no <b>alt</b>, Wagtail falls back to the
            <b>image title</b> &mdash; how it is filed in the CMS, not what it shows.</div>
            """,
            say="Now something that matters more than it looks. If you write the image tag with no "
                "alt attribute, Wagtail falls back to the image's title. Ours came out as alt "
                "equals Studio hero. That is how the image is filed in the C M S. It tells somebody "
                "using a screen reader absolutely nothing about the picture.",
        ),
        Scene(
            id="imageblock",
            body="""
            <h2>ImageBlock, not ImageChooserBlock</h2>
            <pre class="code" style="font-size:31px"><span class="k">class</span> CaptionedImageBlock(blocks.StructBlock):
    image = <span class="k">ImageBlock</span>()        <span class="c"># Wagtail 6.3+</span>
    caption = blocks.CharBlock(required=<span class="s">False</span>)
    width = blocks.ChoiceBlock(&hellip;)</pre>
            <div class="sub" style="margin-top:36px">It carries <b>alt text</b> and a
            <b>decorative</b> checkbox next to the image, so the person writing the page supplies
            them. Still behaves as an Image everywhere the old block did.</div>
            """,
            say="In a StreamField, the answer is image block, not image chooser block. It arrived in "
                "Wagtail six point three, and it carries alt text and a decorative checkbox right "
                "next to the image chooser, so the person writing the page is the one who supplies "
                "them. It still behaves as an image everywhere the old block did, so switching is "
                "cheap.",
        ),
        Scene(
            id="alt_opinion",
            body="""
            <div class="eyebrow">This episode's opinion</div>
            <h2>Alt text is content</h2>
            <div class="quote" style="font-size:44px">If your CMS makes alt text
            <span class="hl">optional and invisible</span>,<br>
            you will ship a site without it.</div>
            <div class="sub" style="margin-top:36px">On a plain ForeignKey there is nothing to
            inherit, so we added our own <b>hero_alt</b> field.</div>
            """,
            say="And here is the opinion. If your C M S makes alt text optional and invisible, you "
                "will ship a site without it. On the hero, which is a plain foreign key, there is "
                "nothing to inherit from, so we added our own hero alt field right next to the "
                "image chooser where nobody can miss it.",
        ),

        # ------------------------------------------------------- documents
        Scene(
            id="documents",
            body="""
            <div class="filename">home/blocks/download_block.html</div>
            <pre class="code" style="font-size:29px">&lt;a href=<span class="s">"</span>{{ value.document.url }}<span class="s">"</span> download&gt;
  {{ value.title|default:value.document.title }}
&lt;/a&gt;
{{ value.document.file_extension|upper }} &middot;
{{ value.document.file.size|filesizeformat }}</pre>
            <div class="sub" style="margin-top:32px">Renders as
            <b>Download our rate card &mdash; TXT &middot; 144 bytes</b>.</div>
            """,
            say="Documents work the same way, with a document chooser block. And the size and file "
                "type come straight off the document, so the visitor knows what they are about to "
                "download before they click it.",
        ),
        Scene(
            id="doc_url",
            body="""
            <h2>Documents are served by a <span class="hl">view</span></h2>
            <pre class="code" style="font-size:32px"><span class="o">/documents/1/rate-card.txt</span></pre>
            <div class="sub" style="margin-top:36px">Not a static file &mdash; a URL Wagtail
            handles. That is what makes <b>private documents</b> possible later.<br><br>
            Images are different: those really are plain files under <b>/media/</b>.</div>
            """,
            say="One thing to notice: that document U R L is not a static file path. Documents are "
                "served by a Wagtail view, which is exactly what makes private documents and "
                "permission checks possible later on. Images are different. Those really are plain "
                "files sitting under slash media.",
        ),
        Scene(
            id="custom_model",
            body="""
            <div class="eyebrow">Know it, don't do it today</div>
            <h2>WAGTAILIMAGES_IMAGE_MODEL</h2>
            <div class="sub" style="margin-top:32px">Swaps in your own image model, with extra
            fields &mdash; a credit line, a licence, an expiry date.<br><br>
            <b>Decide it on day one or not at all.</b> Retrofitting means migrating every image
            ForeignKey in the project.</div>
            """,
            say="One warning before we look at the result. There is a setting that lets you swap in "
                "your own image model, with extra fields like a photo credit or a licence. It is "
                "genuinely useful, and it is a day one decision. Retrofitting it onto a site that "
                "already has content means migrating every image foreign key in the project. Know "
                "it exists. Do not do it to this site today.",
        ),

        # ------------------------------------------------------- payoff
        Scene(
            id="after_home_top",
            body=f"""
            <div class="eyebrow">The hero</div>
            {shot("localhost:8000", SHOT_HOME_TOP)}
            """,
            say="And here is the result. A hero above the title, with its caption, cropped to a "
                "banner from an image nearly twice as wide as it needed to be.",
        ),
        Scene(
            id="after_home_bottom",
            body=f"""
            <div class="eyebrow">Further down the same page</div>
            {shot("localhost:8000", SHOT_HOME_BOTTOM)}
            """,
            say="And further down, the image block set to full width. Look at where it ends "
                "compared to the quote and the download underneath it. It genuinely breaks "
                "out past the text column. Its caption came from the editor, and the download "
                "shows its file type and its size before anybody clicks it.",
        ),
        Scene(
            id="after_about",
            body=f"""
            <div class="eyebrow">Cropped correctly, because of a focal point</div>
            {shot("localhost:8000/about/", SHOT_ABOUT)}
            """,
            say="And the About page. That is a tall portrait image being cropped into a wide "
                "banner, and the face is still in the middle of it, because the focal point tells "
                "Wagtail what the picture is actually of.",
        ),
        terminal_scene(
            scene_id="commit",
            eyebrow="Checkpoint",
            title="",
            bar="(.venv) &nbsp;&middot;&nbsp; PowerShell",
            steps=[
                Cmd(text="git add -A", prompt=VENV),
                Cmd(text='git commit -m "episode 6"', prompt=VENV),
                Cmd(text="git tag ep06-end", prompt=VENV),
            ],
            say="Commit, and tag. Remember the images themselves are not in there.",
        ),
        Scene(
            id="next",
            body="""
            <div class="eyebrow">Next</div>
            <h2>Ep 7 &mdash; Blog: Parent &amp; Child Pages</h2>
            <div class="sub" style="margin-top:36px">An index page and its posts,
            <b>subpage_types</b>, ordering, and pagination.</div>
            """,
            say="Next episode, the blog. An index page with posts underneath it, restricting which "
                "page types can go where, and pagination.",
        ),
    ],
)
