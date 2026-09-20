# Ep 4 — Templates & Static Files

Transcript of the narration.

Video: https://www.youtube.com/watch?v=e-FeE6O9AhM

Code at the end of this episode: `git checkout ep04-end`

---

**[0:00]** Templates, and static files.

**[0:04]** Four episodes in, and the front of our site still shows Wagtail's welcome page. A teal egg, and welcome to your new Wagtail site. Today, it goes.

**[0:17]** It lives in an include, and Wagtail tells you in a comment that it is disposable. So we delete the include, the welcome template, and its stylesheet. Three files gone.

**[0:30]** Remember the rule from episode two. Model name, lowercased, with underscores. Home page becomes home_page.html, and you never wire it up anywhere. Wagtail just looks for it.

**[0:47]** And there are two places templates can live, both switched on in settings. App dirs finds templates inside each app, which is where page templates go. And the dirs setting points at the project templates folder, which is where base.html lives, because every app uses it.

**[1:06]** Open base.html. The head that Wagtail generated is already good. An SEO title with a fallback, the user bar, and that preview panel fix we looked at in episode two. Keep all of it. We are only replacing the body.

**[1:24]** A header, a main, and a footer, wrapped around the content block. That is the whole layout. Every page in the series inherits it from here.

**[1:35]** Three tags do all the linking. Page url takes a page object and gives you its address. Slug url looks a page up by slug, which is why the brand link keeps working even if somebody renames the home page. And the rich text filter turns a rich text field into HTML. All three need the wagtail core tags load at the top.

**[1:59]** And this is where last episode's warning pays off. Never build a link out of url path. It gives you/home/about, which is a 404. Page url gives you the real address.

**[2:14]** And here is the page tree finally doing something useful. The home page lists its own children. It does not know that an About page exists. It just asks the tree. Dot live means published pages only, so drafts stay hidden from visitors.

**[2:33]** Now the styling. Wagtail generates a stylesheet at studio/static/css/studio.css, links it in base.html, and leaves it completely empty. Zero bytes. We fill it in with plain CSS. No build step, no framework, not in this episode and not in any of them.

**[2:56]** The static tag turns a path inside your static folder into a URL, using the static files dirs setting we read in episode two. In development the server just serves it. In production there is a collect static step, and that is episode thirteen.

**[3:14]** And now the thing that will cost you ten minutes, because it cost me ten minutes. You write the CSS. You reload. And the page is still completely unstyled. Nothing is wrong with your code.

**[3:30]** Here is the proof. The stylesheet is attached to the page, but it has zero rules in it. Meanwhile fetching the same URL returns two thousand bytes of perfectly good CSS. The server is fine. Your browser cached that file back when it was zero bytes, and it is still using the empty copy.

**[3:52]** The fix is a hard reload. Control F five on Windows, or command shift R on a Mac. Every single person following along will hit this, because the file ships empty and you loaded the site before you wrote anything into it.

**[4:09]** And there it is. A header, a title, the intro from episode three, a list of child pages generated from the tree, and a footer. That is our studio site.

**[4:22]** The About page gets the same layout for free, because it extends the same base template. And that back link is built from page.get_parent, so it always points at wherever the page actually sits in the tree.

**[4:37]** And one media query makes it work on a phone. At 375 pixels the heading drops from two point six rem to two rem. That is the entire responsive story for this site.

**[4:51]** One last thing. If you try a bad URL you still get Django's yellow debug page. The 404 template exists and extends our base, but Django only uses it when debug is switched off. That is episode thirteen, not a bug.

**[5:09]** Commit, and tag.

**[5:12]** Our pages look like a site now, but the body field is still one big blob of rich text. Next episode, StreamField replaces it with real content blocks. That is the episode most people come to Wagtail for.

**[5:28]** Next episode, StreamField. Thanks for watching.
