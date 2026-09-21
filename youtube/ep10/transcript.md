# Ep 10 — Forms That Work

Transcript of the narration.

Code at the end of this episode: `git checkout ep10-end`

---

**[0:00]** Forms that work.

**[0:04]** The site has a menu, a journal and a team, and no way to get in touch. Today we add a contact form. And a form that actually works turns out to mean four separate things, three of which the defaults get wrong.

**[0:20]** Two models. A form field, tied to the page with a parental key, and the contact page itself, which is an abstract email form. The editor builds the form in the admin, field by field. Every submission is stored in the database, and emailed if the page has a to address.

**[0:40]** The template loops over the form and prints each field with its errors. Leave out the CSRF token and every single submission is a 403 forbidden. That is the first of the four things, and the easy one.

**[0:56]** Second thing. Submit the form before you have written a thank you page. Five hundred. Template does not exist. And yet. The submission was saved, and the email was sent.

**[1:11]** Think about what the visitor sees. A server error. So they assume nothing happened, and they send it again, and the studio gets two enquiries. The thank you template is the page template's name plus _landing, in the same folder. Write it first.

**[1:31]** Third thing. Refresh the thank you page. Wagtail renders it as the direct response to the post, so refreshing makes the browser send the post again. Two submissions, two emails. Every refresh, another one.

**[1:47]** The fix is the oldest pattern on the web. Post, redirect, get. After a good submission, redirect to the contact page with sent equals one, and render the thank you template for that. Now the post answers with a 302, and I refreshed the thank you page twice. Still one submission.

**[2:08]** Fourth thing. The budget question is optional. But Wagtail builds a dropdown from the editor's choices and nothing else, so there is no blank option. Under five thousand is selected by default, and the browser sends it. Every single enquiry records a budget that the person never picked.

**[2:30]** A small custom form builder fixes it. If a dropdown is optional, put a blank choice in front of the editor's list. Tell the page to use it, and a budget left blank is now stored as blank.

**[2:45]** And spam. A honeypot is an ordinary text input, pushed off screen with CSS. People never see it, and keyboard users can not tab into it. Bots fill in every input they find. If it comes back filled in, the bot gets exactly the same thank you page, and nothing is stored or sent. Do not make it a hidden input, because bots skip those. And never tell the bot that it failed.

**[3:14]** In development, the email does not go anywhere. The development settings already use the console backend, so it prints in the terminal running the server. That is the whole email. Real sending is episode thirteen.

**[3:29]** And here is the form. Notice contact appeared in the menu on its own, because of the show in menus default from last episode.

**[3:39]** And the thank you page, at its own address. Refresh it as often as you like.

**[3:46]** Commit, and tag.

**[3:50]** Next episode, search. The search app we unboxed in episode two, finally doing something.

**[3:58]** Next episode, search. Thanks for watching.
