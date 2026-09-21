# Ep 11 — Search

Transcript of the narration.

Code at the end of this episode: `git checkout ep11-end`

---

**[0:00]** Search.

**[0:04]** Back in episode two we unboxed an app called search. A view, a template and a URL, all generated for us, and untouched ever since. It does work out of the box. Today we find four ways it does not work well.

**[0:21]** Search for a word in a post's title, and it is found. A phrase from the intro. Nothing. A word from the body. Nothing.

**[0:33]** Because the page class only indexes the title. Every other field has to be named in search fields. Intro and body as search fields, and the date as a filter field for later. It is not a schema change, so there is no migration.

**[0:50]** Fields added. Search again. Still nothing.

**[0:56]** The search index holds whatever was written when each page was last saved, and changing search fields does not rewrite it. Update index rebuilds it. Nineteen objects. And now the intro is found. From here on, publishing a page reindexes it automatically.

**[1:16]** Now try a team member's name. Priya is right there on the About page. Search finds nothing. Same for the testimonial on the home page. The team block fetches its names when the page renders, and the testimonial block only stores an id. So when the page is indexed, that text simply is not part of it.

**[1:39]** Blocks have a method for exactly this. Get searchable content returns the words that should be indexed for this block. Return the quote and the author, do the same for the team, reindex, and now Priya finds the About page. The honest trade off. Those words are copied into the page's index entry, so if the team changes, the About page is stale until someone saves it or you run update index.

**[2:07]** And this one matters. I password protected the pricing post and searched. The query in the generated view still returns it. Add public, and it does not.

**[2:20]** The view that Wagtail generates uses live, and live means published. It does not mean visible to everyone. So the title of every private page on your site shows up in search results for any visitor. Add public. And add specific while you are there, so each result is its real page type and can show its intro.

**[2:43]** So the view becomes this. Strip the query, search only public live pages as their specific types, and paginate with get page, exactly like the journal in episode seven.

**[2:57]** The template gets a properly labelled search box, a result count, each result's page type, title and intro, and pagination links that carry the query along, which is the lesson from episode eight.

**[3:11]** And here it is, with search in the menu. Handover finds nine pages, across three page types.

**[3:20]** And a team member's name, which only lives in a snippet, now finds the About page.

**[3:27]** Commit, and tag.

**[3:30]** And with that, the site is feature complete. Next episode starts the final act. Making the admin pleasant for the client who actually has to use it.

**[3:43]** Next episode, the editor experience. Thanks for watching.
