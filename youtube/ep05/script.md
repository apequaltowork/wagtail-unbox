# Ep 5 — StreamField, Properly

The episode people search for. Start from `git checkout ep04-end`.

Everything quoted here was run on the recording machine — see `notes.md`.

## Beats

### Cold open — one field, one blob
`body` is a `RichTextField`. One box. The editor can put anything in it and the designer has
no say in what comes out. Today it becomes a **list of blocks**, each with its own fields and
its own template.

### What StreamField actually is
Not a rich text editor with extras. A **JSON column holding an ordered list of typed blocks**.
That one sentence explains the migration failure coming up in four minutes.

### The block hierarchy, smallest first
| Block | What it is |
|---|---|
| `CharBlock`, `TextBlock`, `RichTextBlock`, `URLBlock`, `PageChooserBlock` | primitives |
| `StructBlock` | *these fields go together* — a quote and its attribution |
| `ListBlock` | *and there can be several of these* — three services |
| `StreamBlock` | *the editor picks from these, in any order* — the body itself |

`StructBlock` and `ListBlock` are the two people confuse. Say it as: StructBlock is a
**record**, ListBlock is a **repeat**. `ServicesBlock` uses both — a heading plus a repeated
`ServiceBlock`.

### blocks.py
Write it bottom-up on screen: `QuoteBlock`, then `ServiceBlock` + `ServicesBlock`, then
`CTABlock`, then `BodyBlock` collecting them. Each `Meta` carries `icon`, `label`, `template`.
Icons come from Wagtail's own set — `openquote`, `list-ul`, `title`, `pilcrow`, `link`.

### The model change
```python
body = StreamField(BodyBlock(), blank=True)
```
Two lines gone, two lines in. **Do not type `use_json_field=True`** — every pre-Wagtail-6
tutorial says to, and in 7.4 the parameter is ignored outright.

### ⭐ The migration blows up
`makemigrations`, `migrate`, and:

```
IntegrityError: CHECK constraint failed: (JSON_VALID("body") OR "body" IS NULL)
```

Nothing in that message says StreamField. Here is what it means: the About page still holds
`<p>We are a small studio.</p>` from episode 3, the new column is JSON, and that is not JSON.

Two things worth saying immediately:
1. **Nothing is broken.** Django runs migrations in a transaction. `showmigrations` shows
   `0004` unapplied and the row is untouched.
2. Postgres gives a different message for the same cause. Same fix.

### The fix: a data migration, in front
Hand-edit the generated `0004`. Add a `RunPython` **before** the `AlterField`, while the
column is still text — read the HTML, write back `[{"type": "paragraph", "value": ..., "id": ...}]`.
Write the reverse too; it is six lines and it makes the migration undoable.

Point at the generated block half: Wagtail 7's `block_lookup` format, numbered definitions,
unreadable, and nobody hand-edits it. We only touch the top of the file.

### Templates
`{{ page.body|richtext }}` becomes `{{ page.body }}`. StreamField renders each block through
its own template; there is nothing left to filter.

Then the block templates — and the thing that cost ten minutes here:

### ⭐ Wagtail already wrapped your block
The CTA rendered as a teal box **inside** a teal box. Wagtail 7 wraps every block in
`<div class="w-block-NAME block-NAME">` on its own. Naming your own class `block-cta` styles
it twice.

```js
[...document.querySelectorAll('.block-cta')].map(e => e.tagName + '.' + e.className)
// ["DIV.w-block-cta block-cta", "ASIDE.block-cta"]
```

Delete the hand-written classes, style the wrapper. Fewer lines, and every block added later
gets the same treatment for free.

### In the admin
The payoff. One "+" opens the block menu with the icons and labels from `Meta`. Services
expands to three nested service items. Drag to reorder. This is what the client sees, and it
is why StreamField exists.

`block_counts = {"services": {"max_num": 1}}` caps a block **type** across the stream;
`max_num` on the ListBlock caps items **inside** it. Different knobs, same word.

### Before and after
About: the migrated paragraph, still there, now with a real heading block under it.
Home: paragraph, services grid, pull quote, call to action — four blocks, four templates.

### Next
Ep 6: images and documents. `ImageChooserBlock` is the block everyone wanted today.

## Do NOT do in this episode
- `ImageChooserBlock` — no image handling until ep 6.
- Custom `StructValue` or block `get_context()` — ep 8.
- Search indexing the StreamField — ep 11.
