# Ep 12 — Editor Experience Polish

Transcript of the narration.

Code at the end of this episode: `git checkout ep12-end`

---

**[0:00]** The editor experience.

**[0:04]** Every episode so far, we have been logged in as a superuser. The client will not be. So this episode starts by creating a user called Casey, putting them in Wagtail's default editors group, and looking at the admin through their eyes.

**[0:21]** Pages work. But the team, the testimonials and the studio settings all bounce straight back to the dashboard, and the menu items are not even there. We spent two episodes building those things for the client, and the client can not open any of them. The default editors group can edit pages, images and documents, and nothing we defined.

**[0:45]** You could fix it by clicking in the groups screen. That fixes one database. Put it in a data migration and it fixes every copy of the site. A colleague's laptop, staging, and production. The obvious version looks like this. Find the permissions, add them to the group.

**[1:06]** Run it on a fresh database. Okay. The editors group got nothing. And yet, ask whether the permissions exist, and they do.

**[1:17]** Django creates permission rows in a signal that runs after every migration has finished. On a fresh database they do not exist yet when our migration runs. So the filter finds nothing, the migration says okay, and a moment later the permissions appear, so nothing looks wrong. Create them first. And the nasty part. On my existing database, the broken version worked. It would only have failed in production.

**[1:48]** Fixed, and tested on a fresh database this time. All seven permissions, and Casey can open everything we built.

**[1:58]** Now a bug we wrote ourselves. The contact page has two preview modes. The form previews fine. The landing page preview redirects.

**[2:10]** In episode ten, we turned render landing page into a redirect, to fix the refresh problem. Wagtail's preview calls that same method. So the preview jumped to the live thank you page, and an editor rewriting the thank you message would only ever see the published version. Render the template directly for previews. I checked it against an unpublished draft, and the draft text now shows.

**[2:37]** Now something for the client. The newest enquiries, right on the admin dashboard. A small component, registered with the construct homepage panels hook. Homepage here means the admin's own front page, not the website's.

**[2:54]** The important line is get forms for user. It applies exactly the same permission rule as the forms screen. I checked three users. The superuser and Casey see the panel. A user who can only log in sees nothing. If you queried every submission instead, the dashboard would show enquiries, names and email addresses, to anyone with a login.

**[3:19]** And here is Casey's dashboard. Studio and Settings in the menu, and recent enquiries at the top.

**[3:28]** Every page type now has a page description, which Wagtail shows when an editor chooses between page types. And then I went to add a page under Home, and the chooser never appeared. The journal and the contact page are both at their max count, so only one type is allowed, and Wagtail skips straight to the form. That is episode seven's rules doing their job.

**[3:53]** And every piece of help text we have written since episode three is right there, under its field. Including the alt text guidance from episode six.

**[4:04]** Commit, and tag.

**[4:07]** Next episode, production settings. Postgres, environment variables, debug off, and the checklist Django already ships with.

**[4:19]** Next episode, production settings. Thanks for watching.
