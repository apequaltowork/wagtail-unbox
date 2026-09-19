# Ep 3 — The Page Model & the Tree

Transcript of the narration.

Video: https://www.youtube.com/watch?v=1Oxev2holT4

Code at the end of this episode: `git checkout ep03-end`

---

**[0:00]** The page model, and the tree.

**[0:04]** Last episode we made a prediction. A page one level under Home would get the path zero zero zero one, zero zero zero one, zero zero zero one. Today we build that page, and we check.

**[0:20]** Here is where we left the home page. Two lines, and already a working page type, because Page brings title, slug, SEO fields, publishing, revisions and permissions. What it does not have is anything of ours. So let us add some.

**[0:39]** Two fields. Intro is an ordinary Django char field, and the help text is what the editor sees under the box, so write it for them. Body is a rich text field, Wagtail's editor. And then the part people forget: content panels.

**[0:57]** A field on the model is not the same as a field in the admin. Adding it gives you a database column, and nothing else. It only becomes editable once it has a field panel. And we add to Page.content_panels, rather than replacing it, so we keep the title field that Wagtail already provides.

**[1:17]** And a second page type. Standard page, for About, Services, anything that is mostly words. Same two fields. Having two page types is what lets us build an actual tree.

**[1:32]** Every page type needs a template, named by the rule from last episode: standard_page.html. Leave it out and you get template does not exist, but only when you hit view live, so the admin looks perfectly fine right up until you preview. We keep this template bare. Styling is episode four.

**[1:54]** Make the migration. One new model, two new fields. Then apply it.

**[2:02]** Now open that migration, because one line in it explains how every Wagtail page is stored. Page pointer. A one to one field, pointing at wagtail core page.

**[2:15]** That is Django multi table inheritance, and it is the mental model for the rest of this series. Every page lives in two tables. The shared page table has twenty nine columns: title, slug, path, depth, and the content type from last episode. Our standard page table has three. Page pointer, intro, and body. Only what is unique to this page type. Page pointer is what joins them.

**[2:46]** Over to the admin. Edit the home page, and there are the two new fields, with our help text underneath. Fill in the intro and publish.

**[2:56]** Now on Home, add a child page. Choose standard page, call it About, fill it in, and publish. That is our first page that we made ourselves.

**[3:09]** Now the moment of truth. Open the shell and print the tree.

**[3:15]** There it is. About sits at zero zero zero one, zero zero zero one, zero zero zero one. Exactly what the animation predicted last episode. It is Home's path, plus four more characters.

**[3:32]** But look closely at that url path. It says/home/about. Visit that and you get a 404. The page is actually at/about. The url path is the route from the root of the tree, so it includes home. But home is the root of the site, so it drops out of the real address. If you ever build links, use page.url, not url_path.

**[3:59]** And one more thing that catches everyone. Ask Page.objects for About, and you get a plain Page, with no intro field. Call .specific, and you get the real standard page, with everything on it. That is the two tables again. Page.objects only reads the shared one.

**[4:21]** Before we finish, something is still wrong. When you add a child under Home, Wagtail offers you Home page as well. Nothing stops you putting a home page inside a home page. We fix that with sub page types, in episode seven.

**[4:38]** Commit it, and tag it. E p zero three end is our first checkpoint with real code changes in it.

**[4:47]** Our pages have content now, but the home page still shows Wagtail's welcome egg. Next episode, we replace it with real templates.

**[4:58]** Next episode, we replace the welcome page with real templates. Thanks for watching.
