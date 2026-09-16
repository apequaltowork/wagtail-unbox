# Ep 2 — Opening the Box: Every File Explained

Transcript of the narration.

Video: https://www.youtube.com/watch?v=FoElBiKp_fI

Code at the end of this episode: `git checkout ep02-end`

---

**[0:00]** Opening the box. Every file, explained.

**[0:04]** Wagtail start generated twenty nine files. Most tutorials explain three of them and tell you to ignore the rest. We are reading all of them, because the ones you are told to ignore are the ones deciding how your site actually behaves.

**[0:21]** And we change nothing. Not one line. Start from git checkout e p zero one end if you are following along. Read the box before you rebuild it.

**[0:33]** Start at manage.py. Standard Django, and one line matters: the settings module defaults to studio.settings.dev. That is the split. You get development settings by default, and production settings only when you ask for them.

**[0:51]** Then two path variables that look almost the same and are not. Project dir is the package. Base dir is the folder above it. They are one letter apart in your head and mixing them up is a classic bug two episodes from now.

**[1:08]** Now the file that matters most. Installed apps.

**[1:14]** This is the whole thesis of the series. Wagtail is not a black box bolted onto Django. It is eleven Django apps sitting in your installed apps list. Every one of them has models, and you can query them like any other Django model.

**[1:31]** Middleware is the standard Django stack plus exactly one addition, and it is last on purpose. The redirect middleware only acts once everything else has produced a 404, and then it checks the redirects table.

**[1:46]** Then four settings people mix up constantly. Static files dirs is where you put CSS. Static root is where collect static dumps it for production. Media root is where uploads land. The rule that keeps it straight: static is code, media is content. Static gets committed, media never does.

**[2:10]** And the Wagtail block at the bottom. Site name, the search backend, a ten megabyte cap on document uploads. But look at wagtail admin base url. It ships as http://example.com. That is a placeholder that ships broken. It builds absolute URLs for notification emails and previews. We fix it in episode thirteen.

**[2:36]** The two settings files are tiny. Dev turns debug on and ships a secret key marked, in the variable name, as insecure. Production turns debug off. And both end with the same trick: a local.py file that does not exist and is not committed can override anything. That is the escape hatch for machine specific config.

**[3:01]** Now urls.py, and the order is the whole point.

**[3:06]** That last line is Wagtail's catch all. Any URL that did not match above gets handed to the page tree, which resolves it by walking slugs. That is why a page at/about/team just works and nobody wrote a URL pattern for it. And it is why this line has to stay last. Put a route after it and it will never be reached.

**[3:31]** The home app. models.py is six lines, and that is already a working CMS page type. Title, slug, SEO fields, publishing dates, revisions, previews, permissions. All of it inherited from Page. We add fields to it next episode.

**[3:51]** And notice the template naming convention. The model is called HomePage, so Wagtail looks for home_page.html. Model name, lowercased, with underscores. You never wire it up. Episode four exploits that.

**[4:10]** Now the centrepiece of this episode, and the file almost nobody opens. Your homepage was not a fixture, and you did not create it in the admin. A data migration made it, the first time you ran migrate. That is why a brand new Wagtail site already has exactly one page.

**[4:31]** It does three things. It deletes the default page that wagtail core ships. It gets or creates a content type, which is how a single Page row knows which model it really is. And then it creates the page, with values that look like magic.

**[4:49]** Path equals zero zero zero one, zero zero zero one. That is a materialised path, from django treebeard, the package we watched install in episode one. Four characters per level. Zero zero zero one is the root. Its first child is that plus another zero zero zero one. Its child adds four more. The entire ancestry is encoded in the string, which is how Wagtail can fetch a page's parents in one query instead of walking up the tree one level at a time.

**[5:23]** Run that query on your own site and you will see something surprising: there are two pages, not one. There is an invisible Root above your homepage. That is why the admin shows your page nested one level down.

**[5:38]** And one last line in that migration creates a Site row. Hostname localhost, default site, root page set to our homepage. Wagtail is multi site out of the box, and this is the row that makes your one site exist.

**[5:54]** The search app is a plain Django function view, about thirty five lines, with a paginator. Note .live, which means published pages only, so drafts are excluded. It is wired up already, but nothing is indexed yet. That is episode eleven.

**[6:13]** base.html gives you an SEO title with a fallback for free, and the wagtail user bar, which is the floating admin bar that logged in editors see on the front end of the site. The content block is empty, waiting for episode four.

**[6:30]** And one last thing, which is a genuine inconsistency. The requirements file that the template generated caps Django below six point one. But the Django pip actually installed is six point one point one. They disagree, because Wagtail's own package metadata asks only for Django five point two or newer with no upper limit, and pip follows the metadata, not this file. Nothing is broken. But that is exactly how your environment drifts away from mine.

**[7:03]** Five things to carry forward. Wagtail is about eleven Django apps in installed apps. The wagtail urls catch all must stay last. Your homepage came from a data migration, and its position is a treebeard path string. Templates resolve from app/model_name.html automatically. And two settings ship as placeholders: the dev secret key, and the admin base url.

**[7:31]** Next episode we finally change something, and the first thing to understand is the Page model that those six lines inherit from.

**[7:41]** Next episode, we finally change something. Thanks for watching.
