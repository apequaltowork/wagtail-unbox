"""Content blocks for the studio site.

A StreamField is a list of blocks. This file defines the blocks an editor is
allowed to choose from, smallest first:

    QuoteBlock     - a StructBlock: several fields that belong together
    ServicesBlock  - a StructBlock containing a ListBlock: a repeating group
    CTABlock       - a StructBlock that links to a page or an external URL

and BodyBlock at the bottom, which is the StreamBlock the model actually uses.

Every block that needs custom HTML names its own template. Blocks without a
`template` fall back to Wagtail's default rendering, which for a RichTextBlock
is exactly what we want.
"""

from wagtail import blocks


class QuoteBlock(blocks.StructBlock):
    """A pull quote with an optional attribution line."""

    quote = blocks.TextBlock(rows=3)
    attribution = blocks.CharBlock(
        required=False,
        max_length=120,
        help_text="Who said it. Leave blank for an unattributed quote.",
    )

    class Meta:
        icon = "openquote"
        label = "Pull quote"
        template = "home/blocks/quote_block.html"


class ServiceBlock(blocks.StructBlock):
    """One service. Only ever used inside ServicesBlock's ListBlock."""

    name = blocks.CharBlock(max_length=80)
    description = blocks.TextBlock(rows=3)


class ServicesBlock(blocks.StructBlock):
    """A heading plus a repeating list of services.

    This is the pattern worth remembering: StructBlock for "these fields go
    together", ListBlock for "and there can be several of these".
    """

    heading = blocks.CharBlock(max_length=80, default="What we do")
    services = blocks.ListBlock(ServiceBlock(), min_num=1, max_num=6)

    class Meta:
        icon = "list-ul"
        label = "Services"
        template = "home/blocks/services_block.html"


class CTABlock(blocks.StructBlock):
    """A call to action pointing at a page in the tree, or at an external URL."""

    text = blocks.CharBlock(max_length=120, help_text="The line above the button.")
    button_text = blocks.CharBlock(max_length=40, default="Get in touch")
    page = blocks.PageChooserBlock(
        required=False,
        help_text="A page on this site. Takes priority over the URL below.",
    )
    external_url = blocks.URLBlock(required=False)

    class Meta:
        icon = "link"
        label = "Call to action"
        template = "home/blocks/cta_block.html"


class BodyBlock(blocks.StreamBlock):
    """The top-level block: everything an editor may put in a page body."""

    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        template="home/blocks/heading_block.html",
    )
    paragraph = blocks.RichTextBlock(
        icon="pilcrow",
        features=["bold", "italic", "link", "ol", "ul", "document-link"],
    )
    quote = QuoteBlock()
    services = ServicesBlock()
    cta = CTABlock()

    class Meta:
        block_counts = {"services": {"max_num": 1}}
