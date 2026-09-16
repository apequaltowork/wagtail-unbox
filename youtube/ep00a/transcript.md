# Ep 0a — What This Series Is (and Who It's For)

Transcript of the narration.

Video: https://www.youtube.com/watch?v=ck4T3lnkhqs

No code in this episode.

---

**[0:00]** Wagtail Unboxed. Learning by building.

**[0:04]** That is a real website. And that is somebody editing it, without touching any code. By the end of this series you will have built it, from an empty folder, and you will understand every file in it.

**[0:18]** So, what is Wagtail? It is a content management system built on Django.

**[0:26]** It is not a fork of Django, and it is not a competitor to it. It is a set of Django apps that you pip install. Models are still models. Templates are still templates. What Wagtail adds is a page tree, a genuinely good editing interface, an image system, and a content block system called StreamField.

**[0:48]** If you already write Django, you already know about seventy percent of Wagtail. This series is about the other thirty.

**[0:57]** Who is this for? Three groups. Django developers who keep getting asked, can the client edit this. Agency and freelance developers, building sites for people who are not developers. And people leaving WordPress, who want that editing experience without the PHP plugin ecosystem.

**[1:19]** Now the part I am not going to soften.

**[1:24]** You need basic Python. Functions, classes, imports, pip. And you need Django. Models, migrations, templates, settings.py. That is the real prerequisite, because Wagtail is Django. Plus enough HTML and CSS to edit a template, and enough command line to run a command and read an error.

**[1:48]** If models.py and make migrations are not familiar yet, pause this video and go do the official Django tutorial. It is about a weekend of work. Then come back. You will get far more out of this, and you will not spend fourteen episodes copying code you cannot change.

**[2:08]** What you do not need: any prior Wagtail, any prior CMS experience, no front end frameworks, and no Docker. Wagtail itself is taught from zero.

**[2:21]** One practical note. I record on Windows, so Windows commands are what you will see on screen. Every episode ships a commands file in the repo with the mac and Linux equivalents. Nothing in this series is Windows only.

**[2:38]** Here is the plan. Fourteen episodes, in three acts. One concept per episode, fifteen to twenty five minutes each, and nothing gets hand waved.

**[2:50]** Act one, episodes one to three. Unboxing. We create the project, and then we read every single file Wagtail generated. All twenty nine of them. Most tutorials skip that, and it is exactly why people stay confused.

**[3:08]** Act two, episodes four to eleven. We build. Templates and static files, StreamField, images and documents, a blog, reusable snippets, navigation, a working contact form, and search.

**[3:25]** And act three, episodes twelve to fourteen. Shipping. Polishing the editor experience for the client, real production settings, and deploying to an actual domain.

**[3:38]** Everything is in a public repo. Every episode ends on a git tag. So if you want to start at episode seven, you check out the tag from episode six, and you have exactly the code that episode begins with.

**[3:54]** The database is not in the repo. You make your own content as you follow along. That is deliberate. Actually making content is how the admin stops being abstract.

**[4:07]** And what this series is not. It is not a Django tutorial. It is not a front end course. There is no React, no Tailwind, and no Node, at any point. We write plain CSS by hand so the episodes stay about Wagtail. It is not a headless or API series. And it is not a clone the repo and you are done series. You will type the code.

**[4:35]** Versions are pinned, so the code on screen is the code you get. Wagtail seven point four point three, Django six point one point one, Python three point twelve. Wagtail eight is out. We are on seven point four on purpose: wider package compatibility, and it ages more slowly.

**[4:57]** Next episode, we set up your machine. Python, git, and virtual environments. But if you already have Python, a virtualenv habit, and git, then skip it and go straight to episode one. I will see you there.

**[5:14]** Thanks for watching. Everything is linked below. Let us open the box.
