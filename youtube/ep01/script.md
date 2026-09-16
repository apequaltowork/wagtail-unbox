# Ep 1 — What Wagtail Actually Is

**Target: 18 min.** Ends with a running Wagtail site and a successful admin login.

## Beats

### 0:00–1:00 — Cold open: the thing itself
**[SCREEN: terminal, empty folder]**
No preamble. Four commands, sped up, ending on the Wagtail welcome page with the teal egg.

> "That took about ninety seconds. Now let's do it slowly, and understand every piece."

### 1:00–3:30 — Wagtail vs Django vs WordPress
**[SCREEN: one diagram, three columns]**

| | What it is | Who edits content |
|---|---|---|
| **Django** | A web framework. No content editing at all. | Developers, via code or the bare Django admin |
| **Wagtail** | Django apps that add a page tree + a real editor | Non-technical people, comfortably |
| **WordPress** | A PHP CMS with its own everything | Non-technical people |

Three points, said clearly:
- **Wagtail is not an alternative to Django — it runs on Django.** It's `pip install`ed into a Django project. Every Django skill still applies.
- **Versus the Django admin:** the Django admin is a database table editor for *staff*. Wagtail's admin is a publishing tool — drafts, previews, workflow, a page hierarchy, image cropping.
- **Versus WordPress:** you get the editor experience without the plugin ecosystem. The tradeoff is real — fewer drop-in plugins, but you write Python instead of fighting someone else's PHP.

> "Wagtail is what you reach for when you'd write a Django site anyway, but somebody who isn't you needs to change the words on it."

### 3:30–5:00 — The folder and the virtualenv
**[SCREEN: terminal]**
```
mkdir wagtail-unboxed
cd wagtail-unboxed
py -m venv .venv
.venv\Scripts\activate
```
- Point at `(.venv)`. Callback to ep 0b: new terminal, activate again.
- Note `.venv` is a folder in the project but never gets committed.

### 5:00–7:30 — Installing Wagtail
```
pip install "wagtail==7.4.3" "Django==6.1.1"
```
**[SCREEN: let the install scroll — don't cut it]**
- Watch the dependency list go by: Django, Pillow, Willow, django-treebeard, django-modelcluster, djangorestframework. Name a couple:
  - **treebeard** — the page tree. That's how hierarchy is stored.
  - **Pillow** — image processing, so Wagtail can generate resized versions.
- **Why we pin both.** Wagtail 7.4 declares `Django>=5.2` with *no upper bound*. Unpinned, you'd get whatever Django released this month, and your screen would stop matching mine.
```
wagtail --version
```

### 7:30–10:30 — `wagtail start`
```
wagtail start studio site
```
Stop and explain the two arguments — this trips people up constantly:
- `studio` → the **Django project package**. Ours is a design studio site.
- `site` → the **folder** to put it in. Wagtail creates it for you.

**The naming warning, on camera:**
> "Do not call your project `site`. Python already has a built-in module called `site`, and
> shadowing it gives you import errors that make no sense. Same for `test`, `json`, `email`.
> This is a genuinely common beginner mistake and it costs an afternoon."

Then `ls` the result. **Don't explain the files yet** — resist it. Name them only:

> "That's the box. Next episode we open it, and I mean every file. For now, let's just get it running."

### 10:30–13:00 — Migrate and create a login
```
cd site
python manage.py migrate
```
**[SCREEN: the migration list scrolling]**
- **184** migrations run before you've written a line. Those are Wagtail's own tables — pages, images, documents, revisions, permissions. (Counted on a clean run, not estimated.)
- It creates `db.sqlite3`, right there in the folder. **No database server. Nothing to install.** Postgres comes in ep 13.

```
python manage.py createsuperuser
```
- The password is invisible while typing. Say this — people think their keyboard died.
- A "too common" warning is fine in development.

### 13:00–16:00 — First run
```
python manage.py runserver
```
**[SCREEN: browser at 127.0.0.1:8000 — the teal egg]**
- The welcome page. It's a real template, and we delete it in episode 4.
- Then `/admin/`, log in.
- **Quick tour only, 90 seconds:** Pages, Images, Documents, Snippets, Settings. Don't teach the admin yet — just prove it's there and it's nice.
- Click into **Pages → Welcome to your new Wagtail site!** Show the edit form existing. Close it without saving.

> "One page exists already. Wagtail created it in a migration. We'll look at that migration next episode — it's one of the more surprising files in the box."

### 16:00–18:00 — Commit, tag, close
```
git init -b main
```
- Write `.gitignore` on camera: `.venv/`, `*.sqlite3`, `media/`, `__pycache__/`.
- **Why the db is ignored:** your content is yours; the code is what's shared.
```
git add -A
git commit -m "ep01: pristine wagtail start output"
git tag ep01-end
```
> "That commit is the untouched output of `wagtail start`, and it stays untouched, because
> next episode is a guided tour of exactly this tree. Every file. Including the ones you'd
> normally ignore for a year."

## Do NOT do in this episode
- Explain `settings/base.py`. That's ep 2.
- Explain `HomePage(Page)`. That's ep 3.
- Touch CSS. That's ep 4.
- The temptation to "just quickly show StreamField." No.

## On-screen captions to add in edit
- macOS/Linux venv activation (`source .venv/bin/activate`) when the Windows one is shown
- `python3` vs `py`
- Link to `commands.md` at the first terminal command
