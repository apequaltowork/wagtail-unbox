# Ep 9 — Navigation & Site Settings

Transcript of the narration.

Code at the end of this episode: `git checkout ep09-end`

---

**[0:00]** Navigation, and site settings.

**[0:04]** There is an About page and a journal, and the only way to reach either of them is the list at the bottom of the homepage. And the footer says Studio, because somebody typed that word into a template. Today, a real menu, and details the client can edit.

**[0:22]** There is no menu model here, and no hard coded links. The menu is simply the children of the site's root page that are live and marked as in menu. So an editor adds a page to the menu by ticking one checkbox, on that page's Promote tab.

**[0:39]** It is an inclusion tag. It finds the site for this request, takes the root page's children, and works out which one is active. Then base.html just says main menu.

**[0:53]** Reload the page, and. Template syntax error. Navigation tags is not a registered tag library. And the code is correct.

**[1:04]** The development server had already reloaded itself for the models change a minute earlier. But the reloader only watches files that are already imported, and a brand new tag library is not one of them. So any time you add a new template tags module, stop the server and start it again.

**[1:24]** Restarted, and now the menu is empty. Nothing there at all. Because every page on this site has show in menus set to false. That is the default for every page type. Tick the box on About and on the journal, publish, and the menu appears.

**[1:43]** And to stop that happening next time, set show in menus default to true on the page types that belong in a menu. But be clear what it does. New pages start with the box ticked. Pages that already exist are not touched.

**[1:59]** The active item is a prefix match on the URL path. So when you are reading a post, which lives under the journal, the journal stays highlighted. And because a URL path always ends in a/, About can never accidentally match a page called About us.

**[2:18]** And it is cheap. I rendered the menu tag on its own and counted. One database query. No caching needed. That changes once you build dropdowns, because each level is another query per item.

**[2:34]** Now the footer. Wagtail's settings app, plus its context processor, and every template on the site can read the studio's details.

**[2:44]** A settings model is a normal Django model with one decorator. Site setting, rather than generic setting, means one row per site, so if this install ever runs a second site, it gets its own phone number.

**[3:00]** And watch this. No rows before any request. Load one page, and there is a row. Wagtail creates it the first time something reads it, using your defaults. Which is why the studio name needs a sensible default. It is what the header shows before anyone has opened the settings screen.

**[3:21]** In a template it is settings, then the app label, then the model name, then the field. The brand, the email as a mail to link, and the phone as a tel link, with the spaces cut out so it actually dials.

**[3:36]** And here it is. Reading a post, and the journal is still highlighted in the menu.

**[3:43]** And the footer. The name, the email, the phone number, the address and the social link. All of it comes from the settings screen, and the client can change any of it without calling you.

**[3:57]** Commit, and tag.

**[4:01]** Next episode, forms. A contact page that emails the studio, and keeps every submission in the admin.

**[4:10]** Next episode, forms. Thanks for watching.
