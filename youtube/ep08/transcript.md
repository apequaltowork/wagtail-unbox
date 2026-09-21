# Ep 8 — Snippets & Reusable Content

Transcript of the narration.

Video: https://www.youtube.com/watch?v=L9A5RAPO5uI

Code at the end of this episode: `git checkout ep08-end`

---

**[0:00]** Snippets, and reusable content.

**[0:04]** A team member does not have a URL. A testimonial does not have a place in the page tree. But both belong on pages, and usually on more than one page. That is what a snippet is. A plain Django model, that editors can manage in the admin.

**[0:23]** Two models. A team member, and a testimonial. Neither one inherits from Page. The team member inherits from Orderable, which adds a sort order column, and that alone gives the admin drag and drop reordering.

**[0:39]** And you register them with a snippet view set, which is the Wagtail seven way. One class per model sets the icon, the menu label, the listing columns and what is searchable. A view set group puts both of them under a single Studio item in the admin menu, instead of burying them in a generic snippets list.

**[1:01]** There are two ways to put a snippet on a page. Either the editor chooses one, which is what the testimonial block does with a snippet chooser. Or the block fetches them itself. The team block has nothing to choose. It loads every team member, so when somebody joins the studio, every page showing the team updates on its own.

**[1:24]** Blocks have a get context method as well, exactly like pages did last episode. And notice the import is inside the method, not at the top of the file.

**[1:36]** Because the models file imports the blocks file, to build the body field. If the blocks file imported the models file back, that is a circular import and Django will not start. So the snippet chooser names its model as a string, and the team block imports its model only when it actually runs.

**[1:57]** Now, what happens when somebody deletes a testimonial that a page is using. Before the delete, Wagtail already knows. Its reference index says used one time, on the home page, and the admin shows that on the confirmation screen. After the delete, the page still loads. But the block's value is now None, and without a guard in the template you ship an empty, styled quote box. Every chooser value can become None. Write the template for it.

**[2:29]** Now tags for the journal. A small through model, and a taggable manager on the post. The detail that matters is parental key instead of foreign key. It means the tags are saved as part of the page's revision, so an editor can change the tags on a draft without touching the live post.

**[2:49]** Filtering by tag is four lines in get context. And the last of those four lines matters a lot more than it looks. Here is why.

**[3:00]** Filter by the process tag. Page one of two. Click older. The link is question mark page equals two, and it lands on page two of three. That is the unfiltered journal. The tag just vanished.

**[3:17]** Last episode's pagination links replace the entire query string. The moment you add a second parameter, every link that builds a query string has to carry both of them. Pass the tag back to the template, put it in the link, and older now goes to page two of two.

**[3:36]** And one small fix on the way. The tag list inside each post is a list as well, so the post row's border and padding landed on every tag pill. One child selector instead of a descendant selector.

**[3:51]** And here it is. The team, on the About page, in the order set by dragging rows in the admin.

**[3:59]** A testimonial on the home page, chosen by the editor from the snippet list.

**[4:06]** And the journal, filtered by tag, with every post showing its own tags as links.

**[4:13]** Commit, and tag.

**[4:17]** Next episode, navigation. A menu built from the page tree, and footer and contact details the client can edit themselves.

**[4:27]** Next episode, navigation and site settings. Thanks for watching.
