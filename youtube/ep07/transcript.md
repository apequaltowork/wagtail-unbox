# Ep 7 — Blog: Parent & Child Pages

Transcript of the narration.

Video: https://www.youtube.com/watch?v=lvWFyLOHSBo

Code at the end of this episode: `git checkout ep07-end`

---

**[0:00]** The blog. Parent and child pages.

**[0:04]** Right now the studio's site is a homepage and an About page. A studio that wants clients needs to say something, so today we build a journal. An index page, posts underneath it, newest first, three at a time.

**[0:20]** This is the first time we have added an app of our own. Start app blog, and then delete two of the files it made. A Wagtail page app does not use Django's admin.py or views.py. Add blog to installed apps, and we are ready.

**[0:38]** Why a separate app rather than two more models in home. The blog has its own templates and its own rules, and next episode it grows tags. Home stays the site shell. But the blog still imports the hero and the content blocks from home, so there is one definition of each, used everywhere.

**[0:59]** Two models. The index is just a page with an intro. A post has a date, an intro, the hero from last episode, and the same StreamField body as every other page. The date is deliberately its own field and not the publish date, because editors backdate posts, and fixing a typo must not move a post to the top of the blog.

**[1:23]** Before writing any rules, I printed what each existing page type allows underneath it. Look at the About page. It will happily accept a second homepage. And a bare Page, which has no template, and throws an error the moment anybody visits it. Wagtail's default is anything, anywhere.

**[1:45]** Two lists fix it. Every page type says where it may live, and what may live under it. A post may only sit under the journal, and nothing may sit under a post. The homepage lives at the root, and max count one means there can only ever be one.

**[2:03]** And checked. A second homepage, no. A second journal, no. A blog post under About, no. A post under the journal, yes. And these rules live entirely in Python. Make migrations says no changes detected, because nothing about the database changed.

**[2:25]** Now the index page needs its posts, newest first. And here is the query everybody writes first. Get children, live ones, ordered by date descending. It looks right.

**[2:39]** Field error. Cannot resolve keyword date. And take the order by off, and look at what comes back. Not blog pages. Plain Page objects.

**[2:52]** Here is why. Get children queries the page table, the one every page type shares. It gives you page objects, in the order they sit in the tree, and the page table has no date column. So ask the blog page model directly, for children of this page. Now you get real blog pages, and you can order them by date.

**[3:16]** And get context is where it goes. This is how any Wagtail page hands extra data to its template. Call super, add what you need, return it. Here that is the posts, newest first, with the first published date as a tie breaker, and wrapped in Django's paginator.

**[3:36]** And use get page, not page. The page number comes from the URL, which means anybody can type anything into it. Page raises an exception for rubbish, or for a page that does not exist. Get page just clamps it to something sensible.

**[3:54]** The index template loops over posts. That is a paginator page, which iterates like a list, and also knows whether there is a next or previous page, which is all the prev and next links need.

**[4:09]** A small thing I fixed on the way. The page counter jumped from one side of the screen to the other between page one and page three, because a missing link took an item out of the flex row. Three fixed grid slots, empty or not, and it stays in the middle.

**[4:26]** And here is the journal. Newest first, three posts, and an older link.

**[4:34]** Page three. The oldest post, a newer link, and the counter still in the middle. Type page 999 into the address bar and you land here too, instead of on an error page.

**[4:49]** And a post. The date, the title, the intro, the same StreamField blocks as every other page, and a back link to the journal built from the tree.

**[5:00]** Commit, and tag.

**[5:03]** Next episode, snippets. Team members and testimonials, written once and used on any page. And tags for the journal.

**[5:14]** Next episode, snippets. Thanks for watching.
