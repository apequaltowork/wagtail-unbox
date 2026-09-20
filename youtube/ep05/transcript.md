# Ep 5 — StreamField, Properly

Transcript of the narration.

Video: https://www.youtube.com/watch?v=8_wrJLU57Qw

Code at the end of this episode: `git checkout ep05-end`

---

**[0:00]** StreamField, properly.

**[0:04]** Right now the body of every page is a single rich text field. One box. The editor can put anything they like in it, and you, the person who designed the site, have no say at all in what comes out the other end.

**[0:20]** So what is StreamField. It is not a fancier rich text editor. It is a JSON column holding an ordered list of typed blocks. Hold on to the JSON part of that sentence, because it explains an error we are going to hit in about four minutes.

**[0:38]** There are four kinds of block and they nest inside each other. Primitives hold one value. A struct block is a record: these fields belong together. A list block is a repeat: several of the same thing. And a stream block is a choice: pick any of these, in any order. That last one is the body field itself.

**[1:01]** These two are the ones everybody confuses. A service has a name and a description, and those two always travel together, so that is a struct block. A studio offers several services, so we wrap it in a list block. Struct, then list. Record, then repeat.

**[1:21]** Here is the first real block. A quote, and an optional attribution. The fields are constructor arguments. Everything in Meta is about presentation: the icon that shows in the block menu, the label the editor reads, and the template it renders through on the front end.

**[1:40]** And this is the pattern worth remembering. A struct block containing a list block. A heading that appears once, and then between one and six services under it. Min num and max num are the guard rails you hand the client.

**[1:57]** And the top level block collects them. Five things an editor is allowed to add to a page. Notice rich text has not gone away. It is still here, it is just one block among several now instead of being the entire field.

**[2:14]** The model change is two lines, on both page types. And the content panel underneath does not change one character. It is still just a field panel pointing at body.

**[2:27]** One warning before we migrate. Nearly every StreamField tutorial you will find tells you to pass use json field equals true. That was needed before Wagtail six. In seven point four the parameter is still accepted and, in Wagtail's own words, ignored. Don't type it into new code.

**[2:48]** So. Make migrations, migrate, and it blows up. Integrity error. Check constraint failed. JSON valid body.

**[3:01]** And nothing in that message says the word StreamField. Here is what it means. Back in episode three you typed some text into the About page, so that column holds a paragraph of HTML. The new column is JSON, and a paragraph of HTML is not JSON. Every single person following along will hit this.

**[3:24]** And before you panic: nothing is broken. Django runs a migration inside a transaction, so when it failed it rolled the whole thing back. Show migrations still lists 0004 as not applied, and your content is exactly where it was. On Postgres you get a different message for the same cause, and the same fix.

**[3:47]** The fix is to hand edit the migration Django just generated, and convert the data before the column changes type. The order is the entire trick. That run python runs while the column is still plain text, so it can read the HTML out and write valid JSON back in.

**[4:07]** And this is it. Take whatever HTML is in the field, wrap it as a single paragraph block, and write it back as JSON. Note the shape of a block: a type, a value, and a unique id. That id matters, it is how Wagtail tracks a block across revisions. Write the reverse function too. It is six more lines and it means you can undo this.

**[4:33]** Run it again, and it applies. And the About page's paragraph is still there, now living inside a block.

**[4:42]** While we are in there, the rest of that file looks horrifying. That is Wagtail seven's compact migration format. Every block definition is written once and then referred to by number. It is unreadable and it is meant to be. Nobody hand edits that half. We only touched the top.

**[5:04]** The page templates get one line shorter. The rich text filter goes, because StreamField renders every block through that block's own template. There is nothing left for a filter to do.

**[5:17]** And a block template is tiny. Inside one, the block is always called value, and a struct block's fields hang off it by name. value.quote, value.attribution. That is the whole API.

**[5:33]** And here is this episode's ten minute lesson. My call to action rendered as a teal box inside another teal box, twice the height it should have been. And the CSS was correct.

**[5:47]** Two elements matched. Wagtail seven already wraps every block in a div, and that div already carries a class named after the block. Block dash c t a. My template added a class with exactly the same name, so the styling landed twice.

**[6:06]** So delete the wrapper class from your templates and style Wagtail's instead. It is fewer lines, and every block you add later gets a wrapper class for free without you doing anything.

**[6:19]** And this is the payoff, in the admin. One plus button opens a menu of exactly five things, with the icons and labels we set in Meta. Add them, drag them into any order you like. The editor gets freedom, you keep control of what the page can contain. That is the whole reason StreamField exists.

**[6:41]** Two settings, same word, different jobs. Block counts on the stream block limits how many of a block type the whole page may have. Max num on the list block limits how many items go inside one list. One services section per page. Up to six services in it.

**[7:01]** And here is the home page. A paragraph, a services grid, a pull quote, and a call to action whose button link came out of the page chooser. Four blocks, four templates, all ordered by the editor.

**[7:17]** And the About page. That first paragraph is the one we wrote in episode three, carried across by the data migration, with a new heading block underneath it. Nothing was lost.

**[7:31]** Commit, and tag.

**[7:34]** Next episode, images and documents. Renditions, focal points, and the image chooser block, which is the block everybody wanted today.

**[7:46]** Next episode, images and documents. Thanks for watching.
