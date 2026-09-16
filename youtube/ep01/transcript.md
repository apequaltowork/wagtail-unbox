# Ep 1 — What Wagtail Actually Is

Transcript of the narration.

Video: https://www.youtube.com/watch?v=X7FgE9j1XLY

Code at the end of this episode: `git checkout ep01-end`

---

**[0:00]** What Wagtail actually is.

**[0:04]** By the end of this episode you will have Wagtail installed, a project created, and you will be logged into a real content management system. And then we stop. Because episode two reads every single file it just generated.

**[0:20]** First, where Wagtail sits. Django is a web framework with no content editing at all. WordPress is a PHP CMS with its own everything. Wagtail is in between: Django apps that add a page tree and a genuinely good editor on top of a normal Django project.

**[0:40]** A fair question: Django already has an admin. But the Django admin is a database table editor, built for staff. Wagtail's admin is a publishing tool. Drafts, previews, workflow, a page hierarchy, image cropping. You would not hand a client the Django admin. You would hand them this.

**[1:02]** So here is the one sentence version. Wagtail is what you reach for when you would write a Django site anyway, but somebody who is not you needs to change the words on it.

**[1:14]** Start with an empty folder and a virtual environment. If you watched episode zero b, this is exactly what we practised. Make it, then activate it. Watch for the .venv prefix on the prompt. On Mac and Linux the activate line is source .venv/bin/activate.

**[1:35]** Now install Wagtail. Watch the dependency list. Two worth naming. Treebeard, which is what stores the page tree. And Pillow, which is image processing, so Wagtail can generate resized versions of whatever you upload.

**[1:53]** You might wonder why we pinned Django as well as Wagtail. Because Wagtail seven four only asks for Django five point two or newer, with no upper limit. Unpinned, you get whatever Django shipped most recently, and three episodes from now your screen stops matching mine. Pin both.

**[2:14]** Check the version, then create the project. One command.

**[2:20]** Those two arguments trip people up constantly, so let us be precise. Studio is the name of the Django project package. Ours is a design studio site. And site is the folder to create it in. Wagtail creates that folder for you, so you do not need to make it first.

**[2:41]** And one warning that genuinely costs people an afternoon. Do not name your project site. Python already has a built in module called site, and shadowing it gives you import errors that make no sense at all. The same goes for test, json, and email. The folder can be called site. The package cannot.

**[3:04]** Now build the database. And look at what goes past: 184 migrations, before you have written a single line of code. Those are Wagtail's own tables. Pages, images, documents, revisions, permissions.

**[3:21]** And notice what you did not have to do. There is no database server. That created a file called db.sqlite3, right there in the folder. SQLite ships inside Python. Postgres turns up in episode thirteen, and not before.

**[3:40]** Create your login. One thing that worries people: the password is invisible while you type it. Your keyboard is fine. Keep typing and press enter.

**[3:53]** And run it. Your site is now live on port eight thousand.

**[3:59]** Two addresses matter. The site itself, which right now shows Wagtail's welcome page, and we delete that in episode four. And/admin, which is the CMS. Log in there with the superuser you just created.

**[4:16]** Open the pages section and notice something. A page already exists. You did not create it, and it did not come from a fixture. A migration made it, the first time you ran migrate. That file is one of the more surprising things in the box, and we open it next episode.

**[4:36]** Last thing. Put it in git, and tag it. Gitignore the virtual environment, the database and the media folder. Your content is yours; the code is what gets shared.

**[4:50]** We are leaving that generated project completely untouched, because next episode is a guided tour of exactly this tree. Twenty nine files. Most tutorials explain three of them. We read all of them, including the ones you are told to ignore.

**[5:08]** Next episode, we open the box and read every file. Thanks for watching.
