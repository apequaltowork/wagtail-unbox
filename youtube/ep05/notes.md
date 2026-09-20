# Ep 5 — Build notes & gotchas

## Verified on this machine

- `manage.py check` → no issues.
- Migration `0004` applies cleanly **with** the data step, and the About page's existing
  paragraph survives as a `paragraph` block.
- Home renders 4 blocks: paragraph, services, quote, cta. Read out of the response HTML:
  `block-services`, `block-quote`, `block-cta`, `service-grid`, and the CTA's
  `href="/about/"` resolved through `{% pageurl %}`.
- `/about/` renders the migrated paragraph plus a new `heading` block.
- Admin edit view (`/admin/pages/3/edit/`) returns 200 and shows every block by its label:
  Paragraph, Services, Pull quote, Call to action — with the ListBlock's three service
  items nested inside Services.
- `body` is genuinely optional: `field.blank is True` and `field.stream_block.required is False`.

## ⭐ Gotcha 1 — the migration fails on any page that already has content

Running `makemigrations` and then `migrate` with nothing else produces, on SQLite:

```
django.db.utils.IntegrityError: CHECK constraint failed: (JSON_VALID("body") OR "body" IS NULL)
```

StreamField's column is JSON. `<p>We are a small studio.</p>` is not JSON. The About page
was written in episode 3, so **every viewer following along will hit this**, and the error
message never says the word "StreamField".

Django wraps the migration in a transaction, so the failure rolls back cleanly —
`showmigrations` still shows `0004` unapplied and the data is intact. That is worth saying
out loud, because the error looks catastrophic and is not.

Postgres fails at the same point with a different message
(`invalid input syntax for type json`), so the fix is the same either way.

The fix is a `RunPython` **before** the `AlterField`, while the column is still plain text:
wrap each page's HTML as one `paragraph` block and write it back as JSON. Reversible, too —
`stream_to_html` flattens it back.

## ⭐ Gotcha 2 — Wagtail already gives you a wrapper class

Hit this live. The block templates originally carried their own `class="block-cta"`, and the
CTA rendered as a **teal box inside a teal box**, 300px tall instead of 150px. Measured:

```js
[...document.querySelectorAll('.block-cta')].map(e => e.tagName + '.' + e.className)
// ["DIV.w-block-cta block-cta", "ASIDE.block-cta"]
```

Wagtail 7 wraps every block in `<div class="w-block-NAME block-NAME">` automatically. Naming
your own class `block-cta` applies the styling twice. Dropped the hand-written classes and
styled the wrapper instead — `.block-quote blockquote`, `.block-cta p`, and so on. Fewer
lines, and it works for any block that gets added later.

## Gotcha 3 — `use_json_field=True` does nothing now

Every StreamField tutorial written before Wagtail 6 says to pass `use_json_field=True`. In
7.4 the signature still accepts it, and the docstring says it outright: *"Ignored, but
retained for compatibility with historical migrations."* Don't type it into new code.

## Worth pointing at on screen

- The generated migration uses Wagtail 7's compact `block_lookup` format — block definitions
  are numbered and listed once instead of being repeated inline. It is unreadable and that
  is fine; nobody hand-edits the block half of it. We only hand-edit the top.
- `block_counts = {"services": {"max_num": 1}}` on the StreamBlock Meta caps a block type
  across the whole stream, as opposed to `max_num` on a ListBlock which caps items inside it.
  Both are used here, which makes the difference easy to show.

## Not done in this episode, deliberately

- `ImageChooserBlock` — there is no image handling until ep 6. The services grid is text.
- `StreamField` on the blog — the blog doesn't exist until ep 7.
- A custom `StructValue` or block `get_context()`. Ep 8, alongside snippets.
- Search indexing the StreamField. Ep 11.

## Local state note

The Home page's blocks were authored locally; they live in the gitignored `db.sqlite3`.
Viewers build their own in the admin — that is the point of the episode.
