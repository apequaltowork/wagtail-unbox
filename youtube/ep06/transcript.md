# Ep 6 — Images & Documents

Transcript of the narration.

Video: https://www.youtube.com/watch?v=YYxtwAx4a0w

Code at the end of this episode: `git checkout ep06-end`

---

**[0:00]** Images, and documents.

**[0:04]** Six episodes into building a design studio's website, and there is not one image on it. Today we fix that. And this is the first episode where the thing we make does not live in the repository at all.

**[0:19]** And there is nothing to install. We toured all of this back in episode two. The images app and the documents app have been sitting in installed apps since the first minute. Media root and media URL are already in settings. The URL config already serves uploaded files, but only when debug is on. Production is episode thirteen.

**[0:43]** And this is worth being clear about. Your repository holds the site. The database and the media folder hold what is in it. Uploading an image is not a code change, which is why media is in git ignore, and why the images in this episode will not arrive when you check out the tag.

**[1:03]** An image on a page is just a Django foreign key. There is no special image field. But three of these arguments matter, and people get them wrong.

**[1:15]** Cascade would mean that deleting an image in the admin deletes every page that used it. An editor tidying up the image library could take out half the site. Set null means the page just loses its hero, which is what anybody would expect. And related name plus, because we never ask an image which pages are using it.

**[1:37]** So what does the image tag actually do. It does not resize anything on each request. The first time, it generates a copy, writes it into the media folder, and records a row in the rendition table. Every time after that, the row wins. And your original upload is never touched. Every rendition is a copy.

**[2:01]** There are a handful of filter specs. Width scales. Fill crops to exactly the size you asked for. Max fits the image inside a box without cropping and without enlarging it. The one to remember is that fill crops and max does not.

**[2:19]** And responsive images are one tag. Srcset image takes a list of specs, generates all three, and writes out a proper srcset and sizes attribute. I checked it at 375 pixels wide, and the browser downloads the 800-pixel file, not the 1600. Your phone visitors stop paying for desktop images.

**[2:44]** Now, cropping. These are two renditions of exactly the same image, at exactly the same fill spec. On the left, Wagtail crops from the centre and slices the subject off at the edge. On the right, the same crop, with a focal point set. That is the whole feature, and you set it by dragging a box in the admin.

**[3:07]** Two details. First, the filename changes when you set a focal point. That hash is part of the cache key, so a stale crop can never be served. And second, focal points only affect fill. Width and max do not crop anything, so there is nothing for a focal point to decide.

**[3:28]** And here is the one that will catch you in production. Look at what get rendition actually does. It looks for a database row. If it finds one, it returns it. It never checks whether the file that row points at still exists.

**[3:45]** So I cleared out the rendition files and audited it. Fourteen rows, eleven of them pointing at files that no longer exist. And the site cheerfully puts all eleven URLs into image tags, and every single one is a 404. Nothing in the logs tells you why. This is not contrived. It is what happens after a media restore, or a move to a new server, or somebody clearing out disk space.

**[4:15]** And the fix ships with Wagtail. Purge the rendition rows, and they regenerate on the next request. After that the audit came back clean: nine rows, nine files, nothing missing. Put this one in your deployment notes.

**[4:32]** Now something that matters more than it looks. If you write the image tag with no alt attribute, Wagtail falls back to the image's title. Ours came out as alt equals Studio hero. That is how the image is filed in the CMS. It tells somebody using a screen reader absolutely nothing about the picture.

**[4:54]** In a StreamField, the answer is image block, not image chooser block. It arrived in Wagtail six point three, and it carries alt text and a decorative checkbox right next to the image chooser, so the person writing the page is the one who supplies them. It still behaves as an image everywhere the old block did, so switching is cheap.

**[5:17]** And here is the opinion. If your CMS makes alt text optional and invisible, you will ship a site without it. On the hero, which is a plain foreign key, there is nothing to inherit from, so we added our own hero alt field right next to the image chooser where nobody can miss it.

**[5:37]** Documents work the same way, with a document chooser block. And the size and file type come straight off the document, so the visitor knows what they are about to download before they click it.

**[5:50]** One thing to notice: that document URL is not a static file path. Documents are served by a Wagtail view, which is exactly what makes private documents and permission checks possible later on. Images are different. Those really are plain files sitting under/media.

**[6:10]** One warning before we look at the result. There is a setting that lets you swap in your own image model, with extra fields like a photo credit or a licence. It is genuinely useful, and it is a day one decision. Retrofitting it onto a site that already has content means migrating every image foreign key in the project. Know it exists. Do not do it to this site today.

**[6:37]** And here is the result. A hero above the title, with its caption, cropped to a banner from an image nearly twice as wide as it needed to be.

**[6:49]** And further down, the image block set to full width. Look at where it ends compared to the quote and the download underneath it. It genuinely breaks out past the text column. Its caption came from the editor, and the download shows its file type and its size before anybody clicks it.

**[7:09]** And the About page. That is a tall portrait image being cropped into a wide banner, and the face is still in the middle of it, because the focal point tells Wagtail what the picture is actually of.

**[7:22]** Commit, and tag. Remember the images themselves are not in there.

**[7:29]** Next episode, the blog. An index page with posts underneath it, restricting which page types can go where, and pagination.

**[7:39]** Next episode, the blog. Thanks for watching.
